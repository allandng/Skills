#!/usr/bin/env python3
"""Survey a codebase and print JSON describing it.

Reads an existing repository and reports the things you need before planning a
change to it: detected stack and dependencies, language breakdown, directory
shape, entry points, tests, migrations, infrastructure, route hints, and git
activity.

Python standard library only. Never raises on a single unreadable file - problems
are collected into the "notes" list so partial results stay usable.

Usage:
    python survey_repo.py <path>
    python survey_repo.py <path> --max-depth 4 --top 30
    python survey_repo.py <path> --no-git
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

IGNORE_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "bower_components", "vendor",
    "target", "dist", "build", "out", "bin", "obj", ".next", ".nuxt", ".svelte-kit",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".tox",
    "venv", ".venv", "env", ".env.d", "site-packages",
    ".gradle", ".idea", ".vscode", ".terraform", ".serverless",
    "coverage", "htmlcov", ".nyc_output", "Pods", "DerivedData",
    ".cache", ".parcel-cache", ".turbo", "storybook-static",
}

EXT_LANG = {
    ".py": "Python", ".rs": "Rust", ".go": "Go", ".java": "Java", ".kt": "Kotlin",
    ".ts": "TypeScript", ".tsx": "TypeScript", ".js": "JavaScript", ".jsx": "JavaScript",
    ".mjs": "JavaScript", ".cjs": "JavaScript", ".svelte": "Svelte", ".vue": "Vue",
    ".rb": "Ruby", ".php": "PHP", ".cs": "C#", ".swift": "Swift", ".m": "Objective-C",
    ".c": "C", ".h": "C/C++ header", ".cc": "C++", ".cpp": "C++", ".cxx": "C++",
    ".hpp": "C++ header", ".scala": "Scala", ".ex": "Elixir", ".exs": "Elixir",
    ".dart": "Dart", ".lua": "Lua", ".r": "R", ".jl": "Julia", ".zig": "Zig",
    ".sql": "SQL", ".sh": "Shell", ".bash": "Shell", ".ps1": "PowerShell",
    ".html": "HTML", ".css": "CSS", ".scss": "SCSS", ".sass": "SCSS", ".less": "LESS",
    ".md": "Markdown", ".mdx": "Markdown", ".json": "JSON", ".yaml": "YAML",
    ".yml": "YAML", ".toml": "TOML", ".proto": "Protobuf", ".graphql": "GraphQL",
    ".gql": "GraphQL", ".tf": "Terraform", ".hcl": "HCL", ".prisma": "Prisma",
}

# Languages that are configuration or prose rather than implementation.
NON_CODE_LANGS = {"Markdown", "JSON", "YAML", "TOML", "HTML", "CSS", "SCSS", "LESS"}

ENTRY_POINT_NAMES = {
    "main.rs", "lib.rs", "main.py", "__main__.py", "app.py", "wsgi.py", "asgi.py",
    "manage.py", "main.go", "main.java", "Main.java", "Program.cs", "main.ts",
    "main.js", "index.ts", "index.js", "server.ts", "server.js", "app.ts", "app.js",
    "_app.tsx", "_app.jsx", "layout.tsx", "App.tsx", "App.jsx", "App.vue",
    "main.dart", "application.rb", "config.ru", "index.php",
}

INFRA_PATTERNS = [
    ("Docker", re.compile(r"^(Dockerfile|Containerfile)(\..+)?$|^docker-compose(\..+)?\.ya?ml$", re.I)),
    ("CI", re.compile(r"^\.github/workflows/.+\.ya?ml$|^\.gitlab-ci\.ya?ml$|^\.circleci/|^Jenkinsfile$|^azure-pipelines\.ya?ml$|^\.travis\.ya?ml$")),
    ("Kubernetes", re.compile(r"^(k8s|kubernetes|charts|helm|manifests)/")),
    ("Terraform", re.compile(r"\.tf$|\.tfvars$")),
    ("Serverless", re.compile(r"^serverless\.ya?ml$|^template\.ya?ml$|^sam\.ya?ml$")),
    ("Platform config", re.compile(r"^(vercel|netlify|railway|fly|render|app|Procfile|nixpacks)(\.|$)", re.I)),
    ("Env template", re.compile(r"^\.env\.(example|sample|template)$|^\.env\.dist$")),
]

TEST_DIR_NAMES = {"test", "tests", "__tests__", "spec", "e2e", "integration", "cypress", "playwright"}
TEST_FILE_RE = re.compile(r"(^test_|_test\.|\.test\.|\.spec\.|Test\.java$|Tests\.cs$|_spec\.rb$)")

MIGRATION_DIR_RE = re.compile(r"(^|/)(migrations?|migrate|db/migrate|prisma/migrations|alembic|supabase/migrations|liquibase|flyway)(/|$)", re.I)
SCHEMA_FILE_RE = re.compile(r"(schema\.(sql|rb|prisma|graphql|ts)|structure\.sql|\.dbml$|models?\.py$|entities?\.ts$)", re.I)

ROUTE_PATTERNS = [
    ("Express/Fastify", re.compile(r"""(?:app|router|server|fastify)\.(get|post|put|patch|delete|all)\s*\(\s*['"`]([^'"`]+)""")),
    ("Flask", re.compile(r"""@\w+\.route\s*\(\s*['"]([^'"]+)""")),
    ("FastAPI", re.compile(r"""@\w+\.(get|post|put|patch|delete)\s*\(\s*['"]([^'"]+)""")),
    ("Django", re.compile(r"""path\s*\(\s*['"]([^'"]*)['"]""")),
    ("Spring", re.compile(r"""@(Get|Post|Put|Patch|Delete|Request)Mapping\s*\(\s*(?:value\s*=\s*)?['"]([^'"]+)""")),
    ("Axum/Actix", re.compile(r"""\.route\s*\(\s*"([^"]+)"|#\[(get|post|put|patch|delete)\s*\(\s*"([^"]+)""")),
    ("Rails", re.compile(r"""^\s*(get|post|put|patch|delete|resources)\s+['":]([^'",\s]+)""", re.M)),
]

MAX_READ_BYTES = 2_000_000
MAX_GREP_FILES = 600


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def read_text(path: Path, notes: list[str], limit: int = MAX_READ_BYTES) -> str:
    try:
        if path.stat().st_size > limit:
            return ""
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:  # noqa: BLE001
        notes.append(f"could not read {path}: {exc.__class__.__name__}")
        return ""


def rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def walk(root: Path, notes: list[str]):
    """Yield (Path, relative_posix_string) for every non-ignored file."""
    for dirpath, dirnames, filenames in os.walk(root, onerror=lambda e: notes.append(str(e))):
        dirnames[:] = sorted(d for d in dirnames if d not in IGNORE_DIRS and not d.startswith(".egg"))
        for name in sorted(filenames):
            p = Path(dirpath) / name
            yield p, rel(p, root)


# --------------------------------------------------------------------------- #
# Manifest parsing
# --------------------------------------------------------------------------- #

def parse_toml(text: str) -> dict:
    if tomllib is None or not text:
        return {}
    try:
        return tomllib.loads(text)
    except Exception:  # noqa: BLE001
        return {}


def parse_manifest(name: str, text: str, notes: list[str]) -> dict:
    """Return {ecosystem, runtime, dependencies, dev_dependencies, scripts}."""
    out: dict = {"dependencies": [], "dev_dependencies": [], "scripts": {}}

    if name == "package.json":
        out["ecosystem"] = "npm"
        try:
            data = json.loads(text)
        except Exception:  # noqa: BLE001
            notes.append("package.json is not valid JSON")
            return out
        out["dependencies"] = sorted(data.get("dependencies", {}))
        out["dev_dependencies"] = sorted(data.get("devDependencies", {}))
        out["scripts"] = data.get("scripts", {}) or {}
        eng = data.get("engines", {}) or {}
        if eng:
            out["runtime"] = ", ".join(f"{k} {v}" for k, v in eng.items())
        if data.get("type"):
            out["module_type"] = data["type"]
        ws = data.get("workspaces")
        if ws:
            out["workspaces"] = ws if isinstance(ws, list) else ws.get("packages", [])

    elif name == "Cargo.toml":
        out["ecosystem"] = "cargo"
        data = parse_toml(text)
        out["dependencies"] = sorted(data.get("dependencies", {}))
        out["dev_dependencies"] = sorted(data.get("dev-dependencies", {}))
        pkg = data.get("package", {}) or {}
        if pkg.get("edition"):
            out["runtime"] = f"Rust edition {pkg['edition']}"
        if "workspace" in data:
            out["workspaces"] = (data.get("workspace") or {}).get("members", [])
        if not data and text:
            out["dependencies"] = sorted(set(re.findall(r"^([A-Za-z0-9_-]+)\s*=", text, re.M)))

    elif name == "pyproject.toml":
        out["ecosystem"] = "python"
        data = parse_toml(text)
        proj = data.get("project", {}) or {}
        deps = list(proj.get("dependencies", []) or [])
        poetry = ((data.get("tool") or {}).get("poetry") or {})
        deps += list((poetry.get("dependencies") or {}).keys())
        out["dependencies"] = sorted({re.split(r"[<>=!~\[ ;]", d)[0] for d in deps if d})
        out["dev_dependencies"] = sorted((poetry.get("dev-dependencies") or {}).keys())
        if proj.get("requires-python"):
            out["runtime"] = f"Python {proj['requires-python']}"

    elif name in {"requirements.txt", "requirements-dev.txt"}:
        out["ecosystem"] = "python"
        deps = []
        for line in text.splitlines():
            line = line.split("#")[0].strip()
            if line and not line.startswith("-"):
                deps.append(re.split(r"[<>=!~\[ ;]", line)[0])
        key = "dev_dependencies" if "dev" in name else "dependencies"
        out[key] = sorted(set(deps))

    elif name == "go.mod":
        out["ecosystem"] = "go"
        out["dependencies"] = sorted(set(re.findall(r"^\s+([\w./~-]+)\s+v", text, re.M)))
        m = re.search(r"^go\s+([\d.]+)", text, re.M)
        if m:
            out["runtime"] = f"Go {m.group(1)}"

    elif name == "Gemfile":
        out["ecosystem"] = "bundler"
        out["dependencies"] = sorted(set(re.findall(r"""^\s*gem\s+['"]([^'"]+)""", text, re.M)))

    elif name == "composer.json":
        out["ecosystem"] = "composer"
        try:
            data = json.loads(text)
            out["dependencies"] = sorted(data.get("require", {}))
            out["dev_dependencies"] = sorted(data.get("require-dev", {}))
        except Exception:  # noqa: BLE001
            notes.append("composer.json is not valid JSON")

    elif name == "pubspec.yaml":
        out["ecosystem"] = "pub"
        out["dependencies"] = sorted(set(re.findall(r"^  ([a-z0-9_]+):", text, re.M)))

    elif name == "pom.xml":
        out["ecosystem"] = "maven"
        out["dependencies"] = sorted(set(re.findall(r"<artifactId>([^<]+)</artifactId>", text)))

    elif name.endswith(".gradle") or name.endswith(".gradle.kts"):
        out["ecosystem"] = "gradle"
        out["dependencies"] = sorted(set(re.findall(r"""['"]([\w.-]+:[\w.-]+):""", text)))

    elif name.endswith(".csproj"):
        out["ecosystem"] = "nuget"
        out["dependencies"] = sorted(set(re.findall(r'PackageReference\s+Include="([^"]+)"', text)))

    return out


FRAMEWORK_HINTS = {
    "next": "Next.js", "react": "React", "vue": "Vue", "svelte": "Svelte",
    "@angular/core": "Angular", "express": "Express", "fastify": "Fastify",
    "nestjs": "NestJS", "@nestjs/core": "NestJS", "hono": "Hono",
    "prisma": "Prisma", "@prisma/client": "Prisma", "drizzle-orm": "Drizzle",
    "typeorm": "TypeORM", "sequelize": "Sequelize", "mongoose": "Mongoose",
    "@supabase/supabase-js": "Supabase", "firebase": "Firebase",
    "tailwindcss": "Tailwind", "vite": "Vite", "webpack": "Webpack",
    "jest": "Jest", "vitest": "Vitest", "playwright": "Playwright",
    "@playwright/test": "Playwright", "cypress": "Cypress", "mocha": "Mocha",
    "django": "Django", "flask": "Flask", "fastapi": "FastAPI",
    "sqlalchemy": "SQLAlchemy", "alembic": "Alembic", "pydantic": "Pydantic",
    "pytest": "pytest", "celery": "Celery",
    "axum": "Axum", "actix-web": "Actix", "rocket": "Rocket", "tokio": "Tokio",
    "sqlx": "SQLx", "diesel": "Diesel", "serde": "Serde", "tauri": "Tauri",
    "gin-gonic/gin": "Gin", "labstack/echo": "Echo", "gorm.io/gorm": "GORM",
    "rails": "Rails", "sinatra": "Sinatra", "laravel/framework": "Laravel",
    "spring-boot-starter-web": "Spring Boot",
}


# --------------------------------------------------------------------------- #
# Survey
# --------------------------------------------------------------------------- #

def survey(root: Path, max_depth: int, top: int, use_git: bool) -> dict:
    notes: list[str] = []
    result: dict = {"root": str(root.resolve()), "notes": notes}

    files = list(walk(root, notes))
    result["file_count"] = len(files)
    if not files:
        notes.append("no readable files found - check the path and permissions")

    # -- languages ---------------------------------------------------------- #
    loc: Counter = Counter()
    counts: Counter = Counter()
    for path, r in files:
        lang = EXT_LANG.get(path.suffix.lower())
        if not lang:
            continue
        counts[lang] += 1
        text = read_text(path, notes)
        if text:
            loc[lang] += text.count("\n") + 1

    total_code = sum(v for k, v in loc.items() if k not in NON_CODE_LANGS) or 1
    result["languages"] = [
        {
            "language": lang,
            "files": counts[lang],
            "lines": n,
            "pct_of_code": round(100 * n / total_code, 1) if lang not in NON_CODE_LANGS else None,
        }
        for lang, n in loc.most_common()
    ]

    # -- manifests ---------------------------------------------------------- #
    manifest_names = {
        "package.json", "Cargo.toml", "pyproject.toml", "requirements.txt",
        "requirements-dev.txt", "go.mod", "Gemfile", "composer.json",
        "pubspec.yaml", "pom.xml",
    }
    manifests = {}
    all_deps: set[str] = set()
    for path, r in files:
        n = path.name
        is_manifest = (
            n in manifest_names
            or n.endswith(".csproj")
            or n in {"build.gradle", "build.gradle.kts"}
        )
        if not is_manifest:
            continue
        parsed = parse_manifest(n, read_text(path, notes), notes)
        if parsed:
            manifests[r] = parsed
            all_deps.update(parsed.get("dependencies", []))
            all_deps.update(parsed.get("dev_dependencies", []))
    result["manifests"] = manifests

    # -- frameworks --------------------------------------------------------- #
    found = set()
    for dep in all_deps:
        low = dep.lower()
        for key, label in FRAMEWORK_HINTS.items():
            k = key.lower()
            # Exact match, or a path-qualified key like "gin-gonic/gin".
            if low == k or low.endswith("/" + k) or ("/" in k and k in low):
                found.add(label)
    result["frameworks_detected"] = sorted(found)

    # -- directory tree ----------------------------------------------------- #
    tree: dict[str, int] = defaultdict(int)
    for path, r in files:
        parts = r.split("/")[:-1]
        for d in range(1, min(len(parts), max_depth) + 1):
            tree["/".join(parts[:d])] += 1
    result["tree"] = [
        {"path": k, "files": v}
        for k, v in sorted(tree.items(), key=lambda kv: (-kv[1], kv[0]))[:top]
    ]

    # -- entry points ------------------------------------------------------- #
    entries = [r for _, r in files if Path(r).name in ENTRY_POINT_NAMES]
    entries += [r for _, r in files if re.search(r"(^|/)(app|pages)/.*(page|route|layout)\.(tsx?|jsx?)$", r)]
    result["entry_points"] = sorted(set(entries))[:40]

    # -- tests -------------------------------------------------------------- #
    test_files = [
        r for _, r in files
        if TEST_FILE_RE.search(Path(r).name) or any(p in TEST_DIR_NAMES for p in r.split("/")[:-1])
    ]
    result["tests"] = {
        "count": len(test_files),
        "directories": sorted({"/".join(r.split("/")[:-1]) for r in test_files})[:20],
        "examples": sorted(test_files)[:12],
    }
    if not test_files:
        notes.append("no test files detected - confirm before assuming the project is untested")

    # -- data layer --------------------------------------------------------- #
    result["data_layer"] = {
        "migration_paths": sorted({r for _, r in files if MIGRATION_DIR_RE.search(r)})[:40],
        "schema_files": sorted({r for _, r in files if SCHEMA_FILE_RE.search(Path(r).name)})[:20],
        "sql_files": sorted({r for _, r in files if r.endswith(".sql")})[:20],
    }

    # -- infrastructure ----------------------------------------------------- #
    infra = defaultdict(list)
    for _, r in files:
        name = Path(r).name
        for label, pattern in INFRA_PATTERNS:
            if pattern.search(r) or pattern.search(name):
                infra[label].append(r)
    result["infrastructure"] = {k: sorted(set(v))[:15] for k, v in infra.items()}

    # -- config surface (names only, never values) -------------------------- #
    env_keys: set[str] = set()
    for path, r in files:
        if re.match(r"^\.env\.(example|sample|template|dist)$", path.name):
            for line in read_text(path, notes).splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    env_keys.add(line.split("=", 1)[0].strip())
    result["env_vars_declared"] = sorted(env_keys)
    result["env_note"] = "Names only. Real .env files are never read by this script."

    # -- route hints -------------------------------------------------------- #
    routes = defaultdict(set)
    code_files = [
        (p, r) for p, r in files
        if EXT_LANG.get(p.suffix.lower()) not in (None, *NON_CODE_LANGS)
    ][:MAX_GREP_FILES]
    for path, r in code_files:
        text = read_text(path, notes)
        if not text:
            continue
        for label, pattern in ROUTE_PATTERNS:
            for m in pattern.finditer(text):
                groups = [g for g in m.groups() if g and g.startswith(("/", ":", "api"))]
                if groups:
                    routes[label].add(f"{groups[-1]}  ({r})")
    result["route_hints"] = {k: sorted(v)[:25] for k, v in routes.items()}
    if len(code_files) == MAX_GREP_FILES:
        notes.append(f"route scan capped at {MAX_GREP_FILES} files - results are a sample")

    # -- docs --------------------------------------------------------------- #
    result["existing_docs"] = sorted(
        r for _, r in files
        if r.lower().endswith((".md", ".mdx", ".adoc", ".rst"))
        and ("doc" in r.lower() or "/" not in r or "adr" in r.lower())
    )[:40]

    # -- git ---------------------------------------------------------------- #
    if use_git and (root / ".git").exists():
        result["git"] = git_info(root, notes)
    else:
        result["git"] = {"available": False}

    return result


def git_info(root: Path, notes: list[str]) -> dict:
    def run(args: list[str]) -> str:
        try:
            out = subprocess.run(
                ["git", "-C", str(root), *args],
                capture_output=True, text=True, timeout=20, check=False,
            )
            return out.stdout.strip()
        except Exception as exc:  # noqa: BLE001
            notes.append(f"git {' '.join(args)} failed: {exc.__class__.__name__}")
            return ""

    info: dict = {"available": True}
    info["branch"] = run(["rev-parse", "--abbrev-ref", "HEAD"])
    info["commit_count"] = run(["rev-list", "--count", "HEAD"])
    info["first_commit"] = run(["log", "--reverse", "--format=%as", "--max-count=1"])
    info["latest_commit"] = run(["log", "-1", "--format=%as"])
    info["recent_commits"] = [
        l for l in run(["log", "-15", "--format=%as  %an  %s"]).splitlines() if l
    ]
    authors = Counter(
        l for l in run(["log", "--format=%an", "-500"]).splitlines() if l
    )
    info["top_authors"] = [{"name": a, "commits": c} for a, c in authors.most_common(8)]
    hot = Counter(
        l for l in run(["log", "--name-only", "--format=", "-200"]).splitlines()
        if l and not any(seg in IGNORE_DIRS for seg in l.split("/"))
    )
    info["most_changed_files"] = [{"path": p, "changes": c} for p, c in hot.most_common(15)]
    return info


# --------------------------------------------------------------------------- #

def main() -> int:
    ap = argparse.ArgumentParser(description="Survey a codebase and print JSON.")
    ap.add_argument("path", help="path to the repository root")
    ap.add_argument("--max-depth", type=int, default=3, help="directory tree depth (default 3)")
    ap.add_argument("--top", type=int, default=25, help="max directories to list (default 25)")
    ap.add_argument("--no-git", action="store_true", help="skip git history")
    args = ap.parse_args()

    root = Path(args.path).expanduser()
    if not root.exists():
        print(json.dumps({"fatal": f"path does not exist: {root}"}, indent=2))
        return 1
    if not root.is_dir():
        print(json.dumps({"fatal": f"not a directory: {root}"}, indent=2))
        return 1

    try:
        data = survey(root, args.max_depth, args.top, not args.no_git)
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"fatal": f"{exc.__class__.__name__}: {exc}"}, indent=2))
        return 1

    print(json.dumps(data, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())

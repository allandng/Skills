#!/usr/bin/env python3
"""Check that an /addon plan does not assert things that are not in the repo.

Pulls every file path and function-like symbol out of a plan document and checks
them against the actual codebase, sorting them into three buckets:

    exists     the repo has it
    new        the plan declares it as something being created
    MISSING    neither - a typo, or something invented

Anything in the MISSING bucket is a hallucination waiting to be implemented
against. Exit code is 1 when the bucket is non-empty.

Python standard library only.

Usage:
    python verify_plan.py docs/addons/push-notifications.md ../my-repo
    python verify_plan.py plan.md ../my-repo --json
    python verify_plan.py plan.md ../my-repo --no-symbols
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

IGNORE_DIRS = {
    ".git", "node_modules", "bower_components", "vendor", "target", "dist",
    "build", "out", "bin", "obj", ".next", ".nuxt", ".svelte-kit", "__pycache__",
    ".pytest_cache", ".mypy_cache", ".ruff_cache", ".tox", "venv", ".venv", "env",
    ".gradle", ".idea", ".terraform", "coverage", "htmlcov", "Pods", ".cache",
    ".turbo", ".parcel-cache", "storybook-static", ".serverless",
}

CODE_EXTS = {
    ".py", ".rs", ".go", ".java", ".kt", ".ts", ".tsx", ".js", ".jsx", ".mjs",
    ".cjs", ".svelte", ".vue", ".rb", ".php", ".cs", ".swift", ".c", ".h", ".cc",
    ".cpp", ".hpp", ".scala", ".ex", ".exs", ".dart", ".sql", ".sh", ".graphql",
    ".prisma", ".proto",
}

# Bare filenames that are paths even without a slash.
BARE_FILES = {
    "package.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock",
    "Cargo.toml", "Cargo.lock", "pyproject.toml", "requirements.txt", "go.mod",
    "go.sum", "Gemfile", "Gemfile.lock", "composer.json", "pubspec.yaml",
    "pom.xml", "build.gradle", "build.gradle.kts", "Dockerfile", "Makefile",
    "Procfile", "README.md", "tsconfig.json", "vite.config.ts", "next.config.js",
    "next.config.mjs", "tailwind.config.js", "tailwind.config.ts", ".env.example",
    "docker-compose.yml", "docker-compose.yaml", "schema.prisma",
}

PATH_EXT_RE = re.compile(r"\.[A-Za-z0-9]{1,8}$")
BACKTICK_RE = re.compile(r"`([^`\n]+)`")
PLACEHOLDER_CHARS = set("<>{}*$|")

# Markers that mean "the paths mentioned here do not exist yet, by design".
NEW_SECTION_RE = re.compile(
    r"\b(will\s+create|creates?|new\s+files?|adds?|to\s+be\s+created|scaffold)\b", re.I
)
NEW_INLINE_RE = re.compile(r"\((?:new|to\s+create|created)\)|\bnew\s+file\b", re.I)

# A symbol worth checking: a function-like reference the plan asserts exists.
SYMBOL_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)?)\(\)?$")
SYMBOL_STOPWORDS = {
    "if", "for", "while", "return", "print", "main", "test", "get", "set", "run",
    "init", "new", "self", "this", "async", "await", "function", "def", "fn",
    "console.log", "require", "import", "export", "true", "false", "null", "none",
}


# --------------------------------------------------------------------------- #

def looks_like_path(token: str) -> bool:
    if not token or len(token) > 200:
        return False
    if any(c in PLACEHOLDER_CHARS for c in token):
        return False
    if "..." in token or " " in token:
        return False
    if token.startswith(("http://", "https://", "mailto:", "git@")):
        return False
    if token in BARE_FILES:
        return True
    if "/" not in token:
        return False
    # Skip things that are clearly not filesystem paths.
    if token.startswith(("/api/", "api/v", ":")) and not PATH_EXT_RE.search(token):
        return False
    return bool(PATH_EXT_RE.search(token)) or token.endswith("/")


def clean_path(token: str) -> str:
    token = token.strip().strip("\"'")
    token = re.sub(r":\d+(?:-\d+)?$", "", token)      # src/a.ts:42
    token = token.rstrip(".,;:)")
    token = re.sub(r"^\./", "", token)
    return token.lstrip("/")


def extract(plan_text: str) -> tuple[dict[str, list[int]], set[str], dict[str, list[int]]]:
    """Return (paths -> line numbers, paths declared new, symbols -> line numbers)."""
    paths: dict[str, list[int]] = {}
    new_paths: set[str] = set()
    symbols: dict[str, list[int]] = {}

    in_new_block = False
    in_fence = False

    for n, raw in enumerate(plan_text.split("\n"), 1):
        stripped = raw.strip()

        if stripped.startswith("```"):
            in_fence = not in_fence

        # A heading, bold label, or bare all-caps marker can open a "new" block.
        is_marker = bool(
            re.match(r"^\s*(#{1,6}\s+|\*\*|[A-Z][A-Z ]{2,}$)", raw)
            or re.match(r"^\s*[A-Z][A-Z_ ]{2,}\b", raw)
        )
        if is_marker:
            in_new_block = bool(NEW_SECTION_RE.search(stripped))
        if not stripped:
            in_new_block = False

        line_is_new = in_new_block or bool(NEW_INLINE_RE.search(stripped)) or bool(
            NEW_SECTION_RE.search(stripped) and len(stripped) < 160
        )

        tokens = BACKTICK_RE.findall(raw)
        # Inside fenced blocks the plan writes bare paths, so scan whitespace tokens too.
        if in_fence:
            tokens += re.split(r"[\s,]+", stripped)

        for tok in tokens:
            candidate = clean_path(tok)
            if looks_like_path(candidate):
                paths.setdefault(candidate, []).append(n)
                if line_is_new:
                    new_paths.add(candidate)
                continue
            m = SYMBOL_RE.match(tok.strip())
            if m:
                name = m.group(1)
                if name.lower() in SYMBOL_STOPWORDS or len(name) < 4:
                    continue
                if line_is_new:
                    continue
                symbols.setdefault(name, []).append(n)

    return paths, new_paths, symbols


def index_repo(root: Path) -> tuple[set[str], str]:
    """Return (set of relative paths, concatenated code text for symbol lookup)."""
    known: set[str] = set()
    chunks: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        d = Path(dirpath)
        rel_dir = d.relative_to(root).as_posix()
        if rel_dir and rel_dir != ".":
            known.add(rel_dir)
            known.add(rel_dir + "/")
        for name in filenames:
            p = d / name
            known.add(p.relative_to(root).as_posix())
            if p.suffix.lower() in CODE_EXTS:
                try:
                    if p.stat().st_size < 2_000_000:
                        chunks.append(p.read_text(encoding="utf-8", errors="replace"))
                except Exception:  # noqa: BLE001
                    pass
    return known, "\n".join(chunks)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Verify that an /addon plan only references things that exist."
    )
    ap.add_argument("plan", help="the plan markdown file")
    ap.add_argument("repo", help="the repository root the plan describes")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--no-symbols", action="store_true", help="skip symbol checking")
    args = ap.parse_args()

    plan_path = Path(args.plan).expanduser()
    repo = Path(args.repo).expanduser()
    if not plan_path.is_file():
        print(f"plan not found: {plan_path}", file=sys.stderr)
        return 2
    if not repo.is_dir():
        print(f"repo not found: {repo}", file=sys.stderr)
        return 2

    plan_text = plan_path.read_text(encoding="utf-8", errors="replace")
    paths, new_paths, symbols = extract(plan_text)
    known, code = index_repo(repo)

    exists, declared_new, missing = {}, {}, {}
    for p, lines in sorted(paths.items()):
        if p in known or p.rstrip("/") in known:
            exists[p] = lines
        elif p in new_paths:
            declared_new[p] = lines
        else:
            missing[p] = lines

    missing_symbols = {}
    if not args.no_symbols:
        for s, lines in sorted(symbols.items()):
            tail = s.split(".")[-1]
            if not re.search(r"\b" + re.escape(tail) + r"\b", code):
                missing_symbols[s] = lines

    # A new file placed in a directory that does not exist is worth flagging.
    orphan_dirs = {}
    for p in declared_new:
        parent = "/".join(p.split("/")[:-1])
        if parent and parent not in known:
            orphan_dirs[p] = parent

    result = {
        "plan": str(plan_path),
        "repo": str(repo.resolve()),
        "exists": exists,
        "declared_new": declared_new,
        "missing": missing,
        "missing_symbols": missing_symbols,
        "new_files_in_nonexistent_dirs": orphan_dirs,
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"plan: {plan_path}")
        print(f"repo: {repo.resolve()}\n")
        print(f"  {len(exists):>3} path(s) verified in the repo")
        print(f"  {len(declared_new):>3} path(s) declared as new by the plan")
        print(f"  {len(missing):>3} path(s) MISSING and not declared new")

        if missing:
            print("\nMISSING - these do not exist and the plan does not say it creates them:")
            for p, lines in missing.items():
                where = ", ".join(f"line {l}" for l in lines[:4])
                print(f"  {p}   ({where})")
            print("\n  Each one is a typo or an invention. Re-read the code rather than")
            print("  substituting another guess, then correct the plan.")

        if missing_symbols:
            print("\nSymbols not found anywhere in the repo:")
            for s, lines in missing_symbols.items():
                where = ", ".join(f"line {l}" for l in lines[:4])
                print(f"  {s}   ({where})")
            print("\n  If the plan creates these, mark them as new. Otherwise they are invented.")

        if orphan_dirs:
            print("\nNew files placed in directories that do not exist:")
            for p, parent in orphan_dirs.items():
                print(f"  {p}   (needs {parent}/)")
            print("\n  Fine if intended, but confirm the location matches where")
            print("  comparable files already live.")

        if not (missing or missing_symbols or orphan_dirs):
            print("\nclean - every path and symbol in the plan is grounded")

    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())

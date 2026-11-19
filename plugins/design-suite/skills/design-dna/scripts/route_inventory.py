#!/usr/bin/env python3
"""List the screens in a codebase from its file-based routes.

Finds routes for Next.js (app and pages routers), Expo Router, SvelteKit,
Nuxt, Astro and plain HTML, and reports which have loading, error and
not-found files where the framework has a convention for them. The first step
of a teardown (references/app-dna.md).

    python3 route_inventory.py ./my-app
    python3 route_inventory.py ./my-app --json > routes.json

A route with a dynamic segment is a template: one screen, many pages. Count
those, not pages. For routers defined in code (React Router, SwiftUI, Compose,
Flutter) this finds nothing useful: read the router by hand.

Standard library only. Python 3.11+.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

SKIP_DIRS = {"node_modules", ".git", ".next", ".nuxt", ".svelte-kit", "dist", "build", "out",
             ".expo", ".vercel", ".turbo", "coverage", "__tests__", "ios", "android"}
CODE_EXT = {".tsx", ".jsx", ".ts", ".js", ".mdx", ".md"}
NEXT_STATE_FILES = {"loading": "loading", "error": "error", "not-found": "not-found"}


@dataclass
class Route:
    route: str
    file: str
    framework: str
    dynamic: bool
    states: dict[str, str] = field(default_factory=dict)


def walk(root: Path):
    for path in sorted(root.rglob("*")):
        if path.is_file() and not (set(path.relative_to(root).parts[:-1]) & SKIP_DIRS):
            yield path


def segment(part: str) -> str | None:
    """Turn one folder or file name into a URL segment. None means it adds nothing."""
    if part.startswith("(") and part.endswith(")"):  # route group
        return None
    if part.startswith("@") or part.startswith("_"):  # parallel slot, private folder
        return None
    if part in {"index", "page", "+page"}:
        return None
    part = re.sub(r"^\[\[?\.\.\.(.+?)\]?\]$", r"*\1", part)  # catch-all
    part = re.sub(r"^\[(.+?)\]$", r":\1", part)  # dynamic
    return part


def url(parts: list[str]) -> str:
    segments = [s for s in (segment(p) for p in parts) if s]
    return "/" + "/".join(segments)


def has_file(folder: Path, stem: str) -> bool:
    return any((folder / f"{stem}{ext}").is_file() for ext in CODE_EXT)


def next_states(page_dir: Path, app_dir: Path) -> dict[str, str]:
    """own, inherited from a parent segment, or absent."""
    states = {}
    for label, stem in NEXT_STATE_FILES.items():
        verdict = "absent"
        current = page_dir
        while True:
            if has_file(current, stem):
                verdict = "own" if current == page_dir else "inherited"
                break
            if current == app_dir:
                break
            current = current.parent
        states[label] = verdict
    return states


def find_dirs(root: Path, names: tuple[str, ...]) -> list[Path]:
    return [root / n for n in names if (root / n).is_dir()]


def scan(root: Path) -> list[Route]:
    routes: list[Route] = []

    for app_dir in find_dirs(root, ("app", "src/app")):
        files = list(walk(app_dir))
        pages = [f for f in files if f.stem == "page" and f.suffix in CODE_EXT]
        if pages:  # Next.js app router
            for page in pages:
                parts = list(page.parent.relative_to(app_dir).parts)
                routes.append(Route(url(parts), page.relative_to(root).as_posix(), "next-app",
                                    any("[" in p for p in parts), next_states(page.parent, app_dir)))
        elif any(f.stem == "_layout" for f in files):  # Expo Router
            for f in files:
                if f.suffix not in CODE_EXT or f.stem.startswith(("_", "+")):
                    continue
                parts = list(f.relative_to(app_dir).with_suffix("").parts)
                routes.append(Route(url(parts), f.relative_to(root).as_posix(), "expo-router",
                                    any("[" in p for p in parts)))

    for pages_dir in find_dirs(root, ("pages", "src/pages")):
        for f in walk(pages_dir):
            rel = f.relative_to(pages_dir)
            if rel.parts[0] == "api" or f.stem.startswith("_"):
                continue
            if f.suffix in {".vue"}:
                framework = "nuxt"
            elif f.suffix in {".astro"} or (root / "astro.config.mjs").exists() or (root / "astro.config.ts").exists():
                framework = "astro"
            elif f.suffix in CODE_EXT:
                framework = "next-pages"
            else:
                continue
            parts = list(rel.with_suffix("").parts)
            states = {}
            if framework == "next-pages":
                states = {"error": "inherited" if has_file(pages_dir, "_error") or has_file(pages_dir, "500") else "absent",
                          "not-found": "inherited" if has_file(pages_dir, "404") else "absent"}
                if f.stem in {"404", "500"}:
                    continue
            routes.append(Route(url(parts), f.relative_to(root).as_posix(), framework,
                                any("[" in p for p in parts), states))

    for routes_dir in find_dirs(root, ("src/routes",)):  # SvelteKit
        for f in walk(routes_dir):
            if f.name != "+page.svelte":
                continue
            parts = list(f.parent.relative_to(routes_dir).parts)
            verdict, current = "absent", f.parent
            while True:
                if (current / "+error.svelte").is_file():
                    verdict = "own" if current == f.parent else "inherited"
                    break
                if current == routes_dir:
                    break
                current = current.parent
            routes.append(Route(url(parts), f.relative_to(root).as_posix(), "sveltekit",
                                any("[" in p for p in parts), {"error": verdict}))

    if not routes:  # plain HTML
        for f in walk(root):
            if f.suffix == ".html":
                parts = list(f.relative_to(root).with_suffix("").parts)
                routes.append(Route(url(parts), f.relative_to(root).as_posix(), "html", False))

    return sorted(routes, key=lambda r: r.route)


def report(routes: list[Route]) -> None:
    if not routes:
        print("No file-based routes found. If the router is defined in code, read it by hand.")
        return
    width = min(max(len(r.route) for r in routes), 44)
    state_keys = sorted({k for r in routes for k in r.states})
    header = f"{'ROUTE':<{width}}  {'KIND':<8}  " + "  ".join(f"{k.upper():<9}" for k in state_keys) + "  FILE"
    print(header)
    for r in routes:
        kind = "template" if r.dynamic else "page"
        cells = "  ".join(f"{r.states.get(k, '-'):<9}" for k in state_keys)
        print(f"{r.route:<{width}}  {kind:<8}  {cells}  {r.file}")
    templates = sum(r.dynamic for r in routes)
    frameworks = ", ".join(sorted({r.framework for r in routes}))
    print(f"\n{len(routes)} route(s): {len(routes) - templates} page(s), {templates} template(s). Framework: {frameworks}.")
    for key in state_keys:
        absent = [r.route for r in routes if r.states.get(key) == "absent"]
        if absent:
            shown = ", ".join(absent[:6]) + (" ..." if len(absent) > 6 else "")
            print(f"No {key} file for {len(absent)} route(s): {shown}")
    print("File-level states only. A route can still handle loading or errors inside its component: "
          "label these [measured] for the files and check the rest by running it.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("root", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not args.root.is_dir():
        print(f"not a folder: {args.root}", file=sys.stderr)
        return 2
    routes = scan(args.root.resolve())
    if args.json:
        print(json.dumps([asdict(r) for r in routes], indent=2))
    else:
        report(routes)
    return 0


if __name__ == "__main__":
    sys.exit(main())

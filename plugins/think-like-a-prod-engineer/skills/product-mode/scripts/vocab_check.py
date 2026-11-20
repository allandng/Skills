#!/usr/bin/env python3
"""Find places where the codebase calls one thing by two names.

    python3 vocab_check.py glossary.csv <path-to-repo>
    python3 vocab_check.py glossary.csv <repo> --include src,app,docs
    python3 vocab_check.py --template > glossary.csv

If the interface says "Workspace", the schema, the API, the copy and the
analytics events should not say "Organization" or "Tenant". Every synonym is a
question a new teammate has to ask and a join an analyst gets wrong.

The glossary is a CSV with three columns:

    term        the one name for the thing: workspace
    not         names that must not be used for it, separated by semicolons
    definition  what it is, in a sentence

The script searches the repo for each banned name as a whole word, in any case
style (tenant, Tenant, TENANT_ID, tenantId, tenant_id). Exit code is 1 when it
finds any, so it runs in CI. A name that is legitimately used for something
else belongs in the glossary as its own term. Standard library only.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", "dist", "build", ".next", "vendor", "__pycache__", ".venv", "venv",
             "coverage", "Pods", ".gradle", "target", ".turbo"}
TEXT = {".ts", ".tsx", ".js", ".jsx", ".py", ".rb", ".go", ".rs", ".java", ".kt", ".swift", ".sql", ".prisma",
        ".graphql", ".json", ".yaml", ".yml", ".md", ".mdx", ".html", ".vue", ".svelte", ".css", ".scss", ".dart"}
TEMPLATE = """term,not,definition
workspace,organization;tenant;team_account,The top-level container a customer's data lives in
project,board;space,A body of work inside a workspace
"""


def pattern(word: str) -> re.Pattern[str]:
    """Match the word in snake, camel, Pascal or upper case, but not inside a longer word."""
    parts = [re.escape(p) for p in re.split(r"[\s_-]+", word.strip().lower()) if p]
    body = r"[\s_-]?".join(parts)
    # Lower-case letter before, or lower-case letter after, means it is part of another word.
    return re.compile(rf"(?<![A-Za-z])(?i:{body})(?:s|S)?(?![a-z])|(?<=[a-z])(?:{body.title()})(?:s)?(?![a-z])")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("glossary", nargs="?", type=Path)
    parser.add_argument("repo", nargs="?", type=Path)
    parser.add_argument("--include", help="comma-separated top-level folders to search (default: all)")
    parser.add_argument("--template", action="store_true")
    parser.add_argument("--max", type=int, default=8, help="examples to show per name")
    args = parser.parse_args()
    if args.template:
        print(TEMPLATE, end="")
        return 0
    if not args.glossary or not args.repo:
        parser.error("give a glossary and a repo, or --template")
    try:
        with args.glossary.open(newline="", encoding="utf-8-sig") as handle:
            entries = [{k: (v or "").strip() for k, v in row.items() if k} for row in csv.DictReader(handle)]
    except OSError as error:
        sys.exit(f"cannot read {args.glossary}: {error}")
    if not entries or not {"term", "not"} <= set(entries[0]):
        sys.exit("the glossary needs 'term' and 'not' columns. Run --template to see the format.")

    terms = {e["term"].lower() for e in entries}
    banned: list[tuple[str, str, re.Pattern[str]]] = []
    for entry in entries:
        for name in filter(None, (n.strip() for n in entry["not"].split(";"))):
            if name.lower() in terms:
                sys.exit(f"'{name}' is both a term and a banned name for '{entry['term']}'. Decide which.")
            banned.append((name, entry["term"], pattern(name)))

    roots = [args.repo / d for d in args.include.split(",")] if args.include else [args.repo]
    hits: dict[tuple[str, str], list[str]] = defaultdict(list)
    scanned = 0
    for root in roots:
        for path in sorted(root.rglob("*")) if root.is_dir() else []:
            if not path.is_file() or path.suffix not in TEXT or set(path.relative_to(args.repo).parts) & SKIP_DIRS:
                continue
            if path.resolve() == args.glossary.resolve():
                continue
            try:
                lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
            except OSError:
                continue
            scanned += 1
            for number, line in enumerate(lines, start=1):
                for name, term, regex in banned:
                    if regex.search(line):
                        hits[(name, term)].append(f"{path.relative_to(args.repo).as_posix()}:{number}")

    for (name, term), places in sorted(hits.items(), key=lambda kv: -len(kv[1])):
        files = len({p.rsplit(":", 1)[0] for p in places})
        print(f"FAIL  '{name}' is used {len(places)} time(s) in {files} file(s). The term is '{term}'.")
        for place in places[: args.max]:
            print(f"        {place}")
        if len(places) > args.max:
            print(f"        ... and {len(places) - args.max} more")
    print(f"\n{scanned:,} file(s) searched for {len(banned)} banned name(s): {len(hits)} in use.")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())

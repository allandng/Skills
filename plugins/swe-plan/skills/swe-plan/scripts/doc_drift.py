#!/usr/bin/env python3
"""Find planning docs that the code has moved past.

For each document in a bundle, reads its "Updated" date and every file path it
names, then asks git when each of those files last changed. A file that changed
after the document was last updated is a place the document may now be wrong.
A file the document names that no longer exists is a place it is wrong.

    python doc_drift.py docs/ <path-to-repo>
    python doc_drift.py docs/ <repo> --json

It finds where to look. It cannot tell whether the change mattered: read the
diff, then amend the document or bump its Updated date to say it was checked.
Exit code is 1 when anything drifted, so it can run in CI.

Python standard library only. Needs git.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_plan import extract  # noqa: E402

UPDATED = re.compile(r"^>\s*\*\*(?:Updated|Date):\*\*\s*(\d{4}-\d{2}-\d{2})", re.M)


def last_changed(repo: Path) -> dict[str, tuple[str, str]]:
    """Map each tracked path to (date, short hash) of the last commit that touched it."""
    out = subprocess.run(
        ["git", "-C", str(repo), "log", "--format=%x00%cs %h", "--name-only"],
        capture_output=True, text=True, check=True,
    ).stdout
    latest: dict[str, tuple[str, str]] = {}
    for chunk in out.split("\x00")[1:]:
        head, *files = chunk.strip().split("\n")
        date, commit = head.split(" ", 1)
        for name in files:
            name = name.strip()
            if name and name not in latest:  # log is newest first
                latest[name] = (date, commit)
    return latest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("docs", type=Path, help="the docs/ directory")
    parser.add_argument("repo", type=Path, help="the repository the docs describe")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not args.docs.is_dir():
        print(f"not a directory: {args.docs}", file=sys.stderr)
        return 2
    try:
        latest = last_changed(args.repo)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"cannot read git history in {args.repo}: is it a git repository, and is git installed?", file=sys.stderr)
        return 2

    repo = args.repo.resolve()
    docs_root = args.docs.resolve()
    report = []
    for doc in sorted(docs_root.rglob("*.md")):
        text = doc.read_text(encoding="utf-8", errors="replace")
        name = doc.relative_to(docs_root).as_posix()
        match = UPDATED.search(text)
        paths, declared_new, _ = extract(text)
        entry = {"doc": name, "updated": match.group(1) if match else None, "changed": [], "gone": []}
        for path in sorted(paths):
            target = repo / path
            if docs_root in target.resolve().parents or path.endswith("/"):
                continue
            if not target.exists():
                if path not in declared_new:
                    entry["gone"].append(path)
                continue
            if match and path in latest and latest[path][0] > match.group(1):
                entry["changed"].append({"path": path, "date": latest[path][0], "commit": latest[path][1]})
        entry["named"] = len(paths)
        report.append(entry)

    drifted = [e for e in report if e["changed"] or e["gone"]]
    undated = [e for e in report if e["updated"] is None and e["named"]]
    if args.json:
        print(json.dumps({"drifted": len(drifted), "docs": report}, indent=2))
    else:
        for entry in report:
            if not (entry["changed"] or entry["gone"]):
                continue
            print(f"\n{entry['doc']}  (updated {entry['updated'] or 'unknown'})")
            for item in entry["changed"]:
                print(f"  changed  {item['path']}  on {item['date']} in {item['commit']}")
            for path in entry["gone"]:
                print(f"  GONE     {path}  is named here and is not in the repo")
        for entry in undated:
            print(f"\n{entry['doc']}  names {entry['named']} path(s) but has no Updated date, so drift cannot be judged")
        clean = len(report) - len(drifted)
        print(f"\n{len(report)} doc(s): {len(drifted)} to re-read, {clean} with nothing changed underneath them")
        if drifted:
            print("For each: read the diff, then amend the doc, or bump its Updated date to record that it still holds.")
    return 1 if drifted else 0


if __name__ == "__main__":
    sys.exit(main())

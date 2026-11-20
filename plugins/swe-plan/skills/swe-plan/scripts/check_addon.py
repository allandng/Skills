#!/usr/bin/env python3
"""Check that an /addon plan holds together as a contract.

verify_plan.py asks "does everything this plan names exist?". This asks "does
the plan agree with itself?": the allowlist only names files that were read,
the seam and every phase stay inside the allowlist, every phase can be checked
and undone, and the parts that get skipped under time pressure are present.

    python check_addon.py docs/addons/<feature>.md
    python check_addon.py docs/addons/<feature>.md <path-to-repo>
    python check_addon.py <plan> <repo> --json

With a repo it also confirms that MAY TOUCH paths exist and WILL CREATE paths
do not exist yet. Exit code is 1 when a check fails. The plan format is the
"Addon plan" template in references/document-templates.md.

Python standard library only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_plan import clean_path, looks_like_path  # noqa: E402

REQUIRED_SECTIONS = [
    "Evidence ledger", "Scope fence", "Seam", "Options", "Blast radius",
    "Phases", "Grounding check", "Doc delta",
]
FENCE_LABELS = ["IN SCOPE", "OUT OF SCOPE", "MAY TOUCH", "WILL CREATE", "WILL NOT", "NOTICED"]
LEDGER_LABELS = ["VERIFIED", "INFERRED", "UNKNOWN"]
SEAM_LABELS = ["TOUCHES", "ADDS", "DATA", "INTERFACES", "DEPENDENCIES", "CONFIG"]
EMPTY = re.compile(r"^(\.\.\.|…|tbd|todo|n/?a|none yet|\?+|-+|<[^>]*>)?$", re.I)
BOILERPLATE = re.compile(r"^(nothing outside this list|stop and amend)", re.I)


def sections(text: str) -> dict[str, str]:
    """Body of each '## Heading', keyed by lowercased heading."""
    out: dict[str, str] = {}
    current, in_fence = None, False
    for line in text.split("\n"):
        if line.strip().startswith("```"):
            in_fence = not in_fence
        heading = None if in_fence else re.match(r"^##\s+(.+?)\s*$", line)
        if heading:
            current = heading.group(1).strip().lower()
            out[current] = ""
        elif current is not None:
            out[current] += line + "\n"
    return out


def find(secs: dict[str, str], name: str) -> str | None:
    key = name.lower()
    for heading, body in secs.items():
        if heading == key or heading.startswith(key):
            return body
    return None


def labeled_blocks(body: str, labels: list[str]) -> dict[str, list[str]]:
    """Split text into the lines that follow each all-caps label."""
    pattern = re.compile(rf"^\s*\**({'|'.join(re.escape(l) for l in labels)})\**\b[ \t:]*(.*)$", re.I)
    blocks: dict[str, list[str]] = {}
    current = None
    for line in body.split("\n"):
        if line.strip().startswith("```"):
            continue
        match = pattern.match(line)
        # Labels are written in capitals. A sentence starting "Adds a column" is not one.
        if match and match.group(1).upper() == match.group(1):
            current = match.group(1).upper()
            blocks.setdefault(current, [])
            if match.group(2).strip():
                blocks[current].append(match.group(2).strip())
        elif current and line.strip():
            blocks[current].append(line.strip())
    return blocks


def paths_in(lines: list[str]) -> set[str]:
    found = set()
    for line in lines:
        for token in re.findall(r"`([^`]+)`", line) + re.split(r"[\s,]+", line):
            candidate = clean_path(token)
            if looks_like_path(candidate):
                found.add(candidate)
    return found


def items(lines: list[str]) -> list[str]:
    return [l for l in lines if not BOILERPLATE.match(l.lstrip("-* 0123456789.")) and not EMPTY.match(l.lstrip("-* 0123456789.").strip())]


def covered(path: str, allowed: set[str]) -> bool:
    return path in allowed or any(a.endswith("/") and path.startswith(a) for a in allowed)


def phase_blocks(body: str) -> dict[str, str]:
    """Text of each P-## block, whether written as a heading, a table or a fenced list."""
    blocks: dict[str, str] = {}
    current = None
    for line in body.split("\n"):
        start = re.match(r"^\s*(?:#{2,6}\s+)?\**(P-\d{2,4})\b", line)
        if start:
            current = start.group(1)
            blocks[current] = ""
        if current:
            blocks[current] += line + "\n"
    return blocks


def field(block: str, name: str) -> str | None:
    """Value after a field label, across the layouts the templates use."""
    match = re.search(rf"^[\s|*]*{re.escape(name)}\**\s*[|:]?\s*(.*?)\s*\|?\s*$", block, re.I | re.M)
    if not match:
        return None
    value = match.group(1).strip(" |*")
    return "" if EMPTY.match(value) else value


def check(plan: Path, repo: Path | None) -> list[dict]:
    text = plan.read_text(encoding="utf-8", errors="replace")
    secs = sections(text)
    results: list[dict] = []

    def add(level: str, message: str) -> None:
        results.append({"level": level, "message": message})

    for name in REQUIRED_SECTIONS:
        if find(secs, name) is None:
            add("FAIL", f'no "## {name}" section')

    # ---- evidence ledger
    ledger = labeled_blocks(find(secs, "Evidence ledger") or "", LEDGER_LABELS)
    verified = paths_in(ledger.get("VERIFIED", []))
    inferred = paths_in(ledger.get("INFERRED", []))
    if find(secs, "Evidence ledger") is not None:
        if not items(ledger.get("VERIFIED", [])):
            add("FAIL", "evidence ledger has no VERIFIED entries: nothing in this plan was read")
        elif not verified:
            add("FAIL", "VERIFIED entries name no file paths: say which file confirmed each fact")
        if "INFERRED" not in ledger and "UNKNOWN" not in ledger:
            add("warn", "ledger has neither INFERRED nor UNKNOWN: a plan with nothing uncertain is rarely honest")
        else:
            add("ok", f"ledger: {len(verified)} verified path(s), {len(items(ledger.get('INFERRED', [])))} inferred, "
                      f"{len(items(ledger.get('UNKNOWN', [])))} unknown")

    # ---- scope fence
    fence_body = find(secs, "Scope fence")
    fence = labeled_blocks(fence_body or "", FENCE_LABELS)
    may_touch = paths_in(fence.get("MAY TOUCH", []))
    will_create = paths_in(fence.get("WILL CREATE", []))
    if fence_body is not None:
        if re.search(r"unconfirmed", fence_body, re.I):
            add("warn", "scope fence is UNCONFIRMED: the scope is one person's assumption")
        elif re.search(r"confirmed by\W+\w", fence_body, re.I):
            add("ok", "scope fence is confirmed")
        else:
            add("FAIL", 'scope fence says neither "Confirmed by: <who, when>" nor "Unconfirmed"')
        for label in ("IN SCOPE", "OUT OF SCOPE", "WILL NOT"):
            if not items(fence.get(label, [])):
                extra = " (the load-bearing half: name what a reader would expect and will not get)" if label == "OUT OF SCOPE" else ""
                add("FAIL", f"scope fence has no {label} entries{extra}")
        if not may_touch and not will_create:
            add("FAIL", "scope fence names no files under MAY TOUCH or WILL CREATE")
        unread = sorted(p for p in may_touch if not covered(p, verified))
        if unread:
            where = "only INFERRED" if any(p in inferred for p in unread) else "not in the VERIFIED ledger"
            add("FAIL", f"MAY TOUCH lists files that were never read ({where}): {', '.join(unread)}")
        elif may_touch:
            add("ok", f"all {len(may_touch)} MAY TOUCH path(s) are in the VERIFIED ledger")

    allowed = may_touch | will_create

    # ---- seam
    seam = labeled_blocks(find(secs, "Seam") or "", SEAM_LABELS)
    outside = sorted(p for p in paths_in(seam.get("TOUCHES", [])) if not covered(p, may_touch))
    if outside:
        add("FAIL", f"Seam TOUCHES files that are not in MAY TOUCH: {', '.join(outside)}")
    unplanned = sorted(p for p in paths_in(seam.get("ADDS", [])) if not covered(p, will_create))
    if unplanned:
        add("FAIL", f"Seam ADDS files that are not in WILL CREATE: {', '.join(unplanned)}")
    untouched = sorted(p for p in may_touch if seam.get("TOUCHES") and not covered(p, paths_in(seam["TOUCHES"])))
    if untouched:
        add("warn", f"MAY TOUCH allows files the Seam never touches (narrow the fence?): {', '.join(untouched)}")

    # ---- options
    options = find(secs, "Options")
    if options is not None:
        rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in options.split("\n") if l.strip().startswith("|")]
        header = next((r for r in rows if any(re.match(r"option\b", c, re.I) for c in r)), None)
        count = sum(bool(re.match(r"option\b", c, re.I)) for c in header) if header else 0
        if count < 2:
            add("FAIL", "Options compares fewer than two approaches: one option is a preference, not a plan")
        fails = next((r for r in rows if r and re.match(r"\**fails when", r[0], re.I)), None)
        if not fails:
            add("FAIL", 'Options has no "Fails when" row')
        elif any(EMPTY.match(c) for c in fails[1:1 + max(count, 1)]):
            add("FAIL", '"Fails when" is empty for at least one option')
        elif count >= 2:
            add("ok", f"{count} options, each with a failure condition")

    # ---- blast radius
    blast = find(secs, "Blast radius")
    if blast is not None:
        rollback = field(blast, "ROLLBACK")
        if not rollback:
            add("FAIL", "Blast radius has no ROLLBACK line saying exactly how to undo the change")

    # ---- phases
    phases = phase_blocks(find(secs, "Phases") or "")
    if find(secs, "Phases") is not None and not phases:
        add("FAIL", "Phases has no P-## blocks")
    for pid, block in phases.items():
        for name in ("Verified by", "Reverts by"):
            value = field(block, name)
            if value is None:
                add("FAIL", f"{pid} has no \"{name}\" line")
            elif not value:
                add("FAIL", f"{pid}: \"{name}\" is empty")
        touches = field(block, "Touches")
        if touches:
            stray = sorted(p for p in paths_in([touches]) if not covered(p, allowed))
            if stray:
                add("FAIL", f"{pid} touches files outside the fence: {', '.join(stray)}")
    if phases and not any(r["level"] == "FAIL" and r["message"].startswith("P-") for r in results):
        add("ok", f"{len(phases)} phase(s), each with a check and an undo, all inside the fence")

    # ---- grounding
    grounding = find(secs, "Grounding check")
    if grounding is not None and not re.search(r"\bclean\b|\b0 missing\b|missing\W+0\b|exists", grounding, re.I):
        add("warn", "Grounding check does not show a verify_plan.py result")

    # ---- against the repo
    if repo is not None:
        gone = sorted(p for p in may_touch if not (repo / p).exists())
        if gone:
            add("FAIL", f"MAY TOUCH names paths that are not in the repo: {', '.join(gone)}")
        present = sorted(p for p in will_create if (repo / p).exists() and not p.endswith("/"))
        if present:
            add("warn", f"WILL CREATE names files that already exist (already built, or a collision?): {', '.join(present)}")
        if not gone and may_touch:
            add("ok", "every MAY TOUCH path exists in the repo")

    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("plan", type=Path, help="the addon plan markdown file")
    parser.add_argument("repo", nargs="?", type=Path, help="the repository the plan describes")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not args.plan.is_file():
        print(f"plan not found: {args.plan}", file=sys.stderr)
        return 2
    if args.repo is not None and not args.repo.is_dir():
        print(f"repo not found: {args.repo}", file=sys.stderr)
        return 2
    results = check(args.plan, args.repo)
    failures = [r for r in results if r["level"] == "FAIL"]
    if args.json:
        print(json.dumps({"plan": str(args.plan), "failed": len(failures), "results": results}, indent=2))
    else:
        for r in results:
            print(f"{r['level']:<5} {r['message']}")
        print(f"\n{len(failures)} failure(s), {sum(r['level'] == 'warn' for r in results)} warning(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Check that an extraction folder is complete before it is handed off.

Confirms tokens.json parses and holds colors, that profile.md has a filled
Evidence block and Manual pass block (and a Structure block with --structure),
and counts how many claims carry each evidence label. Formats are in
references/evidence.md, references/extraction.md and references/app-dna.md.

    python3 dna_check.py ./dna/example
    python3 dna_check.py ./dna/example --structure

It checks that the work was done and labeled. It cannot check that the claims
are true: the round-trip specimen in references/evidence.md does that.

Standard library only. Python 3.11+.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

BLOCKS = {
    "Evidence": ["SOURCE", "CAPTURED", "COVERAGE", "THEMES", "NOT SEEN"],
    "Manual pass": ["SIGNATURE", "TYPE ROLES", "COLOR ROLES", "FRAMEWORK", "DEAD TOKENS", "GRID",
                    "STATES", "RHYTHM", "IMAGERY", "VOICE", "INTENT", "GAPS"],
    "Structure": ["SURFACE", "APP TYPE", "LOOP", "SHELL", "LEVELS", "SCREENS", "FLOWS", "STATES",
                  "COMPONENTS", "OVERLAYS", "DENSITY", "GAPS"],
}
LABELS = ("measured", "observed", "inferred", "guess")
# Lines that state what is missing or where things came from do not take a label.
UNLABELED = {"GAPS", "SOURCE", "CAPTURED", "COVERAGE", "THEMES", "NOT SEEN"}
COLOR = re.compile(r"^(#[0-9a-fA-F]{3,8}|(rgb|hsl|oklch|oklab|lab|lch|color)a?\(.+\))$")
PLACEHOLDER = re.compile(r"^(\.\.\.|…|tbd|todo|\?+|-+|<.*>)$", re.I)


def block(text: str, heading: str) -> str | None:
    match = re.search(rf"^##\s+{re.escape(heading)}\s*$(.*?)(?=^##\s|\Z)", text, re.S | re.M | re.I)
    if not match:
        return None
    return "\n".join(line for line in match.group(1).splitlines() if not line.strip().startswith("```"))


def fields(body: str, keys: list[str]) -> dict[str, str]:
    """Each KEY starts a line and runs until the next KEY."""
    pattern = re.compile(rf"^({'|'.join(re.escape(k) for k in sorted(keys, key=len, reverse=True))})\b[ \t:]*", re.M)
    found: dict[str, str] = {}
    marks = list(pattern.finditer(body))
    for i, mark in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(body)
        found.setdefault(mark.group(1), " ".join(body[mark.end():end].split()))
    return found


def check_tokens(folder: Path, problems: list[str]) -> None:
    path = folder / "tokens.json"
    if not path.is_file():
        problems.append("tokens.json is missing")
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        problems.append(f"tokens.json does not parse: {error}")
        return
    tokens = data.get("tokens", data) if isinstance(data, dict) else {}
    colors = {k: v for k, v in tokens.items() if isinstance(v, str) and COLOR.match(v.strip())}
    if len(colors) < 3:
        problems.append(f"tokens.json holds {len(colors)} color(s). A palette needs at least surface, ink and one more")
    pairs = data.get("pairs") if isinstance(data, dict) else None
    print(f"tokens.json    {len(colors)} color token(s), "
          + (f"{len(pairs)} declared pair(s)" if pairs else "no declared pairs: contrast.py is checking guesses"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("folder", type=Path, help="an extraction folder holding tokens.json and profile.md")
    parser.add_argument("--structure", action="store_true", help="also require the teardown's Structure block")
    args = parser.parse_args()
    if not args.folder.is_dir():
        print(f"not a folder: {args.folder}", file=sys.stderr)
        return 2

    problems: list[str] = []
    check_tokens(args.folder, problems)

    profile = args.folder / "profile.md"
    counts = dict.fromkeys(LABELS, 0)
    unlabeled: list[str] = []
    if not profile.is_file():
        problems.append("profile.md is missing")
    else:
        text = profile.read_text(encoding="utf-8")
        wanted = ["Evidence", "Manual pass"] + (["Structure"] if args.structure else [])
        for heading in wanted:
            body = block(text, heading)
            if body is None:
                problems.append(f'profile.md has no "## {heading}" block')
                continue
            found = fields(body, BLOCKS[heading])
            missing = [k for k in BLOCKS[heading] if k not in found]
            empty = [k for k, v in found.items() if not v or PLACEHOLDER.match(v)]
            if missing:
                problems.append(f"{heading}: no line for {', '.join(missing)}")
            if empty:
                problems.append(f"{heading}: nothing written for {', '.join(empty)}")
            for key, value in found.items():
                if key in UNLABELED or key in empty:
                    continue
                labels = re.findall(rf"\[({'|'.join(LABELS)})\]", value)
                if not labels:
                    unlabeled.append(f"{heading}/{key}")
                for label in labels:
                    counts[label] += 1
            print(f"{heading:<14} {len(found) - len(empty)} of {len(BLOCKS[heading])} line(s) filled")

    if unlabeled:
        problems.append("no evidence label on: " + ", ".join(unlabeled))
    total = sum(counts.values())
    if total:
        print("labels         " + ", ".join(f"{counts[l]} {l}" for l in LABELS))
        weak = counts["inferred"] + counts["guess"]
        if weak * 2 > total:
            print(f"note           {weak} of {total} claims are inferred or guessed. Say so first in the handoff.")

    for problem in problems:
        print(f"FAIL  {problem}")
    if not problems:
        print("ok    complete and labeled. Now run the round-trip specimen (references/evidence.md).")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

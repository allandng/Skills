#!/usr/bin/env python3
"""Check that every screen has every state its family requires.

Reads a states.json manifest (format in references/states.md) and fails when a
required state has no entry, points at a file that does not exist, quotes text
that is not in that file, or is marked n/a without a reason.

    python3 state_coverage.py states.json
    python3 state_coverage.py states.json --root ./apps/web
    python3 state_coverage.py --template collection:table,object:detail
    python3 state_coverage.py states.json --bundle docs/

With --bundle it also reads a planning bundle (the swe-plan skill's docs/) and
checks the screens against its use cases: every UC-## in the bundle is covered
by some screen's "covers" list, and every ID a screen claims to cover exists.

It cannot judge whether a state is well designed. It can show that one was
never made. Standard library only. Python 3.11+.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Keep in step with references/states.md, section 1.
REQUIRED: dict[str, list[str]] = {
    "entry": ["pristine", "invalid", "submitting", "submit-error", "resumed", "blocked"],
    "orientation": ["loading", "first-run", "partial", "error", "dense"],
    "collection": [
        "loading", "first-run", "no-results", "error", "offline",
        "permission-denied", "single-item", "dense", "max-length",
    ],
    "object": ["loading", "not-found", "error", "permission-denied", "max-length", "missing-fields"],
    "input": ["pristine", "invalid", "submitting", "submit-error", "success", "unsaved-exit"],
    "outcome": ["next-action"],
    "system": ["loading", "saving", "save-error", "saved", "permission-denied"],
}

OK, NA, FAIL = "ok", "n/a", "FAIL"


def family_of(screen_type: str) -> str:
    return screen_type.split(":", 1)[0].strip().lower()


def judge(value: object, root: Path) -> tuple[str, str]:
    """Return (verdict, detail) for one state's manifest value."""
    if not isinstance(value, str) or not value.strip():
        return FAIL, "no evidence given"
    value = value.strip()
    if value.lower().startswith("n/a"):
        reason = value[3:].lstrip(" :-").strip()
        return (NA, reason) if len(reason) >= 8 else (FAIL, "n/a needs a reason a reviewer could disagree with")
    path_part, _, needle = value.partition("#")
    path = (root / path_part.strip()).resolve()
    if not path.is_file():
        return FAIL, f"file not found: {path_part.strip()}"
    if needle:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as error:
            return FAIL, f"cannot read {path_part.strip()}: {error}"
        if needle.strip() not in text:
            return FAIL, f'"{needle.strip()}" is not in {path_part.strip()}'
    return OK, value


def template(types: list[str]) -> dict:
    screens = []
    for screen_type in types:
        family = family_of(screen_type)
        if family not in REQUIRED:
            raise SystemExit(f"unknown family '{family}'. Use one of: {', '.join(REQUIRED)}")
        screens.append({
            "name": "",
            "type": screen_type,
            "states": {state: "" for state in REQUIRED[family]},
        })
    return {"root": ".", "screens": screens}


def trace(screens: list[dict], bundle: Path) -> int:
    """Check screens' "covers" lists against the IDs a planning bundle defines."""
    text = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in sorted(bundle.rglob("*.md")))
    known = set(re.findall(r"\b(?:UC|PR|SR)-\d{2,4}\b", text))
    use_cases = sorted(i for i in known if i.startswith("UC-"))
    claimed: dict[str, list[str]] = {}
    for screen in screens:
        for ident in screen.get("covers") or []:
            claimed.setdefault(ident, []).append(screen.get("name") or "(unnamed)")
    failures = 0
    print(f"\nTrace against {bundle}")
    for ident in use_cases:
        if ident in claimed:
            print(f"  {OK:<5} {ident:<18} {', '.join(claimed[ident])}")
        else:
            print(f"  {FAIL:<5} {ident:<18} no screen covers this use case")
            failures += 1
    for ident in sorted(set(claimed) - known):
        print(f"  {FAIL:<5} {ident:<18} claimed by {', '.join(claimed[ident])} but not defined in the bundle")
        failures += 1
    if not use_cases:
        print(f"  {FAIL:<5} the bundle defines no UC-## use cases to trace against")
        failures += 1
    return failures


def check(manifest_path: Path, root_override: Path | None, bundle: Path | None = None) -> int:
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"cannot read {manifest_path}: {error}")
        return 2
    screens = manifest.get("screens")
    if not isinstance(screens, list) or not screens:
        print('manifest needs a non-empty "screens" list')
        return 2
    root = root_override or (manifest_path.parent / manifest.get("root", ".")).resolve()

    failures = covered = waived = 0
    for screen in screens:
        name = screen.get("name") or "(unnamed)"
        screen_type = screen.get("type", "")
        family = family_of(screen_type)
        print(f"\n{name}  [{screen_type or 'no type'}]")
        if family not in REQUIRED:
            print(f"  {FAIL:<5} type must start with one of: {', '.join(REQUIRED)}")
            failures += 1
            continue
        states = screen.get("states") or {}
        for state in REQUIRED[family]:
            verdict, detail = judge(states.get(state), root)
            print(f"  {verdict:<5} {state:<18} {detail}")
            failures += verdict == FAIL
            covered += verdict == OK
            waived += verdict == NA
        for extra in sorted(set(states) - set(REQUIRED[family])):
            verdict, detail = judge(states[extra], root)
            print(f"  {verdict:<5} {extra + ' (extra)':<18} {detail}")
            failures += verdict == FAIL
            covered += verdict == OK
            waived += verdict == NA

    total = covered + waived + failures
    untraced = trace(screens, bundle) if bundle else 0
    print(f"\n{len(screens)} screen(s), {total} state(s): {covered} shown, {waived} n/a, {failures} missing"
          + (f", {untraced} trace problem(s)" if bundle else ""))
    return 1 if failures or untraced else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("manifest", nargs="?", type=Path, help="path to states.json")
    parser.add_argument("--root", type=Path, help="resolve evidence paths against this folder")
    parser.add_argument("--bundle", type=Path, help="a planning bundle (docs/) to trace screens against")
    parser.add_argument("--template", metavar="TYPES",
                        help="print a blank manifest for comma-separated family:type values")
    args = parser.parse_args()
    if args.template:
        print(json.dumps(template([t.strip() for t in args.template.split(",") if t.strip()]), indent=2))
        return 0
    if not args.manifest:
        parser.error("give a manifest path, or --template")
    if args.bundle and not args.bundle.is_dir():
        parser.error(f"not a directory: {args.bundle}")
    return check(args.manifest, args.root.resolve() if args.root else None, args.bundle)


if __name__ == "__main__":
    sys.exit(main())

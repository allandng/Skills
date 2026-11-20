#!/usr/bin/env python3
"""Lint a tracking plan, and compare it with the events that actually fire.

    python3 tracking_plan.py lint plan.csv
    python3 tracking_plan.py diff plan.csv events.csv
    python3 tracking_plan.py template > plan.csv

The plan is a CSV, so it can live in a spreadsheet and in the repo. One row per
event, with these columns:

    event        snake_case, object first then a past-tense action: ticket_purchased
    description  what happened, in a sentence a new teammate would understand
    trigger      the exact moment it fires, and where (client or server)
    properties   name:type pairs separated by semicolons. Types: string, int,
                 float, bool, timestamp, enum(a|b|c)
    owner        the person or team who answers questions about it
    status       planned, live, or deprecated
    pii          none, pseudonymous, or personal

lint fails on names that break the convention, duplicates and near-duplicates,
empty fields, untyped properties, and properties that look like personal data
in an event not marked personal. diff needs an events file (user_id, event,
timestamp) and reports events that fire but are not in the plan, live events
that never fire, and deprecated events that still do.

Exit code is 1 when anything fails, so both run in CI. Standard library only.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter
from pathlib import Path

COLUMNS = ["event", "description", "trigger", "properties", "owner", "status", "pii"]
NAME = re.compile(r"^[a-z][a-z0-9]*(_[a-z0-9]+)+$")
PROPERTY = re.compile(r"^[a-z][a-z0-9_]*$")
TYPE = re.compile(r"^(string|int|float|bool|timestamp|enum\([^()|]+(\|[^()|]+)+\))$")
STATUSES = {"planned", "live", "deprecated"}
PII = {"none", "pseudonymous", "personal"}
# A word anywhere in the name, or one of a few whole names. "step_name" is not a person's name.
PERSONAL = re.compile(r"(^|_)(email|phone|address|street|postcode|zip|ip|dob|birth|birthday|ssn|password|"
                      r"latitude|longitude)(_|$)|^(name|first_name|last_name|full_name|user_name|username|"
                      r"customer_name|card_number|lat|lng)$")
EMPTY = re.compile(r"^(\.\.\.|tbd|todo|\?+|-+|n/?a)?$", re.I)

TEMPLATE = """event,description,trigger,properties,owner,status,pii
signup_completed,A new account exists and the user is signed in,Server: after the account row is committed,method:enum(email|google|apple);referrer_source:string,growth,live,pseudonymous
onboarding_step_completed,The user finished one step of onboarding,Client: on the step's continue action,step_name:string;step_index:int;seconds_on_step:float,growth,live,pseudonymous
"""


def stem(name: str) -> tuple[str, ...]:
    """A name reduced to its sorted word stems, to catch the same event named twice."""
    words = []
    for word in name.split("_"):
        for suffix in ("ing", "ed", "es", "s", "d"):
            if len(word) > len(suffix) + 2 and word.endswith(suffix):
                word = word[: -len(suffix)]
                break
        words.append(word[:-1] if len(word) > 3 and word.endswith("e") else word)
    return tuple(sorted(words))


def read_plan(path: Path) -> list[dict]:
    try:
        with path.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            missing = [c for c in COLUMNS if c not in (reader.fieldnames or [])]
            if missing:
                sys.exit(f"{path} is missing column(s): {', '.join(missing)}. Run 'template' to see the format.")
            return [{k: (v or "").strip() for k, v in row.items() if k} for row in reader]
    except OSError as error:
        sys.exit(f"cannot read {path}: {error}")


def lint(rows: list[dict]) -> tuple[list[str], list[str]]:
    errors, warnings = [], []
    seen: dict[str, int] = {}
    stems: dict[tuple[str, ...], str] = {}
    for number, row in enumerate(rows, start=2):
        name = row["event"]
        where = f"line {number} ({name or 'unnamed'})"
        if not name:
            errors.append(f"{where}: no event name")
            continue
        if not NAME.match(name):
            errors.append(f"{where}: name must be snake_case with at least two words, object then action "
                          f"(ticket_purchased, not purchase or TicketPurchased)")
        if name in seen:
            errors.append(f"{where}: duplicate of line {seen[name]}")
        seen.setdefault(name, number)
        key = stem(name)
        if key in stems and stems[key] != name:
            errors.append(f"{where}: looks like the same event as {stems[key]} under another name. Keep one.")
        stems.setdefault(key, name)
        for column in ("description", "trigger", "owner"):
            if EMPTY.match(row[column]):
                errors.append(f"{where}: no {column}")
        if row["trigger"] and not re.search(r"client|server|backend|webhook|job", row["trigger"], re.I):
            warnings.append(f"{where}: trigger does not say whether it fires on the client or the server")
        if row["status"] not in STATUSES:
            errors.append(f"{where}: status must be one of {', '.join(sorted(STATUSES))}")
        if row["pii"] not in PII:
            errors.append(f"{where}: pii must be one of {', '.join(sorted(PII))}")
        for pair in filter(None, (p.strip() for p in row["properties"].split(";"))):
            prop, _, kind = pair.partition(":")
            prop, kind = prop.strip(), kind.strip()
            if not PROPERTY.match(prop):
                errors.append(f"{where}: property '{prop}' must be snake_case")
            if not TYPE.match(kind):
                errors.append(f"{where}: property '{prop}' needs a type: string, int, float, bool, timestamp, or enum(a|b)")
            is_reference = prop.endswith(("_id", "_count", "_type"))  # an ID of an address is not an address
            if PERSONAL.search(prop) and not is_reference and row["pii"] != "personal":
                errors.append(f"{where}: property '{prop}' looks like personal data but pii is '{row['pii']}'. "
                              "Send an ID instead, or mark the event personal and say why it is needed.")
        if row["pii"] == "personal":
            warnings.append(f"{where}: carries personal data. Analytics rarely needs it: can an ID do the job?")
    return errors, warnings


def cmd_lint(args) -> int:
    rows = read_plan(args.plan)
    errors, warnings = lint(rows)
    for message in errors:
        print(f"FAIL  {message}")
    for message in warnings:
        print(f"warn  {message}")
    by_status = Counter(r["status"] for r in rows)
    print(f"\n{len(rows)} event(s): " + ", ".join(f"{n} {s or 'no status'}" for s, n in sorted(by_status.items()))
          + f". {len(errors)} failure(s), {len(warnings)} warning(s).")
    return 1 if errors else 0


def cmd_diff(args) -> int:
    rows = read_plan(args.plan)
    status = {r["event"]: r["status"] for r in rows}
    fired: Counter = Counter()
    try:
        with args.events.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            if "event" not in (reader.fieldnames or []):
                sys.exit(f"{args.events} has no 'event' column")
            for row in reader:
                fired[(row["event"] or "").strip()] += 1
    except OSError as error:
        sys.exit(f"cannot read {args.events}: {error}")
    fired.pop("", None)
    problems = 0
    for name, count in fired.most_common():
        if name not in status:
            print(f"FAIL  {name}: fires ({count:,} times) but is not in the plan. Nobody has said what it means.")
            problems += 1
        elif status[name] == "deprecated":
            print(f"FAIL  {name}: marked deprecated but still fires ({count:,} times)")
            problems += 1
        elif status[name] == "planned":
            print(f"warn  {name}: marked planned but already fires ({count:,} times). Set it to live.")
    for name, state in status.items():
        if state == "live" and name not in fired:
            print(f"FAIL  {name}: marked live but never fires in this file. Broken tracking, or a window too short to see it.")
            problems += 1
    total = sum(fired.values())
    print(f"\n{len(fired)} distinct event(s) fired {total:,} times. {len(status)} in the plan. {problems} problem(s).")
    return 1 if problems else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    one = sub.add_parser("lint", help="check the plan against the conventions")
    one.add_argument("plan", type=Path)
    one.set_defaults(run=cmd_lint)
    two = sub.add_parser("diff", help="compare the plan with an events file")
    two.add_argument("plan", type=Path)
    two.add_argument("events", type=Path)
    two.set_defaults(run=cmd_diff)
    three = sub.add_parser("template", help="print a starter plan")
    three.set_defaults(run=lambda _: print(TEMPLATE, end="") or 0)
    args = parser.parse_args()
    return args.run(args)


if __name__ == "__main__":
    sys.exit(main())

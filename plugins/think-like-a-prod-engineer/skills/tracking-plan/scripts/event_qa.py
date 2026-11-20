#!/usr/bin/env python3
"""Find the tracking faults that quietly corrupt every chart built on them.

    python3 event_qa.py events.csv
    python3 event_qa.py events.csv --platform-column platform
    python3 event_qa.py events.csv --requires project_created:signup_completed
    python3 event_qa.py events.csv --json

Run it on a few days of events before a launch is called instrumented, and
again on a schedule. It checks six things, each a known way for analytics to
lie (references/event-edge-cases.md explains the cause of each):

  double fires     the same user and event twice within --dup-window seconds
  platform gaps    an event that fires on one platform and never on another
  order            users who did a later step with no trace of the earlier one
  clocks           timestamps after the file's real end (give --as-of to be exact)
  heavy users      one "user" with an impossible volume: a bot, a test account
  blank fields     a property column that is empty for part of an event

Events file: user_id, event, timestamp, plus any property columns. Exit code is
1 when a check fails. Standard library only.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


def parse_ts(value: str) -> float:
    stamp = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    return (stamp if stamp.tzinfo else stamp.replace(tzinfo=timezone.utc)).timestamp()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("events", type=Path)
    parser.add_argument("--dup-window", type=float, default=2.0, help="seconds within which a repeat counts as a double fire")
    parser.add_argument("--dup-rate", type=float, default=0.01, help="share of an event's rows that may be double fires")
    parser.add_argument("--platform-column", default="platform")
    parser.add_argument("--requires", action="append", default=[], metavar="LATER:EARLIER",
                        help="an event that should never happen without an earlier one. Repeatable")
    parser.add_argument("--heavy", type=int, default=500, help="events from one user in one day that is not a person")
    parser.add_argument("--blank-rate", type=float, default=0.01)
    parser.add_argument("--as-of", help="when the file was exported (ISO 8601). Anything a day later is a bad clock")
    parser.add_argument("--clock-gap", type=float, default=3.0,
                        help="without --as-of: days of silence that separate stragglers from the file")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    rows: list[tuple[str, str, float, dict]] = []
    bad = 0
    try:
        with args.events.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            fields = reader.fieldnames or []
            missing = [c for c in ("user_id", "event", "timestamp") if c not in fields]
            if missing:
                sys.exit(f"{args.events} is missing column(s): {', '.join(missing)}")
            extra = [c for c in fields if c not in ("user_id", "event", "timestamp")]
            for row in reader:
                try:
                    rows.append((row["user_id"].strip(), row["event"].strip(), parse_ts(row["timestamp"]), row))
                except (ValueError, AttributeError):
                    bad += 1
    except OSError as error:
        sys.exit(f"cannot read {args.events}: {error}")
    if not rows:
        sys.exit("no readable rows")

    findings: list[dict] = []

    def add(level: str, check: str, message: str) -> None:
        findings.append({"level": level, "check": check, "message": message})

    if bad:
        add("FAIL", "format", f"{bad:,} row(s) have an unreadable timestamp")

    per_event = Counter(event for _, event, _, _ in rows)

    # ---- double fires
    last: dict[tuple[str, str], float] = {}
    doubles: Counter = Counter()
    for user, event, ts, _ in sorted(rows, key=lambda r: r[2]):
        key = (user, event)
        if key in last and ts - last[key] <= args.dup_window:
            doubles[event] += 1
        last[key] = ts
    clean = True
    for event, count in doubles.most_common():
        rate = count / per_event[event]
        if rate > args.dup_rate:
            clean = False
            add("FAIL", "double fires", f"{event}: {count:,} of {per_event[event]:,} rows ({rate:.1%}) repeat within "
                                         f"{args.dup_window:g}s for the same user. Counts and funnels for it are inflated.")
    if clean:
        add("ok", "double fires", f"no event repeats within {args.dup_window:g}s more than {args.dup_rate:.0%} of the time")

    # ---- platform gaps
    column = args.platform_column
    if column in extra:
        users_on: dict[str, set[str]] = defaultdict(set)
        fires_on: dict[str, Counter] = defaultdict(Counter)
        for user, event, _, row in rows:
            platform = (row.get(column) or "").strip()
            if platform:
                users_on[platform].add(user)
                fires_on[event][platform] += 1
        total_users = len({u for s in users_on.values() for u in s}) or 1
        major = [p for p, s in users_on.items() if len(s) / total_users >= 0.05]
        gaps = 0
        for event, by in sorted(fires_on.items()):
            absent = [p for p in major if by[p] == 0]
            if absent and sum(by.values()) >= 50:
                gaps += 1
                add("FAIL", "platform gaps", f"{event}: fires on {', '.join(sorted(p for p in by if by[p]))} and never on "
                                              f"{', '.join(sorted(absent))}. Missing tracking there, or a feature that does not "
                                              "exist there. Either way a cross-platform chart of it is wrong.")
        if not gaps:
            add("ok", "platform gaps", f"every event with volume fires on all of: {', '.join(sorted(major))}")
    else:
        add("warn", "platform gaps", f"no '{column}' column, so platform coverage was not checked. "
                                     "Put the user's platform on every event, including server-side ones.")

    # ---- order
    seen_by_user: dict[str, dict[str, float]] = defaultdict(dict)
    for user, event, ts, _ in rows:
        if event not in seen_by_user[user] or ts < seen_by_user[user][event]:
            seen_by_user[user][event] = ts
    for pair in args.requires:
        later, _, earlier = pair.partition(":")
        if later not in per_event or earlier not in per_event:
            add("FAIL", "order", f"--requires {pair}: no such event in the file")
            continue
        did = [u for u, seen in seen_by_user.items() if later in seen]
        orphans = [u for u in did if earlier not in seen_by_user[u] or seen_by_user[u][earlier] > seen_by_user[u][later]]
        rate = len(orphans) / len(did)
        if rate > 0.005:
            add("FAIL", "order", f"{len(orphans):,} of {len(did):,} users ({rate:.1%}) have {later} with no earlier "
                                 f"{earlier}. Usually two identities for one person, or {earlier} not firing. "
                                 f"Example ids: {', '.join(orphans[:3])}")
        else:
            add("ok", "order", f"{later} is preceded by {earlier} for {1 - rate:.1%} of users")

    # ---- clocks
    # With --as-of, anything after the export time is wrong. Without it, look for stragglers: events
    # separated from the body of the file by a gap of days, within its last 1% of rows.
    stamps = sorted(ts for _, _, ts, _ in rows)
    edge = None
    if args.as_of:
        edge = parse_ts(args.as_of) + 86400
    else:
        tail = max(1, len(stamps) // 100)
        for i in range(len(stamps) - tail, len(stamps)):
            if i > 0 and stamps[i] - stamps[i - 1] > args.clock_gap * 86400:
                edge = stamps[i - 1]
                break
    ahead = [r for r in rows if edge is not None and r[2] > edge]
    if ahead:
        worst = max(r[2] for r in ahead)
        add("FAIL", "clocks", f"{len(ahead):,} event(s) are stamped after the rest of the file ends, the latest at "
                              f"{datetime.fromtimestamp(worst, timezone.utc):%Y-%m-%d}. Device clocks are wrong: use the "
                              "server's receive time for ordering and windows.")
    else:
        add("ok", "clocks", "no timestamps ahead of the rest of the file")

    # ---- heavy users
    per_user_day: Counter = Counter((user, int(ts // 86400)) for user, _, ts, _ in rows)
    heavy = Counter()
    for (user, _), count in per_user_day.items():
        if count >= args.heavy:
            heavy[user] = max(heavy[user], count)
    if heavy:
        listed = ", ".join(f"{u} ({c:,}/day)" for u, c in heavy.most_common(5))
        add("FAIL", "heavy users", f"{len(heavy)} user(s) sent {args.heavy:,}+ events in a day: {listed}. "
                                   "Bots, scripts or test accounts. Exclude them before computing anything.")
    else:
        add("ok", "heavy users", f"nobody sent {args.heavy:,}+ events in a day")

    # ---- blank fields
    blanks = 0
    for name in extra:
        empty: Counter = Counter()
        for _, event, _, row in rows:
            if not (row.get(name) or "").strip():
                empty[event] += 1
        for event, count in empty.most_common():
            rate = count / per_event[event]
            if args.blank_rate < rate < 0.999 and count >= 5:
                blanks += 1
                add("FAIL", "blank fields", f"{event}: '{name}' is empty on {count:,} of {per_event[event]:,} rows ({rate:.1%}). "
                                             "A segment by it silently drops those rows. Often a server-side event that "
                                             "lost the client's context.")
    if not blanks:
        add("ok", "blank fields", "no property is partly empty within an event")

    failures = [f for f in findings if f["level"] == "FAIL"]
    if args.json:
        print(json.dumps({"rows": len(rows), "failed": len(failures), "findings": findings}, indent=2))
    else:
        print(f"{len(rows):,} events, {len(per_event)} distinct, {len(seen_by_user):,} users.\n")
        for f in findings:
            print(f"{f['level']:<5} {f['check']:<14} {f['message']}")
        print(f"\n{len(failures)} failure(s). " + ("Fix the tracking before trusting a chart built on these events."
                                                    if failures else "Nothing here stops you reading the data."))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

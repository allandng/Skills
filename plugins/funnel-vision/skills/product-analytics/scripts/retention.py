#!/usr/bin/env python3
"""Measure retention, and look for early behaviours that go with it.

    python3 retention.py events.csv --start-event signup --return-event session_started
    python3 retention.py events.csv --start-event signup --days 1,7,28 --by source
    python3 retention.py events.csv --start-event signup --unit week --periods 1,4,8
    python3 retention.py events.csv --start-event signup --candidates --first-days 3 --target 28

The definition, so the number can be reproduced by hand:

  * A user's clock starts at their first --start-event.
  * "Retained on day N" means at least one --return-event (default: any event
    other than the start event) between N and N+1 days after that moment.
    These are rolling 24-hour windows from the user's own start, not calendar
    days. With --unit week, period N is days 7N to 7N+6.
  * A user counts toward day N only if day N has fully passed for them. Without
    this, recent users who have not had the chance to return are counted as
    lost, and retention looks like it is falling when it is not.

--candidates compares users who did each event at least k times in their first
days against users who did not. It finds behaviours that GO WITH retention. It
cannot show that the behaviour CAUSES retention: people who were going to stay
anyway do more of everything. Treat each row as a hypothesis for an experiment.

Every rate has n and a 95% Wilson interval. Standard library only.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _events import DAY, diff_interval, load, load_report, pct, wilson  # noqa: E402


def returned(events, t0: float, start: float, stop: float, start_event: str, return_event: str | None) -> bool:
    for ts, name, _ in events:
        if t0 + start <= ts < t0 + stop and (name == return_event if return_event else name != start_event):
            return True
    return False


def line(label: str, kept: int, n: int, width: int = 22) -> str:
    low, high = wilson(kept, n)
    return f"  {label:<{width}}{pct(kept / n if n else 0)}   {pct(low).strip():>6} to {pct(high).strip():<6}   n={n:,}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("events", type=Path)
    parser.add_argument("--start-event", required=True)
    parser.add_argument("--return-event", help="default: any event other than the start event")
    parser.add_argument("--unit", choices=["day", "week"], default="day")
    parser.add_argument("--days", "--periods", dest="periods", default=None,
                        help="comma-separated periods (default 1,7,28 for days; 1,4,8 for weeks)")
    parser.add_argument("--by", help="a property column to segment by, read at the start event")
    parser.add_argument("--cohorts", action="store_true", help="also break down by the week users started")
    parser.add_argument("--candidates", action="store_true", help="rank early behaviours by how they go with retention")
    parser.add_argument("--first-days", type=float, default=3.0, help="how long 'early' is, for --candidates")
    parser.add_argument("--target", type=int, help="the period that counts as retained, for --candidates")
    parser.add_argument("--min-n", type=int, default=100)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    span = DAY if args.unit == "day" else 7 * DAY
    periods = [int(p) for p in (args.periods or ("1,7,28" if args.unit == "day" else "1,4,8")).split(",")]
    users, end, notes = load(args.events)

    starts: dict[str, tuple[float, dict]] = {}
    for uid, events in users.items():
        first = next(((ts, props) for ts, name, props in events if name == args.start_event), None)
        if first:
            starts[uid] = first
    if not starts:
        known = sorted({name for events in users.values() for _, name, _ in events})
        sys.exit(f"no '{args.start_event}' events in the file. Events present: {', '.join(known)}")

    def measure(uids: list[str], period: int) -> tuple[int, int]:
        """(retained, mature) for one period among these users."""
        mature = [u for u in uids if starts[u][0] + (period + 1) * span <= end]
        kept = sum(returned(users[u], starts[u][0], period * span, (period + 1) * span,
                            args.start_event, args.return_event) for u in mature)
        return kept, len(mature)

    everyone = list(starts)
    out: dict = {"unit": args.unit, "start_event": args.start_event, "return_event": args.return_event or "(any)",
                 "started": len(everyone), "overall": {}}

    if not args.json:
        print(load_report(notes, end))
        print(f"{len(everyone):,} users have a '{args.start_event}'. Returned = "
              f"{'any other event' if not args.return_event else repr(args.return_event)} in the period. "
              f"Only users whose period has fully passed are counted.")
        print(f"\nRetention by {args.unit}")
    for period in periods:
        kept, n = measure(everyone, period)
        out["overall"][period] = {"retained": kept, "n": n, "rate": kept / n if n else None, "interval": wilson(kept, n)}
        if args.json:
            continue
        if n == 0:
            print(f"  {args.unit} {period:<17}no users are old enough yet")
            continue
        print(line(f"{args.unit} {period}", kept, n))
    if not args.json and len(periods) >= 2:
        rates = [(p, out["overall"][p]["rate"]) for p in periods if out["overall"][p]["rate"]]
        if len(rates) >= 2 and rates[-2][1]:
            ratio = rates[-1][1] / rates[-2][1]
            print(f"\n{args.unit.capitalize()} {rates[-1][0]} keeps {pct(ratio).strip()} of {args.unit} {rates[-2][0]}'s level. "
                  + ("The curve is flattening: the users still here mostly stay." if ratio >= 0.85 else
                     "The curve is still falling: users are still leaving at this point."))

    groups: dict[str, dict[str, list[str]]] = {}
    if args.by:
        by: dict[str, list[str]] = defaultdict(list)
        for uid, (_, props) in starts.items():
            by[props.get(args.by) or "(blank)"].append(uid)
        groups[args.by] = by
    if args.cohorts:
        weeks: dict[str, list[str]] = defaultdict(list)
        for uid, (t0, _) in starts.items():
            monday = datetime.fromtimestamp(t0 - datetime.fromtimestamp(t0, timezone.utc).weekday() * DAY, timezone.utc)
            weeks[f"{monday:%Y-%m-%d}"].append(uid)
        groups["start week"] = dict(sorted(weeks.items()))
    for title, by in groups.items():
        out[title] = {}
        if not args.json:
            print(f"\nBy {title}  (" + ", ".join(f"{args.unit} {p}" for p in periods) + ")")
        for name, uids in (by.items() if title == "start week" else sorted(by.items(), key=lambda kv: -len(kv[1]))):
            cells = []
            out[title][name] = {}
            for period in periods:
                kept, n = measure(uids, period)
                out[title][name][period] = {"retained": kept, "n": n}
                cells.append("   too few" if n < args.min_n and title != "start week" else
                             ("      -   " if n == 0 else f"{pct(kept / n)} ({n:,})".rjust(14)))
            if not args.json:
                print(f"  {name:<18}" + " ".join(c.rjust(14) for c in cells))
        if not args.json and title != "start week":
            print("  A segment that retains worse may just be a different kind of user. Check the mix before the cause.")

    if args.candidates:
        target = args.target or periods[-1]
        early = args.first_days * DAY
        mature = [u for u in everyone if starts[u][0] + (target + 1) * span <= end]
        kept_by_user = {u: returned(users[u], starts[u][0], target * span, (target + 1) * span,
                                    args.start_event, args.return_event) for u in mature}
        counts: dict[str, Counter] = {}
        for u in mature:
            t0 = starts[u][0]
            counts[u] = Counter(name for ts, name, _ in users[u] if t0 < ts <= t0 + early and name != args.start_event)
        names = sorted({name for c in counts.values() for name in c})
        rows = []
        for name in names:
            for k in (1, 2, 3, 5):
                did = [u for u in mature if counts[u][name] >= k]
                rest = [u for u in mature if counts[u][name] < k]
                if len(did) < args.min_n or len(rest) < args.min_n:
                    continue
                a, b = sum(kept_by_user[u] for u in did), sum(kept_by_user[u] for u in rest)
                rows.append({"event": name, "at_least": k, "did_n": len(did), "share": len(did) / len(mature),
                             "did_rate": a / len(did), "rest_rate": b / len(rest),
                             "difference": a / len(did) - b / len(rest),
                             "interval": diff_interval(a, len(did), b, len(rest))})
        rows.sort(key=lambda r: -r["difference"])
        out["candidates"] = rows
        if not args.json:
            print(f"\nEarly behaviours and {args.unit}-{target} retention  "
                  f"(first {args.first_days:g} days, {len(mature):,} users old enough)")
            print(f"  {'did this early':<34}{'share':>7}  {'retained':>9}  {'others':>8}  {'difference':>11}  95% interval")
            for r in rows[:12]:
                low, high = r["interval"]
                print(f"  {(r['event'] + ' x' + str(r['at_least'])):<34}{pct(r['share']):>7}  {pct(r['did_rate']):>9}  "
                      f"{pct(r['rest_rate']):>8}  {100 * r['difference']:>+9.1f}pt  {100 * low:+.1f} to {100 * high:+.1f}")
            if not rows:
                print(f"  no behaviour has at least {args.min_n} users on both sides")
            print("\nThese go WITH retention. None is shown to CAUSE it: users who were going to stay do more of "
                  "everything.\nPick one that the product could plausibly move, and test it (see the experiment skill).")

    if args.json:
        print(json.dumps(out, indent=2, default=list))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Measure an ordered funnel from an events file.

    python3 funnel.py events.csv --steps signup,profile_completed,first_project_created
    python3 funnel.py events.csv --steps signup,profile_completed --window-days 7 --by platform
    python3 funnel.py events.csv --steps ... --json

The definition, so the number can be reproduced by hand:

  * A user enters at their first occurrence of the first step.
  * Each later step counts if it happens at or after the step before it and
    within --window-days of entering. Order matters. Repeats do not.
  * Users who entered less than one window before the data ends are left out.
    They have not had their full chance yet, and counting them makes recent
    conversion look worse than it is. The number left out is printed.

Every rate is shown with n and a 95% Wilson interval. A segment below --min-n
users is marked too small to read. Events file format: see _events.py.
Standard library only.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from statistics import median

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _events import DAY, load, load_report, pct, wilson  # noqa: E402


def walk(events, steps: list[str], window: float):
    """Times at which this user reached each step, or None from the first miss on."""
    entry = next((ts for ts, name, _ in events if name == steps[0]), None)
    if entry is None:
        return None, None
    times = [entry]
    props = next(p for ts, name, p in events if name == steps[0] and ts == entry)
    for step in steps[1:]:
        hit = next((ts for ts, name, _ in events if name == step and times[-1] <= ts <= entry + window), None)
        if hit is None:
            break
        times.append(hit)
    return times, props


def summarize(reached: list[list[float]], steps: list[str]) -> list[dict]:
    rows = []
    for i, step in enumerate(steps):
        here = [t for t in reached if len(t) > i]
        prev = len([t for t in reached if len(t) > i - 1]) if i else len(here)
        row = {"step": step, "users": len(here), "of_start": len(here) / len(reached) if reached else 0.0}
        if i:
            row["of_previous"] = len(here) / prev if prev else 0.0
            row["interval"] = wilson(len(here), prev)
            row["lost"] = prev - len(here)
            gaps = [t[i] - t[i - 1] for t in here]
            row["median_seconds"] = median(gaps) if gaps else None
            row["p90_seconds"] = sorted(gaps)[min(len(gaps) - 1, int(len(gaps) * 0.9))] if gaps else None
        rows.append(row)
    return rows


def human(seconds: float | None) -> str:
    if seconds is None:
        return "-"
    for unit, size in (("d", DAY), ("h", 3600), ("m", 60)):
        if seconds >= size:
            return f"{seconds / size:.1f}{unit}"
    return f"{seconds:.0f}s"


def show(rows: list[dict], title: str) -> None:
    print(f"\n{title}")
    print(f"  {'step':<28}{'users':>8}  {'of previous':>12}  {'95% interval':>17}  {'of start':>9}  {'median wait':>11}  {'p90 wait':>9}")
    for row in rows:
        if "of_previous" in row:
            low, high = row["interval"]
            print(f"  {row['step']:<28}{row['users']:>8,}  {pct(row['of_previous']):>12}  "
                  f"{pct(low).strip():>7} to {pct(high).strip():<6}  {pct(row['of_start']):>9}  {human(row['median_seconds']):>11}  {human(row['p90_seconds']):>9}")
        else:
            print(f"  {row['step']:<28}{row['users']:>8,}  {'':>12}  {'':>17}  {pct(row['of_start']):>9}  {'':>11}  {'':>9}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("events", type=Path)
    parser.add_argument("--steps", required=True, help="comma-separated event names, in order")
    parser.add_argument("--window-days", type=float, default=7.0)
    parser.add_argument("--by", help="a property column to segment by, read at the first step")
    parser.add_argument("--min-n", type=int, default=100)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    steps = [s.strip() for s in args.steps.split(",") if s.strip()]
    if len(steps) < 2:
        parser.error("a funnel needs at least two steps")

    users, end, notes = load(args.events)
    window = args.window_days * DAY
    known = {name for events in users.values() for _, name, _ in events}
    unknown = [s for s in steps if s not in known]
    if unknown:
        sys.exit(f"no such event in the file: {', '.join(unknown)}. Events present: {', '.join(sorted(known))}")

    reached, segments, immature = [], {}, 0
    for events in users.values():
        times, props = walk(events, steps, window)
        if times is None:
            continue
        if times[0] > end - window:
            immature += 1
            continue
        reached.append(times)
        if args.by:
            segments.setdefault(props.get(args.by) or "(blank)", []).append(times)
    if not reached:
        sys.exit("nobody entered the funnel early enough to have a full window. Shorten --window-days or get more data.")

    overall = summarize(reached, steps)
    if args.json:
        print(json.dumps({
            "steps": steps, "window_days": args.window_days, "entered": len(reached),
            "left_out_immature": immature, "overall": overall,
            "segments": {k: summarize(v, steps) for k, v in segments.items()},
        }, indent=2))
        return 0

    print(load_report(notes, end))
    print(f"Funnel: {' > '.join(steps)}, each within {args.window_days:g} days of entering.")
    print(f"{len(reached):,} users entered with a full window. {immature:,} entered too recently and are left out.")
    show(overall, "All users")
    worst = max(overall[1:], key=lambda r: r["lost"])
    before = overall[overall.index(worst) - 1]["step"]
    print(f"\nLargest loss: {worst['lost']:,} users between {before} and {worst['step']} "
          f"({pct(1 - worst['of_previous']).strip()} of those who reached {before}). "
          "Largest is not the same as most fixable: an optional step loses people by design.")
    for name, group in sorted(segments.items(), key=lambda kv: -len(kv[1])):
        label = f"{args.by} = {name}  ({len(group):,} users)"
        if len(group) < args.min_n:
            print(f"\n{label}: too small to read (under {args.min_n}).")
            continue
        show(summarize(group, steps), label)
    if segments:
        print("\nA gap between segments is a place to look, not a cause. Check that the intervals do not overlap, "
              "then ask what else differs between the segments.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

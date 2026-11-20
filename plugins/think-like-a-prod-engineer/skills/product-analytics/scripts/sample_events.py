#!/usr/bin/env python3
"""Write a synthetic events file with known answers planted in it.

Use it to try the other scripts, and to check that an analysis method finds an
effect when you already know the effect is there. Run a method on data with a
known answer before trusting it on data without one.

    python3 sample_events.py events.csv
    python3 sample_events.py events.csv --users 8000 --seed 7
    python3 sample_events.py --truth

What is planted (print it with --truth):

  * iOS completes the profile step far less often than web (55% against 80%).
  * Users who invite a teammate in their first days are retained far more
    often (55%, against 30% with a project only and 15% with neither).
  * Paid signups are retained 0.6 times as often as everyone else.

With --dirty it also plants six tracking faults, for trying event_qa.py in the
tracking-plan skill: double fires of task_completed on iOS, an event that only
fires on web, users with a project and no signup, a bot, clocks set a year
ahead, and a server-side event that lost its platform.

Standard library only. Deterministic for a given seed.
"""

from __future__ import annotations

import argparse
import csv
import random
import sys
from datetime import datetime, timedelta, timezone

TRUTH = {
    "profile_completed | web": 0.80,
    "profile_completed | ios": 0.55,
    "project_created | profile_completed": 0.65,
    "teammate_invited | project_created": 0.30,
    "retained | no project": 0.15,
    "retained | project, no invite": 0.30,
    "retained | invited a teammate": 0.55,
    "paid multiplier on retained": 0.60,
    "retained user: daily active probability": 0.35,
    "churner: active on days 1 to 3 only, daily probability": 0.30,
}


def generate(users: int, seed: int, signup_days: int, total_days: int):
    rng = random.Random(seed)
    start = datetime(2026, 1, 5, tzinfo=timezone.utc)
    end = start + timedelta(days=total_days)
    for i in range(users):
        uid = f"u{i:06d}"
        platform = "web" if rng.random() < 0.60 else "ios"
        source = rng.choices(["organic", "paid", "referral"], [0.5, 0.3, 0.2])[0]
        t0 = start + timedelta(seconds=rng.uniform(0, signup_days * 86400))
        props = (platform, source)
        yield uid, "signup_completed", t0, props

        project = invited = False
        if rng.random() < TRUTH[f"profile_completed | {platform}"]:
            t1 = t0 + timedelta(minutes=rng.uniform(1, 40))
            yield uid, "profile_completed", t1, props
            if rng.random() < TRUTH["project_created | profile_completed"]:
                project = True
                t2 = t1 + timedelta(hours=rng.uniform(0.1, 30))
                yield uid, "project_created", t2, props
                if rng.random() < TRUTH["teammate_invited | project_created"]:
                    invited = True
                    yield uid, "teammate_invited", t2 + timedelta(hours=rng.uniform(0.1, 36)), props

        p = TRUTH["retained | invited a teammate"] if invited else (
            TRUTH["retained | project, no invite"] if project else TRUTH["retained | no project"])
        if source == "paid":
            p *= TRUTH["paid multiplier on retained"]
        retained = rng.random() < p
        day = 1
        while t0 + timedelta(days=day) < end:
            if retained:
                active = rng.random() < TRUTH["retained user: daily active probability"]
            else:
                active = day <= 3 and rng.random() < TRUTH["churner: active on days 1 to 3 only, daily probability"]
            if active:
                ts = t0 + timedelta(days=day, seconds=rng.uniform(0, 86399))
                if ts < end:
                    yield uid, "session_started", ts, props
                    if project and rng.random() < 0.5:
                        yield uid, "task_completed", ts + timedelta(minutes=rng.uniform(1, 50)), props
            day += 1


DIRT = [
    "task_completed fires twice, 1.2s apart, on about half of iOS completions",
    "export_clicked fires on web only",
    "40 users have project_created and no signup_completed",
    "one account (bot_0001) sends 2,000 session_started events in a day",
    "12 events are stamped 400 days ahead",
    "teammate_invited has a blank platform on about a quarter of rows",
]


def dirty(rows: list, seed: int) -> list:
    rng = random.Random(seed + 1)
    out = []
    for uid, event, ts, (platform, source) in rows:
        if event == "teammate_invited" and rng.random() < 0.25:
            platform = ""
        out.append((uid, event, ts, (platform, source)))
        if event == "task_completed" and platform == "ios" and rng.random() < 0.5:
            out.append((uid, event, ts + timedelta(seconds=1.2), (platform, source)))
        if event == "project_created" and platform == "web" and rng.random() < 0.4:
            out.append((uid, "export_clicked", ts + timedelta(minutes=5), (platform, source)))
    first = min(r[2] for r in rows)
    for i in range(40):
        out.append((f"anon_{i:04d}", "project_created", first + timedelta(days=10 + i), ("web", "organic")))
    for i in range(2000):
        out.append(("bot_0001", "session_started", first + timedelta(days=20, seconds=i * 40), ("web", "organic")))
    for i in range(12):
        uid, event, ts, props = rows[i * 97]
        out.append((uid, "session_started", ts + timedelta(days=400), props))
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("out", nargs="?", help="where to write the CSV")
    parser.add_argument("--users", type=int, default=4000)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--signup-days", type=int, default=60)
    parser.add_argument("--total-days", type=int, default=100)
    parser.add_argument("--dirty", action="store_true", help="also plant six tracking faults")
    parser.add_argument("--truth", action="store_true", help="print what is planted and exit")
    args = parser.parse_args()
    if args.truth:
        for key, value in TRUTH.items():
            print(f"{value:5.2f}  {key}")
        print("\nWith --dirty:")
        for fault in DIRT:
            print(f"  - {fault}")
        return 0
    if not args.out:
        parser.error("give an output path, or --truth")
    rows = list(generate(args.users, args.seed, args.signup_days, args.total_days))
    if args.dirty:
        rows = dirty(rows, args.seed)
    rows.sort(key=lambda r: r[2])
    with open(args.out, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["user_id", "event", "timestamp", "platform", "source"])
        for uid, event, ts, (platform, source) in rows:
            writer.writerow([uid, event, ts.strftime("%Y-%m-%dT%H:%M:%S+00:00"), platform, source])
    print(f"wrote {len(rows):,} events for {args.users:,} users to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

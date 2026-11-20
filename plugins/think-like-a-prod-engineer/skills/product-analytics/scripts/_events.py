"""Shared loading and statistics for the product-analytics scripts.

Events file: a CSV with a header and at least these columns.

    user_id     any stable identifier. Pseudonymous IDs, never emails.
    event       the event name, as in the tracking plan
    timestamp   ISO 8601, for example 2026-03-02T14:05:00 or with an offset

Any other column is a property you can segment by (platform, source, plan).
Timestamps without an offset are read as UTC. Standard library only.
"""

from __future__ import annotations

import csv
import math
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import NormalDist

DAY = 86400
REQUIRED = ("user_id", "event", "timestamp")


def parse_ts(value: str) -> float:
    text = value.strip().replace("Z", "+00:00")
    stamp = datetime.fromisoformat(text)
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=timezone.utc)
    return stamp.timestamp()


def load(path: Path) -> tuple[dict[str, list[tuple[float, str, dict]]], float, dict]:
    """Return (events per user sorted by time, last timestamp, load notes)."""
    users: dict[str, list[tuple[float, str, dict]]] = defaultdict(list)
    notes = {"rows": 0, "skipped": 0, "duplicates": 0}
    seen: set[tuple[str, str, float]] = set()
    try:
        handle = path.open(newline="", encoding="utf-8-sig")
    except OSError as error:
        sys.exit(f"cannot read {path}: {error}")
    with handle:
        reader = csv.DictReader(handle)
        missing = [c for c in REQUIRED if c not in (reader.fieldnames or [])]
        if missing:
            sys.exit(f"{path} is missing column(s): {', '.join(missing)}. Needs {', '.join(REQUIRED)}.")
        for row in reader:
            notes["rows"] += 1
            try:
                ts = parse_ts(row["timestamp"])
            except (ValueError, AttributeError):
                notes["skipped"] += 1
                continue
            user, event = (row["user_id"] or "").strip(), (row["event"] or "").strip()
            if not user or not event:
                notes["skipped"] += 1
                continue
            key = (user, event, ts)
            if key in seen:  # exact duplicates are almost always double-fired tracking
                notes["duplicates"] += 1
                continue
            seen.add(key)
            props = {k: v for k, v in row.items() if k not in REQUIRED}
            users[user].append((ts, event, props))
    if not users:
        sys.exit(f"{path} has no usable rows")
    for events in users.values():
        events.sort(key=lambda e: e[0])
    end = max(events[-1][0] for events in users.values())
    return users, end, notes


def wilson(successes: int, n: int, confidence: float = 0.95) -> tuple[float, float]:
    """Wilson score interval for a proportion. Sound at small n and near 0 or 1."""
    if n == 0:
        return (0.0, 0.0)
    z = NormalDist().inv_cdf(1 - (1 - confidence) / 2)
    p = successes / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (max(0.0, centre - half), min(1.0, centre + half))


def diff_interval(a: int, na: int, b: int, nb: int, confidence: float = 0.95) -> tuple[float, float]:
    """Newcombe interval for the difference of two proportions (a/na minus b/nb)."""
    la, ua = wilson(a, na, confidence)
    lb, ub = wilson(b, nb, confidence)
    pa, pb = (a / na if na else 0.0), (b / nb if nb else 0.0)
    d = pa - pb
    return (d - math.sqrt((pa - la) ** 2 + (ub - pb) ** 2), d + math.sqrt((ua - pa) ** 2 + (pb - lb) ** 2))


def pct(x: float) -> str:
    return f"{100 * x:5.1f}%"


def load_report(notes: dict, end: float) -> str:
    parts = [f"{notes['rows']:,} rows"]
    if notes["duplicates"]:
        parts.append(f"{notes['duplicates']:,} exact duplicates dropped")
    if notes["skipped"]:
        parts.append(f"{notes['skipped']:,} unreadable rows skipped")
    return f"{', '.join(parts)}. Data ends {datetime.fromtimestamp(end, timezone.utc):%Y-%m-%d %H:%M} UTC."

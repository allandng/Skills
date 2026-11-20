#!/usr/bin/env python3
"""The three calculations an A/B test on a conversion rate needs.

    python3 experiment.py size --baseline 0.20 --mde 0.02 --daily-users 800
    python3 experiment.py srm  --counts 5021,4979
    python3 experiment.py read --control 400/5000 --treatment 460/5000 --planned-n 6510

size   How many users each arm needs before the test starts. --mde is the
       smallest absolute change worth detecting (0.02 = two points); add
       --relative to give it as a fraction of the baseline instead.
srm    Sample ratio mismatch: did the arms get the share of users they were
       meant to? If not, assignment or logging is broken and the result
       cannot be read, whatever it says.
read   The difference, its 95% interval, and a two-sided p-value. It runs the
       SRM check first and refuses to give a verdict if that fails. With
       --planned-n it also refuses if the test has not reached its size.

For one conversion metric with users randomized individually. Not for revenue
per user, repeated measures, or clustered assignment: those need a different
test. Standard library only.
"""

from __future__ import annotations

import argparse
import math
import sys
from statistics import NormalDist

N = NormalDist()
SRM_ALPHA = 0.001  # deliberately strict: SRM is a bug detector, not a hypothesis of interest


def chi2_sf(x: float, dof: int) -> float:
    """Upper tail of the chi-square distribution, by the regularized incomplete gamma."""
    if x <= 0:
        return 1.0
    a, half = dof / 2.0, x / 2.0
    if half < a + 1:  # series for the lower tail
        term = total = 1.0 / a
        for n in range(1, 500):
            term *= half / (a + n)
            total += term
            if abs(term) < abs(total) * 1e-15:
                break
        return max(0.0, 1.0 - total * math.exp(-half + a * math.log(half) - math.lgamma(a)))
    b, c, d = half + 1 - a, 1e300, 1.0 / (half + 1 - a)  # continued fraction for the upper tail
    h = d
    for n in range(1, 500):
        an = -n * (n - a)
        b += 2
        d = an * d + b
        d = 1e-300 if abs(d) < 1e-300 else d
        c = b + an / c
        c = 1e-300 if abs(c) < 1e-300 else c
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1) < 1e-15:
            break
    return min(1.0, h * math.exp(-half + a * math.log(half) - math.lgamma(a)))


def sample_size(p1: float, p2: float, alpha: float, power: float) -> int:
    """Users per arm for a two-sided test of two proportions."""
    za, zb = N.inv_cdf(1 - alpha / 2), N.inv_cdf(power)
    pbar = (p1 + p2) / 2
    top = za * math.sqrt(2 * pbar * (1 - pbar)) + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))
    return math.ceil(top * top / (p2 - p1) ** 2)


def srm(counts: list[int], ratio: list[float]) -> tuple[float, float]:
    total, weight = sum(counts), sum(ratio)
    expected = [total * r / weight for r in ratio]
    chi2 = sum((c - e) ** 2 / e for c, e in zip(counts, expected))
    return chi2, chi2_sf(chi2, len(counts) - 1)


def fraction(text: str) -> tuple[int, int]:
    try:
        a, b = text.split("/")
        a, b = int(a.replace(",", "")), int(b.replace(",", ""))
    except ValueError:
        raise argparse.ArgumentTypeError("give it as conversions/users, for example 400/5000")
    if not 0 <= a <= b or b == 0:
        raise argparse.ArgumentTypeError("conversions must be between 0 and users")
    return a, b


def cmd_size(args) -> int:
    p1 = args.baseline
    p2 = p1 * (1 + args.mde) if args.relative else p1 + args.mde
    if not (0 < p1 < 1 and 0 < p2 < 1) or p1 == p2:
        sys.exit("baseline and baseline + mde must both be between 0 and 1, and differ")
    n = sample_size(p1, p2, args.alpha, args.power)
    print(f"Baseline {p1:.2%}, smallest change worth detecting {100 * (p2 - p1):+.2f} points (to {p2:.2%}).")
    print(f"Two-sided alpha {args.alpha}, power {args.power}.")
    print(f"\n  {n:,} users per arm, {n * args.arms:,} in total across {args.arms} arms.")
    if args.daily_users:
        days = math.ceil(n * args.arms / args.daily_users)
        weeks = math.ceil(days / 7)
        print(f"  At {args.daily_users:,} eligible users a day: {days} days. Run it for {weeks} full week(s) "
              f"({weeks * 7} days) so every weekday is covered equally.")
        if days > 56:
            print("  That is over eight weeks. Detect a bigger change, test further up the funnel where rates "
                  "are higher, or accept that this cannot be tested here.")
    print("\nDecide the size, the metric and the stopping date before it starts. Stopping when the result "
          "looks good is how a false positive gets shipped.")
    return 0


def cmd_srm(args) -> int:
    counts = [int(c.replace(",", "")) for c in args.counts.split(",")]
    ratio = [float(r) for r in args.ratio.split(",")] if args.ratio else [1.0] * len(counts)
    if len(counts) < 2 or len(ratio) != len(counts):
        sys.exit("give one count per arm, and one ratio per arm if you give ratios")
    chi2, p = srm(counts, ratio)
    total, weight = sum(counts), sum(ratio)
    for i, (c, r) in enumerate(zip(counts, ratio)):
        print(f"  arm {i + 1}: {c:,} users, {c / total:.2%} of traffic (meant to be {r / weight:.2%})")
    print(f"  chi-square {chi2:.3f}, p = {p:.4g}")
    if p < SRM_ALPHA:
        print(f"\nSAMPLE RATIO MISMATCH (p < {SRM_ALPHA}). The split is not what was configured. Do not read this "
              "test. Find out why: a redirect that loses one arm, bots, a filter applied after assignment, "
              "logging that fires on only one path.")
        return 1
    print("\nNo sample ratio mismatch. The split is consistent with what was configured.")
    return 0


def cmd_read(args) -> int:
    (xc, nc), (xt, nt) = args.control, args.treatment
    ratio = [float(r) for r in args.ratio.split(",")] if args.ratio else [1.0, 1.0]
    chi2, p_srm = srm([nc, nt], ratio)
    pc, pt = xc / nc, xt / nt
    print(f"  control    {xc:,}/{nc:,} = {pc:.2%}")
    print(f"  treatment  {xt:,}/{nt:,} = {pt:.2%}")
    if p_srm < SRM_ALPHA:
        print(f"\nSAMPLE RATIO MISMATCH (chi-square {chi2:.2f}, p = {p_srm:.3g}). The arms did not get the split "
              "that was configured, so the difference above cannot be trusted. No verdict.")
        return 1
    if args.planned_n and min(nc, nt) < args.planned_n:
        print(f"\nNOT FINISHED. The plan was {args.planned_n:,} per arm and the smaller arm has {min(nc, nt):,}. "
              "Reading now and stopping if it looks good inflates false positives. No verdict.")
        return 1
    diff = pt - pc
    se = math.sqrt(pc * (1 - pc) / nc + pt * (1 - pt) / nt)
    z = N.inv_cdf(1 - args.alpha / 2)
    low, high = diff - z * se, diff + z * se
    pooled = (xc + xt) / (nc + nt)
    se0 = math.sqrt(pooled * (1 - pooled) * (1 / nc + 1 / nt))
    p = 2 * (1 - N.cdf(abs(diff) / se0)) if se0 else 1.0
    pts = lambda x: f"{100 * x:+.2f}"  # noqa: E731 - percentage points
    print(f"\n  difference  {pts(diff)} points" + (f"  ({diff / pc:+.1%} relative)" if pc else ""))
    print(f"  {1 - args.alpha:.0%} interval  {pts(low)} to {pts(high)} points")
    print(f"  p-value     {p:.4f}  (two-sided)")
    if min(xc, xt, nc - xc, nt - xt) < 10:
        print("\nToo few conversions or non-conversions in one arm for this approximation. Treat the result as unreadable.")
        return 1
    if low > 0 or high < 0:
        direction = "higher" if diff > 0 else "lower"
        print(f"\nThe treatment rate is {direction}. The interval excludes zero. The true change is plausibly anywhere "
              f"from {pts(low)} to {pts(high)} points: decide whether the near-zero end of that is worth shipping.")
    else:
        print(f"\nNo difference detected. The interval includes zero. That is not the same as no effect: anything "
              f"from {pts(low)} to {pts(high)} points is still consistent with this data.")
    print("Check the guardrail metrics before any decision. A win on one number that costs another is not a win.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)

    s = sub.add_parser("size", help="users per arm, before the test")
    s.add_argument("--baseline", type=float, required=True, help="current conversion rate, as a fraction")
    s.add_argument("--mde", type=float, required=True, help="smallest change worth detecting")
    s.add_argument("--relative", action="store_true", help="--mde is relative to the baseline")
    s.add_argument("--alpha", type=float, default=0.05)
    s.add_argument("--power", type=float, default=0.80)
    s.add_argument("--arms", type=int, default=2)
    s.add_argument("--daily-users", type=int, help="eligible users per day, to turn the size into a duration")
    s.set_defaults(run=cmd_size)

    m = sub.add_parser("srm", help="sample ratio mismatch check")
    m.add_argument("--counts", required=True, help="users per arm, comma-separated")
    m.add_argument("--ratio", help="intended split, comma-separated (default: equal)")
    m.set_defaults(run=cmd_srm)

    r = sub.add_parser("read", help="difference, interval and p-value, after the test")
    r.add_argument("--control", type=fraction, required=True, help="conversions/users")
    r.add_argument("--treatment", type=fraction, required=True, help="conversions/users")
    r.add_argument("--ratio", help="intended split control,treatment (default 1,1)")
    r.add_argument("--planned-n", type=int, help="the per-arm size decided before the test")
    r.add_argument("--alpha", type=float, default=0.05)
    r.set_defaults(run=cmd_read)

    args = parser.parse_args()
    return args.run(args)


if __name__ == "__main__":
    sys.exit(main())

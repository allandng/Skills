#!/usr/bin/env python3
"""
contrast.py - WCAG 2.2 contrast ratios across a design token palette.

Checks every foreground/background pair so failures are found at token-design
time rather than after the interface is built on top of them.

Usage:
    python3 contrast.py --tokens tokens.json
    python3 contrast.py --pair "#1A1614" "#FDFCFA"
    python3 contrast.py --tokens tokens.json --tokens-dark dark.json
    python3 contrast.py --tokens tokens.json --json

tokens.json is a flat map of name -> hex:
    {"surface": "#FDFCFA", "ink": "#1A1614", "primary": "#0B4F6C"}

A flat map cannot say which foreground sits on which surface, so all-pairs
mode guesses - and guesses wrong on any palette with inverted bands, where it
will pair a color against itself. Declare the real combinations instead:

    {
      "tokens": {"stock": "#EDE9E1", "ink-body": "#17130F",
                 "band-bg": "#17130F", "band-ink": "#EDE9E1"},
      "pairs":  [["ink-body", "stock"], ["band-ink", "band-bg"]]
    }

With "pairs" present only those combinations are checked. Without it the tool
falls back to all-pairs and labels the output as heuristic.
"""

from __future__ import annotations

import argparse
import json
import sys
from itertools import permutations
from pathlib import Path

# Names treated as backgrounds / as foregrounds when pairing a palette.
BG_HINTS = ("surface", "bg", "background", "ground", "canvas", "base", "paper")
FG_HINTS = ("ink", "text", "fg", "foreground", "primary", "accent", "danger",
            "success", "warning", "border", "muted", "link")


def load_token_file(path: Path) -> tuple[dict, list | None]:
    """Return (tokens, declared_pairs_or_None) for either file shape."""
    data = json.loads(path.read_text())
    if isinstance(data, dict) and "tokens" in data:
        tokens = {k: v for k, v in data["tokens"].items() if isinstance(v, str)}
        pairs = data.get("pairs")
        if pairs:
            pairs = [tuple(p) for p in pairs if len(p) == 2]
        return tokens, pairs or None
    return {k: v for k, v in data.items() if isinstance(v, str)}, None


def parse_hex(s: str) -> tuple[int, int, int]:
    s = s.strip().lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) == 8:  # #RRGGBBAA - alpha ignored, warn upstream
        s = s[:6]
    if len(s) != 6:
        raise ValueError(f"cannot parse color: {s!r}")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))  # type: ignore


def relative_luminance(rgb: tuple[int, int, int]) -> float:
    def channel(v: int) -> float:
        c = v / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(a: str, b: str) -> float:
    la, lb = relative_luminance(parse_hex(a)), relative_luminance(parse_hex(b))
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def grade(ratio: float) -> dict:
    return {
        "ratio": round(ratio, 2),
        "normal_aa": ratio >= 4.5,     # body text
        "normal_aaa": ratio >= 7.0,
        "large_aa": ratio >= 3.0,      # >=18.66px bold or >=24px
        "large_aaa": ratio >= 4.5,
        "ui_component": ratio >= 3.0,  # WCAG 2.2 non-text contrast
    }


def verdict(g: dict) -> str:
    if g["normal_aaa"]:
        return "AAA  body text"
    if g["normal_aa"]:
        return "AA   body text"
    if g["large_aa"]:
        return "AA   large text / UI only"
    return "FAIL"


def split_roles(tokens: dict[str, str]):
    bgs = {k: v for k, v in tokens.items()
           if any(h in k.lower() for h in BG_HINTS)}
    fgs = {k: v for k, v in tokens.items()
           if any(h in k.lower() for h in FG_HINTS)}
    # If hints matched nothing useful, fall back to all-vs-all.
    if not bgs or not fgs:
        return tokens, tokens, True
    return bgs, fgs, False


def check_palette(tokens: dict[str, str], label: str, as_json: bool,
                  declared: list | None = None) -> list[dict]:
    if declared:
        pairs = [(f, b) for f, b in declared if f in tokens and b in tokens]
        missing = [(f, b) for f, b in declared
                   if f not in tokens or b not in tokens]
        for f, b in missing:
            print(f"warning: pair {f}:{b} references an undefined token",
                  file=sys.stderr)
        fallback = False
    else:
        bgs, fgs, fallback = split_roles(tokens)
        pairs = (list((f, b) for f in fgs for b in bgs if f != b)
                 if not fallback else list(permutations(tokens, 2)))

    rows = []
    seen = set()
    for fg, bg in pairs:
        key = tuple(sorted((fg, bg)))
        if key in seen:
            continue
        seen.add(key)
        # Two token names holding the same value are not a real pair - they
        # are one color under two names, typically a band inversion. Checking
        # them produces a 1.0:1 "failure" that does not exist on screen.
        if not declared and tokens[fg].lower() == tokens[bg].lower():
            continue
        try:
            r = contrast_ratio(tokens[fg], tokens[bg])
        except ValueError as e:
            print(f"warning: {e}", file=sys.stderr)
            continue
        g = grade(r)
        rows.append({"theme": label, "fg": fg, "bg": bg,
                     "fg_hex": tokens[fg], "bg_hex": tokens[bg], **g,
                     "verdict": verdict(g)})

    rows.sort(key=lambda x: x["ratio"])

    if not as_json:
        mode = ("declared pairs" if declared else
                "all-pairs, HEURISTIC - declare \"pairs\" for accuracy")
        print(f"\n=== {label} ({mode}) ===")
        print(f"{'foreground':<18} {'background':<18} {'ratio':>7}  result")
        print("-" * 68)
        for r in rows:
            mark = " " if r["normal_aa"] else ("!" if r["large_aa"] else "x")
            print(f"{mark} {r['fg']:<16} {r['bg']:<18} "
                  f"{r['ratio']:>6.2f}  {r['verdict']}")
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description="WCAG 2.2 contrast checker.")
    ap.add_argument("--tokens", help="path to a flat name->hex JSON file")
    ap.add_argument("--tokens-dark", help="dark theme token file")
    ap.add_argument("--pair", nargs=2, metavar=("FG", "BG"),
                    help="check a single pair")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if not args.tokens and not args.pair:
        ap.error("pass --tokens or --pair")

    if args.pair:
        fg, bg = args.pair
        try:
            r = contrast_ratio(fg, bg)
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            return 2
        g = grade(r)
        if args.json:
            print(json.dumps({"fg": fg, "bg": bg, **g,
                              "verdict": verdict(g)}, indent=2))
        else:
            print(f"{fg} on {bg}: {r:.2f}:1  {verdict(g)}")
        return 0 if g["large_aa"] else 1

    all_rows = []
    for path, label in ((args.tokens, "light"), (args.tokens_dark, "dark")):
        if not path:
            continue
        p = Path(path)
        if not p.exists():
            print(f"error: {path} not found", file=sys.stderr)
            return 2
        try:
            tokens, declared = load_token_file(p)
        except json.JSONDecodeError as e:
            print(f"error: {path} is not valid JSON: {e}", file=sys.stderr)
            return 2
        if not tokens:
            print(f"error: no string values in {path}", file=sys.stderr)
            return 2
        all_rows += check_palette(tokens, label, args.json, declared)
        if not declared and not args.json:
            print("\nNo \"pairs\" declared - combinations above are guessed from"
                  "\nrole names and some may never co-occur on screen.")

    if args.json:
        print(json.dumps(all_rows, indent=2))
        return 0

    fails = [r for r in all_rows if not r["large_aa"]]
    body_fails = [r for r in all_rows if r["large_aa"] and not r["normal_aa"]]

    print(f"\n{'-' * 68}")
    print(f"{len(all_rows)} pair(s) checked - "
          f"{len(fails)} failing, {len(body_fails)} large-text-only")
    if fails:
        print("\nFailing pairs cannot be used together at any size:")
        for r in fails[:12]:
            print(f"  {r['theme']}: {r['fg']} on {r['bg']} = {r['ratio']}:1")
    if body_fails:
        print("\nLarge-text-only pairs - safe for headings and UI glyphs,")
        print("not for body copy. 'muted' text failing here is a common bug:")
        for r in body_fails[:12]:
            print(f"  {r['theme']}: {r['fg']} on {r['bg']} = {r['ratio']}:1")

    print("\nThresholds: 4.5:1 body - 3:1 large text and UI components - 7:1 AAA")
    print("Purely decorative borders and dividers are exempt from 3:1; borders")
    print("that carry meaning (focus rings, input outlines, state) are not.")
    print("Contrast is necessary, not sufficient: never signal by color alone.")
    return 1 if fails else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        # piping into head/less closes stdout early; not an error
        try:
            sys.stdout.close()
        finally:
            sys.exit(0)

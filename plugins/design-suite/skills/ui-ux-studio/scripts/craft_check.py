#!/usr/bin/env python3
"""
craft_check.py - measure the positive craft floor.

ai_tells.py is a negative filter: it catches what makes a page look
machine-made. Passing it produces a page that is inoffensive, not one that
looks designed. This measures the other half - the presence of the things
that give a page visual authority.

It exists because a real study passed the tell scan cleanly while every
direction topped out at 25px type with zero ramps and zero elevation. Nothing
was wrong; nothing was designed either.

Usage:
    python3 craft_check.py page.html
    python3 craft_check.py site/ --json
    python3 craft_check.py page.html tokens.css
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

EXTS = {".html", ".htm", ".css", ".scss", ".jsx", ".tsx", ".vue", ".svelte"}
SKIP = {"node_modules", ".git", "dist", "build", ".next", "out", "__pycache__"}

STYLE_BLOCK = re.compile(r"<style[^>]*>(.*?)</style>", re.I | re.S)
FONT_SIZE = re.compile(r"font-size:\s*([\d.]+)(px|rem|em)", re.I)
CLAMP = re.compile(r"font-size:\s*clamp\([^,]+,[^,]+,\s*([\d.]+)(px|rem|em)", re.I)
CUSTOM = re.compile(r"(--[\w-]+)\s*:\s*([^;}]+)")
RAMP_KEY = re.compile(r"-(50|100|200|300|400|500|600|700|800|900)$")
RADIUS = re.compile(r"border-radius:\s*([^;}]+)", re.I)
SHADOW = re.compile(r"box-shadow:\s*([^;}]+)", re.I)
BORDER = re.compile(r"border(?:-top|-right|-bottom|-left)?:\s*([^;}]*\d[^;}]*)", re.I)
BG = re.compile(r"background(?:-color)?:\s*([^;}]+)", re.I)


VAR_REF = re.compile(r"var\(\s*(--[\w-]+)\s*(?:,[^)]*)?\)")
LEN = re.compile(r"^\s*([\d.]+)(px|rem|em)\s*$")


def resolve_vars(css: str) -> dict[str, str]:
    """Map custom property -> literal value, following one var() chain."""
    props = dict(CUSTOM.findall(css))
    props = {k: v.strip() for k, v in props.items()}
    for _ in range(4):  # depth cap; token chains are shallow in practice
        changed = False
        for k, v in list(props.items()):
            m = VAR_REF.fullmatch(v)
            if m and m.group(1) in props:
                props[k] = props[m.group(1)]
                changed = True
        if not changed:
            break
    return props


def px(v: str, u: str) -> float:
    try:
        return float(v) * (16 if u in ("rem", "em") else 1)
    except ValueError:
        return 0.0


def gather(paths: list[str]) -> str:
    blob = []
    for raw in paths:
        p = Path(raw)
        files = ([p] if p.is_file() else
                 [f for f in sorted(p.rglob("*"))
                  if f.is_file() and f.suffix.lower() in EXTS
                  and not any(s in f.parts for s in SKIP)])
        for f in files:
            try:
                t = f.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            blob.append(t)
            blob.extend(STYLE_BLOCK.findall(t))
    return "\n".join(blob)


def analyse(css: str) -> dict:
    props = resolve_vars(css)

    # Literal declarations, plus any font-size: var(--x) resolved through the
    # token map. Well-tokenized CSS declares almost nothing literally, so
    # skipping this step reports a one-step scale on the best-built sites.
    sizes_raw = [px(v, u) for v, u in FONT_SIZE.findall(css)]
    sizes_raw += [px(v, u) for v, u in CLAMP.findall(css)]
    for ref in re.findall(r"font-size:\s*var\(\s*(--[\w-]+)", css, re.I):
        val = props.get(ref, "")
        m = LEN.match(val)
        if m:
            sizes_raw.append(px(m.group(1), m.group(2)))
        else:
            cm = re.search(r"clamp\([^,]+,[^,]+,\s*([\d.]+)(px|rem|em)", val)
            if cm:
                sizes_raw.append(px(cm.group(1), cm.group(2)))
    # Type tokens that exist but are only referenced indirectly still count.
    for k, v in props.items():
        if re.search(r"(^--fs-|font-size|--text-|--type-)", k, re.I):
            m = LEN.match(v)
            if m:
                sizes_raw.append(px(m.group(1), m.group(2)))

    sizes = sorted(set(sizes_raw))
    sizes = [s for s in sizes if 8 <= s <= 400]
    body = min((s for s in sizes if 14 <= s <= 20), default=(sizes[0] if sizes else 0))
    largest = sizes[-1] if sizes else 0

    ramp_families: dict[str, int] = {}
    for k in props:
        m = RAMP_KEY.search(k)
        if m:
            fam = k[: m.start()]
            ramp_families[fam] = ramp_families.get(fam, 0) + 1
    ramps = {k: v for k, v in ramp_families.items() if v >= 3}

    radii = {r.strip() for r in RADIUS.findall(css)} | {
        v.strip() for k, v in props.items() if "radius" in k}
    radii = {r for r in radii if r and r not in ("0", "0px", "none")}

    shadows = {s.strip() for s in SHADOW.findall(css) if s.strip().lower() != "none"} | {
        v.strip() for k, v in props.items() if "shadow" in k}

    borders = len(BORDER.findall(css))
    # Count page GROUNDS, not every fill. A ramp step used as a component
    # tint (--accent-100 on a tag) is correct tint-layering, not patchwork —
    # counting it as a surface penalises exactly the technique we asked for.
    ramp_names = {f"--{k.lstrip('-')}" for k in ramp_families}
    bgs = set()
    for b in BG.findall(css):
        v = b.strip().lower()
        if v in ("none", "transparent", "inherit", "currentcolor") or v.startswith("url"):
            continue
        ref = re.search(r"var\(\s*(--[\w-]+)", v)
        if ref:
            name = ref.group(1)
            if RAMP_KEY.search(name):
                continue  # a ramp step: component tint, not a ground
            if any(name.startswith(r) for r in ramp_names):
                continue
        if v.startswith("color-mix"):
            continue  # derived tint, not a declared ground
        bgs.add(v)

    return {
        "type_steps": len(sizes), "body_px": body, "largest_px": largest,
        "scale_range": round(largest / body, 2) if body else 0,
        "ramp_families": ramps, "radii": sorted(radii)[:6],
        "shadow_levels": len(shadows), "border_decls": borders,
        "distinct_bg": len(bgs),
    }


def evaluate(a: dict) -> list[tuple[str, bool, str]]:
    """(check, passed, message)"""
    out = []

    r = a["scale_range"]
    out.append((
        "scale contrast", r >= 3.0,
        f"largest type is {a['largest_px']:.0f}px against {a['body_px']:.0f}px body "
        f"= {r}x. Want 3.5-6x on any page with a focal element. Under 2.5x "
        f"means nothing dominates and the page reads as one flat block."))

    n = a["type_steps"]
    out.append((
        "scale discipline", 4 <= n <= 8,
        f"{n} distinct type sizes. Want 5-7. More than 8 means sizes were "
        f"picked per element rather than generated from a scale."))

    nr = len(a["ramp_families"])
    out.append((
        "color ramps", nr >= 1,
        f"{nr} color family/families with 3+ steps"
        + (f" ({', '.join(sorted(a['ramp_families'])[:3])})" if nr else "")
        + ". Without a ramp there are no tinted fills, so the only way to "
          "separate a surface is a border or a heavy shadow - which is what "
          "makes output look boxy."))

    has_form = bool(a["radii"]) or a["shadow_levels"] > 0 or nr >= 1
    out.append((
        "form language", has_form,
        f"{len(a['radii'])} radius value(s), {a['shadow_levels']} shadow level(s), "
        f"{nr} ramp(s), {a['border_decls']} border declarations. A design with "
        f"none of the first three is border-delimited by default rather than "
        f"by decision - fine if declared, a tell if unexamined."))

    out.append((
        "surface layering", 2 <= a["distinct_bg"] <= 3,
        f"{a['distinct_bg']} distinct background values. Want 2-3: a ground, a "
        f"raised surface, and at most one deliberate inversion. One means no "
        f"layering; 4+ is the patchwork tell."))

    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Measure the positive craft floor.")
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    css = gather(args.paths)
    if not css.strip():
        print("error: no CSS found", file=sys.stderr)
        return 2

    a = analyse(css)
    checks = evaluate(a)

    if args.json:
        print(json.dumps({"metrics": a, "checks": [
            {"check": c, "passed": p, "message": m} for c, p, m in checks]}, indent=2))
        return 0 if all(p for _, p, _ in checks) else 1

    print(f"\n{'CRAFT FLOOR':<20} {'':<6}")
    print("-" * 72)
    for name, passed, msg in checks:
        print(f"[{'pass' if passed else 'FAIL'}] {name}")
        print(f"       {msg}")
    failed = [c for c, p, _ in checks if not p]
    print("-" * 72)
    if failed:
        print(f"{len(failed)} of {len(checks)} below the floor: {', '.join(failed)}")
        print("These are minimums, not targets. A page can clear every one and "
              "still be dull —\nbut it cannot look designed while failing them.")
    else:
        print("All checks clear. The floor is a floor: it says nothing about "
              "whether the\ndesign is any good, only that it has the equipment "
              "to be.")
    return 1 if failed else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)

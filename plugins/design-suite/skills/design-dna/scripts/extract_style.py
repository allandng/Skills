#!/usr/bin/env python3
"""
extract_style.py - pull a design system out of a website's HTML and CSS.

Produces a tokens.json that feeds ui-ux-studio's contrast.py directly, plus a
markdown profile with the divergence-matrix axes estimated from the evidence.

Usage:
    python3 extract_style.py --dir ./saved-site --out ./dna
    python3 extract_style.py --files index.html main.css --out ./dna
    python3 extract_style.py --url https://example.com --out ./dna
    python3 extract_style.py --dir ./site --json

--url needs network access from wherever this runs. When the sandbox has no
egress, fetch the page with your own web tooling, save it, and use --dir.

What this cannot see: anything applied at runtime by JavaScript, styles behind
auth, and every judgement call about *why* a choice was made. Those need the
manual pass in references/extraction.md.
"""

from __future__ import annotations

import argparse
import colorsys
import json
import re
import sys
from collections import Counter
from pathlib import Path

# ------------------------------------------------------------------ patterns

HEX = re.compile(r"#([0-9a-fA-F]{3,8})\b")
RGB = re.compile(r"rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)(?:[,\s/]+([\d.%]+))?\s*\)")
HSL = re.compile(r"hsla?\(\s*([\d.]+)(?:deg)?[,\s]+([\d.]+)%[,\s]+([\d.]+)%(?:[,\s/]+([\d.%]+))?\s*\)")

CUSTOM_PROP = re.compile(r"(--[\w-]+)\s*:\s*([^;}]+)[;}]")
FONT_FAMILY = re.compile(r"font-family\s*:\s*([^;}]+)", re.I)
FONT_SIZE = re.compile(r"font-size\s*:\s*([\d.]+)(px|rem|em)", re.I)
FONT_WEIGHT = re.compile(r"font-weight\s*:\s*(\d{3}|bold|normal)", re.I)
LINE_HEIGHT = re.compile(r"line-height\s*:\s*([\d.]+)(px|rem|em)?", re.I)
SPACING = re.compile(r"(?:margin|padding|gap|row-gap|column-gap)[\w-]*\s*:\s*([^;}]+)", re.I)
LEN_PX = re.compile(r"(-?[\d.]+)(px|rem)")
RADIUS = re.compile(r"border-radius\s*:\s*([^;}]+)", re.I)
SHADOW = re.compile(r"box-shadow\s*:\s*([^;}]+)", re.I)
DURATION = re.compile(r"(?:transition|animation)(?:-duration)?\s*:[^;}]*?([\d.]+)(m?s)", re.I)
EASING = re.compile(r"(cubic-bezier\([^)]*\)|linear|ease-in-out|ease-in|ease-out|ease|steps\([^)]*\))", re.I)
KEYFRAMES = re.compile(r"@keyframes\s+([\w-]+)", re.I)
MEDIA_W = re.compile(r"@media[^{]*?(?:min|max)-width\s*:\s*([\d.]+)(px|rem)", re.I)
MAX_WIDTH = re.compile(r"max-width\s*:\s*([\d.]+)(px|rem)", re.I)
GRID_COLS = re.compile(r"grid-template-columns\s*:\s*([^;}]+)", re.I)
LINK_CSS = re.compile(r'<link[^>]+href=["\']([^"\']+\.css[^"\']*)["\']', re.I)
GFONT = re.compile(r'fonts\.googleapis\.com/css2?\?([^"\'<>\s]+)', re.I)
STYLE_BLOCK = re.compile(r"<style[^>]*>(.*?)</style>", re.I | re.S)
STYLE_ATTR = re.compile(r'\bstyle=["\']([^"\']+)["\']', re.I)
TW_ARBITRARY = re.compile(r"\[(#[0-9a-fA-F]{3,8})\]")

# Colors that are tells rather than choices (mirrors ui-ux-studio/ai-tells.md)
TELLS = {
    "#d97757": "Anthropic terracotta accent", "#da7756": "Anthropic terracotta accent",
    "#cc785c": "Anthropic terracotta accent", "#f4f1ea": "AI cluster look #1 cream",
    "#faf9f5": "AI cluster look #1 cream", "#667eea": "template gradient",
    "#764ba2": "template gradient", "#6366f1": "Tailwind indigo default",
    "#4f46e5": "Tailwind indigo default", "#a3e635": "AI cluster look #2 acid",
}
DEFAULT_FONTS = {"inter", "roboto", "poppins", "montserrat", "open sans",
                 "geist", "nunito sans", "system-ui", "-apple-system"}


# -------------------------------------------------------------------- colors

def norm_hex(h: str) -> str | None:
    h = h.lower().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) == 8:
        h = h[:6]
    if len(h) != 6 or any(c not in "0123456789abcdef" for c in h):
        return None
    return "#" + h


def to_rgb(hx: str) -> tuple[int, int, int]:
    h = hx.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))  # type: ignore


def luminance(hx: str) -> float:
    def ch(v):
        c = v / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(v) for v in to_rgb(hx))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def hsl_of(hx: str) -> tuple[float, float, float]:
    r, g, b = (v / 255 for v in to_rgb(hx))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h * 360, s, l


def temperature(hx: str) -> str:
    h, s, _ = hsl_of(hx)
    if s < 0.04:
        return "neutral"
    return "warm" if (h < 90 or h > 300) else "cool"


DARK_MEDIA = re.compile(
    r"@media[^{]*prefers-color-scheme\s*:\s*dark[^{]*\{", re.I)
DARK_SELECTOR = re.compile(
    r"(?:^|[},])\s*((?:html|body|:root)?[^{},]*?"
    r"(?:\.dark\b|\[data-theme=[\"']?dark|\[data-mode=[\"']?dark|"
    r"\.theme-dark\b)[^{},]*)\{", re.I)


def _matching_block(css: str, open_idx: int) -> int:
    """Index just past the brace-balanced block starting at open_idx."""
    depth, i = 0, open_idx
    while i < len(css):
        if css[i] == "{":
            depth += 1
        elif css[i] == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return len(css)


def split_themes(css: str) -> tuple[str, str]:
    """
    Separate default-theme CSS from dark-theme CSS.

    Without this, a site with a dark mode reports whichever theme block
    happened to parse last as its palette - so `surface` on a light-default
    site with dark support comes back dark. Both themes are real; they are
    just different systems and must be measured separately.
    """
    dark_parts, keep, cursor = [], [], 0
    for m in DARK_MEDIA.finditer(css):
        if m.start() < cursor:
            continue
        end = _matching_block(css, m.end() - 1)
        keep.append(css[cursor:m.start()])
        dark_parts.append(css[m.end():end - 1])
        cursor = end
    keep.append(css[cursor:])
    light = "".join(keep)

    rest, cursor = [], 0
    for m in DARK_SELECTOR.finditer(light):
        brace = light.find("{", m.start(1))
        if brace == -1 or brace < cursor:
            continue
        end = _matching_block(light, brace)
        rest.append(light[cursor:m.start(1)])
        dark_parts.append(light[brace + 1:end - 1])
        cursor = end
    rest.append(light[cursor:])
    return "".join(rest), "\n".join(dark_parts)


SHADOW_DECL = re.compile(r"(?:box|text)-shadow\s*:[^;}]*", re.I)


def harvest_colors(css: str, strip_shadows: bool = True) -> Counter:
    # Shadow colors are almost always near-black at low alpha and would
    # otherwise out-frequency the real background. They are not palette.
    if strip_shadows:
        css = SHADOW_DECL.sub("", css)
    c: Counter = Counter()
    for m in HEX.finditer(css):
        n = norm_hex(m.group(1))
        if n:
            c[n] += 1
    for m in TW_ARBITRARY.finditer(css):
        n = norm_hex(m.group(1))
        if n:
            c[n] += 1
    for m in RGB.finditer(css):
        try:
            r, g, b = (int(round(float(m.group(i)))) for i in (1, 2, 3))
            if all(0 <= v <= 255 for v in (r, g, b)):
                c["#%02x%02x%02x" % (r, g, b)] += 1
        except ValueError:
            pass
    for m in HSL.finditer(css):
        try:
            h, s, l = (float(m.group(i)) for i in (1, 2, 3))
            r, g, b = colorsys.hls_to_rgb((h % 360) / 360, l / 100, s / 100)
            c["#%02x%02x%02x" % tuple(round(v * 255) for v in (r, g, b))] += 1
        except ValueError:
            pass
    return c


ROLE_WORDS = {
    "surface": ("surface", "background", "bg", "canvas", "paper", "ground", "base"),
    "surface-raised": ("card", "raised", "elevated", "panel", "popover", "overlay"),
    "ink": ("ink", "foreground", "text", "fg", "copy", "body-color"),
    "ink-muted": ("muted", "secondary-text", "subtle", "dim", "tertiary", "placeholder"),
    "primary": ("primary", "brand", "action", "cta"),
    "accent": ("accent", "highlight", "secondary"),
    "border": ("border", "divider", "rule", "outline", "stroke", "hairline"),
    "danger": ("danger", "error", "destructive", "critical", "negative"),
    "success": ("success", "positive", "confirm", "valid"),
}


def palette_from_props(props: dict[str, str]) -> dict:
    """
    Roles the site declared itself. A named custom property is authoritative
    in a way no heuristic is - if the author wrote --primary, that is the
    primary, whatever its saturation happens to be.
    """
    candidates: dict[str, tuple[tuple[int, int], str]] = {}
    for name, raw in props.items():
        val = raw.strip()
        hx = None
        m = HEX.fullmatch(val) or HEX.match(val)
        if m and val.startswith("#"):
            hx = norm_hex(m.group(1))
        else:
            counts = harvest_colors(val)
            if len(counts) == 1:
                hx = next(iter(counts))
        if not hx:
            continue
        key = name.lstrip("-").lower()
        segs = set(re.split(r"[-_]+", key))
        for role, words in ROLE_WORDS.items():
            # Match whole segments, not substrings: --bs-primary-bg-subtle
            # should not be able to claim `surface` off the "bg" fragment.
            hit = any(w in segs for w in words) or any(
                w in key for w in words if "-" in w)
            if not hit:
                continue
            # Prefer the most canonical name: --surface beats
            # --surface-raised-hover-alt for the `surface` role.
            prev = candidates.get(role)
            score = (len(segs), len(key))
            if prev is None or score < prev[0]:
                candidates[role] = (score, hx)
            break
    return {role: hx for role, (_, hx) in candidates.items()}


BODY_RULE = re.compile(r"(?:^|[},])\s*(?:html|body)\b[^{}]*\{([^}]*)\}", re.I)
BODY_BG = re.compile(r"background(?:-color)?\s*:\s*([^;}]+)", re.I)
BODY_FG = re.compile(r"(?<!-)\bcolor\s*:\s*([^;}]+)", re.I)


def body_colors(css: str) -> tuple[str | None, str | None]:
    """
    What html/body actually declares. This beats frequency counting: the page
    background is the surface by definition, however few times it is written.
    """
    bg = fg = None
    for block in BODY_RULE.findall(css):
        for m in BODY_BG.finditer(block):
            c = harvest_colors(m.group(1))
            if len(c) == 1:
                bg = bg or next(iter(c))
        for m in BODY_FG.finditer(block):
            c = harvest_colors(m.group(1))
            if len(c) == 1:
                fg = fg or next(iter(c))
    return bg, fg


def classify_palette(counts: Counter, props: dict[str, str] | None = None,
                     css: str = "") -> dict:
    """Assign roles from declared custom properties first, then from evidence."""
    declared = palette_from_props(props or {})
    if not counts:
        return declared
    ranked = counts.most_common()
    pool = [hx for hx, _ in ranked]

    body_bg, body_fg = body_colors(css)
    lights = [h for h in pool if luminance(h) > 0.75]
    darks = [h for h in pool if luminance(h) < 0.12]
    surface = declared.get("surface") or body_bg or (
        lights[0] if lights and (not darks or counts[lights[0]] > counts[darks[0]])
        else (darks[0] if darks else pool[0]))

    ink = declared.get("ink") or body_fg or (
        max(pool, key=lambda h: (contrast(h, surface), counts[h])) if pool else surface)

    out = {"surface": surface, "ink": ink}
    out.update(declared)
    out["surface"], out["ink"] = declared.get("surface", surface), declared.get("ink", ink)

    used = set(out.values())
    # 0.18 is the boundary: below it a color reads as a neutral, above it as
    # chroma. Two separate thresholds with a gap silently dropped colors.
    CHROMA = 0.18
    chroma = sorted((h for h in pool if h not in used and hsl_of(h)[1] >= CHROMA),
                    key=lambda h: -counts[h])
    neutrals = sorted((h for h in pool if h not in used and hsl_of(h)[1] < CHROMA),
                      key=lambda h: -counts[h])

    for role in ("primary", "accent", "accent-2"):
        if role not in out and chroma:
            out[role] = chroma.pop(0)

    for h in neutrals:
        c = contrast(h, surface)
        if "ink-muted" not in out and 2.5 <= c < 7:
            out["ink-muted"] = h
        elif "border" not in out and c < 2.5:
            out["border"] = h
    return out


# ------------------------------------------------------------------- gather

def px(val: str, unit: str) -> float:
    try:
        v = float(val)
    except ValueError:
        return 0.0
    return v * 16 if unit in ("rem", "em") else v


def gather(html: str, css: str) -> dict:
    blob = css + "\n" + html
    d: dict = {}

    d["custom_props"] = {k: v.strip() for k, v in CUSTOM_PROP.findall(css)}

    fams: Counter = Counter()
    for raw in FONT_FAMILY.findall(blob):
        first = raw.split(",")[0].strip().strip("'\"")
        if first and not first.startswith("var(") and len(first) < 40:
            fams[first] += 1
    d["fonts"] = fams.most_common(8)
    d["google_fonts"] = sorted({
        f.replace("+", " ")
        for q in GFONT.findall(html)
        for f in re.findall(r"family=([^&:]+)", q)
    })

    size_counts: Counter = Counter(round(px(v, u), 1)
                                   for v, u in FONT_SIZE.findall(blob))
    d["type_scale"] = sorted(s for s in size_counts if 8 <= s <= 200)
    d["_size_counts"] = size_counts
    d["weights"] = sorted({w for w in FONT_WEIGHT.findall(blob)})
    d["line_heights"] = sorted({v for v, u in LINE_HEIGHT.findall(blob) if not u})[:8]

    sp: set = set()
    for chunk in SPACING.findall(blob):
        for v, u in LEN_PX.findall(chunk):
            p = px(v, u)
            if 0 < p <= 256:
                sp.add(round(p, 1))
    d["spacing"] = sorted(sp)

    rad: set = set()
    for chunk in RADIUS.findall(blob):
        if "%" in chunk or "9999" in chunk:
            rad.add("pill/circle")
        for v, u in LEN_PX.findall(chunk):
            rad.add(round(px(v, u), 1))
    d["radii"] = sorted(rad, key=lambda x: (isinstance(x, str), x))

    shadows = {s.strip() for s in SHADOW.findall(blob) if s.strip().lower() != "none"}
    d["shadow_levels"] = len(shadows)
    d["shadows"] = sorted(shadows, key=len)[:4]

    durs = sorted({(float(v) if u == "s" else float(v) / 1000)
                   for v, u in DURATION.findall(blob)})
    d["durations_ms"] = [round(x * 1000) for x in durs if 0 < x <= 5]
    d["easings"] = sorted({e.lower() for e in EASING.findall(blob)})[:6]
    d["keyframes"] = sorted(set(KEYFRAMES.findall(css)))[:12]

    d["breakpoints"] = sorted({round(px(v, u)) for v, u in MEDIA_W.findall(css)})
    d["max_widths"] = sorted({round(px(v, u)) for v, u in MAX_WIDTH.findall(blob)
                              if 320 <= px(v, u) <= 2400})
    d["grid_patterns"] = sorted({g.strip()[:60] for g in GRID_COLS.findall(blob)})[:6]

    return d


def infer_axes(d: dict, palette: dict) -> dict:
    """Estimate the ui-ux-studio divergence-matrix axes from the evidence."""
    ax = {}
    surf = palette.get("surface")
    if surf:
        lum = luminance(surf)
        ax["contrast_model"] = ("light ground" if lum > 0.6 else
                                "dark ground" if lum < 0.2 else "mid-tone ground")

    sp = [s for s in d["spacing"] if s >= 4]
    if sp:
        typical = sorted(sp)[len(sp) // 2]
        ax["density"] = ("dense" if typical <= 16 else
                         "spacious" if typical >= 40 else "standard")
        base = 8 if any(abs(s % 8) < 0.01 for s in sp[:10]) else 4
        ax["spacing_base"] = f"{base}px"

    ts = d["type_scale"]
    if len(ts) >= 3:
        # Body is the size that appears most often in the readable range -
        # taking the smallest picks up the utility/caption face instead.
        sc = d.get("_size_counts", {})
        candidates = [s for s in ts if 13 <= s <= 20]
        body = (max(candidates, key=lambda s: (sc.get(s, 0), -abs(s - 16)))
                if candidates else ts[0])
        ratios = [round(ts[i + 1] / ts[i], 3) for i in range(len(ts) - 1)
                  if ts[i] >= 12 and ts[i + 1] / ts[i] < 2]
        if ratios:
            ax["type_ratio"] = round(sum(ratios) / len(ratios), 3)
        ax["body_size"] = body
        ax["scale_steps"] = len(ts)

    durs = d["durations_ms"]
    if not durs:
        ax["motion"] = "still (no transitions found)"
    elif max(durs) > 600:
        ax["motion"] = "orchestrated or ambient"
    elif max(durs) <= 200:
        ax["motion"] = "interaction-only, fast"
    else:
        ax["motion"] = "standard transitions"

    rad_nums = [r for r in d["radii"] if isinstance(r, (int, float))]
    if rad_nums or "pill/circle" in d["radii"]:
        top = max(rad_nums) if rad_nums else 999
        ax["radius_personality"] = ("sharp" if top <= 2 else "soft" if top <= 8
                                    else "round" if top <= 20 else "very round/pill")

    if palette:
        temps = [temperature(v) for k, v in palette.items()
                 if k in ("surface", "ink", "border", "ink-muted")]
        warm, cool = temps.count("warm"), temps.count("cool")
        ax["neutral_temperature"] = ("warm-tinted" if warm > cool else
                                     "cool-tinted" if cool > warm else
                                     "untinted (a tell - tinted neutrals read as designed)")
    return ax


TW_DEFAULT_HEXES = {
    "#6366f1", "#4f46e5", "#3b82f6", "#2563eb", "#0ea5e9", "#8b5cf6",
    "#64748b", "#94a3b8", "#cbd5e1", "#f8fafc", "#f1f5f9", "#1e293b",
    "#0f172a", "#ef4444", "#22c55e", "#f59e0b", "#10b981",
}


def detect_frameworks(props: dict[str, str], hexes: set[str]) -> list[str]:
    """
    Off-the-shelf design-system fingerprints. Extraction still describes what
    renders, but stock tokens are a purchased suit, not a tailored one - the
    profile should say so instead of presenting Bootstrap's palette as the
    site's own identity.
    """
    out = []
    keys = set(props)
    if any(k.startswith("--bs-") for k in keys):
        out.append("Bootstrap (--bs-* custom properties)")
    if any(k.startswith(("--mdc-", "--md-sys-")) for k in keys):
        out.append("Material (MDC / M3 tokens)")
    if any(k.startswith(("--colorNeutral", "--fluent")) for k in keys):
        out.append("Fluent UI (v9 token names)")
    if {"--background", "--foreground", "--muted", "--card"} <= keys:
        out.append("shadcn/ui token layer (--background/--foreground/--muted/--card)")
    tw = hexes & TW_DEFAULT_HEXES
    if len(tw) >= 3:
        out.append(f"Tailwind default palette ({len(tw)} stock hexes, e.g. {sorted(tw)[0]})")
    return out


def flag_tells(palette: dict, d: dict) -> list[str]:
    out = []
    for role, hx in palette.items():
        if hx in TELLS:
            out.append(f"{role} {hx} - {TELLS[hx]}")
    for fam, _ in d["fonts"][:3]:
        if fam.lower() in DEFAULT_FONTS:
            out.append(f"font '{fam}' - default face, not a choice")
    if len(d["weights"]) > 4:
        out.append(f"{len(d['weights'])} font weights in use - weight soup")
    if d["shadow_levels"] > 4:
        out.append(f"{d['shadow_levels']} distinct shadows - elevation has no system")
    return out


# --------------------------------------------------------------------- input

def load_url(url: str) -> tuple[str, str]:
    try:
        from urllib.request import Request, urlopen
        from urllib.parse import urljoin
    except ImportError:
        return "", ""
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (design-dna)"})
    try:
        html = urlopen(req, timeout=20).read().decode("utf-8", "replace")
    except Exception as e:
        print(f"error: could not fetch {url}: {e}", file=sys.stderr)
        print("Fetch it with your own web tooling, save it, and use --dir.",
              file=sys.stderr)
        sys.exit(2)
    css = "\n".join(STYLE_BLOCK.findall(html))
    for href in LINK_CSS.findall(html)[:8]:
        try:
            full = urljoin(url, href)
            css += "\n" + urlopen(Request(full, headers={"User-Agent": "design-dna"}),
                                  timeout=20).read().decode("utf-8", "replace")
        except Exception:
            continue
    return html, css


def load_paths(paths: list[Path]) -> tuple[str, str]:
    html_parts, css_parts = [], []
    for p in paths:
        try:
            t = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if p.suffix.lower() in (".css", ".scss", ".less"):
            css_parts.append(t)
        else:
            html_parts.append(t)
            css_parts.extend(STYLE_BLOCK.findall(t))
            css_parts.extend(STYLE_ATTR.findall(t))
    return "\n".join(html_parts), "\n".join(css_parts)


# -------------------------------------------------------------------- report

def write_report(name: str, palette: dict, d: dict, axes: dict,
                 tells: list[str], fingerprints: list[str] | None = None) -> str:
    L = [f"# Design DNA: {name}", ""]

    L += ["## Palette", "", "| role | hex | luminance | temperature |",
          "|---|---|---|---|"]
    for role, hx in palette.items():
        L.append(f"| {role} | `{hx}` | {luminance(hx):.2f} | {temperature(hx)} |")
    L.append("")

    if d["custom_props"]:
        L += [f"The site exposes {len(d['custom_props'])} CSS custom properties, "
              "so it already has a token layer — prefer those names over the "
              "roles inferred above.", "", "```css"]
        for k, v in list(d["custom_props"].items())[:24]:
            L.append(f"{k}: {v};")
        if len(d["custom_props"]) > 24:
            L.append(f"/* +{len(d['custom_props']) - 24} more */")
        L += ["```", ""]

    L += ["## Type", ""]
    if d["fonts"]:
        L.append("Families by frequency: " +
                 ", ".join(f"`{f}` ({n})" for f, n in d["fonts"][:5]))
    if d["google_fonts"]:
        L.append(f"Google Fonts loaded: {', '.join(d['google_fonts'])}")
    if d["type_scale"]:
        L.append(f"Scale ({len(d['type_scale'])} steps): "
                 f"{', '.join(str(s) for s in d['type_scale'])}")
    if "type_ratio" in axes:
        L.append(f"Mean ratio between steps: {axes['type_ratio']}")
    if d["weights"]:
        L.append(f"Weights: {', '.join(d['weights'])}")
    L.append("")

    L += ["## Space and form", ""]
    if d["spacing"]:
        L.append(f"Spacing values: {', '.join(str(s) for s in d['spacing'][:16])}"
                 + (" …" if len(d["spacing"]) > 16 else ""))
    if d["radii"]:
        L.append(f"Radii: {', '.join(str(r) for r in d['radii'])}")
    L.append(f"Distinct shadows: {d['shadow_levels']}")
    if d["max_widths"]:
        L.append(f"Container widths: {', '.join(str(w) for w in d['max_widths'])}")
    if d["breakpoints"]:
        L.append(f"Breakpoints: {', '.join(str(b) for b in d['breakpoints'])}")
    if d["grid_patterns"]:
        L.append("Grid patterns: " + "; ".join(f"`{g}`" for g in d["grid_patterns"]))
    L.append("")

    L += ["## Motion", ""]
    L.append(f"Durations (ms): {d['durations_ms'] or 'none found'}")
    if d["easings"]:
        L.append(f"Easings: {', '.join(d['easings'])}")
    if d["keyframes"]:
        L.append(f"Keyframes: {', '.join(d['keyframes'])}")
    L.append("")

    L += ["## Divergence-matrix axes (estimated)", "",
          "Feed these to ui-ux-studio. For `remix`, pick *different* values.",
          "For `update`, match them exactly.", "",
          "| axis | value |", "|---|---|"]
    for k, v in axes.items():
        L.append(f"| {k.replace('_', ' ')} | {v} |")
    L.append("")

    if fingerprints:
        L += ["## Framework fingerprints", ""]
        L += [f"- {f}" for f in fingerprints]
        L += ["", "These tokens are an off-the-shelf system, not this site's own "
              "identity. The extraction above describes what renders, but "
              "style-naming should say 'stock <framework>' rather than treating "
              "the framework's choices as the site's — and any differentiation "
              "analysis should look past them to what, if anything, was "
              "customized.", ""]

    L += ["## AI tells present", ""]
    if tells:
        L += [f"- {t}" for t in tells]
        L += ["", "In `remix`, treat these as things to fix. In `update`, match "
              "the house style anyway — consistency beats correctness when "
              "extending someone else's system; raise them separately."]
    else:
        L.append("None detected in the extracted values.")
    L += ["", "---", "",
          "Extracted mechanically. Runtime-applied styles, auth-gated pages, and "
          "every question of *why* are invisible here — do the manual pass in "
          "`references/extraction.md` before treating this as complete."]
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser(description="Extract a design system from HTML/CSS.")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--url")
    src.add_argument("--dir")
    src.add_argument("--files", nargs="+")
    ap.add_argument("--out", default="./dna")
    ap.add_argument("--name", help="label for the report")
    ap.add_argument("--json", action="store_true", help="print JSON, write nothing")
    args = ap.parse_args()

    if args.url:
        html, css = load_url(args.url)
        name = args.name or args.url
    elif args.dir:
        root = Path(args.dir)
        if not root.is_dir():
            print(f"error: {root} is not a directory", file=sys.stderr)
            return 2
        paths = [p for p in sorted(root.rglob("*"))
                 if p.is_file() and p.suffix.lower() in
                 (".html", ".htm", ".css", ".scss", ".less", ".jsx", ".tsx", ".vue", ".svelte")
                 and "node_modules" not in p.parts]
        html, css = load_paths(paths)
        name = args.name or root.name
    else:
        html, css = load_paths([Path(f) for f in args.files])
        name = args.name or "site"

    if not (html or css):
        print("error: no HTML or CSS content found", file=sys.stderr)
        return 2

    light_css, dark_css = split_themes(css)
    has_dark = bool(dark_css.strip())
    if has_dark:
        # stderr: stdout must stay clean JSON in --json mode
        print(f"Detected a dark theme ({len(dark_css)} chars). Reporting the "
              "default theme as primary; dark written separately.",
              file=sys.stderr)
    css = light_css

    counts = harvest_colors(css + "\n" + html)
    props_all = gather(html, css)["custom_props"]
    palette = classify_palette(counts, props_all, css)
    fingerprints = detect_frameworks(props_all, set(counts))
    dark_palette = {}
    if has_dark:
        dcounts = harvest_colors(dark_css)
        dark_palette = classify_palette(
            dcounts, gather("", dark_css)["custom_props"], dark_css)
    d = gather(html, css)
    axes = infer_axes(d, palette)
    d.pop("_size_counts", None)
    tells = flag_tells(palette, d)

    if args.json:
        print(json.dumps({"name": name, "palette": palette,
                          "dark_palette": dark_palette, "axes": axes,
                          "framework_fingerprints": fingerprints,
                          "tells": tells, "raw": d,
                          "color_frequency": counts.most_common(24)}, indent=2))
        return 0

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "tokens.json").write_text(json.dumps(palette, indent=2))
    if dark_palette:
        (out / "tokens-dark.json").write_text(json.dumps(dark_palette, indent=2))
    (out / "profile.md").write_text(
        write_report(name, palette, d, axes, tells, fingerprints))
    (out / "raw.json").write_text(json.dumps(
        {"axes": axes, "raw": d, "color_frequency": counts.most_common(40)}, indent=2))

    print(f"Extracted from: {name}")
    print(f"  {len(counts)} distinct colors -> {len(palette)} roles")
    print(f"  {len(d['fonts'])} font families, {len(d['type_scale'])} type steps")
    print(f"  {len(d['spacing'])} spacing values, {d['shadow_levels']} shadow levels")
    if tells:
        print(f"  {len(tells)} AI tell(s) flagged")
    for f in fingerprints:
        print(f"  stock framework: {f}")
    if dark_palette:
        print(f"  dark theme: {len(dark_palette)} roles -> tokens-dark.json")
    print(f"\nWrote {out}/tokens.json, {out}/profile.md, {out}/raw.json")
    print(f"Check contrast:  python3 contrast.py --tokens {out}/tokens.json"
          + (f" --tokens-dark {out}/tokens-dark.json" if dark_palette else ""))
    print("Contrast pairs are guessed from role names; add a \"pairs\" list to "
          "the token file for an accurate reading.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
favicon.py - turn a designed SVG mark into a complete favicon + head setup.

Emits favicon.svg (with an embedded dark-mode variant), icon-mono.svg for
pinned tabs, site.webmanifest, and a ready-to-paste head-snippet.html.
Rasterizes PNGs when cairosvg or rsvg-convert is available; prints the exact
fallback command when neither is.

Usage:
    python3 favicon.py --svg mark.svg --name "Ashfield" \
        --theme "#0B4F6C" --background "#FDFCFA" --out ./public

    python3 favicon.py --svg mark.svg --check      # 16px legibility preview

Design rules the mark must satisfy live in references/favicon-and-head.md.
--check flags the mechanically detectable ones.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SVG_NS = "http://www.w3.org/2000/svg"

MANIFEST = """{{
  "name": "{name}",
  "short_name": "{short}",
  "icons": [
    {{ "src": "/favicon.svg", "type": "image/svg+xml", "sizes": "any" }},
    {{ "src": "/icon-192.png", "type": "image/png", "sizes": "192x192" }},
    {{ "src": "/icon-512.png", "type": "image/png", "sizes": "512x512" }},
    {{ "src": "/icon-maskable-512.png", "type": "image/png",
       "sizes": "512x512", "purpose": "maskable" }}
  ],
  "theme_color": "{theme}",
  "background_color": "{background}",
  "display": "standalone",
  "start_url": "/"
}}
"""

HEAD = """<!-- Icons -->
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="mask-icon" href="/icon-mono.svg" color="{theme}">
<link rel="manifest" href="/site.webmanifest">

<!-- Theme -->
<meta name="theme-color" content="{background}" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="{theme}" media="(prefers-color-scheme: dark)">
<meta name="color-scheme" content="light dark">

<!-- Viewport - viewport-fit=cover is required for env(safe-area-inset-*) -->
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">

<!-- Title and description: write these per references/favicon-and-head.md §3 -->
<title>{name}</title>
<meta name="description" content="TODO - under 155 characters, says what this
      page is and why someone would open it.">
<link rel="canonical" href="TODO">

<!-- Social - 1200x630, designed not screenshotted -->
<meta property="og:type" content="website">
<meta property="og:title" content="{name}">
<meta property="og:description" content="TODO">
<meta property="og:image" content="TODO/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
"""


# --------------------------------------------------------------------- checks

def get_viewbox(root: ET.Element) -> tuple[float, float, float, float] | None:
    vb = root.get("viewBox")
    if not vb:
        return None
    try:
        parts = [float(x) for x in re.split(r"[,\s]+", vb.strip()) if x]
        return tuple(parts[:4]) if len(parts) >= 4 else None  # type: ignore
    except ValueError:
        return None


def check_mark(svg_text: str) -> list[str]:
    """Mechanically detectable violations of the 16px legibility rules."""
    issues: list[str] = []
    try:
        root = ET.fromstring(svg_text)
    except ET.ParseError as e:
        return [f"SVG does not parse: {e}"]

    vb = get_viewbox(root)
    if not vb:
        issues.append("no viewBox - add one (512x512 recommended) so it scales")
        span = 512.0
    else:
        span = max(vb[2], vb[3])
        if vb[2] != vb[3]:
            issues.append(f"viewBox is not square ({vb[2]:g}x{vb[3]:g}) - "
                          "favicons render in square slots")

    def tag(e):
        return e.tag.split("}")[-1]

    elems = list(root.iter())
    drawables = [e for e in elems if tag(e) in
                 {"path", "circle", "rect", "ellipse", "polygon",
                  "polyline", "line"}]

    if len(drawables) > 6:
        issues.append(f"{len(drawables)} drawn elements - three shapes become "
                      "mud at 16px; simplify toward one or two")

    min_stroke = span * 0.08
    for e in elems:
        sw = e.get("stroke-width")
        if sw:
            try:
                if float(re.sub(r"[a-z%]", "", sw)) < min_stroke:
                    issues.append(
                        f"stroke-width {sw} is below 8% of the viewBox "
                        f"({min_stroke:.0f}) - it will vanish at 16px")
                    break
            except ValueError:
                pass

    texts = [e for e in elems if tag(e) == "text"]
    for t in texts:
        content = "".join(t.itertext()).strip()
        if len(content) > 2:
            issues.append(f"text {content!r} is longer than 2 characters - "
                          "unreadable at 16px")
    if texts:
        issues.append("text elements do not render in all favicon contexts - "
                      "convert type to paths")

    if "<image" in svg_text:
        issues.append("embedded raster image - favicons must be pure vector")
    if "font-family" in svg_text and not texts:
        issues.append("font-family present with no text element - dead style")

    size = len(svg_text.encode("utf-8"))
    if size > 4096:
        issues.append(f"{size} bytes - aim under ~2KB; simplify paths")

    if "prefers-color-scheme" not in svg_text:
        issues.append("no dark-mode variant - the mark may disappear against "
                      "dark browser chrome (favicon.py adds a wrapper, but "
                      "designing it in is better)")

    return issues


def preview_16(svg_path: Path) -> str | None:
    """Rasterize to 16px and render as ASCII, if a rasterizer exists."""
    png = rasterize(svg_path, 16, None)
    if png is None:
        return None
    try:
        from PIL import Image
    except ImportError:
        return None
    img = Image.open(png).convert("LA").resize((32, 16))
    ramp = " .:-=+*#%@"
    out = []
    for y in range(16):
        row = ""
        for x in range(32):
            lum, alpha = img.getpixel((x, y))
            if alpha < 40:
                row += " "
            else:
                row += ramp[min(len(ramp) - 1, int((255 - lum) / 256 * len(ramp)))]
        out.append(row)
    png.unlink(missing_ok=True)
    return "\n".join(out)


# ----------------------------------------------------------------- raster ops

def rasterize(svg: Path, size: int, out: Path | None) -> Path | None:
    """Render svg to png at size. Returns path, or None if no rasterizer."""
    target = out or svg.parent / f".tmp-{size}.png"
    try:
        import cairosvg  # type: ignore
        cairosvg.svg2png(url=str(svg), write_to=str(target),
                         output_width=size, output_height=size)
        return target
    except ImportError:
        pass
    except Exception as e:
        print(f"warning: cairosvg failed ({e})", file=sys.stderr)

    rsvg = shutil.which("rsvg-convert")
    if rsvg:
        try:
            subprocess.run([rsvg, "-w", str(size), "-h", str(size),
                            str(svg), "-o", str(target)],
                           check=True, capture_output=True)
            return target
        except subprocess.CalledProcessError as e:
            print(f"warning: rsvg-convert failed: {e}", file=sys.stderr)

    for tool in ("resvg", "inkscape"):
        exe = shutil.which(tool)
        if not exe:
            continue
        cmd = ([exe, "-w", str(size), "-h", str(size), str(svg), str(target)]
               if tool == "resvg" else
               [exe, str(svg), "-w", str(size), "-h", str(size),
                "-o", str(target)])
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return target
        except subprocess.CalledProcessError:
            continue
    return None


COLOR_ATTR = re.compile(r'\b(fill|stroke)="(#[0-9a-fA-F]{3,8}|rgb\([^)]*\))"')


def distinct_colors(svg_text: str) -> list[str]:
    """Distinct literal colors, in document order."""
    seen, order = set(), []
    for _, val in COLOR_ATTR.findall(svg_text):
        key = val.lower()
        if key not in seen:
            seen.add(key)
            order.append(val)
    return order


def wrap_dark_mode(svg_text: str, theme: str, background: str) -> tuple[str, str | None]:
    """
    Rewire literal fills to CSS variables and swap them under dark mode.

    Only does this for two-color marks, where swapping is unambiguously
    correct. Anything more complex needs a designed dark variant, not a
    mechanical inversion - in that case return the mark untouched plus a note.
    Returns (svg, warning_or_None).
    """
    if "prefers-color-scheme" in svg_text:
        return svg_text, None

    colors = distinct_colors(svg_text)
    if len(colors) != 2:
        return svg_text, (
            f"mark has {len(colors)} literal color(s) - a dark variant was NOT "
            "injected. Add a prefers-color-scheme block to the SVG by hand; a "
            "mechanical inversion of a multi-color mark is usually wrong."
        )

    c0, c1 = colors
    out = svg_text
    for name, val in (("--fav-a", c0), ("--fav-b", c1)):
        out = re.sub(
            r'\b(fill|stroke)="' + re.escape(val) + r'"',
            lambda m, n=name: f'{m.group(1)}="var({n})"',
            out, flags=re.I,
        )

    style = (
        "<style>"
        f":root{{--fav-a:{c0};--fav-b:{c1};}}"
        "@media (prefers-color-scheme: dark){"
        f":root{{--fav-a:{c1};--fav-b:{c0};}}}}"
        "</style>"
    )
    m = re.search(r"<svg\b[^>]*>", out)
    if not m:
        return svg_text, "no <svg> element found - dark variant not injected"
    return out[:m.end()] + style + out[m.end():], None


def make_mono(svg_text: str) -> str:
    """
    Single-color mark for Safari pinned tabs and other monochrome contexts.

    The background plate must go: pinned tabs render the mark as a silhouette,
    so a full-bleed rect would produce a solid square. Drop any rect that
    covers the whole viewBox, then set everything remaining to currentColor.
    """
    out = re.sub(r"<style>.*?</style>", "", svg_text, flags=re.S)

    vb = None
    m = re.search(r'viewBox="([^"]+)"', out)
    if m:
        try:
            parts = [float(x) for x in re.split(r"[,\s]+", m.group(1).strip()) if x]
            if len(parts) >= 4:
                vb = (parts[2], parts[3])
        except ValueError:
            pass

    if vb:
        def drop_plate(match: re.Match) -> str:
            tag = match.group(0)
            w = re.search(r'\bwidth="([\d.]+)"', tag)
            h = re.search(r'\bheight="([\d.]+)"', tag)
            if not (w and h):
                return tag
            if float(w.group(1)) >= vb[0] * 0.98 and float(h.group(1)) >= vb[1] * 0.98:
                return ""
            return tag
        out = re.sub(r"<rect\b[^>]*/?>", drop_plate, out)

    out = re.sub(r'\bfill="(?!none)[^"]*"', 'fill="currentColor"', out)
    out = re.sub(r'\bstroke="(?!none)[^"]*"', 'stroke="currentColor"', out)
    out = re.sub(r"\n\s*\n", "\n", out)
    return out


# ---------------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description="Build a favicon set from an SVG mark.")
    ap.add_argument("--svg", required=True, help="the designed mark")
    ap.add_argument("--name", default="Site", help="product name for manifest and title")
    ap.add_argument("--short", help="short name (defaults to --name)")
    ap.add_argument("--theme", default="#000000", help="theme color hex")
    ap.add_argument("--background", default="#FFFFFF", help="background color hex")
    ap.add_argument("--out", default="./public", help="output directory")
    ap.add_argument("--check", action="store_true",
                    help="only run legibility checks and a 16px preview")
    args = ap.parse_args()

    src = Path(args.svg)
    if not src.exists():
        print(f"error: {src} not found", file=sys.stderr)
        return 2
    svg_text = src.read_text(encoding="utf-8")

    issues = check_mark(svg_text)
    print("=== 16px legibility check ===")
    if issues:
        for i in issues:
            print(f"  ! {i}")
    else:
        print("  no mechanical issues found")

    art = preview_16(src)
    if art:
        print("\n=== 16px preview ===")
        print(art)
        print("\nIf you have to squint, simplify and re-run.")
    else:
        print("\n(no rasterizer available for the 16px preview - install "
              "cairosvg or rsvg-convert)")

    if args.check:
        print("\nJudgement calls the script cannot make: does the silhouette "
              "read with fills removed? Does the mark derive from the design's "
              "signature element, or is it a letter in a box?")
        return 1 if issues else 0

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    short = args.short or args.name

    written = []
    fav = out / "favicon.svg"
    dark_svg, dark_warning = wrap_dark_mode(svg_text, args.theme, args.background)
    fav.write_text(dark_svg, encoding="utf-8")
    written.append(fav)
    if dark_warning:
        print(f"\n  ! {dark_warning}")

    mono = out / "icon-mono.svg"
    mono.write_text(make_mono(svg_text), encoding="utf-8")
    written.append(mono)

    man = out / "site.webmanifest"
    man.write_text(MANIFEST.format(name=args.name, short=short,
                                   theme=args.theme,
                                   background=args.background),
                   encoding="utf-8")
    written.append(man)

    snippet = out / "head-snippet.html"
    snippet.write_text(HEAD.format(theme=args.theme,
                                   background=args.background,
                                   name=args.name), encoding="utf-8")
    written.append(snippet)

    print("\n=== rasterizing ===")
    targets = [("apple-touch-icon.png", 180), ("icon-192.png", 192),
               ("icon-512.png", 512), ("favicon-32.png", 32)]
    ok = True
    for fname, size in targets:
        p = rasterize(src, size, out / fname)
        if p:
            written.append(out / fname)
            print(f"  wrote {fname}")
        else:
            ok = False
            break

    if not ok:
        print("  no rasterizer found (cairosvg, rsvg-convert, resvg, inkscape)")
        print("  SVG favicons work in every current browser, so the set above")
        print("  is already functional. For the PNG fallbacks, run:")
        print(f"    npx -y sharp-cli -i {fav} -o {out}/icon-512.png resize 512 512")
        print(f"    npx -y sharp-cli -i {fav} -o {out}/apple-touch-icon.png resize 180 180")
        print("  or:  pip install cairosvg  and re-run this script.")

    print("\n=== written ===")
    for w in written:
        print(f"  {w}")
    print(f"\nPaste {snippet} into <head> and fill the TODO fields.")
    print("Reminder: the maskable icon crops to a circle - keep all meaningful")
    print("content inside the centered 80% safe zone.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        # piping into head/less closes stdout early; not an error
        try:
            sys.stdout.close()
        finally:
            sys.exit(0)

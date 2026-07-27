#!/usr/bin/env python3
"""
ai_tells.py - scan frontend source for concrete AI-design tells.

These are the mechanical tells only: colors, fonts, class patterns, copy
phrasings. The structural tells (canonical section order, decorative bento,
keyword-matched icon sets, three-column feature grids) need a human read of
references/ai-tells.md - this script cannot see them.

Usage:
    python3 ai_tells.py src/ app/ styles/
    python3 ai_tells.py page.html --json
    python3 ai_tells.py src/ --min-severity high
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

FILE_NOTES: dict[str, list[str]] = {}

EXTS = {".css", ".scss", ".sass", ".less", ".html", ".htm", ".js", ".jsx",
        ".ts", ".tsx", ".vue", ".svelte", ".astro", ".mdx"}

SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", ".nuxt",
             "out", "vendor", "coverage", ".venv", "venv", "__pycache__",
             ".svelte-kit", "public/build"}

# (id, severity, compiled regex, message)
# severity: high = near-certain tell | med = default worth justifying
#           low  = context-dependent, flag for a look
RULES: list[tuple[str, str, re.Pattern, str]] = [

    # ---------------------------------------------------------------- palette
    ("claude-accent", "high",
     re.compile(r"#(d9775[0-9a-f]|da7756|cc785c|c15f3c)\b", re.I),
     "Anthropic's terracotta interaction accent - reads as a fingerprint"),
    ("claude-cream", "high",
     re.compile(r"#(f4f1ea|faf9f5|f5f4ed|f0eee6)\b", re.I),
     "the cream ground of AI cluster look #1"),
    ("template-gradient", "high",
     re.compile(r"#(667eea|764ba2|6a11cb|2575fc|8e2de2|4a00e0)\b", re.I),
     "the purple-blue template gradient"),
    ("indigo-default", "med",
     re.compile(r"(#6366f1|#4f46e5|#4338ca)\b|\b(bg|text|from|to|via|border|ring)-indigo-(400|500|600)\b", re.I),
     "Tailwind indigo default primary - chosen by not choosing"),
    ("acid-accent", "med",
     re.compile(r"#(a3e635|84cc16|00ff88|39ff14|ccff00|d9f99d)\b", re.I),
     "acid accent of AI cluster look #2 (dark technical)"),
    ("gradient-text", "high",
     re.compile(r"(background-clip:\s*text|-webkit-background-clip:\s*text|\bbg-clip-text\b)", re.I),
     "gradient headline text - decoration where type should carry weight"),
    ("uniform-glass", "med",
     re.compile(r"(backdrop-filter:\s*blur|\bbackdrop-blur-)", re.I),
     "glassmorphism - check it is not applied to every surface uniformly"),
    ("white-alpha-surface", "low",
     re.compile(r"(rgba\(255,\s*255,\s*255,\s*0\.0?[0-9]\)|\bbg-white/(5|10)\b)", re.I),
     "default translucent surface - one material used for everything"),

    # ------------------------------------------------------------- typography
    ("default-font", "high",
     re.compile(r"font-family[^;{}]*\b(Inter|Roboto|Poppins|Montserrat|Open Sans|Geist|Nunito Sans)\b", re.I),
     "default display face - pick something that would look wrong on another brief"),
    ("font-import-default", "med",
     re.compile(r"fonts\.googleapis\.com[^\"')]*family=(Inter|Roboto|Poppins|Montserrat|Open\+Sans|Nunito)", re.I),
     "importing a default font family"),
    ("editorial-serif-reflex", "low",
     re.compile(r"\b(Playfair Display|Instrument Serif|Cormorant Garamond|DM Serif Display)\b", re.I),
     "the reflex serif for 'editorial' - justify against the subject"),
    ("clamp-hero", "med",
     re.compile(r"clamp\(\s*[2-9](\.\d+)?rem\s*,\s*\d+(\.\d+)?vw\s*,\s*\d+(\.\d+)?rem\s*\)", re.I),
     "the clamp hero - check the headline says something concrete"),
    ("tracked-eyebrow", "low",
     re.compile(r"\btext-xs\b[^\"'>]*\buppercase\b[^\"'>]*\btracking-(wide|wider|widest)\b", re.I),
     "uppercase tracked eyebrow - a tell if it sits above every section"),

    # ----------------------------------------------------------------- layout
    # Counted, not per-line: see COUNT_GATED below. A run of 01-19 is a real
    # enumeration (contact sheet frames, a numbered index); the tell is the
    # decorative 2-4 item triad on content that is not a sequence.
    ("sequence-markers", "med",
     re.compile(r">\s*0[1-9]\s*<|[\"'\s]0[1-9]\s*/\s*0[1-9]"),
     "01/02/03 markers - only valid if the content is an actual sequence"),
    ("uniform-section-padding", "low",
     re.compile(r"\bpy-24\b"),
     "check section padding varies by hierarchy rather than repeating"),
    ("default-container", "low",
     re.compile(r"\bmax-w-7xl\s+mx-auto\b"),
     "centered default container on every section - zero asymmetry"),
    ("default-card-chrome", "med",
     re.compile(r"\brounded-2xl\b[^\"'>]*\bshadow-lg\b|\bshadow-lg\b[^\"'>]*\brounded-2xl\b"),
     "default card chrome - same radius and elevation on every surface"),

    # -------------------------------------------------------------- animation
    ("transition-all", "high",
     re.compile(r"transition:\s*all\b|\btransition-all\b"),
     "transition: all - list properties explicitly"),
    ("hover-scale", "med",
     re.compile(r"\bhover:scale-1(0[0-9]|1[0-9])\b"),
     "hover:scale on cards - reserve scale for one element that earns it"),
    ("layout-animation", "high",
     re.compile(r"transition[^;{}]*\b(width|height|top|left|right|bottom|margin|padding)\b\s*[\d.]*s", re.I),
     "animating layout properties - use transform and opacity"),
    ("uniform-fade-up", "med",
     re.compile(r"\b(fade-?in-?up|animate-fade-?up|fadeInUp)\b", re.I),
     "the universal scroll reveal - one orchestrated moment beats scattered effects"),

    # ------------------------------------------------------------ a11y / bugs
    ("outline-none", "high",
     re.compile(r"outline:\s*(none|0)\b|\boutline-none\b"),
     "focus outline removed - verify a focus-visible replacement exists"),
    ("zoom-disabled", "high",
     re.compile(r"user-scalable\s*=\s*no|maximum-scale\s*=\s*1"),
     "zoom disabled - accessibility failure"),
    ("div-onclick", "high",
     re.compile(r"<(div|span)\b[^>]*\bonClick\s*=", re.I),
     "click handler on a non-interactive element - use <button>"),
    ("block-paste", "high",
     re.compile(r"onPaste\s*=\s*\{[^}]*preventDefault", re.I),
     "paste blocked - user-hostile"),
    ("ellipsis-chars", "low",
     re.compile(r"(Loading\.\.\.|Saving\.\.\.|Submitting\.\.\.)"),
     "use the ellipsis character in loading copy"),

    # ------------------------------------------------------------------- copy
    ("copy-transform", "high",
     re.compile(r"\bTransform your\b|\btake your .{2,25} to the next level\b", re.I),
     "template hero copy"),
    ("copy-buzzwords", "med",
     re.compile(r"\b(effortlessly|seamlessly|supercharge|unlock the power|elevate your|revolutioniz\w+|harness the power|game-chang\w+)\b", re.I),
     "AI marketing vocabulary"),
    ("copy-fake-testimonial", "high",
     re.compile(r"\b(Sarah Chen|Marcus Rodriguez|Alex Thompson|Emily Watson|Jane Doe|John Smith)\b\s*,?\s*(CTO|CEO|VP|Head of|Founder|Director)", re.I),
     "invented testimonial persona"),
    ("copy-vague-cta", "med",
     re.compile(r">\s*(Get Started|Learn More|Continue|Submit)\s*<", re.I),
     "vague CTA - say what happens"),
    ("copy-abstract-feature", "low",
     re.compile(r"\b(Smart Insights|Powerful Analytics|Seamless Integration|Lightning Fast|Built for Teams)\b", re.I),
     "two-abstract-noun feature title"),
    ("lorem", "high",
     re.compile(r"\blorem ipsum\b", re.I),
     "placeholder copy - real copy is design material"),

    # ------------------------------------------- borrowed institutional weight
    ("borrowed-archive", "med",
     re.compile(r"\b(on the books|standing record|accession(?: number)?s?\b|register opened|entries are numbered|stamped on delivery|of record\b|in our custody)", re.I),
     "archive register - implies institutional custody; check against real scale"),
    ("borrowed-ops", "med",
     re.compile(r"\b(status:\s*live|currently running|on the crew|board revised|operational status|uptime)\b", re.I),
     "operations register - implies continuous state; check the subject has any"),
    ("empty-readout", "high",
     re.compile(r">\s*(None set|0 currently running|no active\w*|nothing scheduled)\s*<", re.I),
     "live readout displaying emptiness - advertises inactivity; drop the readout"),
    ("defensive-copy", "med",
     re.compile(r"\b(not a brochure|this isn't marketing|no fluff|unlike other)\b", re.I),
     "defensive framing - the design should carry this, not the copy"),

    # ------------------------------------------------------------ iconography
    ("emoji-icon", "med",
     re.compile(r"[\U0001F300-\U0001FAFF\u2699\u26A1\u2728]"),
     "emoji present - never use emoji as a structural icon"),
    ("keyword-icons", "low",
     re.compile(r"\b(Zap|Rocket|Sparkles|ShieldCheck|BarChart3)\b\s*/?>"),
     "keyword-matched Lucide icon - the loudest iconography tell"),
]

# Rules where a small number of hits is a tell but many hits means the content
# is genuinely enumerated. Maps rule id -> max hits per file before it is
# treated as a real sequence and suppressed.
COUNT_GATED = {"sequence-markers": 4}

# ---------------------------------------------------------------- file rules
# Some tells are properties of a whole file, not a line. Each function takes
# the full text and returns a list of (id, severity, message) plus optional
# informational notes that are reported but not counted as violations.

SECTION_RE = re.compile(r"<section\b", re.I)
NAV_RE = re.compile(r"<nav\b.*?</nav>", re.S | re.I)
HREF_RE = re.compile(r'href="([^"]+)"')
BG_DECL = re.compile(r"background(?:-color)?\s*:\s*([^;}]+)", re.I)
SURFACE_SEL = re.compile(
    r"\b(body|html|main|section|article|header|footer|\.(?:band|strip|panel|"
    r"surface|ground|recess|sheet|hero|masthead|wrap|page|bg)[\w-]*)\b", re.I)


def rule_route_collapse(text: str) -> tuple[list, list]:
    """
    A multi-section page whose nav points only at #anchors is very likely a
    multi-route site flattened onto one page. This is the reliable signal;
    the background patchwork it causes is not mechanically separable from
    legitimate component backgrounds, so it is reported rather than flagged.
    """
    hits, notes = [], []
    sections = len(SECTION_RE.findall(text))
    nav = "".join(NAV_RE.findall(text))
    if not nav:
        return hits, notes
    hrefs = HREF_RE.findall(nav)
    anchors = [h for h in hrefs if h.startswith("#")]
    internal = [h for h in hrefs
                if not h.startswith(("#", "http://", "https://", "mailto:", "tel:"))]
    if sections >= 5 and len(anchors) >= 4 and not internal:
        hits.append((
            "route-collapse", "med",
            f"{sections} sections, {len(anchors)} nav anchors, 0 internal links - "
            "one-page shape. Correct for a genuine one-pager; a defect if the "
            "source has routes. This script cannot see the source - verify "
            "against references/site-architecture.md"))
    return hits, notes


def rule_background_report(text: str) -> tuple[list, list]:
    """Count surface-level backgrounds. Informational: see docstring above."""
    css = " ".join(re.findall(r"<style[^>]*>(.*?)</style>", text, re.S | re.I))
    if not css:
        return [], []
    vals = set()
    for sel, body in re.findall(r"([^{}@]+)\{([^{}]*)\}", css):
        if not SURFACE_SEL.search(sel):
            continue
        for v in BG_DECL.findall(body):
            v = v.strip().lower()
            if v in ("none", "transparent", "inherit", "initial",
                     "currentcolor") or v.startswith("url"):
                continue
            vals.add(v)
    if len(vals) >= 4:
        return [], [f"{len(vals)} distinct surface backgrounds - one ground plus "
                    "one or two deliberate departures is the target. Four or more "
                    "is patchwork; if the page needs bands to be legible, split it "
                    "(references/site-architecture.md §3) rather than restyling."]
    return [], [f"{len(vals)} distinct surface background(s)"]


FILE_RULES = [rule_route_collapse, rule_background_report]

SEV_ORDER = {"low": 0, "med": 1, "high": 2}
COLOR = {"high": "\033[31m", "med": "\033[33m", "low": "\033[36m"}
RESET = "\033[0m"


def iter_files(paths: list[str]):
    for raw in paths:
        p = Path(raw)
        if p.is_file():
            yield p
        elif p.is_dir():
            for f in sorted(p.rglob("*")):
                if not f.is_file() or f.suffix.lower() not in EXTS:
                    continue
                if any(part in SKIP_DIRS for part in f.parts):
                    continue
                yield f
        else:
            print(f"warning: {raw} not found", file=sys.stderr)


def scan(path: Path) -> list[dict]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        print(f"warning: cannot read {path}: {e}", file=sys.stderr)
        return []

    hits, seen, notes = [], set(), []

    for fn in FILE_RULES:
        fhits, fnotes = fn(text)
        notes.extend(fnotes)
        for rid, sev, msg in fhits:
            hits.append({"file": str(path), "line": 0, "id": rid,
                         "severity": sev, "message": msg, "excerpt": ""})

    for lineno, line in enumerate(text.splitlines(), 1):
        if len(line) > 4000:
            line = line[:4000]
        for rid, sev, pat, msg in RULES:
            if pat.search(line):
                # one hit per rule per line
                key = (rid, lineno)
                if key in seen:
                    continue
                seen.add(key)
                hits.append({
                    "file": str(path), "line": lineno, "id": rid,
                    "severity": sev, "message": msg,
                    "excerpt": line.strip()[:110],
                })

    # Suppress count-gated rules that fired often enough to be real content.
    for rid, ceiling in COUNT_GATED.items():
        n = sum(1 for h in hits if h["id"] == rid)
        if n > ceiling:
            hits = [h for h in hits if h["id"] != rid]
    FILE_NOTES[str(path)] = notes
    return hits


def main() -> int:
    ap = argparse.ArgumentParser(description="Scan for AI-design tells.")
    ap.add_argument("paths", nargs="+", help="files or directories")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--min-severity", choices=["low", "med", "high"],
                    default="low", help="minimum severity to report")
    ap.add_argument("--no-color", action="store_true")
    args = ap.parse_args()

    floor = SEV_ORDER[args.min_severity]
    all_hits = []
    scanned = 0
    for f in iter_files(args.paths):
        scanned += 1
        all_hits.extend(h for h in scan(f) if SEV_ORDER[h["severity"]] >= floor)

    if args.json:
        print(json.dumps({"scanned": scanned, "count": len(all_hits),
                          "tells": all_hits}, indent=2))
        return 1 if any(h["severity"] == "high" for h in all_hits) else 0

    use_color = not args.no_color and sys.stdout.isatty()

    def paint(s, sev):
        return f"{COLOR[sev]}{s}{RESET}" if use_color else s

    for fname, notes in sorted(FILE_NOTES.items()):
        for n in notes:
            if "patchwork" in n:
                print(f"{paint('[note]', 'med')} {fname} - {n}")

    if not all_hits:
        print(f"No mechanical AI tells found across {scanned} file(s).")
        print("Structural tells still need a human pass: read references/ai-tells.md")
        return 0

    by_file: dict[str, list[dict]] = {}
    for h in all_hits:
        by_file.setdefault(h["file"], []).append(h)

    for fname in sorted(by_file):
        print(f"\n## {fname}")
        for h in sorted(by_file[fname], key=lambda x: (-SEV_ORDER[x["severity"]], x["line"])):
            tag = paint(f"[{h['severity']:>4}]", h["severity"])
            loc = f"{fname}:{h['line']}" if h["line"] else f"{fname} (file)"
            print(f"{tag} {loc} - {h['id']}: {h['message']}")
            if h["excerpt"]:
                print(f"       {h['excerpt']}")

    counts = {s: sum(1 for h in all_hits if h["severity"] == s)
              for s in ("high", "med", "low")}
    print(f"\n{'-' * 68}")
    print(f"{len(all_hits)} tell(s) across {len(by_file)} file(s) "
          f"({scanned} scanned) - "
          f"{counts['high']} high, {counts['med']} med, {counts['low']} low")
    if counts["high"] + counts["med"] > 3:
        print("More than three substantive tells: this is a default, not a design.")
        print("Go back to the plan rather than patching. See references/ai-tells.md §10.")
    else:
        print("Each remaining tell needs a reason tied to the brief, or it goes.")
    print("Structural tells (section order, feature triads, icon keyword-matching)")
    print("are not detectable here - walk references/ai-tells.md by hand.")
    print("Concept-level tells are also invisible to this script: a design that")
    print("implies more scale than the subject has will pass clean. Run the")
    print("scale-honesty test in references/archetypes.md separately.")

    return 1 if counts["high"] else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        # piping into head/less closes stdout early; not an error
        try:
            sys.stdout.close()
        finally:
            sys.exit(0)

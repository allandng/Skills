#!/usr/bin/env python3
"""Lint a SWE Plan document bundle.

Checks the things that silently rot: requirement IDs referenced but never
defined, product requirements nobody is building, system requirements that
trace to nothing, broken relative links, missing status headers, and Mermaid
diagrams that will not render.

Also checks rigor, the parts a plan can skip and still look finished: a
non-functional target with no number, a requirement with no acceptance
criterion, an assumption with no stated consequence, a question nobody owns, a
phase with no check or no undo, and a decision record with no rejected option.

Python standard library only. Exit code is 1 when there are errors, so this
drops into CI unchanged.

Usage:
    python check_docs.py docs/
    python check_docs.py docs/ --json
    python check_docs.py docs/ --strict     # warnings also fail
    python check_docs.py docs/ --no-rigor   # structure only, for a bundle written before the rigor rules
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ID_RE = re.compile(r"\b((?:PR|SR|NFR|UC|ADR|E|A|Q|R|T|P)-\d{2,4})\b")

# An ID counts as DEFINED when it leads a table row, leads a heading, or leads
# a bolded line. Everything else is a reference.
DEF_PATTERNS = [
    re.compile(r"^\s*\|\s*\*{0,2}((?:PR|SR|NFR|UC|ADR|E|A|Q|R|T|P)-\d{2,4})\*{0,2}\s*\|"),
    re.compile(r"^\s*#{1,6}\s+\*{0,2}((?:PR|SR|NFR|UC|ADR|E|A|Q|R|T|P)-\d{2,4})\b"),
    re.compile(r"^\s*\*\*((?:PR|SR|NFR|UC|ADR|E|A|Q|R|T|P)-\d{2,4})\*\*\s*[-–:]"),
    re.compile(r"^\s*-\s+\*\*((?:PR|SR|NFR|UC|ADR|E|A|Q|R|T|P)-\d{2,4})\*\*"),
]

MERMAID_TYPES = {
    "flowchart", "graph", "sequenceDiagram", "erDiagram", "stateDiagram",
    "stateDiagram-v2", "classDiagram", "journey", "gantt", "pie", "mindmap",
    "timeline", "gitGraph", "quadrantChart", "requirementDiagram", "C4Context",
    "C4Container", "C4Component", "C4Dynamic", "block-beta", "sankey-beta",
    "xychart-beta", "packet-beta", "architecture-beta",
}

BLOCK_OPENERS = re.compile(r"^\s*(subgraph|alt|opt|loop|par|critical|rect|box)\b")
MULTILINE_NOTE = re.compile(r"^\s*note\s+(right|left|over)\b(?![^\n]*:)")
BLOCK_CLOSER = re.compile(r"^\s*end(\s+note)?\s*;?\s*$")
ER_CARDINALITY = re.compile(r"(\|\||\|o|o\||\}o|o\{|\}\||\|\{)\s*\.{2}|(\|\||\|o|o\||\}o|o\{|\}\||\|\{)\s*-{2}")
RESERVED_END_NODE = re.compile(r"^\s*end\s*[\[\(\{]")
BRACKET_LABEL = re.compile(r"\[([^\[\]\n]*)\]")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


class Report:
    def __init__(self) -> None:
        self.items: list[dict] = []

    def add(self, level: str, path: str, line: int | None, message: str) -> None:
        self.items.append({"level": level, "file": path, "line": line, "message": message})

    def error(self, path: str, line, message: str) -> None:
        self.add("error", path, line, message)

    def warn(self, path: str, line, message: str) -> None:
        self.add("warning", path, line, message)

    @property
    def errors(self) -> list[dict]:
        return [i for i in self.items if i["level"] == "error"]

    @property
    def warnings(self) -> list[dict]:
        return [i for i in self.items if i["level"] == "warning"]


# --------------------------------------------------------------------------- #

def strip_code_blocks(text: str) -> str:
    """Blank out fenced code so IDs inside examples do not count as real."""
    out, in_fence, fence = [], False, ""
    for line in text.split("\n"):
        s = line.lstrip()
        if not in_fence and s.startswith("```"):
            in_fence, fence = True, s[: len(s) - len(s.lstrip("`"))]
            out.append("")
            continue
        if in_fence and s.startswith(fence) and s.strip("`") == "":
            in_fence = False
            out.append("")
            continue
        out.append("" if in_fence else line)
    return "\n".join(out)


def extract_mermaid(text: str) -> list[tuple[int, list[str]]]:
    """Return [(start_line_number, block_lines)] for each mermaid fence."""
    blocks, cur, start = [], None, 0
    for n, line in enumerate(text.split("\n"), 1):
        s = line.strip()
        if cur is None and re.match(r"^`{3,}mermaid\s*$", s):
            cur, start = [], n
        elif cur is not None and re.match(r"^`{3,}\s*$", s):
            blocks.append((start, cur))
            cur = None
        elif cur is not None:
            cur.append(line)
    return blocks


def check_mermaid(path: str, text: str, rep: Report) -> None:
    for start, lines in extract_mermaid(text):
        body = [l for l in lines if l.strip() and not l.strip().startswith("%%")]
        if not body:
            rep.warn(path, start, "empty mermaid block")
            continue

        head = body[0].strip().split()[0].rstrip(";")
        if head not in MERMAID_TYPES:
            rep.error(path, start + 1, f"unknown mermaid diagram type '{head}'")
            continue

        is_flow = head in {"flowchart", "graph"}
        is_er = head == "erDiagram"

        opens = closes = 0
        for offset, raw in enumerate(lines, start + 1):
            s = raw.strip()
            if not s or s.startswith("%%"):
                continue

            if BLOCK_OPENERS.match(s) or MULTILINE_NOTE.match(s):
                opens += 1
            elif BLOCK_CLOSER.match(s):
                closes += 1

            if "\\n" in s:
                rep.warn(path, offset, "literal \\n in a label renders as characters - use <br/>")

            if is_flow and RESERVED_END_NODE.match(s):
                rep.error(path, offset, "'end' is reserved in flowcharts - rename the node or quote it")

            if is_flow:
                for label in BRACKET_LABEL.findall(s):
                    inner = label.strip()
                    if inner.startswith("(") and inner.endswith(")"):
                        inner = inner[1:-1].strip()  # cylinder shape [(...)]
                    if not inner or (inner.startswith('"') and inner.endswith('"')):
                        continue
                    if any(c in inner for c in "()[]{}:;"):
                        rep.warn(
                            path, offset,
                            f'label with punctuation should be quoted: ["{inner}"]',
                        )

            if is_er and ER_CARDINALITY.search(s) and ":" not in s:
                rep.error(path, offset, "ERD relationship needs a label after ':' (use \"\" if empty)")

        if opens != closes:
            diff = opens - closes
            word = "unclosed" if diff > 0 else "extra 'end'"
            rep.error(path, start, f"mermaid block has {abs(diff)} {word} block(s)")


def check_header(path: str, text: str, rep: Report) -> None:
    head = "\n".join(text.split("\n")[:14])
    if "**Status:**" not in head:
        rep.error(path, 1, "missing status header - add the blockquote header block")
        return
    if "**Updated:**" not in head:
        rep.warn(path, 1, "header has no Updated date")
    if "**Owner:**" not in head:
        rep.warn(path, 1, "header has no Owner - 'unassigned' is a valid value")
    m = re.search(r"\*\*Status:\*\*\s*([^\n|]+)", head)
    if m:
        status = m.group(1).strip().split("|")[0].strip()
        known = {"Draft", "In review", "Approved", "Superseded", "Accepted", "Proposed", "Rejected"}
        if not any(k.lower() in status.lower() for k in known):
            rep.warn(path, 1, f"unrecognised status '{status}'")


def check_links(path: Path, root: Path, text: str, rep: Report) -> None:
    rel_path = path.relative_to(root).as_posix()
    for n, line in enumerate(text.split("\n"), 1):
        for target in LINK_RE.findall(line):
            if target.startswith(("http://", "https://", "mailto:", "#", "tel:")):
                continue
            clean = target.split("#")[0]
            if not clean:
                continue
            if not (path.parent / clean).exists():
                rep.error(rel_path, n, f"broken relative link: {target}")


# --------------------------------------------------------------------------- #

def parse_matrix(text: str) -> dict[str, dict[str, set[str]]]:
    """Read the coverage matrix out of 06-traceability.md."""
    matrix: dict[str, dict[str, set[str]]] = {}
    for line in strip_code_blocks(text).split("\n"):
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells:
            continue
        pr = re.fullmatch(r"\*{0,2}(PR-\d{2,4})\*{0,2}", cells[0])
        if not pr:
            continue
        rest = " ".join(cells[1:])
        matrix[pr.group(1)] = {
            "sr": set(re.findall(r"\b(?:SR|NFR)-\d{2,4}\b", rest)),
            "t": set(re.findall(r"\bT-\d{2,4}\b", rest)),
            "p": set(re.findall(r"\bP-\d{2,4}\b", rest)),
        }
    return matrix


def parse_must_requirements(text: str) -> set[str]:
    must = set()
    for line in strip_code_blocks(text).split("\n"):
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells:
            continue
        m = re.fullmatch(r"\*{0,2}(PR-\d{2,4})\*{0,2}", cells[0])
        if m and any(re.fullmatch(r"\*{0,2}Must\*{0,2}", c, re.I) for c in cells[1:]):
            must.add(m.group(1))
    return must


def check_traceability(docs: dict[str, str], defs: dict[str, list], rep: Report) -> None:
    trace_file = next((n for n in docs if "traceability" in n.lower()), None)
    if not trace_file:
        rep.warn("(bundle)", None, "no traceability document found - PR to SR coverage not checked")
        return

    matrix = parse_matrix(docs[trace_file])
    if not matrix:
        rep.error(trace_file, None, "no coverage matrix rows found - expected rows starting with a PR id")
        return

    defined_prs = {i for i in defs if i.startswith("PR-")}
    defined_srs = {i for i in defs if i.startswith("SR-")}

    for pr in sorted(defined_prs):
        if pr not in matrix:
            rep.error(trace_file, None, f"{pr} is defined but missing from the coverage matrix")
        elif not matrix[pr]["sr"]:
            rep.error(trace_file, None, f"{pr} has no system requirement - nobody is building it")

    covered = {sr for row in matrix.values() for sr in row["sr"]}
    for sr in sorted(defined_srs - covered):
        rep.warn(trace_file, None, f"{sr} appears in no matrix row - what product requirement does it serve?")

    prd_file = next((n for n in docs if re.search(r"prd|product", n, re.I)), None)
    if prd_file:
        for pr in sorted(parse_must_requirements(docs[prd_file])):
            if pr in matrix and not matrix[pr]["t"]:
                rep.warn(trace_file, None, f"{pr} is priority Must but has no test in the matrix")

    srd_file = next((n for n in docs if re.search(r"srd|system|design", n, re.I)), None)
    if srd_file:
        for line in strip_code_blocks(docs[srd_file]).split("\n"):
            if not line.strip().startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cells and re.fullmatch(r"\*{0,2}(SR-\d{2,4})\*{0,2}", cells[0]):
                rest = " ".join(cells[1:])
                if not re.search(r"\b(?:PR|NFR)-\d{2,4}\b", rest):
                    rep.warn(srd_file, None, f"{cells[0]} does not name the requirement it satisfies")


# --------------------------------------------------------------------------- #
# Rigor: the parts a plan can leave out and still look finished.

PLACEHOLDER = re.compile(r"^(\.\.\.|…|tbd|todo|n/?a|\?+|-+|<[^>]*>)?$", re.I)
ROW_ID = re.compile(r"\*{0,2}((?:PR|SR|NFR|UC|ADR|E|A|Q|R|T|P)-\d{2,4})\*{0,2}")

# (id prefix, header text to find, level, what is wrong when the cell is empty)
CELL_RULES = [
    ("NFR", "measured", "error", "does not say how it will be measured"),
    ("PR", "acceptance", "error", "has no acceptance criterion - if one cannot be written, make it a Q-##"),
    ("A", "wrong means", "error", "does not say what breaks if it is wrong - without that it is a note, not a tripwire"),
    ("A", "confirm by", "warning", "has no way to confirm it"),
    ("Q", "who answers", "error", "has nobody to answer it"),
    ("Q", "blocks", "error", "does not say what it blocks"),
    ("R", "early warning", "warning", "has no early warning sign - it will be found by a user"),
    ("R", "mitigation", "warning", "has no mitigation"),
    ("T", "traces to", "warning", "does not trace to a requirement"),
]
PHASE_FIELDS = [
    ("Verified by", "error", "has no check - a phase that cannot be verified cannot be called done"),
    ("Reverts by", "error", "has no undo"),
    ("Done when", "warning", "has no objective completion check"),
]


def tables(text: str):
    """Yield (lowercased header cells, rows, line number of the first row) per table."""
    lines = strip_code_blocks(text).split("\n")
    i = 0
    while i < len(lines):
        if not lines[i].strip().startswith("|"):
            i += 1
            continue
        start, block = i, []
        while i < len(lines) and lines[i].strip().startswith("|"):
            block.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
            i += 1
        if len(block) >= 3 and all(re.fullmatch(r":?-{2,}:?", c) for c in block[1] if c):
            yield [c.lower().strip("* ") for c in block[0]], block[2:], start + 3


def check_rigor(docs: dict[str, str], rep: Report) -> None:
    for name, raw in docs.items():
        for header, rows, first_line in tables(raw):
            for offset, cells in enumerate(rows):
                ident = ROW_ID.fullmatch(cells[0]) if cells else None
                if not ident:
                    continue
                prefix = ident.group(1).split("-")[0]
                line = first_line + offset
                for rule_prefix, column, level, message in CELL_RULES:
                    if prefix != rule_prefix:
                        continue
                    index = next((i for i, h in enumerate(header) if column in h), None)
                    if index is None or index >= len(cells):
                        continue
                    if PLACEHOLDER.match(cells[index]):
                        rep.add(level, name, line, f"{ident.group(1)} {message}")
                if prefix == "NFR":
                    index = next((i for i, h in enumerate(header) if h.startswith("target")), None)
                    if index is not None and index < len(cells) and not re.search(r"\d", cells[index]):
                        rep.error(name, line, f"{ident.group(1)} target has no number - "
                                              "\"fast\" is a feeling, \"p95 under 300ms\" is a requirement")

        prose = strip_code_blocks(raw)

        # Phases written as "### P-01 - name" followed by a two-column table.
        for match in re.finditer(r"^#{2,6}\s+\*{0,2}(P-\d{2,4})\b.*$", prose, re.M):
            rest = prose[match.end():]
            end = re.search(r"^#{1,6}\s", rest, re.M)
            block = rest[: end.start()] if end else rest
            line = prose[: match.start()].count("\n") + 1
            for label, level, message in PHASE_FIELDS:
                found = re.search(rf"^\|\s*\*{{0,2}}{label}\*{{0,2}}\s*\|\s*(.*?)\s*\|\s*$", block, re.M | re.I)
                if not found or PLACEHOLDER.match(found.group(1).strip()):
                    rep.add(level, name, line, f"{match.group(1)} {message}")

        # Decision records.
        if re.search(r"(^|/)adr/\d", name, re.I):
            options = re.search(r"^##\s+Options considered\s*$(.*?)(?=^##\s|\Z)", prose, re.S | re.M | re.I)
            count = len(re.findall(r"^###\s", options.group(1), re.M)) if options else 0
            if count < 2:
                rep.error(name, None, f"records {count} option(s) - a decision with no alternative is a press release")
            elif not re.search(r"rejected because\W+\w", options.group(1), re.I):
                rep.error(name, None, "no option says why it was rejected - the rejected half is the useful half")
            revisit = re.search(r"^##\s+Revisit when\s*$(.*?)(?=^##\s|\Z)", prose, re.S | re.M | re.I)
            if not revisit or PLACEHOLDER.match(revisit.group(1).strip()):
                rep.warn(name, None, "no \"Revisit when\" condition - nothing says when this decision should be reopened")


# --------------------------------------------------------------------------- #

def run(root: Path, rep: Report, rigor: bool = True) -> dict:
    md_files = sorted(p for p in root.rglob("*.md") if ".git" not in p.parts)
    if not md_files:
        rep.error(str(root), None, "no markdown files found")
        return {}

    docs: dict[str, str] = {}
    defs: dict[str, list] = defaultdict(list)
    refs: dict[str, list] = defaultdict(list)

    for path in md_files:
        name = path.relative_to(root).as_posix()
        try:
            raw = path.read_text(encoding="utf-8", errors="replace")
        except Exception as exc:  # noqa: BLE001
            rep.error(name, None, f"unreadable: {exc.__class__.__name__}")
            continue
        docs[name] = raw

        check_header(name, raw, rep)
        check_mermaid(name, raw, rep)
        check_links(path, root, raw, rep)

        # The traceability document maps requirements; it does not define them.
        # Assumptions, questions, tests, phases and risks may be defined anywhere.
        maps_only = "traceability" in name.lower()

        prose = strip_code_blocks(raw)
        for n, line in enumerate(prose.split("\n"), 1):
            hit = None
            for pattern in DEF_PATTERNS:
                m = pattern.match(line)
                if m:
                    hit = m.group(1)
                    break
            if hit and maps_only and hit.split("-")[0] in {"PR", "SR", "NFR", "UC", "E"}:
                hit = None
            if hit:
                defs[hit].append((name, n))
            for ident in ID_RE.findall(line):
                if ident != hit:
                    refs[ident].append((name, n))

    for ident in sorted(set(refs) - set(defs)):
        where = refs[ident][0]
        rep.error(where[0], where[1], f"{ident} is referenced but never defined")

    for ident, places in sorted(defs.items()):
        if len(places) > 1:
            spots = ", ".join(f"{f}:{l}" for f, l in places)
            rep.warn(places[0][0], places[0][1], f"{ident} defined more than once ({spots})")

    check_traceability(docs, defs, rep)
    if rigor:
        check_rigor(docs, rep)

    return {
        "files": len(docs),
        "ids_defined": {k: len(v) for k, v in sorted(defs.items())},
        "ids_referenced_only": sorted(set(refs) - set(defs)),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Lint a SWE Plan document bundle.")
    ap.add_argument("path", help="the docs/ directory")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--strict", action="store_true", help="warnings fail too")
    ap.add_argument("--no-rigor", action="store_true",
                    help="skip the rigor checks (numbers, acceptance criteria, owners, phase checks, rejected options)")
    args = ap.parse_args()

    root = Path(args.path).expanduser()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2

    rep = Report()
    summary = run(root, rep, rigor=not args.no_rigor)

    if args.json:
        print(json.dumps({"summary": summary, "issues": rep.items}, indent=2))
    else:
        by_file: dict[str, list[dict]] = defaultdict(list)
        for item in rep.items:
            by_file[item["file"]].append(item)
        for fname in sorted(by_file):
            print(f"\n{fname}")
            for item in sorted(by_file[fname], key=lambda i: (i["line"] or 0)):
                loc = f":{item['line']}" if item["line"] else ""
                mark = "ERROR  " if item["level"] == "error" else "warning"
                print(f"  {mark} {fname}{loc}  {item['message']}")
        print(
            f"\n{summary.get('files', 0)} files, "
            f"{len(summary.get('ids_defined', {}))} ids defined, "
            f"{len(rep.errors)} errors, {len(rep.warnings)} warnings"
        )
        if not rep.items:
            print("clean")

    if rep.errors:
        return 1
    if args.strict and rep.warnings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

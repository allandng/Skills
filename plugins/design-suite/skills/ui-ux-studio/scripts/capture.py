#!/usr/bin/env python3
"""Capture a page at the widths the proof ladder asks for.

Rung 1 of references/proof.md is "rendered": look at the real thing at 375,
768 and 1280 wide. This takes those pictures with any installed Chrome,
Chromium or Edge, so the check is one command instead of a claim.

    python3 capture.py index.html
    python3 capture.py http://localhost:3000/projects --name projects
    python3 capture.py index.html --query state=empty --name projects-empty
    python3 capture.py index.html --dark --widths 375,1280 --height 1600

Writes <out>/<name>-<width>[-dark].png and prints each path. Use --query to
capture one state at a time when the page switches state from the URL; the
files it writes are valid evidence in a states.json manifest.

It captures the viewport, not the full scroll height: raise --height for a
long page. It cannot press keys or hover. If no browser is found it says so
and exits 2: open the page by hand, or say in your reply that it was not
rendered. Standard library only. Python 3.11+.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

NAMES = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome",
         "microsoft-edge", "msedge", "brave-browser"]
PATHS = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]


def find_browser() -> str | None:
    override = os.environ.get("CHROME") or os.environ.get("CHROME_PATH")
    if override and Path(override).exists():
        return override
    for name in NAMES:
        found = shutil.which(name)
        if found:
            return found
    return next((p for p in PATHS if Path(p).exists()), None)


def to_url(target: str, query: str | None) -> str:
    if "://" not in target:
        path = Path(target).expanduser().resolve()
        if not path.exists():
            raise SystemExit(f"not found: {target}")
        target = path.as_uri()
    if query:
        parts = urlsplit(target)
        joined = f"{parts.query}&{query}" if parts.query else query
        target = urlunsplit((parts.scheme, parts.netloc, parts.path, joined, parts.fragment))
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("target", help="an HTML file or a URL")
    parser.add_argument("--out", type=Path, default=Path("screenshots"))
    parser.add_argument("--name", help="file name stem (default: from the target)")
    parser.add_argument("--widths", default="375,768,1280")
    parser.add_argument("--height", type=int, default=900)
    parser.add_argument("--query", help="query string to add, such as state=empty")
    parser.add_argument("--dark", action="store_true", help="capture with prefers-color-scheme: dark")
    parser.add_argument("--wait", type=int, default=1500, help="milliseconds to let the page settle")
    args = parser.parse_args()

    browser = find_browser()
    if not browser:
        print("No Chrome, Chromium or Edge found. Set CHROME to a browser path, open the page by hand, "
              "or state in the reply that the work was not rendered.", file=sys.stderr)
        return 2

    url = to_url(args.target, args.query)
    stem = args.name or (Path(urlsplit(url).path).stem or "page")
    args.out.mkdir(parents=True, exist_ok=True)
    try:
        widths = [int(w) for w in args.widths.split(",") if w.strip()]
    except ValueError:
        raise SystemExit("--widths takes comma-separated numbers, such as 375,768,1280")

    failed = 0
    with tempfile.TemporaryDirectory() as profile:
        for width in widths:
            shot = (args.out / f"{stem}-{width}{'-dark' if args.dark else ''}.png").resolve()
            command = [
                browser, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                f"--user-data-dir={profile}", f"--window-size={width},{args.height}",
                f"--virtual-time-budget={args.wait}", f"--screenshot={shot}",
            ]
            if args.dark:
                command.append("--blink-settings=preferredColorScheme=0")
            if hasattr(os, "geteuid") and os.geteuid() == 0:
                command.append("--no-sandbox")  # Chrome refuses to start sandboxed as root
            command.append(url)
            try:
                result = subprocess.run(command, capture_output=True, text=True, timeout=90)
            except subprocess.TimeoutExpired:
                print(f"FAIL  {width}: the browser did not finish within 90s")
                failed += 1
                continue
            if shot.is_file() and shot.stat().st_size > 0:
                print(f"ok    {os.path.relpath(shot)}  ({width}x{args.height}{', dark' if args.dark else ''})")
            else:
                tail = (result.stderr or result.stdout).strip().splitlines()[-1:] or ["no output"]
                print(f"FAIL  {width}: no image written. {tail[0][:200]}")
                failed += 1

    if not failed:
        print("Captured. Now look at each one: a file on disk is not a check until someone has seen it.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

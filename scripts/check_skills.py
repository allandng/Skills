#!/usr/bin/env python3
"""Check every skill in this marketplace for the mistakes that ship silently.

    python3 scripts/check_skills.py

For each plugins/*/skills/*/SKILL.md: the frontmatter name matches the folder,
the description fits the 1024-character limit, and every `references/...`,
`playbooks/...`, `scripts/...` or `assets/...` path the skill's own Markdown
names exists in that skill. Also checks that files meant to be identical across
skills still are, and that the marketplace lists every plugin folder.

Standard library only. Python 3.11+.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
# Generated from upstream and verified by fork_pstack.py --check.
GENERATED = {"askillissue"}
PATH = re.compile(r"`((?:references|playbooks|scripts|assets)/[A-Za-z0-9_./-]+\.[a-z]+)`")
# Files that must stay byte-identical wherever they appear.
TWINS = [
    ("plugins/design-suite/skills/ui-ux-studio/references/app-taxonomy.md",
     "plugins/design-suite/skills/design-dna/references/app-taxonomy.md"),
    ("plugins/design-suite/skills/ui-ux-studio/scripts/contrast.py",
     "plugins/design-suite/skills/design-dna/scripts/contrast.py"),
]
# A shared file may name files that live in the other skill.
SHARED = {"app-taxonomy.md"}


def main() -> int:
    failures: list[str] = []
    skills = 0
    for skill_md in sorted(REPO.glob("plugins/*/skills/*/SKILL.md")):
        skill = skill_md.parent
        plugin = skill.parents[1].name
        label = f"{plugin}/{skill.name}"
        text = skill_md.read_text(encoding="utf-8")
        front = re.match(r"---\n(.*?)\n---", text, re.S)
        if not front:
            failures.append(f"{label}: no frontmatter")
            continue
        skills += 1
        name = re.search(r"^name:\s*(.+)$", front.group(1), re.M)
        desc = re.search(r"^description:\s*(.+?)(?=^\S|\Z)", front.group(1), re.M | re.S)
        if not name or name.group(1).strip().strip("\"'") != skill.name:
            failures.append(f"{label}: frontmatter name does not match the folder")
        if not desc:
            failures.append(f"{label}: no description")
        elif len(" ".join(desc.group(1).split())) > 1024:
            failures.append(f"{label}: description is {len(' '.join(desc.group(1).split()))} characters, limit 1024")
        if plugin in GENERATED:
            continue
        for md in skill.rglob("*.md"):
            if md.name in SHARED:
                continue
            for rel in set(PATH.findall(md.read_text(encoding="utf-8"))):
                if not (skill / rel).exists():
                    failures.append(f"{label}: {md.relative_to(skill)} names {rel}, which does not exist")

    for a, b in TWINS:
        pa, pb = REPO / a, REPO / b
        if not (pa.is_file() and pb.is_file()):
            failures.append(f"missing twin: {a} / {b}")
        elif pa.read_bytes() != pb.read_bytes():
            failures.append(f"these must be identical and are not: {a} / {b}")

    market = json.loads((REPO / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    listed = {p["source"].rstrip("/").split("/")[-1] for p in market["plugins"]}
    on_disk = {p.name for p in (REPO / "plugins").iterdir() if p.is_dir()}
    for missing in sorted(on_disk - listed):
        failures.append(f"plugins/{missing} is not in the marketplace manifest")
    for missing in sorted(listed - on_disk):
        failures.append(f"marketplace lists {missing}, which has no folder")
    for plugin in sorted(on_disk):
        manifest = REPO / "plugins" / plugin / ".claude-plugin/plugin.json"
        try:
            if json.loads(manifest.read_text(encoding="utf-8")).get("name") != plugin:
                failures.append(f"plugins/{plugin}: manifest name does not match the folder")
        except (OSError, json.JSONDecodeError) as error:
            failures.append(f"plugins/{plugin}: manifest unreadable: {error}")

    for failure in failures:
        print(f"FAIL  {failure}")
    if not failures:
        print(f"ok    {skills} skills in {len(on_disk)} plugins")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

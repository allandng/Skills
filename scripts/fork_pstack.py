#!/usr/bin/env python3
"""Regenerate plugins/askillissue from upstream pstack.

askillissue is a fork of pstack (https://github.com/cursor/plugins/tree/main/pstack,
MIT, (c) Lauren Tan). This script is the fork: it copies pstack's generated
Claude Code tree, applies a fixed set of renames, and writes the fork's own
README, NOTICE and manifest. Nothing under plugins/askillissue is edited by
hand, so pulling a newer pstack is one command:

    git clone --depth 1 https://github.com/cursor/plugins /tmp/cursor-plugins
    python3 scripts/fork_pstack.py --upstream /tmp/cursor-plugins
    python3 scripts/fork_pstack.py --upstream /tmp/cursor-plugins --check

`--check` regenerates into a temp folder and fails if the committed tree
differs, or if any link, skill route or frontmatter name is broken.

Standard library only. Python 3.11+.
"""

from __future__ import annotations

import argparse
import filecmp
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
UPSTREAM_TREE = Path("harness/pstack/claude-code")
UPSTREAM_URL = "https://github.com/cursor/plugins"

# Paths (relative to the upstream tree) that the fork leaves out.
SKIP_PREFIXES = (
    "README.md",  # rewritten below: upstream's is a first-person author page
    "plugin.json",  # this marketplace keeps one manifest, in .claude-plugin/
    ".claude-plugin/plugin.json",
    "docs/guide/images/",  # illustrations of the upstream author
    "skills/statechart/scripts/test/",  # 3.8 MB corpus for the tool's own tests
)

# Strings that must survive the renames untouched.
PROTECT = re.compile(
    r"https://github\.com/cursor/plugins[^\s)\]`\"'>]*"
    r"|https://x\.com/poteto"
    r"|https://cursor\.com[^\s)\]`\"'>]*"
)

# The one content patch: the router sends design work to this marketplace's design-suite.
ROUTER_ANCHOR = "- Shipping UI / IDE / CLI"
ROUTER_PATCH = (
    "- Designing UI or UX (a screen, a flow, an app shell, a redesign, a design audit) → the "
    "**ui-ux-studio** skill from the `design-suite` plugin, which has its own playbooks and proof "
    "steps. Reverse-engineering how an existing product is designed or organized → the "
    "**design-dna** skill from the same plugin. If `design-suite` is not installed, say so and "
    "continue with the Prototype playbook.\n"
)
EXTERNAL_ROUTES = {"ui-ux-studio", "design-dna"}

IMAGE_LINE = re.compile(r"^!\[[^\]]*\]\((?:\./)?images/[^)]+\)\s*\n\n?", re.M)


def renames(plugin: str, handle: str) -> list[tuple[re.Pattern[str], str]]:
    """Ordered. Each pattern refuses to match inside a longer word."""
    cap = handle.capitalize()
    pairs = [
        (r"poteto-mode", f"{handle}-mode"),
        (r"poteto-agent", f"{handle}-agent"),
        (r"poteto-help", f"{plugin}-help"),
        (r"setup-pstack", f"setup-{plugin}"),
        (r"Poteto mode", f"{cap} mode"),
        (r"Poteto subagent", f"{cap} subagent"),
        (r"poteto's", f"{cap}'s"),
        (r"pstack", plugin),
        (r"[Pp]oteto", cap),
    ]
    return [(re.compile(rf"(?<![A-Za-z]){p}(?![A-Za-z])"), r) for p, r in pairs]


def rewrite(text: str, rules: list[tuple[re.Pattern[str], str]]) -> str:
    kept: list[str] = []

    def stash(m: re.Match[str]) -> str:
        kept.append(m.group(0))
        return f"\x00{len(kept) - 1}\x00"

    text = PROTECT.sub(stash, text)
    for pattern, replacement in rules:
        text = pattern.sub(replacement, text)
    return re.sub(r"\x00(\d+)\x00", lambda m: kept[int(m.group(1))], text)


def rename_path(rel: str, rules: list[tuple[re.Pattern[str], str]]) -> str:
    for pattern, replacement in rules:
        rel = pattern.sub(replacement, rel)
    return rel


def upstream_commit(upstream: Path) -> dict[str, str]:
    def git(*args: str) -> str:
        return subprocess.run(
            ["git", "-C", str(upstream), *args], capture_output=True, text=True, check=True
        ).stdout.strip()

    try:
        return {"commit": git("rev-parse", "HEAD"), "date": git("log", "-1", "--format=%cI")}
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {"commit": "unknown", "date": "unknown"}


def details(readme: str, summary_contains: str) -> str:
    """Body of the <details> block whose <summary> contains the given text."""
    for m in re.finditer(r"<details>\s*<summary>(.*?)</summary>(.*?)</details>", readme, re.S):
        if summary_contains in m.group(1):
            return m.group(2).strip()
    raise SystemExit(f"upstream README no longer has a '{summary_contains}' block")


def build_readme(src: Path, rules, plugin: str, handle: str, marketplace: str, info: dict) -> str:
    upstream_readme = rewrite((src / "README.md").read_text(encoding="utf-8"), rules)
    playbooks = details(upstream_readme, "playbooks")
    skills = details(upstream_readme, "all skills")
    examples = details(upstream_readme, "examples")
    principles = details(upstream_readme, "principles")
    mode = f"{handle}-mode"
    return f"""# {plugin}

Engineering-rigor skills for agentic coding: one router skill, a set of playbooks, single-rule
principles, and workflow skills for understanding, designing, building, reviewing and shipping code.

```bash
/plugin install {plugin}@{marketplace}
```

> **This is a fork of [pstack]({UPSTREAM_URL}/tree/main/pstack) by Lauren Tan (poteto), MIT.**
> Every skill, playbook and principle here is her work. The fork renames `pstack` to `{plugin}` and
> `poteto-mode` to `{mode}` so the stack can be tuned without drifting from a name that isn't mine.
> [NOTICE.md](NOTICE.md) lists exactly what changed. Generated from upstream commit
> `{info["commit"][:12]}` by [`scripts/fork_pstack.py`](../../scripts/fork_pstack.py). Do not edit
> this folder by hand.

## Start here

1. Run `/{plugin}:setup-{plugin}` once. It asks for a reasoning budget and writes your per-role model
   choices to `~/.claude/rules/{plugin}-models.md`.
2. Start any task that needs rigor with `/{plugin}:{mode}`. It restates the goal, matches the task to
   a playbook, copies that playbook's steps into the todo list, and runs the other skills as the
   steps need them.
3. Unsure which skill fits? Ask `/{plugin}:{plugin}-help`.

The skills are written with Cursor's tool names. [`docs/harness/claude-code.md`](docs/harness/claude-code.md)
maps each one to Claude Code, and every skill that needs it tells the agent to read it first. Steps
that need a Cursor-only feature (Bugbot, Cursor Automations, cloud agents) are skipped with a
one-line note.

Most skills set `disable-model-invocation: true`: they run when you type them or when `{mode}`
routes to them, not on their own. That keeps 58 skills from competing for every message.

## The playbooks `/{plugin}:{mode}` routes to

{playbooks}

## Skills

`{mode}` runs most of these for you. The table is for when you want one directly.

{skills}

## Principles

One rule each. `{mode}` indexes them inline and reads the leaf file for any it applies.

{principles}

## Example prompts

{examples}

## Not shipped here

`{mode}` names a few things neither pstack nor this fork bundles: `/deslop`, `control-cli` and
`control-ui` ship in Cursor's `cursor-team-kit` plugin, and `/create-skill` is a Cursor built-in.
The adapter tells the agent to skip or substitute them.

## Design work

pstack has no UI or UX design skills. `{mode}` here carries one added line that routes design work
to the [design-suite](../design-suite) plugin in this marketplace: `ui-ux-studio` for designing and
auditing interfaces, `design-dna` for reverse-engineering existing ones. Both use the same shape as
this stack: playbooks, named principles, and proof before "done".

## The guide

[`docs/guide/`](docs/guide/README.md) is upstream's walkthrough, renamed: setup, the router, how to
understand code before changing it, design, build, verify and ship, overnight runs, the principles,
and making the stack yours.

## Updating from upstream

```bash
git clone --depth 1 {UPSTREAM_URL} /tmp/cursor-plugins
python3 scripts/fork_pstack.py --upstream /tmp/cursor-plugins
python3 scripts/fork_pstack.py --upstream /tmp/cursor-plugins --check
```

## License

MIT. [LICENSE](LICENSE) is upstream's, unchanged.
"""


def build_notice(plugin: str, handle: str, info: dict) -> str:
    return f"""# Notice

`{plugin}` is a fork of **pstack** by Lauren Tan (poteto).

- Source: {UPSTREAM_URL}/tree/main/pstack (the generated Claude Code tree at
  `harness/pstack/claude-code`)
- Upstream commit: `{info["commit"]}` ({info["date"]})
- License: MIT, Copyright (c) 2026 Lauren Tan. See [LICENSE](LICENSE), reproduced unchanged.

## What the fork changes

All changes are made by `scripts/fork_pstack.py` in this repository. None are made by hand.

| Change | Detail |
|---|---|
| Plugin name | `pstack` to `{plugin}`, including the model rule file (`{plugin}-models.md`) |
| Router skill | `poteto-mode` to `{handle}-mode`, and "poteto" to "{handle.capitalize()}" in its text |
| Delegate agent | `poteto-agent` to `{handle}-agent`; its `model:` line is `opus` instead of a Cursor slug |
| Help and setup skills | `poteto-help` to `{plugin}-help`, `setup-pstack` to `setup-{plugin}` |
| Router | One added line in `{handle}-mode`: UI and UX design work routes to `ui-ux-studio` and `design-dna` in this marketplace's `design-suite` plugin |
| README | Rewritten. Upstream's is a first-person page by its author. The skill, playbook, principle and example tables are hers |
| Guide illustrations | Removed (`docs/guide/images/`). They depict the upstream author |
| `statechart` test corpus | Omitted (`skills/statechart/scripts/test/`, 3.8 MB). The tool itself is complete |
| Manifest | One `.claude-plugin/plugin.json`, in this marketplace's format |

Links to `{UPSTREAM_URL}` are left pointing upstream.

The rules, wording and structure of every skill are otherwise upstream's. If something here is
good, credit her. If the fork broke it, that is on this repository.
"""


def build_manifest(plugin: str) -> str:
    manifest = {
        "name": plugin,
        "displayName": "A Skill Issue",
        "description": (
            "Engineering-rigor skills for agentic coding: a router with 22 playbooks, 24 "
            "principles, and workflow skills for understanding, design, review and shipping. "
            "A fork of pstack by Lauren Tan."
        ),
        "author": {"name": "Allan", "url": "https://github.com/allandng"},
        "repository": "https://github.com/allandng/askillissue",
        "homepage": f"https://github.com/allandng/askillissue/tree/main/plugins/{plugin}",
        "license": "MIT",
        "keywords": ["workflow", "principles", "subagents", "code-review", "verification", "pstack"],
    }
    return json.dumps(manifest, indent=2) + "\n"


def generate(upstream: Path, out: Path, plugin: str, handle: str, marketplace: str) -> None:
    src = upstream / UPSTREAM_TREE
    if not (src / "skills").is_dir():
        raise SystemExit(f"{src} has no skills/ folder. Is --upstream a cursor/plugins checkout?")
    rules = renames(plugin, handle)
    info = upstream_commit(upstream)

    if out.exists():
        shutil.rmtree(out)
    for path in sorted(p for p in src.rglob("*") if p.is_file()):
        rel = path.relative_to(src).as_posix()
        if rel.startswith(SKIP_PREFIXES) or "/node_modules/" in rel or rel.endswith(".DS_Store"):
            continue
        dest = out / rename_path(rel, rules)
        dest.parent.mkdir(parents=True, exist_ok=True)
        data = path.read_bytes()
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            dest.write_bytes(data)
        else:
            if rel != "LICENSE":
                text = rewrite(text, rules)
            if rel.startswith("docs/guide/"):
                text = IMAGE_LINE.sub("", text)
            if rel == "skills/poteto-mode/SKILL.md":
                if ROUTER_ANCHOR not in text:
                    raise SystemExit("upstream router no longer has the line the design route follows")
                head, tail = text.split(ROUTER_ANCHOR, 1)
                text = head + ROUTER_PATCH + ROUTER_ANCHOR + tail
            if rel.startswith("agents/"):
                text = re.sub(r"^model: claude-opus[^\n]*$", "model: opus", text, flags=re.M)
            dest.write_text(text, encoding="utf-8")
        shutil.copymode(path, dest)

    (out / "README.md").write_text(
        build_readme(src, rules, plugin, handle, marketplace, info), encoding="utf-8"
    )
    (out / "NOTICE.md").write_text(build_notice(plugin, handle, info), encoding="utf-8")
    manifest = out / ".claude-plugin" / "plugin.json"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(build_manifest(plugin), encoding="utf-8")


# ---------------------------------------------------------------- verification

LINK = re.compile(r"\]\(([^)\s]+)\)")
FRONTMATTER_NAME = re.compile(r"^---\n.*?^name:\s*(\S+)\s*$.*?^---", re.S | re.M)
ROUTE = re.compile(r"the \*\*([a-z0-9-]+)\*\* (?:principle )?skill|`/([a-z0-9-]+)`")


def problems(tree: Path) -> dict[str, set[str]]:
    """Broken things in a plugin tree, keyed by kind."""
    found: dict[str, set[str]] = {"name": set(), "link": set(), "route": set()}
    skills = {p.parent.name for p in (tree / "skills").glob("*/SKILL.md")}
    for skill in skills:
        text = (tree / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
        m = FRONTMATTER_NAME.search(text)
        if not m or m.group(1).strip("\"'") != skill:
            found["name"].add(skill)
    for md in tree.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        rel = md.relative_to(tree).as_posix()
        for target in LINK.findall(text):
            if re.match(r"[a-z]+:|#|<", target):
                continue
            path = (md.parent / target.split("#")[0]).resolve()
            if not path.exists() and tree.resolve() in path.parents:
                found["link"].add(f"{rel} -> {target}")
        for bold, slash in ROUTE.findall(text):
            name = bold or slash
            if name not in skills and f"principle-{name}" not in skills:
                found["route"].add(name)
    return found


def check(upstream: Path, out: Path, plugin: str, handle: str, marketplace: str) -> int:
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        fresh = Path(tmp) / plugin
        generate(upstream, fresh, plugin, handle, marketplace)

        def differing(cmp: filecmp.dircmp, prefix: str = "") -> list[str]:
            names = [prefix + n for n in cmp.left_only + cmp.right_only + cmp.diff_files]
            for sub, child in cmp.subdirs.items():
                names += differing(child, f"{prefix}{sub}/")
            return names

        stale = differing(filecmp.dircmp(fresh, out)) if out.exists() else ["(missing)"]
        if stale:
            failures.append(f"committed tree differs from a fresh fork in {len(stale)} path(s): "
                            + ", ".join(stale[:8]))

    rules = renames(plugin, handle)
    ours = problems(out)
    theirs = problems(upstream / UPSTREAM_TREE)
    if ours["name"]:
        failures.append("frontmatter name does not match its folder: " + ", ".join(sorted(ours["name"])))
    # Upstream names a few skills it does not ship (deslop, control-ui, ...). Those are
    # expected. Anything the fork fails to resolve beyond upstream's own set is a fork bug.
    expected_routes = {rename_path(r, rules) for r in theirs["route"]}
    new_routes = ours["route"] - expected_routes - EXTERNAL_ROUTES
    if new_routes:
        failures.append("skill routes the fork broke: " + ", ".join(sorted(new_routes)))
    # README is rewritten and images are dropped, so compare links outside those.
    expected_links = {rename_path(l, rules) for l in theirs["link"]}
    new_links = {l for l in ours["link"] if l not in expected_links}
    if new_links:
        failures.append("relative links the fork broke: " + "; ".join(sorted(new_links)[:10]))

    leftovers = []
    for path in out.rglob("*"):
        if not path.is_file() or path.name in {"NOTICE.md", "LICENSE", "README.md", "plugin.json"}:
            continue
        try:
            text = PROTECT.sub("", path.read_text(encoding="utf-8"))
        except UnicodeDecodeError:
            continue
        if re.search(r"(?<![A-Za-z])(pstack|[Pp]oteto)(?![A-Za-z])", text):
            leftovers.append(path.relative_to(out).as_posix())
    if leftovers:
        failures.append("upstream names left in: " + ", ".join(leftovers[:10]))

    skills = len(list((out / "skills").glob("*/SKILL.md")))
    upstream_skills = len(list((upstream / UPSTREAM_TREE / "skills").glob("*/SKILL.md")))
    if skills != upstream_skills:
        failures.append(f"{skills} skills in the fork, {upstream_skills} upstream")

    for failure in failures:
        print(f"FAIL  {failure}")
    if not failures:
        print(f"ok    {skills} skills, {len(ours['link'])} broken links, "
              f"{len(ours['route'] - EXTERNAL_ROUTES)} routes to skills upstream also does not ship, "
              f"{len(ours['route'] & EXTERNAL_ROUTES)} to design-suite, tree matches a fresh fork")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--upstream", required=True, type=Path, help="a cursor/plugins checkout")
    parser.add_argument("--out", type=Path, help="default: plugins/<plugin>")
    parser.add_argument("--plugin", default="askillissue")
    parser.add_argument("--handle", default="allan", help="the <handle>-mode router name")
    parser.add_argument("--marketplace", default="allan-skills")
    parser.add_argument("--check", action="store_true", help="verify instead of writing")
    args = parser.parse_args()
    out = args.out or REPO / "plugins" / args.plugin
    if args.check:
        return check(args.upstream, out, args.plugin, args.handle, args.marketplace)
    generate(args.upstream, out, args.plugin, args.handle, args.marketplace)
    print(f"wrote {sum(1 for p in out.rglob('*') if p.is_file())} files to {os.path.relpath(out)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# Notice

`askillissue` is a fork of **pstack** by Lauren Tan (poteto).

- Source: https://github.com/cursor/plugins/tree/main/pstack (the generated Claude Code tree at
  `harness/pstack/claude-code`)
- Upstream commit: `dd24b6707267cd89c6621c4efc6fa91a1d0666ec` (2026-11-19T15:53:07-06:00)
- License: MIT, Copyright (c) 2026 Lauren Tan. See [LICENSE](LICENSE), reproduced unchanged.

## What the fork changes

All changes are made by `scripts/fork_pstack.py` in this repository. None are made by hand.

| Change | Detail |
|---|---|
| Plugin name | `pstack` to `askillissue`, including the model rule file (`askillissue-models.md`) |
| Router skill | `poteto-mode` to `allan-mode`, and "poteto" to "Allan" in its text |
| Delegate agent | `poteto-agent` to `allan-agent`; its `model:` line is `opus` instead of a Cursor slug |
| Help and setup skills | `poteto-help` to `askillissue-help`, `setup-pstack` to `setup-askillissue` |
| Router | One added line in `allan-mode`: UI and UX design work routes to `ui-ux-studio` and `design-dna` in this marketplace's `design-suite` plugin |
| README | Rewritten. Upstream's is a first-person page by its author. The skill, playbook, principle and example tables are hers |
| Guide illustrations | Removed (`docs/guide/images/`). They depict the upstream author |
| `statechart` test corpus | Omitted (`skills/statechart/scripts/test/`, 3.8 MB). The tool itself is complete |
| Manifest | One `.claude-plugin/plugin.json`, in this marketplace's format |

Links to `https://github.com/cursor/plugins` are left pointing upstream.

The rules, wording and structure of every skill are otherwise upstream's. If something here is
good, credit her. If the fork broke it, that is on this repository.

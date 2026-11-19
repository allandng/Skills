### Audit

**You own the diagnosis. Understand, then judge. This playbook adds nothing. It elevates what exists.**

1. Read what exists: tokens, components, routes, flows. Walk every screen at 375, tablet and desktop as a user before opening the code.
2. Classify the archetype and, for an app, name each screen as `family:type` (`references/app-taxonomy.md`). Archetype misfit is the finding that outranks all others.
3. Review every dimension in `references/modes.md`, audit Step 2.
4. Run the scripts: `contrast.py`, `ai_tells.py`, `craft_check.py`. For an app, fill `states.json` from what exists and run `state_coverage.py`: the failures are findings.
5. Apply the reduction filter.
6. Write the three-phase plan. Every item: file and location, the change, the structural reason.
7. Deduplicate by root cause. More than about fifty findings means the scope is too wide.
8. If the design is contested or the stakes are high, run **critique** and merge its verified findings.

**Reply:** what the product is and whether the design fits that, findings by phase with counts, the three highest-leverage changes, script output with labels, what you could not review and why.

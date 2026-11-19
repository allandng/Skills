### Screen

**You own every picture this screen can show, not one of them.**

1. Name the screen as `family:type`. State its ten-second job and its one primary action (`references/app-taxonomy.md` §5).
2. List its regions outside in (§6). Bulk actions replace the toolbar. Choose overlays by the least-interrupting rule.
3. Print the manifest: `python3 scripts/state_coverage.py --template <family:type>`. These are the states you owe.
4. Model the screen's data as one value with one status (`references/states.md` §2). Draw the chart if any state returns to an earlier one.
5. Design the ready state with real data at real volume. Then first-run, no-results, error, and the rest. They are designed, not appended.
6. Build. Tokens only. Copy through `references/copy-gate.md`: empty, error and loading strings included.
7. Fill `states.json` with evidence and run `python3 scripts/state_coverage.py states.json`.
8. Proof ladder (`references/proof.md`). Content stress and keyboard are the rungs screens fail.

**Reply:** the screen's type, job and primary action, the state model, the coverage output, screenshots or their absence stated plainly, the proof ladder with labels, open decisions.

### Review

**You own the verdict. Reviewers find. You verify. Nobody fixes.**

Run it before anyone builds on a plan that is contested, expensive, or going to an implementing agent unattended.

1. State the plan's intent in one or two sentences, from the user's words and the PRD or the addon's "What and why".
2. Run the scripts first, so reviewers spend their attention on what a script cannot see: `check_docs.py`, and for an addon `verify_plan.py` and `check_addon.py`.
3. Pick four to six lenses (`references/review-panel.md`). Implementer, operator and scope lawyer are always in.
4. Give each reviewer the plan, the intent, the repo if there is one, and its lens. Nothing else: no interview notes, no rationale, no earlier review. Subagents in parallel when available, otherwise one lens at a time with each list written down before the next.
5. Verify every finding by going to what it cites: the line of the plan, the file in the repo, the command and its output. Keep it when the evidence shows the problem and the problem breaks the intent.
6. Merge by root cause. Count the dropped ones per lens.
7. Report. Do not rewrite the plan.

**Reply:** `INTENT`, `FINDINGS` (title, where in the plan, evidence, how it breaks the intent, which lenses), `DROPPED` (count and reason per lens). "No verified findings" is a valid result.

### Review

**You own the verdict. Reviewers find. You verify. Nobody fixes.**

1. State what is being reviewed and the decision it will drive.
2. Run the `metric-check` skill on every headline number first, so reviewers spend attention on what a checklist cannot see.
3. Pick four to six lenses (`references/review-panel.md`). The statistician, the data engineer and the user's advocate are always in.
4. Give each reviewer the artifact, the decision and its lens. Nothing else. Subagents in parallel when available, otherwise one lens at a time with each list written down before the next.
5. Verify each finding by rerunning the number or reading the definition it cites. Keep it when the evidence shows the problem and the problem could change the decision.
6. Merge by root cause. Count the dropped ones per lens.
7. Report. Do not rewrite the analysis.

**Reply:** `DECISION`, `FINDINGS` (title, where, evidence, how it could change the decision, which lenses), `DROPPED` (count and reason per lens). "No verified findings" is a valid result.

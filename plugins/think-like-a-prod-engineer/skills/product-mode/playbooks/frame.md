### Frame

**You own the reason this is being built, and how anyone will know it worked.**

1. Step 0 from `SKILL.md`: read `docs/product/context.md`.
2. Write the job: what the user is trying to get done, and what they do today instead. If nobody does anything today, question whether the problem exists.
3. Trace each requirement to a named pain or bottleneck. Cut the ones that trace to nothing.
4. List non-goals for v1, each with a reason.
5. Pick one success metric. Write its definition (`playbooks/metric.md`) and the size of change that would matter. Read its current value now, so there is a baseline.
6. Pick one or two guardrails: what must not get worse.
7. Name the riskiest assumption as value, usability, feasibility or viability, and choose the cheapest test: prototype, fake door, or build.
8. Cut the work into vertical slices that each ship end to end, analytics included. Order them so the riskiest assumption is tested first.
9. Say which lifecycle transition this is meant to move (`references/lifecycle.md`).

**Reply:** the job in one sentence, non-goals, the success metric with its definition and baseline, the guardrails, the riskiest assumption and its test, the slices in order.

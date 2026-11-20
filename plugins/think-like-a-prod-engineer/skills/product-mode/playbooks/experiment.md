### Experiment

**You own a test whose result can be believed, including when it says nothing happened.**

1. Run the `experiment` skill. Its steps, in short:
2. Write the hypothesis: the change, the users, the metric, the direction, and why.
3. Decide whether to test at all: enough traffic, a reversible change, a real decision riding on it.
4. Compute the size per arm and the duration. If the answer is months, change the plan.
5. Write down, before starting: primary metric, guardrails, size per arm, start and stop dates, who is included, what happens for each outcome.
6. One change per arm. Randomize by user. On mobile, account for app version (`references/platforms.md`).
7. During: check the split for sample ratio mismatch. Do not read the metric.
8. After the stop date: read it against the planned size. Read guardrails. Read by platform.
9. Record the result, including a null one, in `docs/product/decisions.md`.

**Reply:** the written plan, the size and duration, the split check, the readout with its interval, guardrails, the per-platform read, and the decision.

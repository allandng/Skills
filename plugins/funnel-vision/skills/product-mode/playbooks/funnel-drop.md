### Funnel drop

**You own one leak: where, for whom, and why.**

1. Define the funnel: ordered events, the window, the unit. Write it down (`playbooks/metric.md`).
2. Run the funnel script from the `product-analytics` skill. Read the count left out as too recent.
3. Find the largest loss. Ask whether that step is meant to lose people: an optional step is not a leak.
4. Segment by platform, then source, then new against returning. Read the intervals: overlapping intervals are not a difference.
5. Check the tracking at the leaking step before believing the leak: does the event fire on every platform, on success, once? (The `tracking-plan` skill's event QA script.)
6. Read the waits. A long p90 before the leaking step is confusion or slowness.
7. Watch replays of users who dropped there.
8. State the cause as measured, observed, inferred or guess, and the smallest change that would test it.

**Reply:** the funnel definition, the table with intervals, the leak and who it affects, tracking confirmed or not, the waits, what replays showed, the suspected cause with its label, and the test.

---
name: product-analytics
description: Measure funnels, retention, and early behaviours that go with retention from an export of product events, with a definition you can reproduce, a count and a 95% interval on every rate, and users who have not had their full window left out. Segments by platform, source, or any property, reports median and p90 time between steps, and includes SQL that gives the same numbers in a warehouse. Use for post-hoc analysis of how users move through a product - where a funnel leaks, whether users come back, what retained users did early, how web and mobile differ, how long a flow takes - and when a number from an analytics tool needs an independent check.
---

# Product analytics

Three scripts that answer the questions product work keeps asking, in a way that can be checked: where do users drop, do they come back, and what did the ones who stayed do early.

An analytics tool's own charts are the right place for daily looking. Use these when a number is going to drive a decision. They give you a written definition, an interval, a result someone else can rerun, and a second computation to hold against the tool's.

## The events file

A CSV with a header:

| Column | |
|---|---|
| `user_id` | A stable pseudonymous ID. One per person, not per device. Never an email |
| `event` | The event name, as in the tracking plan |
| `timestamp` | ISO 8601. No offset is read as UTC |
| anything else | A property to segment by: `platform`, `source`, `plan`, `app_version` |

Export 90 days or more. Exclude internal and test users in the export. No personal data. Before analysing a new export, run the `tracking-plan` skill's event QA on it: every number below inherits whatever is wrong with the events.

To try the scripts, or to see what a known effect looks like:

```bash
python3 scripts/sample_events.py events.csv     # synthetic data with planted answers
python3 scripts/sample_events.py --truth        # what was planted
```

Run a method on data where you know the answer before trusting it on data where you do not.

## Funnels

```bash
python3 scripts/funnel.py events.csv \
    --steps signup_completed,profile_completed,project_created \
    --window-days 7 --by platform
```

The definition it uses, which is the definition to quote:

- A user enters at their first occurrence of the first step.
- Each later step counts if it happens at or after the step before it, within the window from entering. Order matters. Repeats do not.
- Users who entered less than one window before the data ends are left out, and the number left out is printed.

It reports, per step: users, conversion from the previous step with a 95% interval, conversion from the start, and the median and 90th-percentile wait since the previous step. Then the same per segment.

Reading it:

- **The largest loss is not always the leak.** A step that is optional by design loses people on purpose.
- **Overlapping intervals are not a difference.** Web at 80% (78 to 82) and iOS at 56% (54 to 59) differ. Two segments at 31% (28 to 33) and 32% (28 to 35) do not.
- **A segment gap is a place to look.** Platforms differ in source, intent and tracking. Check the tracking at that step before the product.
- **Waits are findings too.** A long p90 before a step is confusion or slowness.

## Retention

```bash
python3 scripts/retention.py events.csv --start-event signup_completed \
    --return-event session_started --days 1,7,28 --by source --cohorts

python3 scripts/retention.py events.csv --start-event signup_completed \
    --unit week --periods 1,4,8
```

The definition:

- A user's clock starts at their first start event.
- Retained in period N means at least one return event between N and N+1 periods after that moment. These are rolling windows from the user's own start, not calendar days.
- A user counts toward period N only once it has fully passed for them.

Choose the unit from the product's natural rhythm. A weekly product measured daily looks like it is dying.

Choose the return event with care. Without `--return-event`, any event counts, including an app open caused by a notification. A meaningful action is a better definition of coming back.

Reading it:

- **Shape first.** A curve that flattens above zero is a product some people keep. One that keeps falling is a leaky bucket.
- **Cohorts second.** Is each newer cohort better than the last at the same age?
- **Segments last,** and check the mix before the cause.

## What retained users did early

```bash
python3 scripts/retention.py events.csv --start-event signup_completed \
    --return-event session_started --unit week \
    --candidates --first-days 3 --target 4
```

For each event and each count threshold, it compares users who did it at least that many times in their first days with users who did not: share who did, retention of each group, the difference, and its interval.

**This finds what goes with retention. It cannot show what causes it.** Users who were always going to stay do more of everything in their first days. Three checks before taking a row seriously:

1. Is it common enough to matter, and rare enough to be a signal? A behaviour 3% or 97% of users do is neither.
2. Could the product plausibly cause more of it?
3. Would doing it change a user's outcome, or does it only reveal who they already were?

A row that survives is a hypothesis for the `experiment` skill.

## The same numbers in SQL

`references/sql.md` has queries for the funnel and for retention that return the same counts as the scripts. They were checked against the scripts on the sample data. Use them when the data is too large to export, and use either one to check the other.

## Before quoting anything

Run the `metric-check` skill on the number. Then report it with its definition, n, interval, the date range, and the command that produced it.

## Reference map

| File | Read it when |
|---|---|
| `references/sql.md` | The data lives in a warehouse, or a script's number needs a second computation |
| `scripts/funnel.py` | Ordered conversion, by segment, with waits |
| `scripts/retention.py` | Retention by day or week, by cohort and segment, and early behaviours |
| `scripts/sample_events.py` | Synthetic events with known answers, clean or with tracking faults |

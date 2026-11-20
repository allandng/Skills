# Proof

A finding is finished when someone else could reproduce it and would reach the same conclusion. Until then it is an impression with numbers attached.

This runs after the analysis and before anyone is told. It is where most wrong product decisions could have been caught.

## The ladder

Work up it. A rung that does not apply keeps its line with `n/a: <reason>`.

| # | Rung | How | Passes when |
|---|---|---|---|
| 1 | **Decision** | State the decision and what each answer would change | Written before the analysis, not fitted after |
| 2 | **Definition** | The metric card (`playbooks/metric.md`) | Numerator, denominator, unit and window are written, and a second person would compute the same thing |
| 3 | **Tracking** | The `tracking-plan` skill's event QA on the events involved | No double fires, platform gaps, identity breaks or blank fields in them, or each is accounted for |
| 4 | **Population** | Who is in and out | Internal users, tests and bots excluded. Only users whose window has passed |
| 5 | **Uncertainty** | n and an interval on every rate | A difference is claimed only when the intervals support it |
| 6 | **Splits** | Platform, source, cohort, and app version on mobile | The finding holds within segments, or the reply says where it does not |
| 7 | **Rivals** | Other explanations: mix shift, season, novelty, another release, a tracking change, selection | Each is ruled out with evidence or listed as open |
| 8 | **Twice** | A second computation: script and tool, or script and SQL | They agree, or the difference is explained |
| 9 | **Causal claim** | Experiment, or observation? | The wording matches. Observational findings say "goes with", not "causes" |
| 10 | **Reproducible** | The exact command or query, the data's date range, the export time | Saved with the finding |

Rung 8 is the one that finds the most. Analytics tools and hand-written queries disagree for reasons that are always worth knowing: a different unit, a different window, a filter one side applied.

## Labels

Every number and every causal statement in the reply carries one.

| Label | Means | Example |
|---|---|---|
| **measured** | Computed from events, with the definition and n shown | "Activation is 41.2% (38.9 to 43.5, n=1,812), measured" |
| **estimated** | Computed from a sample, a proxy, or with a stated assumption | "About 30% of iOS users are on the old version, estimated from the last 7 days" |
| **observed** | Seen directly: walking the flow, watching replays | "4 of 6 users tapped the disabled button first, observed" |
| **inferred** | Reasoned from other findings | "The drop is probably the permission prompt: it is the only step unique to iOS, inferred" |
| **guess** | None of the above | "Could be seasonal, guess: no data from last year" |

And for cause:

| Label | Means |
|---|---|
| **experiment** | Randomized, sized in advance, read at the planned time, no sample ratio mismatch |
| **observational** | Everything else, including before-and-after and adopters against non-adopters |

A reply built on inferred and guess lines has not been verified, whatever its tone. Climb the ladder. Do not reword.

## The reply

Each playbook ends with its own **Reply** line. All of them share this frame:

```
DECISION    the decision this serves
ANSWER      one or two sentences, in plain words, with the causal label
NUMBERS     each with its definition, n, interval and label
SPLITS      by platform and whatever else mattered
CAVEATS     rivals not ruled out, populations not covered, tracking doubts
REPRODUCE   command or query, date range, export time
NEXT        one action
```

Lead with the answer. Do not narrate the method. Do not report a number without its denominator. Do not round away an interval that includes zero.

## Decision log

Append to `docs/product/decisions.md` whenever a number changes what the team does:

```
2026-03-02  Kept the invite step in onboarding.
            Metric: week-4 retention. Test: 6,510 per arm, 21 days.
            Result: +0.4 points (-1.1 to +1.9), experiment. No difference detected.
            Decided by: <who>. Revisit if: onboarding is redesigned.
```

Null results and roll-backs are logged the same way. They are what stops the same idea being tested again next year.

## When a number looks wrong

Suspect the tracking, then the definition, then the population, then the product. In that order, because that is the order of how often each is the cause.

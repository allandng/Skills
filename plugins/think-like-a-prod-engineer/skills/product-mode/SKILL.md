---
name: product-mode
description: Product-engineering rigor for building features users actually adopt, and for proving afterwards whether they did. Routes any product task to a playbook - framing a feature, modeling it, checking flows and states, instrumenting it, shipping it behind a flag, designing onboarding and activation, and the post-launch cadence of watching, reading funnels, measuring retention, and deciding to iterate, double down, or roll back. Use this whenever the user is scoping or shipping a feature, asks about onboarding, activation, engagement, retention, funnels, drop-off, growth, time-to-value, or user adoption, asks whether a launch worked, wants a metric defined or an experiment designed, or mentions PostHog events, flags, or dashboards. Also use it for mobile-versus-web differences in behaviour or tracking, and for making a flow faster or lower-friction.
---

# Product mode

The entry point for product-engineering work: deciding what to build, building it so it can be measured, and finding out afterwards whether it worked.

It has the same shape as an engineering-rigor stack. Match the task to a playbook, copy its steps into your todo list, work them in order, and do not call the work done until it has been checked. The difference is the subject: users, not code.

Three things this stack assumes, stated once:

- **A number is a claim.** Every rate has a definition, a denominator, a count and an interval, or it is not reported.
- **Correlation is labeled.** "Users who do X retain better" is an observation. Only an experiment makes it "X improves retention".
- **The goal is value delivered.** Engagement that the user would not thank you for is not a win here. `references/principles.md` has the list of things this stack will not help build.

## Step 0: read the project's context

Look for `docs/product/context.md` in the repo. It holds what this stack cannot guess: the north-star metric, the activation definition, the lifecycle thresholds, the platforms, where events live, and the guardrail metrics. If it exists, read it before anything else. If it does not, create it from `assets/context-template.md` by asking the user for what only they know, and mark the rest `unknown` instead of inventing it.

Also check for a tracking plan (`docs/product/tracking-plan.csv`) and a glossary (`docs/product/glossary.csv`). Their absence is a finding.

## Route

Pick the playbook from what the user is doing. `references/help.md` when it is not obvious.

**Before building**

| Playbook | Trigger |
|---|---|
| **frame** | A feature request, an idea, "we should add X" |
| **model** | Naming things, objects and their relationships, URLs, roles, migrations |

**While building**

| Playbook | Trigger |
|---|---|
| **build-check** | A flow or screen is being built: states, friction, perceived speed, accessibility |
| **instrument** | Adding or changing tracking for a feature |
| **ship** | Releasing: flags, staged rollout, pre-launch tracking QA |

**Getting users to value**

| Playbook | Trigger |
|---|---|
| **onboarding** | Sign-up to first value: teardown, redesign, time-to-value |
| **activation** | Defining or validating the moment a new user "gets it" |
| **acquisition** | Which sources bring users who stay, not just users |

**After launch**

| Playbook | Trigger |
|---|---|
| **launch-watch** | Days 1 to 3: is it healthy and is tracking clean |
| **friction-review** | Weeks 1 to 2: where do people stall, and why |
| **impact-readout** | Day 30 and later: did it change retention, or was it novelty |
| **decide** | Iterate, double down, pivot, or roll back. Then triage what was found |
| **cleanup** | Remove the flag, the dead code and the dead events. Sunset what is not used |

**Any time**

| Playbook | Trigger |
|---|---|
| **diagnose** | A metric moved, or growth stalled, and nobody knows where |
| **funnel-drop** | One funnel, one leak |
| **retention** | Who stays, who leaves, when |
| **engagement** | Depth and frequency. Getting existing users more of the value |
| **experiment** | Designing, running or reading an A/B test |
| **metric** | Defining a metric, or choosing a north star |
| **review** | Reviewers try to break an analysis or a plan before it is acted on |
| **weekly** | The recurring review of the numbers |

Every playbook is in `playbooks/`. A step that does not apply keeps its line with `n/a: <reason>`, so a skipped step and a forgotten one never look the same. Each ends with a **Reply** line.

## The other skills in this plugin

Product mode runs these as the steps need them. Use one directly when you want one thing.

| Skill | Does |
|---|---|
| `tracking-plan` | Designs, lints and audits the event tracking plan. Finds double fires, platform gaps, identity breaks and blank fields in real events |
| `product-analytics` | Funnels, retention and early-behaviour analysis from an events export, with intervals, and SQL that gives the same numbers |
| `experiment` | Sample size before, sample-ratio check and readout after |
| `onboarding` | Teardown of the path from sign-up to first value, and what to cut |
| `metric-check` | The checklist a number passes before anyone reports or acts on it |

## Non-negotiables

1. **Decision first.** Before any analysis, write the decision it serves and what each possible answer would change. An analysis that changes nothing is not run.
2. **Define, then measure.** A metric has a numerator, a denominator, a time window, a unit (user, workspace, session) and an owner, written down, before the first query (`playbooks/metric.md`).
3. **Success and guardrails before code.** One primary metric and one or two guardrails are chosen in `frame`, not after launch when the choice can be made to flatter the result.
4. **One vocabulary.** The interface, the schema, the API and the events call a thing by the same name. `scripts/vocab_check.py` enforces the glossary.
5. **The tracking plan is the source of truth.** No event ships without a row in it. Critical state changes fire from the server. Every event carries the user's platform (`tracking-plan` skill).
6. **Only users who have had the chance.** A user counts toward day-30 retention after 30 days, and toward a 7-day funnel after 7. Counting the rest makes recent numbers look worse than they are.
7. **Every platform, separately, then together.** Web and mobile differ in tracking, in release speed and in behaviour. A blended number hides all three (`references/platforms.md`).
8. **Speed is a feature with a number.** Time to first value, steps, fields and wait times are measured, not felt (`references/efficiency.md`).
9. **One change per test, decided in advance.** Metric, size and stopping date are fixed before an experiment starts (`experiment` skill).
10. **Done means reproducible.** A finding ships with the command or query that produced it, and every claim is marked measured, estimated, inferred or guess (`references/proof.md`).

When a decision is hard, `references/principles.md` has one rule per situation. Name the principle that changed a decision; skip the ones that changed nothing.

## With the other plugins

| When | Hand off to |
|---|---|
| A flow, screen or app shell needs designing | `ui-ux-studio` in `design-suite` (flow, screen, app-shell playbooks). It owns visual and interaction design |
| A feature needs a plan against an existing codebase | `swe-plan` (`/addon`). Its scope fence and phases carry the metrics from `frame` |
| The code needs writing or reviewing | `/askillissue:allan-mode` |

This stack decides what to measure and whether it worked. It does not replace those.

## Reference map

| File | Read it when |
|---|---|
| `playbooks/` | Always - the step list for the job in hand |
| `references/help.md` | The request does not match one playbook |
| `references/feature-gates.md` | Any feature, start to finish - the seven gates and what each one checks |
| `references/lifecycle.md` | Naming where a user is: new, activated, engaged, at risk, dormant, resurrected |
| `references/platforms.md` | Anything that runs on both web and mobile |
| `references/efficiency.md` | Making a flow faster or lighter, or measuring that it is |
| `references/posthog.md` | The team uses PostHog - events, identity, flags, experiments, replays, export |
| `references/principles.md` | A decision is hard, or a request edges toward a dark pattern |
| `references/proof.md` | Before reporting anything - the ladder, the labels, the reply frame |
| `references/review-panel.md` | Running the review playbook |
| `assets/context-template.md` | No `docs/product/context.md` exists yet |
| `scripts/vocab_check.py` | Checking the repo against the glossary |

The playbook form, the proof-before-done discipline, the review panel and several principles are adapted from pstack by Lauren Tan (MIT).

# Think Like a Prod Engineer

Product-engineering rigor: decide what to build, build it so it can be measured, and find out afterwards whether it worked.

```bash
/plugin install think-like-a-prod-engineer@allan-skills
```

It has the shape of an engineering-rigor stack (playbooks, named principles, proof before done), pointed at users instead of code: onboarding, activation, engagement, retention, and the analysis that tells you which of them moved.

## Start here

1. Describe what you are doing: "frame this feature", "tear down our onboarding", "did the launch work". `product-mode` picks the playbook.
2. The first time, it creates `docs/product/context.md` in your repo: your north star, your activation definition, your platforms, where your events live. That file is what makes a generic stack yours.
3. Before quoting any number, run `metric-check` on it.

## The six skills

| Skill | Does |
|---|---|
| `product-mode` | The entry point. Routes to one of 21 playbooks across a feature's whole life |
| `tracking-plan` | Designs, lints and audits the event tracking plan, and finds tracking faults in real events |
| `product-analytics` | Funnels, retention and early-behaviour analysis from an events export, with intervals |
| `experiment` | Sample size before a test, split check during, readout after |
| `onboarding` | Teardown of the path from sign-up to first value, and what to cut |

Plus `metric-check`: the checklist a number passes before anyone reports or acts on it.

## The 21 playbooks

| When | Playbooks |
|---|---|
| Before building | `frame`, `model` |
| While building | `build-check`, `instrument`, `ship` |
| Getting users to value | `onboarding`, `activation`, `acquisition` |
| After launch | `launch-watch` (days 1 to 3), `friction-review` (weeks 1 to 2), `impact-readout` (day 30 on), `decide`, `cleanup` |
| Any time | `diagnose`, `funnel-drop`, `retention`, `engagement`, `experiment`, `metric`, `review`, `weekly` |

A feature runs through the first four rows in order. `references/feature-gates.md` in `product-mode` is the checklist those playbooks enforce: seven gates from "framed" to "followed through".

## What the rigor consists of

- **Every rate has a definition, a count and a 95% interval.** The scripts print all three.
- **Users who have not had their chance are left out.** A user counts toward day-28 retention after 28 days. On a truncated copy of the sample data, the naive calculation gives 3.7% and the correct one gives 8.0%, from the same events.
- **Correlation is labeled.** The early-behaviour analysis says "goes with retention" and tells you to test it.
- **Tracking is checked, not trusted.** `event_qa.py` finds double fires, events missing on one platform, identity breaks, bad clocks, bots and blank properties.
- **Web and mobile are read separately first.** Every event carries the user's platform, including server-side ones.
- **Experiments are decided in advance.** The readout refuses a verdict when the split is broken or the planned size was not reached.
- **Numbers are computed twice.** The SQL in `product-analytics` returns the same counts as the scripts.
- **Engagement means value.** `principles.md` lists the dark patterns this stack will not help build.

## Scripts

Python 3.11+, standard library only. Nothing to install.

| Script | In | Does |
|---|---|---|
| `funnel.py` | `product-analytics` | Ordered funnel with intervals, by segment, with median and p90 wait per step |
| `retention.py` | `product-analytics` | Retention by day or week, by cohort and segment, and early behaviours that go with it |
| `sample_events.py` | `product-analytics` | Synthetic events with known answers planted, clean or with six tracking faults |
| `tracking_plan.py` | `tracking-plan` | Lints the plan, and compares it with the events that fire |
| `event_qa.py` | `tracking-plan` | Six checks on real events |
| `experiment.py` | `experiment` | Sample size, sample ratio mismatch, readout |
| `vocab_check.py` | `product-mode` | Finds places the codebase calls one thing by two names |

Try them on data where the answer is known:

```bash
cd skills/product-analytics/scripts
python3 sample_events.py events.csv
python3 funnel.py events.csv --steps signup_completed,profile_completed,project_created --by platform
python3 retention.py events.csv --start-event signup_completed --return-event session_started \
    --unit week --candidates --first-days 3 --target 4
python3 sample_events.py --truth     # what was planted
```

The funnel shows iOS completing the profile step at about 56% against 80% on web. The candidates table puts inviting a teammate at the top. Both were planted, and `--truth` confirms the sizes.

## With PostHog

`product-mode`'s `references/posthog.md` maps each rule onto PostHog: explicit events over autocapture, server-side capture for state changes, identify and reset, group analytics, flags as kill switches, replays and surveys at the drop-off, and how to export events for the scripts. The rules do not depend on PostHog. A team on another tool swaps that one file.

## With the other plugins

This plugin decides what to measure and whether it worked. It hands design to `ui-ux-studio` (`design-suite`), planning to `swe-plan`, and code to `askillissue`.

## Credit

The playbook form, the proof-before-done discipline, the review panel, and several principles are adapted from [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan (MIT). The seven feature gates follow a product-engineering checklist written for a team that ships on web and mobile with PostHog.

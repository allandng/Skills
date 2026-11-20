---
name: experiment
description: Design, run, and read an A/B test on a conversion-style metric so the result can be believed. Writes the hypothesis and the plan before the test starts (primary metric, guardrails, minimum detectable effect, sample size, stop date), computes users per arm and duration, checks for sample ratio mismatch, and reads the result with a 95% interval, refusing a verdict when the split is broken or the planned size has not been reached. Use when someone wants to A/B test a change, asks whether a result is significant, asks how long a test must run, proposes stopping a test early, or wants to know if a change is testable with their traffic. Works with PostHog experiments or any flag-based split.
---

# Experiment

An experiment is the only way to say a change caused a result. That is worth protecting, and it is easy to waste: most misleading test results come from decisions made after the data started arriving.

The rule that prevents nearly all of it: **everything is decided before the test starts.**

## 1. Should this be a test?

Not everything should.

| Test it when | Do not test it when |
|---|---|
| A real decision depends on the answer | The change will ship regardless |
| The change can be turned off | It cannot be reversed for the users who got it |
| There is enough traffic to see the smallest effect that matters | The size calculation says months |
| The metric can be read within a few weeks | The outcome takes a year to show |
| The honest prior is "could go either way" | It is a bug fix, or legally required |

When a test is not possible, ship behind a flag to a small share, watch the guardrails, and say plainly afterwards that the readout is observational.

## 2. The hypothesis

One sentence, with every part filled in:

> For `<which users>`, `<the one change>` will `<raise or lower>` `<the primary metric>` by at least `<amount>`, because `<the reason>`.

The reason matters. It is what you learn from when the result is not what you expected.

## 3. The size

```bash
python3 scripts/experiment.py size --baseline 0.22 --mde 0.02 --daily-users 600
```

- `--baseline` is the current rate of the primary metric, measured the same way the test will measure it.
- `--mde` is the smallest change worth detecting, in absolute points (0.02 is two points). Add `--relative` to give it as a fraction of the baseline. Choose it from what would change the decision, not from what the traffic allows.
- It prints users per arm and, with `--daily-users`, the duration in whole weeks.

If the answer is too long: detect a bigger effect and accept missing small ones, move the test to a step with a higher rate, or do not test. Do not run it short and hope.

Run in whole weeks. Weekdays and weekends behave differently, and a test that covers nine days counts two of them twice.

## 4. The plan, written before it starts

```
HYPOTHESIS   the sentence above
USERS        who is included, who is excluded, the unit of randomization (user)
ARMS         control, and one change
PRIMARY      one metric, with its definition (metric card)
GUARDRAILS   one or two: what must not get worse
SIZE         per arm, from the script, with baseline and mde
DATES        start, and the stop date that is not moved
PLATFORMS    which, and for mobile which app versions carry the change
IF IT WINS   what ships
IF IT LOSES  what happens
IF NOTHING   what happens. Decide now: this is the most common outcome
```

Save it in the repo or the decision log before the flag is turned on. A plan written afterwards is a description, not a plan.

## 5. While it runs

Check that it is healthy. Do not read the metric.

```bash
python3 scripts/experiment.py srm --counts 5021,4979
```

**Sample ratio mismatch** means the arms did not get the share of users they were configured to. It is a bug detector: a redirect that loses users in one arm, a filter applied after assignment, tracking that fires on only one path. When it fails, the test cannot be read, whatever the metric says. Find the cause and restart.

Check it in the first days and again at the end. Count users at the point of assignment, not at the point of the metric.

**Do not peek at the metric and stop when it looks good.** A test checked every day and stopped at the first significant reading reports a difference far more often than its stated error rate, even when none exists. The stop date exists so that the result means what it says.

Reasons to stop early that are allowed: a guardrail is clearly harmed, the split is broken, or the change is broken.

## 6. Reading it

After the stop date:

```bash
python3 scripts/experiment.py read --control 400/5000 --treatment 460/5000 --planned-n 6510
```

It checks the split, checks the planned size was reached, then gives the difference in points, the 95% interval, and a two-sided p-value. It refuses a verdict when the split is broken or the test is not finished.

Read the interval, not the p-value:

- **Interval excludes zero.** There is a difference. Its true size is plausibly anywhere in the interval. Ask whether the near-zero end is still worth shipping.
- **Interval includes zero.** No difference was detected. That is not proof of no effect: the interval tells you how large an effect could still be hiding. If the whole interval is too small to care about, that is a clear and useful "it does not matter".

Then:

- **Guardrails.** A win that moved a guardrail the wrong way is not a win.
- **By platform.** Read each platform separately. An effect that exists on web and not on iOS is two findings. Do not go looking through ten segments for one that won: one in twenty will, by chance.
- **Novelty.** If the effect is shrinking week by week, it is curiosity. Say so.
- **Mobile.** Only users on versions that carry the change were really in the test. Those who updated are not a random sample of everyone.

## 7. Record it

In `docs/product/decisions.md`: the plan, the result with its interval, the decision, and the date. Null results too. They are what stops the same idea being retested next year.

## What the script covers, and what it does not

One conversion metric, users randomized individually, two-sided test of two proportions. It is not for revenue or time per user (skewed, needs a different test), metrics where one user contributes many observations, or randomization by group or region. For those, get the method right before trusting a number: a wrong test gives a confident wrong answer.

## With PostHog

PostHog's experiments run the split on a feature flag and report results. Keep the plan from section 4 regardless, compute the size here before starting, and compare this script's sample-ratio check with the exposure counts PostHog shows. If they disagree, exposure is not being counted the way you think, and that is found before the readout or not at all.

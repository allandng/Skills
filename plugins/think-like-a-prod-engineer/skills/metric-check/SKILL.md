---
name: metric-check
description: Vet a product metric before reporting it or acting on it - a conversion rate, a retention number, a lift, an adoption figure, a week-over-week change. Checks the definition, the denominator, who was counted, whether the tracking can be trusted, the uncertainty, and the usual ways a number misleads (mix shift, users counted too early, selection, novelty, season). Use when you computed or were handed a number about users and are about to quote it, put it in a doc, or make a decision on it, and whenever a number looks surprisingly good or bad.
---

# Metric check

Run this on a number before it leaves your hands. It takes a few minutes and it is where most wrong product conclusions get caught.

The stance: a number is a claim about users. The question is never "is the arithmetic right" but "does this mean what the sentence around it says".

Work down the list. Write one line per item: what you checked and what you found. An item that does not apply gets `n/a: <reason>`.

## 1. What is it, exactly

- **Definition.** Numerator, denominator, time window, unit. If it cannot be written in one sentence, it is not ready to be quoted.
- **Unit.** Users, accounts or sessions? The same data gives three different answers. A ratio with users on top and sessions underneath means nothing.
- **Denominator.** Is it the population that could have done the thing? "30% of users used the feature" needs to say whether that is of all users, or of users who could see it.
- **As originally defined.** Is this the metric that was chosen before the work, or one found afterwards that looks better?

## 2. Who was counted

- **Had their chance.** Any metric with a window (7-day conversion, day-30 retention) counts only users whose window has fully passed. Including recent users makes every recent period look worse.
- **Excluded.** Internal users, test accounts, bots, the QA environment.
- **Survivors.** "Users active in month 3 have high NPS" describes people who stayed. It says nothing about the product's effect on anyone.
- **Blank segments.** A split by a property silently drops rows where the property is empty. How many?

## 3. Can the data be trusted

- **Tracking changes.** Did an event get added, renamed, moved from client to server, or fixed inside the date range? A step change on a release date is tracking until shown otherwise.
- **Double fires and gaps.** Has the event been through the `tracking-plan` skill's event QA? An inflated event inflates everything downstream of it.
- **Platform parity.** Does the event fire the same way on web and mobile? A "mobile converts worse" finding is often "mobile tracks worse".
- **Late data.** Mobile events arrive late. The last 48 hours are incomplete.
- **Against a second source.** Does the count match the database, or the same number computed another way?

## 4. How sure

- **n.** Stated, for every rate.
- **Interval.** A 95% interval on every rate, and on every difference. "Conversion rose from 20% to 23%" on 200 users per side is not a rise.
- **Many comparisons.** Twenty segments were checked and one "won"? One in twenty wins by chance.
- **Skew.** Means of counts, durations and revenue are run by a few extreme users. Use the median and the 90th percentile.
- **Percent of a percent.** "Up 50%" from 2% to 3% is one point. Give both.

## 5. Is the comparison fair

- **Mix shift.** A blended rate can fall while every segment's rate rises, when the mix moves toward a lower segment. Check the rate within each platform and source before the total.
- **Same age.** Compare cohorts at the same age. A cohort from last month and a cohort from last year are different ages.
- **Season and calendar.** Compare with the same period last year where that exists, and with the same weekdays. One week against the week before is mostly noise.
- **What else changed.** Another launch, a campaign, an outage, a pricing change in the window.
- **Novelty.** Use that peaks in week one and decays is curiosity. Read it after it settles.

## 6. What does it allow you to say

- **Cause.** An experiment (randomized, sized in advance, read on schedule, no sample ratio mismatch) allows "X caused Y". Everything else allows "X goes with Y".
- **Selection.** Users who adopted a feature chose to. They differ from those who did not before they ever touched it.
- **Who it applies to.** A finding from organizers on web says nothing about attendees on the app.
- **Practical size.** At the low end of the interval, is the effect still worth anything?

## 7. The gaming test

How could this number rise with no user better off? If that is the easiest way to move it, the metric needs a guardrail or a redefinition before anyone is asked to improve it.

## The reply

```
NUMBER      the value, with n and its interval
DEFINITION  one sentence: numerator, denominator, unit, window
CHECKED     the items above that mattered here, one line each
VERDICT     safe to quote / quote with these caveats / do not quote yet
SAY THIS    the sentence it supports, worded with the right causal label
FIX         what would make it firmer
```

"Do not quote yet" is a useful answer. It is cheaper than a retraction.

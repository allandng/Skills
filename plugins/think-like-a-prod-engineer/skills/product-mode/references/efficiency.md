# Efficiency

How fast and how light a flow is, as numbers. "It feels slow" and "it's a lot of steps" are where this starts, not what gets reported.

Two kinds of efficiency matter, and they are measured differently: how much the user has to **do**, and how long the user has to **wait**.

## 1. Effort: the friction count

For the critical flow, count, on each platform:

| Count | What it is |
|---|---|
| **Screens** | Distinct views between start and done |
| **Actions** | Clicks or taps, including dismissals |
| **Fields** | Inputs the user must fill. Optional fields count if they look required |
| **Decisions** | Points where the user must choose between options they have to think about |
| **Waits** | Places the interface blocks on the network |
| **Context switches** | Leaving for email, another app, a document, a card |

Then challenge each line, in this order:

1. **Remove it.** Is it needed at all, for v1?
2. **Defer it.** Can it happen after the user has had value?
3. **Infer it.** Can the system work it out: locale, timezone, a default that is right for most?
4. **Merge it.** Two screens that are one decision.
5. **Speed it up.** Only what survives the first four.

Rules that pay for themselves: undo instead of confirmation for reversible actions. The right keyboard for each field on mobile. Autofill and paste never blocked. One primary action per screen.

Record the before and after: `fields 9 -> 4, decisions 3 -> 1, context switches 1 -> 0`.

## 2. Time: what to measure

| Measure | Definition | Where it comes from |
|---|---|---|
| **Time to first value** | Sign-up to the first-value event, per user | `funnel.py`: median and p90 wait between the two steps |
| **Step time** | Time between consecutive funnel steps | Same. A long median on one step is confusion or a slow screen |
| **Task time** | Start to completion of a repeated task, for returning users | Paired start and completion events |
| **Load performance** | How long until the screen is usable | Web: the Core Web Vitals. Mobile: cold start, and time to first content |
| **Interaction latency** | Tap or click to visible response | Web: Interaction to Next Paint. Mobile: dropped frames, unresponsive screens |

Report the **median and the 90th percentile**, never the mean. The mean of a wait time is dominated by people who left a tab open overnight. The 90th percentile is what your unluckiest regular user lives with.

Web thresholds, measured at the 75th percentile of real page loads: Largest Contentful Paint within 2.5 seconds, Interaction to Next Paint within 200 milliseconds, Cumulative Layout Shift under 0.1. Check current guidance before quoting them in a decision: these have changed before.

## 3. Perceived speed

Work on perception only after the real time is acceptable, or to cover the part that cannot be made faster.

- **Respond at once.** On frequent actions (toggles, likes, reordering, sending), update the interface immediately and reconcile if the server refuses. Say what happened when it does.
- **Skeletons shaped like the content,** shown only when the wait is long enough to notice.
- **Never block the whole screen** for one region's data.
- **Keep what the user typed** through every error.

Optimistic updates change tracking: see "fired on intent, not on success" in the `tracking-plan` skill's edge cases. An event sent when the user tapped, for an action the server then rejected, counts something that did not happen.

## 4. Does it matter? Check before optimizing

Speed work is worth doing where it changes behaviour. Before a performance project:

1. Segment the funnel step by its wait time. Do users who waited longer convert less, on the same platform and source?
2. If yes, that is still a correlation: slow connections go with other things. Size the opportunity, then test a real improvement.
3. If no, the step's problem is not speed.

## What to state

```
FLOW        which flow, which platform, which users (new or returning)
EFFORT      screens, actions, fields, decisions, waits, switches: before -> after
TIME        median and p90, with n, for the whole flow and the slowest step
EVIDENCE    measured (events), observed (walked it), or guess
CHANGED     what was removed, deferred, inferred, merged, sped up
```

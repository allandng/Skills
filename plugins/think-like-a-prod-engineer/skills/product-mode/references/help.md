# Which playbook

Read this when the request does not obviously match one job. Find the row, answer in a sentence or two, and offer the prompt.

## By what the user says

| They say | Playbook |
|---|---|
| "We should add X", "customers keep asking for Y" | `frame` |
| "What should we call this", "how should the URLs work", "who can do what" | `model` |
| "Is this flow ready", "it feels clunky", "too many steps" | `build-check` |
| "What should we track", "add analytics for this" | `instrument` |
| "We're launching Friday" | `ship` |
| "People sign up and never come back", "improve onboarding" | `onboarding` |
| "What's our aha moment", "define activation" | `activation` |
| "Which channel is best" | `acquisition` |
| "We launched yesterday" | `launch-watch` |
| "Where are people getting stuck" | `friction-review`, or `funnel-drop` for an older flow |
| "Did the launch work" | `impact-readout` |
| "Should we keep it" | `decide` |
| "The flag is still in the code" | `cleanup` |
| "Signups are down", "DAU dropped", "something's off" | `diagnose` |
| "Are users sticking around" | `retention` |
| "How do we get people to use it more" | `engagement` |
| "Let's A/B test it", "is this result significant" | `experiment` |
| "How do we measure this", "what's our north star" | `metric` |
| "Check my analysis" | `review` |
| "What happened this week" | `weekly` |
| "Why do the mobile numbers look different" | `diagnose`, with `references/platforms.md` |
| "Make it faster", "reduce friction" | `build-check`, with `references/efficiency.md` |
| "Is this number right" | the `metric-check` skill |

## Chaining

```
a feature, start to finish   frame → model → build-check → instrument → ship
                             → launch-watch → friction-review → impact-readout
                             → decide → cleanup
growth has stalled           diagnose → the playbook it names → experiment → decide
new users do not stick       activation → onboarding → experiment
a number looks wrong         metric-check → instrument → (fix) → launch-watch
```

Finish one playbook's Reply before starting the next. The Reply is the handoff.

## Prompts that work

```
frame            Customers want recurring events. Frame it before we build anything.
instrument       We're adding a waitlist to sold-out events. What do we track, and
                 what are the edge cases on iOS?
onboarding       Tear down organizer onboarding on web and on the app. Where do we
                 lose people before their first published event?
activation       Here's 120 days of events. What early behaviour goes with week-4
                 retention?
funnel-drop      Checkout converts worse on Android. Find the step and tell me
                 whether it's real or tracking.
impact-readout   The new seat map shipped 5 weeks ago behind a flag. Did it work?
experiment       I want to test a shorter sign-up. Baseline 22%, about 600 new
                 visitors a day. Is it testable?
weekly           Run the weekly on this export.
```

A prompt that names the users, the platform and the decision gets a better answer than one that names a chart.

### Retention

**You own who stays, who leaves, and when. In that order.**

1. Set the rhythm: how often would a user with this problem need the product? Measure at that period (`references/lifecycle.md`).
2. Define "came back": a meaningful action, not an app open triggered by a notification.
3. Run the retention script from the `product-analytics` skill at that rhythm, with cohorts. Only users whose period has passed are counted.
4. Read the shape. Does the curve flatten? A curve that flattens above zero is a product some people keep. One that goes to zero is a leaky bucket, and acquisition will not fix it.
5. Read the cohorts. Is each newer cohort better or worse than the last, at the same age?
6. Segment by platform and source. Check the mix before the cause (the `metric-check` skill).
7. Find when people leave. Most loss in the first period is an onboarding problem. Steady loss later is a value or habit problem.
8. Run **activation** to find what the stayers did early.

**Reply:** the rhythm and the definition of returning, the curve with intervals and n, whether it flattens and where, the cohort trend, the segments, when the loss happens, and which playbook follows.

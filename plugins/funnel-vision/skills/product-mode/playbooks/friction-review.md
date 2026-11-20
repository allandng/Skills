### Friction review

**Weeks 1 to 2. You own where people stall, and why.**

1. Run the funnel script from the `product-analytics` skill on the feature's steps, by platform, with waits. Only users with a full window.
2. Find the step with the largest loss that is not optional by design, and the step with the longest p90 wait.
3. Watch replays of users who dropped at that step. At least five per platform. Write one line per user: what they did, where they stopped.
4. Group what you saw. A pattern is three or more users doing the same thing.
5. Check the non-ideal states at that step: is the error message actionable, is the empty state doing its job (`references/feature-gates.md`, gate 3)?
6. If a survey is running at the drop-off, read the answers next to the replays.
7. Write findings as: the step, what users do, the evidence, the smallest change that would test a fix.

**Reply:** the funnel by platform, the worst step and the slowest step, the replay notes and the patterns, findings with their smallest fix, and what is still unexplained.

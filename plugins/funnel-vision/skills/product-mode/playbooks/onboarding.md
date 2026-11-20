### Onboarding

**You own the distance between signing up and getting something of value.**

1. Read `docs/product/context.md` for the activation definition. If there is none, run **activation** first, or state the working guess.
2. Run the `onboarding` skill: sign up fresh on each platform and write the teardown, step by step.
3. Measure it with the `product-analytics` skill: the funnel over the onboarding steps, by platform and by source, with median and p90 wait per step.
4. Mark every step as value, required-for-value, or neither. Everything in the third group is a candidate to remove or defer.
5. Look at how shipped products in the category handle the hardest step, with counts (the `onboarding` skill covers how).
6. Watch replays of users who stalled at the worst step. At least five. Write what each did.
7. Write the hypotheses: what to remove, defer, default or explain, each with the step it targets and the users it could affect.
8. Rank by users affected times plausible change, and say how sure you are of each number.
9. Test the top one (**experiment**). Hand the redesign to `ui-ux-studio`'s flow playbook.

**Reply:** the teardown table, the funnel by platform with waits, the worst step and what replays showed, ranked hypotheses with their evidence labels, and the first test.

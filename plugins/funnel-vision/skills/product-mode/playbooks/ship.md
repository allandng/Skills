### Ship

**You own the release, and the ability to take it back.**

1. Confirm gates 1 to 6 in `references/feature-gates.md`. List any that are `n/a` with the reason.
2. Put the feature behind a flag. State the kill switch and who can flip it.
3. Write the rollout: internal, beta, a small percentage, everyone, with what is checked before each step and who decides.
4. For mobile: state which app version carries the feature, how old versions behave, and that the flag reaches only versions that know it.
5. Check the contracts: mutations safe to repeat, errors that map to a message a user can act on.
6. Check the cost: query plans on the new paths, bundle size, layout shift, cold start on mobile.
7. Pre-launch tracking QA (`playbooks/instrument.md`, step 7) on the build that will ship.
8. Confirm the dashboard exists and the baseline is recorded.
9. Put the three review dates on the calendar now: day 3, week 2, day 30.

**Reply:** the flag and kill switch, the rollout steps and their checks, the mobile version plan, QA results, the dashboard, and the three review dates.

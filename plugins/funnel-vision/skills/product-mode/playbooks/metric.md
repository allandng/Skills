### Metric

**You own a definition two people would compute the same way.**

1. Write the question the metric answers and the decision it informs.
2. Fill in the card:

   ```
   NAME         activation rate
   QUESTION     do new users reach first value?
   NUMERATOR    users who did <event sequence> within <window> of signing up
   DENOMINATOR  users who signed up, and whose window has fully passed
   UNIT         user (not session, not workspace)
   WINDOW       7 days from sign-up, rolling
   EXCLUDES     internal users, test accounts, bots
   SPLITS       platform, source, plan
   SOURCE       events: signup_completed, project_created (tracking plan)
   OWNER        who answers questions about it
   GAMEABLE BY  how the number could rise with no user better off
   GUARDRAIL    what is watched so that does not happen
   ```

3. Check the unit. Users, workspaces and sessions give different answers, and mixing them inside one ratio is the most common silent error.
4. Check the denominator is the population that could have done the numerator.
5. Fill in `GAMEABLE BY` honestly. If the easiest way to move the metric does not help users, change the metric.
6. Compute it twice, two ways (a script and the analytics tool, or a script and SQL). They must agree, or the definition is not finished.
7. Add it to `docs/product/context.md`.

For a north star: it measures value delivered to users, moves when the product gets better, and is something the team can affect within a quarter. Revenue is a result of it, not a candidate for it.

**Reply:** the card, both computations and whether they agree, the current value with n and an interval, and where it is recorded.

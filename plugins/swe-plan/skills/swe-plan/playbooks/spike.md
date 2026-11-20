### Spike

**You own an answer, not code. The spike is a throwaway instrument for one question.**

Adapted from pstack's Prototype playbook. Use it whenever a plan is about to depend on something nobody has checked: a third-party API that may not do what its documentation says, a performance target nobody has measured, an integration nobody has tried, a library that may not support the case.

1. Write the question so that it has an answer: "Can the partner API return 500 items in one call on the free tier?" If it cannot be phrased that way, it is a decision, not a spike: route to **decide**.
2. Write what each possible answer would change in the plan. If no answer changes anything, do not run the spike.
3. Build the smallest thing that answers it, in a scratch folder outside the source tree. No framework, no tests, no abstractions, no error handling beyond what the question needs.
4. Run it. Keep the exact command and what it printed.
5. Explain the number before trusting it (`references/principles.md`): what limited it, how many runs, whether it measured the thing you care about or something next to it.
6. Record it where the plan can cite it - in the ADR's Context, or under the phase it unblocks:

   ```
   SPIKE     <the question>
   RAN       <command>, <date>, <where: machine, tier, data size>
   SAW       <the output that answers it, trimmed>
   SO        <what the plan now does because of it>
   LIMITS    <what this did not test>
   SCRATCH   <path, and that it is throwaway>
   ```

7. Promote the result: the related `Q-##` closes or the `A-##` becomes a verified fact. Update the documents that cited it.

**Reply:** the question, the command and its output, what changed in the plan, what the spike did not cover, and the scratch path. Say plainly that the code is throwaway.

### Launch watch

**Days 1 to 3. You own two questions: is it healthy, and can the data be trusted.**

1. Use the feature yourself in production, on each platform.
2. Compare event volume with the database: the count of the core event against the count of rows it created. A gap over a few percent is a tracking fault, and it is found now or never.
3. Run the event QA script and the plan-against-events comparison from the `tracking-plan` skill on an export.
4. Read adoption: how many of the users who could see the feature found it. By platform, and on mobile by app version.
5. Read errors, latency and the guardrails against the baseline from `frame`.
6. Look for rage clicks and error events on the new screens.
7. Do not read the success metric yet. Three days is novelty and early adopters.

**Reply:** what you saw using it, events against the database, the QA results, adoption by platform and version, guardrails against baseline, and anything that needs fixing before week 2.

### Instrument

**You own the events. If it is not tracked correctly now, the questions asked in a month have no answers.**

1. Start from the questions: the success metric, the guardrails, and the funnel steps from `frame`. List the events each one needs. Add nothing that answers no question.
2. Run the `tracking-plan` skill to add each event to the plan: `object_action` name, exact trigger, typed properties, owner, client or server.
3. Decide client or server for each. State changes (sign-up, purchase, core mutations) fire from the server, on success.
4. Put the user's platform on every event, and the app version on mobile events (`references/platforms.md`).
5. Walk the edge cases for each event (the `tracking-plan` skill has the list): double fire, failure path, offline, retry, logout, a second device, an old app version.
6. Lint the plan with the `tracking-plan` skill's linter. Fix every failure.
7. Implement. Then QA before merge: trigger each event by hand on each platform and watch it arrive with the right name, types and identity. No duplicates. No personal data.
8. After a day of real traffic: compare the plan with what fires, and run the event QA script on an export (both in the `tracking-plan` skill).
9. Build the dashboard now. If a chart cannot be built, an event is missing.

**Reply:** the events added, with trigger and side, the edge cases checked per event, linter and QA results, what was seen live on each platform, and the dashboard link.

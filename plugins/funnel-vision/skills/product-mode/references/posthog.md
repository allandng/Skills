# With PostHog

How the rules in this stack map onto PostHog. The rules do not depend on PostHog: a team on another tool keeps the rules and swaps this file.

PostHog changes often. This file describes practices and names features. For exact method signatures, menu locations and limits, read the current PostHog documentation instead of trusting this file or memory.

## Events

- **Custom events for anything that matters.** Core flows and every metric in `docs/product/context.md` use explicit capture calls with typed properties, named `object_action`, each with a row in the tracking plan. Autocapture is for exploratory questions, never for a number someone will be held to.
- **Server-side for state changes.** Sign-ups, purchases, subscription changes and core mutations are captured from the backend, where an ad blocker or a closed tab cannot drop them. Interface-only interactions (a modal opened, a filter toggled) stay on the client.
- **Pass the same ID to the server.** A backend event must use the same distinct ID as the client, or it lands on a different person. It must also carry the user's platform as a property: the backend does not know it unless told.
- **Describe events where the team looks.** Add each new event's description in PostHog's data management, matching the tracking plan. Mark retired events deprecated there too.

## Identity

- **Identify on login and on sign-up.** That links the anonymous activity before login to the known user.
- **Reset on logout.** Otherwise the next person on that device inherits the last person's identity. On shared devices this is not rare.
- **One stable ID per user,** from your database. Not an email, which changes and is personal data.
- **Do not identify one person under two IDs.** PostHog will not merge two already-identified users through a normal identify call. Decide the ID scheme once.
- **Carry identity across web and mobile.** Pass the ID through the transition (a deep link parameter, the login) instead of letting each platform create its own.
- **Person properties** for standard attributes: plan, source, role. Set-once for things that should never be overwritten, such as the original source.
- **Group analytics** when the product has workspaces or organizations, so that adoption can be read per account and not only per person.

## Release

- **Feature flags** separate deploying from releasing: internal, beta, a small percentage, everyone. The flag is the kill switch.
- **Flags on mobile are evaluated by the installed version.** An old version that does not know the flag behaves as it always did.
- **Remove the flag** when the feature is at 100% and stable: from the code, then archive it. A flag left in place is a branch nobody tests.

## Understanding why

- **Session replay,** with sensitive inputs masked, for the users who dropped at a specific funnel step. Watch at least five before forming a theory, and write down what each did.
- **Surveys** triggered by an action or a drop-off, one question, asked at the moment. Not a quarterly form.

## Experiments

PostHog's experiments run on flags. This stack's rules still hold: metric, guardrails, minimum effect and sample size are written down before it starts, and nobody stops it early because it looks good. `experiment.py` gives the size and checks the split. Compare its sample-ratio check against what PostHog reports: a disagreement means exposure is not being counted the way you think.

## Launch dashboards

Build the feature's dashboard before launch: adoption, the funnel, errors, the guardrails. If the dashboard cannot be built yet, the feature is not instrumented yet.

## Getting events out, for the scripts

PostHog's own funnels and retention are the daily tools. Use the scripts in this plugin when a number will drive a decision and needs an independent check, when the definition must be exact and reproducible, or when you want intervals.

Export from the SQL editor to a CSV with the three columns the scripts need, plus your own properties:

```sql
SELECT
    person_id            AS user_id,
    event,
    timestamp,
    properties.platform  AS platform,
    properties.app_version AS app_version
FROM events
WHERE timestamp >= now() - INTERVAL 120 DAY
  AND event NOT LIKE '$%'
```

- **`person_id`, not `distinct_id`.** One person has several distinct IDs: one anonymous ID per device, plus the identified one. Counting distinct IDs counts some people twice.
- **`properties.platform`** is the property this stack tells you to set yourself. Adjust the names to what the tracking plan defines.
- **Exclude internal and test users** in the query, by whatever marks them.
- **No personal data in the export.** IDs only.

Check the export before trusting it: `python3 event_qa.py events.csv --as-of <export time>` from the `tracking-plan` skill.

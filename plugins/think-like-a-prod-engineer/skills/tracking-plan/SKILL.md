---
name: tracking-plan
description: Design, lint, and audit a product's event tracking plan, and find tracking faults in real event data. Defines events with object_action names, exact triggers, typed properties, client-or-server placement, and an owner; walks the edge cases for each event (double fires, failure paths, offline and retries, logout and shared devices, web versus mobile, old app versions); and checks real events for double fires, platform gaps, identity breaks, bad clocks, bots, and blank properties. Use when adding or changing analytics for a feature, when someone asks what to track or how to name an event, before a launch is called instrumented, when numbers look wrong or differ between platforms, or when auditing PostHog events.
---

# Tracking plan

The tracking plan is a file in the repo that says, for every event the product sends: what it means, exactly when it fires, what it carries, and who owns it. Every chart is only as true as this file and the code that implements it.

Tracking is the one part of a feature that cannot be fixed afterwards. A bug in the interface is fixed with a deploy. A month of events that fired twice, or never fired on iOS, is a month of questions with no answers.

## The plan

A CSV at `docs/product/tracking-plan.csv`, so it can be edited in a spreadsheet and reviewed in a pull request.

```bash
python3 scripts/tracking_plan.py template > docs/product/tracking-plan.csv
```

| Column | Rule |
|---|---|
| `event` | `object_action`, snake_case, object first, past tense: `ticket_purchased`, `invite_sent`. The object is a term from the glossary |
| `description` | What happened, in a sentence a new teammate would understand |
| `trigger` | The exact moment, and whether it fires on the client or the server: "Server: after the order row is committed" |
| `properties` | `name:type` pairs separated by semicolons. Types: `string`, `int`, `float`, `bool`, `timestamp`, `enum(a|b|c)` |
| `owner` | The person or team who answers questions about it |
| `status` | `planned`, `live`, or `deprecated` |
| `pii` | `none`, `pseudonymous`, or `personal` |

## Adding events for a feature

1. **Start from the questions.** The success metric, the guardrails, and each step of the funnel. Each needs specific events. An event that answers no question is not added.
2. **Name from the glossary.** `object_action`, using the product's one name for the object. Check the plan for an existing event first.
3. **Write the trigger precisely.** "When the user purchases" is not a trigger. "Server: after payment is confirmed and the order is committed" is. Fire on success, not on the tap.
4. **Choose the side.** State changes fire from the server: sign-up, purchase, subscription change, anything a metric depends on. An ad blocker or a closed tab cannot drop a server event. Interface-only interactions stay on the client.
5. **Type every property.** Use an enum where the values are known. Required on every event: the user's `platform`, and `app_version` on mobile. A server-side event must be given these by the client: it does not know them.
6. **Mark personal data.** Send IDs. Never emails, names, phone numbers, addresses, or text the user typed.
7. **Walk the edge cases** in `references/event-edge-cases.md` for each event, and write down what happens in each.
8. **Lint.**

   ```bash
   python3 scripts/tracking_plan.py lint docs/product/tracking-plan.csv
   ```

   It fails on names that break the convention, duplicates, the same event under two names, empty fields, untyped properties, and properties that look like personal data in an event not marked personal.

## Checking real events

Before a feature is called instrumented, and on a schedule after:

```bash
# Does what fires match the plan?
python3 scripts/tracking_plan.py diff docs/product/tracking-plan.csv events.csv

# Is what fires trustworthy?
python3 scripts/event_qa.py events.csv --as-of <export time> \
    --requires ticket_purchased:checkout_started
```

`diff` reports events that fire with no row in the plan, live events that never fire, and deprecated events that still do.

`event_qa.py` runs six checks:

| Check | Finds | Usual cause |
|---|---|---|
| double fires | The same user and event twice within two seconds | A re-render, a retry, a handler bound twice, client and server both sending |
| platform gaps | An event that fires on one platform and never on another | Tracking not implemented there, or a different event name |
| order | A later step with no earlier one | One person split across two identities, or the earlier event not firing |
| clocks | Timestamps after the export | Wrong device clocks. Use server receive time |
| heavy users | Hundreds of events a day from one ID | Bots, scripts, test accounts |
| blank fields | A property empty on part of an event | A server-side event that lost the client's context |

The events file is a CSV with `user_id`, `event`, `timestamp`, and any property columns. Both scripts exit non-zero on a failure, so they run in CI. The `product-analytics` skill can generate a sample file with these faults planted, to see what each looks like.

## Pre-merge QA

A script cannot do this part. For each new event, on each platform:

1. Trigger it by hand and watch it arrive in the analytics tool's live view.
2. Check the name, every property and its type, and that it is attached to the right person.
3. Trigger it the wrong way: fail the action, double-tap, go offline, log out and in as someone else. Check what was sent.
4. Confirm nothing personal is in it.

Write down what you triggered and what arrived. "Verified in live events" with no list is not verification.

## Changing and removing

- **Never change what an existing event means.** Add a new event. A redefinition makes every chart across the change date wrong with no visible sign.
- **Record the date of every tracking change** in `docs/product/context.md`. It is the first thing checked when a number moves.
- **Deprecate, then remove.** Mark the row `deprecated`, remove the code, and confirm with `diff` that it stopped.
- **On mobile, old versions keep sending old events.** A removed event stops when the last old version does.

## Reference map

| File | Read it when |
|---|---|
| `references/event-edge-cases.md` | Adding any event, and whenever a number differs between platforms |
| `scripts/tracking_plan.py` | Linting the plan, or comparing it with what fires |
| `scripts/event_qa.py` | Checking an export for the six faults |

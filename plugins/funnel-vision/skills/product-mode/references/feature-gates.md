# The seven gates

A feature passes through seven gates between "we should build this" and "we removed the flag". Each gate is a short list of things that are either done or not. The playbooks run the gates. This file is what they check.

A line that does not apply is marked `n/a: <reason>`. It is never dropped.

## 1. Framed

`playbooks/frame.md`

- [ ] **The job.** The user's underlying job is written down, not just the requested feature. Every requirement traces to a named pain or bottleneck.
- [ ] **Non-goals.** What is deliberately out of v1, each with a reason.
- [ ] **Vertical slices.** The work is cut into thin slices that each ship end to end: schema, API, interface, analytics. No slice is "the backend".
- [ ] **One success metric,** with its definition and the size of change that would matter.
- [ ] **One or two guardrails:** error rate, support tickets, churn, a neighbouring feature's use.
- [ ] **Riskiest assumption named,** as value, usability, feasibility or viability, with how it will be tested: prototype, fake door, or full build.

## 2. Modeled

`playbooks/model.md`

- [ ] **One vocabulary.** Each concept has one name in the interface, schema, API and events. `scripts/vocab_check.py` passes.
- [ ] **Objects before screens.** Core objects, their relationships (1:1, 1:many, many:many), their attributes, and the actions on each.
- [ ] **URLs are part of the product.** Readable, shareable, bookmarkable, and they reflect the hierarchy. Deep links open the same place on mobile.
- [ ] **Permissions in the model.** For each role: view, create, edit, delete, share. Decided now, not bolted on.
- [ ] **Migrations are backward-compatible.** Expand, migrate, contract. Old clients, including app versions still installed, keep working.

## 3. Complete

`playbooks/build-check.md`

- [ ] **Seven states,** for every view and component:
  1. Ideal: normal data
  2. Empty: first use, or cleared
  3. Loading: skeletons, progressive loading
  4. Partial: missing fields, long strings, 1 item, 10,000 items
  5. Error: network, 4xx and 5xx, validation, each with a way to recover
  6. Permission-denied: paywalled, role-restricted, expired
  7. Offline or stale: dropped connection, edits by someone else
- [ ] **Friction counted.** Clicks, fields and decisions in the critical flow, with a number. Undo instead of "Are you sure?" where the action is reversible.
- [ ] **Perceived speed.** The interface responds at once on frequent actions and reconciles on failure.
- [ ] **Accessible.** Keyboard, focus (especially in modals and drawers), semantic markup, contrast, breakpoints. A baseline, not polish.
- [ ] **Each platform checked.** The flow was walked on every platform it ships on (`platforms.md`).

## 4. Activating

`playbooks/onboarding.md`, `playbooks/activation.md`

- [ ] **The first-value moment is named,** and everything between sign-up and it has been challenged.
- [ ] **Deferred:** profile photos, billing, invites and settings wait until after first value, unless one of them is the value.
- [ ] **Empty states act.** Each explains the value and offers one action, a template, or sample data.
- [ ] **Guidance is in context.** Inline hints, defaults and checklists tied to real actions. No multi-step tour.
- [ ] **Activation is defined** as a specific sequence of events, and drop-off is tracked at every step.

## 5. Shippable

`playbooks/ship.md`

- [ ] **Owned end to end.** Query plans, bundle size, layout shift: checked across the stack.
- [ ] **Behind a flag,** with a kill switch, and a rollout plan: internal, beta, 10%, 100%.
- [ ] **Contracts.** Mutations are safe to repeat. Pagination and errors are consistent. Error payloads map to messages a user can act on.
- [ ] **Copy.** Every error says what happened and what to do next.
- [ ] **Tests on the journeys that matter:** auth, billing, the core workflow. Integration and end to end before unit coverage of trivia.

## 6. Instrumented

`playbooks/instrument.md`, the `tracking-plan` skill

- [ ] **In the tracking plan.** Every event has a row: `object_action` name, trigger, typed properties, owner. The linter passes.
- [ ] **Server-side where it matters.** Sign-ups, purchases and core mutations fire from the backend. Interface-only interactions stay on the client.
- [ ] **Identity.** Identify on login, reset on logout, standard person properties, group analytics where the product has workspaces.
- [ ] **Edge cases checked** (the `tracking-plan` skill has the list): no double fires, events on failure paths, parity across platforms, platform on every event.
- [ ] **QA before merge.** Events seen live with the right names and types, no duplicates, no personal data.
- [ ] **Qualitative loop.** Replays with sensitive inputs masked, and a survey at the drop-off or after the key action.
- [ ] **Experiment defined up front,** if there is one: metric, guardrails, minimum effect, sample size.

## 7. Followed through

`playbooks/launch-watch.md`, `friction-review.md`, `impact-readout.md`, `decide.md`, `cleanup.md`

- [ ] **Used by the team** in production from day one.
- [ ] **Dashboard built before launch.**
- [ ] **Days 1 to 3:** event volume matches the database, adoption is visible, no unexpected errors or rage clicks.
- [ ] **Weeks 1 to 2:** funnel read step by step, replays watched for the users who stalled.
- [ ] **Day 30 and later:** retention and stickiness by cohort: adopters against non-adopters, new against returning, free against paid.
- [ ] **A decision is recorded:** iterate, double down, pivot or roll back, against the metrics from gate 1.
- [ ] **Findings triaged:** fix now, fast-follow, backlog.
- [ ] **Cleaned up:** flag removed from code and archived, dead paths deleted, obsolete events marked deprecated.
- [ ] **Sunset on evidence:** features that are not earning their keep get a deprecation plan.

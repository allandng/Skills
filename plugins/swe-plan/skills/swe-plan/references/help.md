# Which playbook

Read this when the request does not obviously match one job, or when the user asks what this skill can do. Find the row, answer in a sentence or two, and offer the prompt.

## By what the user has

| They have | They want | Playbook |
|---|---|---|
| An idea | A plan a team can build against | `start` |
| A codebase and a feature | A scoped, grounded plan for adding it | `addon` |
| A plan that depends on something untested | To find out before building on it | `spike` |
| One hard choice | It made, and written down with what lost | `decide` |
| A finished plan | Someone to try to break it | `review` |
| A working codebase with no docs | Documents that describe what is there | `backfill` |
| Docs and a codebase that have drifted | The docs made true again | `amend` |
| An approved plan | A prompt for an agent to build one phase | `handoff` |

## By symptom

| They say | It is usually |
|---|---|
| "Where do I begin" | `start`, Sketch tier until the answers say otherwise |
| "Just write me a PRD" | `start`, stopped after the PRD - and say what the PRD cannot settle without the rest |
| "Make me an ERD" | `start` Step 2 for a new system, `backfill` for an existing one |
| "Is this plan any good" | `review` |
| "Will this API actually do that" | `spike` |
| "Postgres or Mongo", "monolith or services" | `decide` |
| "The agent built way more than I asked" | `addon` was skipped or the fence was not confirmed. Run `addon`, then `handoff` one phase at a time |
| "Nobody knows why this is here" | `backfill`, and record the unexplained decisions as questions |
| "Are the docs still right" | `amend` |

## Chaining

```
new product        start → spike on the risky part → review → handoff P-01 → amend
new feature        addon → review → handoff P-01 → amend → handoff P-02 ...
inherited system   backfill → amend on each merge
one hard choice    spike → decide
```

With the other plugins in this marketplace:

| When | Hand off | What to pass |
|---|---|---|
| A phase is ready to build | `/askillissue:allan-mode` | The `handoff` prompt. It maps to the feature, bug fix, refactoring or prototype playbook |
| The plan has user-facing screens | `ui-ux-studio`, spec-to-ui or app-shell | `03-data-model.md` for the entities and their states, `04-flows.md` for the use cases. Each screen should name the `UC-##` it serves |
| The product replaces or imitates an existing one | `design-dna`, teardown | Nothing. Its output feeds the PRD's "Today's workaround" and the flows |

Finish one playbook's Reply before starting the next. The Reply is the handoff.

## Prompts that work

```
start      I want to build a habit tracker for climbers. Solo, a month, I know Next.js.
addon      Add push notifications to this repo when a friend logs a cook.
spike      The plan assumes Supabase realtime can handle 200 subscribers per channel
           on the free tier. Find out.
decide     SQLite or Postgres for this. It is one server and maybe 50 users.
review     Run the panel on docs/addons/push.md. Include the operator and the
           scope lawyer.
backfill   This repo has no docs and I am handing it to two teammates next week.
amend      We shipped P-02 yesterday. Bring the docs back in line.
handoff    Write the implementation prompt for P-01.
```

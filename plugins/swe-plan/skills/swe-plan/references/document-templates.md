# Document templates

Use these verbatim for structure. Fill every field or delete the section - a heading with "TBD" underneath teaches readers to skim, and once they skim they stop reading the parts that matter.

Contents:
1. [Header block](#header-block)
2. [00-orientation.md](#00-orientationmd)
3. [01-prd.md](#01-prdmd)
4. [02-srd.md](#02-srdmd)
5. [03-data-model.md](#03-data-modelmd)
6. [04-flows.md](#04-flowsmd)
7. [05-delivery-plan.md](#05-delivery-planmd)
8. [06-traceability.md](#06-traceabilitymd)
9. [ADR](#adr)
10. [Addon plan](#addon-plan)

---

## Header block

Every document starts with this. `check_docs.py` enforces it.

````markdown
> **Status:** Draft
> **Owner:** unassigned
> **Updated:** 2026-07-26
> **Related:** [PRD](01-prd.md) · [Data model](03-data-model.md)
````

---

## 00-orientation.md

The front door. Written last. One page - if it does not fit on a screen and a half, it is doing another document's job.

````markdown
# <Project> - Orientation

> header block

## What this is
Two or three sentences. What it does, for whom, and the current state - idea,
in build, phase 2 of 4, shipped.

## Why it exists
The problem in one paragraph, and what people do today instead.

## How to run it
```bash
<clone, install, env setup, migrate, run>
```
Required environment variables and where to get their values.
If it does not run yet, say so and say what the first phase produces.

## The shape of it
```mermaid
<the container diagram from 02-srd.md, copied here>
```

## Where things live
| Path | What |
|---|---|
| `src/...` | |

## Where to start reading
The one file a new person should open first, and why.

## Current status
| Phase | State | Notes |
|---|---|---|
| P-01 | Done | |
| P-02 | In progress | |

## Decisions you should know about
Three to five lines, each linking to its ADR. Not a list of every ADR - the ones
that will surprise someone.

## Open questions
Link to `06-traceability.md`. Do not duplicate them here; two copies means one is
already wrong.

## The documents
| Doc | Read it when |
|---|---|
| [01-prd.md](01-prd.md) | You need to know what we are building and why |
| [02-srd.md](02-srd.md) | You are about to write code |
| [03-data-model.md](03-data-model.md) | You are touching the database |
| [04-flows.md](04-flows.md) | You need to know how a feature is supposed to behave |
| [05-delivery-plan.md](05-delivery-plan.md) | You are picking up work |
| [06-traceability.md](06-traceability.md) | You are asking why some code exists |
````

---

## 01-prd.md

What and why. No implementation. If a sentence names a framework, it belongs in the SRD.

````markdown
# <Project> - Product Requirements

> header block

## Problem
What is wrong today, for whom, and how you know it is real. Cite evidence if there
is any - a conversation, a support thread, a number, your own experience. "Users
struggle to..." with nothing behind it is a guess wearing a suit.

## Today's workaround
What people currently do instead. Spreadsheet, notes app, group chat, nothing.
This defines the actual bar to clear.

## Users
| Who | What they are trying to get done | What they have now | What they are missing |
|---|---|---|---|

## The core moment
The single interaction that makes the product worth using. One sentence.

## Requirements

| ID | Requirement | Priority | Acceptance criterion |
|---|---|---|---|
| PR-01 | A user can log a dish they cooked in under 15 seconds | Must | From cold app open to saved, median under 15s in manual test on a mid-range phone |
| PR-02 | ... | Should | ... |

Priority: **Must** (no launch without it), **Should** (launch is worse without it),
**Could** (if time allows), **Won't** (explicitly deferred, with the release named).

Every criterion has to be checkable by someone who did not write it. If you cannot
write one, the requirement is not understood yet - move it to `Q-##`.

## Non-goals
| Not doing | Why not | Revisit when |
|---|---|---|

This section is load-bearing. It is the thing you point at in week six.

## Success metrics
| Metric | Now | Target | By when | How measured |
|---|---|---|---|---|

Numbers, not directions. "More engagement" is not a metric.

## Constraints
Deadlines, budget, team size and skills, platform requirements, legal or
institutional rules.

## Assumptions and open questions
`A-##` and `Q-##` relevant to product scope. Full list lives in `06-traceability.md`.
````

---

## 02-srd.md

System Requirements and Design. How it works. Diagram recipes are in `diagrams.md`.

````markdown
# <Project> - System Requirements & Design

> header block

## Scope
One paragraph: what this system is responsible for and what it is not.

## Context
```mermaid
<C4-style context diagram - the system, its users, its external dependencies>
```
| External | What we use it for | What breaks if it is down | Auth |
|---|---|---|---|

## Containers
```mermaid
<container diagram - the deployable pieces and how they talk>
```
| Container | Responsibility | Tech | Scales by |
|---|---|---|---|

## Components
Per container, the internal modules and what each owns. A component with a
responsibility you cannot state in one sentence is two components.

| Component | Owns | Depends on | Notes |
|---|---|---|---|

## Interfaces

### Internal APIs
| Method | Path | Purpose | Auth | Request | Response | Errors |
|---|---|---|---|---|---|---|
| POST | `/api/cooks` | Log a cooked dish | Session | `{dish_id, rating, cooked_at}` | `201 {cook}` | `400`, `401`, `409 duplicate within 5m` |

### Events and jobs
| Name | Trigger | Payload | Handler | Retry | Idempotent? |
|---|---|---|---|---|---|

Idempotency is not optional for anything that retries. Say how it is achieved -
a natural key, a dedupe table, an upsert.

## System requirements

| ID | Requirement | Satisfies | Component |
|---|---|---|---|
| SR-01 | Cook writes are rejected if an identical dish and user pair exists within 5 minutes | PR-01 | API / cook service |

Every `SR-##` traces to at least one `PR-##` or `NFR-##`. One that traces to nothing
is either a missing product requirement or scope that crept in.

## Non-functional requirements

| ID | Category | Target | Measured how | Traces to |
|---|---|---|---|---|
| NFR-01 | Latency | p95 under 300ms for feed read at 1k concurrent | Load test before each release | PR-03 |
| NFR-02 | Cost | Under $50/month to 10k monthly actives | Provider dashboard | Constraint |

Categories worth covering: latency, throughput, availability, durability, cost,
security, privacy, accessibility, offline behavior, observability.

A target with no number is not a requirement. "Highly available" is a feeling;
"99.5% monthly, single region, planned maintenance excluded" is a requirement.

## Data
Summary only - the model lives in `03-data-model.md`. Cover storage choice and why,
retention, backup and restore, and what is personally identifying.

## Security and privacy
| Concern | Approach |
|---|---|
| Authentication | |
| Authorization | |
| Secrets | |
| Data in transit / at rest | |
| Personal data stored | |
| Deletion and export | |

## Deployment
```mermaid
<deployment diagram>
```
Environments, promotion path, migration strategy, rollback.

## Observability
What is logged, what is measured, what pages someone, and what the first debugging
step is when a user reports it is broken.

## Rejected architectures
The serious alternatives and why they lost. Link the ADRs.
````

---

## 03-data-model.md

````markdown
# <Project> - Data Model

> header block

## Entity relationship diagram
```mermaid
<erDiagram - see diagrams.md>
```

## Entities

### E-01 `users`
What one row means, in one sentence.

| Field | Type | Null | Default | Constraint | Notes |
|---|---|---|---|---|---|
| `id` | uuid | no | `gen_random_uuid()` | PK | |
| `email` | citext | no | | unique | login identity |
| `created_at` | timestamptz | no | `now()` | | |

**Relationships:** one user has many cooks (`cooks.user_id`, cascade delete).
**Indexes:** `email` unique; `created_at` for admin listing.
**Lifecycle:** see state machine below, or "none - rows are immutable after insert".

Repeat per entity.

## Lifecycles
```mermaid
<stateDiagram-v2 for any entity with a status column>
```
Any entity with a `status` or `state` column needs one of these. A status column
with no documented transitions becomes a free-text field within two months.

## Access patterns
| Query | Frequency | Index used | Concern |
|---|---|---|---|

Write this before choosing indexes. Indexes chosen without knowing the queries are
guesses that cost write throughput.

## Integrity rules
Rules the database enforces, and rules only the application enforces. Be honest
about the second list - it is where the bugs live.

## Migrations
Ordering, whether each is reversible, whether any needs a backfill, and which ones
lock a table long enough to matter at current row counts.

## Retention and deletion
What is kept, how long, what happens on account deletion, and whether deletes are
hard or soft. If soft, say what excludes them from every query.
````

---

## 04-flows.md

````markdown
# <Project> - Flows

> header block

## Actors
| Actor | Description | Authenticated? |
|---|---|---|

## Use case diagram
```mermaid
<see diagrams.md - Mermaid has no native use case diagram, use the recipe>
```

## Use cases

### UC-01 - Log a cooked dish
| | |
|---|---|
| **Actor** | Home cook |
| **Goal** | Record a dish they cooked so it enters their history and their friends' feed |
| **Preconditions** | Signed in; at least one dish exists or can be created inline |
| **Trigger** | Taps the log button |
| **Satisfies** | PR-01, PR-04 |

**Main path**
1. User taps log.
2. System shows recent and suggested dishes.
3. User picks a dish or enters a new name.
4. User sets a rating.
5. System saves and returns to the feed with the new entry visible.

**Alternate paths**
- 3a. Dish does not exist - user enters a name, system creates it and continues at 4.

**Failure paths**
- 5a. Save fails offline - system queues locally and retries; user sees a pending state.
- 5b. Duplicate within 5 minutes - system offers to edit the existing entry instead.

**Postconditions** A cook row exists; the friend feed includes it within 5 seconds.

The alternate and failure paths are the point of the exercise. A use case with only
a main path documents the demo, not the software.

## Sequence diagrams
One per flow that crosses a boundary - client to server, service to service, or
anything asynchronous. A flow entirely inside one component rarely needs one.

### UC-01 - Log a cooked dish
```mermaid
<sequenceDiagram - see diagrams.md>
```
````

---

## 05-delivery-plan.md

````markdown
# <Project> - Delivery Plan

> header block

## Phases
Each phase ships on its own and can be reverted without unwinding earlier ones.

### P-01 - <name>
| | |
|---|---|
| **Delivers** | What works at the end, stated as user-visible behavior where possible |
| **Covers** | PR-01, SR-01, SR-02 |
| **Tasks** | Numbered list, each half a day or less |
| **Done when** | Objective checks |
| **Verified by** | T-01, T-02 |
| **Reverts by** | The specific undo |
| **Blocked by** | Nothing, or P-0N |
| **Estimate** | Range, not a point |

Sequencing rules: the riskiest unknown goes in P-01, schema lands before the code
that uses it, and any user-visible change of consequence ships behind a flag.

## Parallel work
For plans that several people or agents will execute. One line each:
what must finish before anything else starts, which phases or tasks touch disjoint
files and can run at once, what state they share, and the smallest split that is
safe. If the honest answer is "one worker, in order", say that and why.

## Definition of done
Applies to every task. Typically: tests pass, types check, linter clean, docs
updated, reviewed, deployed to staging, rollback confirmed.

Written once here, not repeated per phase.

## Test plan
| ID | What it verifies | Level | Automated? | Traces to |
|---|---|---|---|---|
| T-01 | Duplicate cook within 5 minutes returns 409 | Integration | Yes | SR-01 |

Cover the failure paths from the use cases. Tests that only cover main paths pass
right up until real users arrive.

## Risks
| ID | Risk | Likelihood | Impact | Early warning sign | Mitigation |
|---|---|---|---|---|---|
| R-01 | Third-party API rate limits below what the feed needs | Med | High | 429s in the P-01 spike | Cache aggressively; fall back to a nightly sync |

The early warning column is the useful one. A risk you cannot detect early is one
you find out about from a user.

## Out of scope for this release
With the release or condition that brings each back.
````

---

## 06-traceability.md

The document that answers "why does this code exist."

````markdown
# <Project> - Traceability

> header block

## Coverage matrix
| Product req | System reqs | Component | Tests | Phase | Status |
|---|---|---|---|---|---|
| PR-01 | SR-01, SR-02 | cook-service | T-01, T-02 | P-01 | Built |
| PR-02 | SR-04 | feed-service | T-05 | P-02 | Planned |

Rules `check_docs.py` enforces:
- Every `PR-##` has at least one `SR-##`. A product requirement with no system
  requirement is not being built by anyone.
- Every `SR-##` traces up to a `PR-##` or `NFR-##`. One that does not is scope
  that arrived without a decision.
- Every `Must` priority requirement has at least one test.

## Assumptions
| ID | Assumption | Made because | Wrong means | Confirm by |
|---|---|---|---|---|
| A-01 | Under 1000 users in the first year | No launch plan beyond one campus | Postgres on a single instance stops being enough | Check actives at month 3 |

"Wrong means" is the column that earns the table. An assumption with no stated
consequence is a note; one with a consequence is a tripwire.

## Open questions
| ID | Question | Blocks | Who answers | Needed by |
|---|---|---|---|---|
| Q-01 | Does the grocery partner allow storing item prices? | SR-09, P-03 | Partner contact | Before P-03 |

## Decisions
| ADR | Decision | Status | Affects |
|---|---|---|---|
| [ADR-0001](adr/0001-postgres-over-mongo.md) | Postgres over Mongo | Accepted | SR-03, E-01..E-06 |
````

---

## ADR

One file per decision, in `docs/adr/`, numbered from 0001 and never renumbered. Never delete one - supersede it, and link both ways. The trail of superseded decisions is a record of how the team's understanding changed, which is usually more useful than the current answer alone.

````markdown
# ADR-0001 - Postgres over MongoDB for primary storage

> **Status:** Accepted
> **Date:** 2026-07-26
> **Deciders:** <names>
> **Supersedes:** none
> **Superseded by:** none

## Context
The situation forcing a decision, and the constraints that were real at the time.
Include what was not known - it explains decisions that look wrong in hindsight.

## Options considered

### A - PostgreSQL (chosen)
Pros. Cons.

### B - MongoDB
Pros. Cons. **Rejected because:** the specific reason, not "it was not the best fit."

### C - <the option someone will ask about>
Even if it was quickly dismissed. Especially if it was quickly dismissed - being
able to see it was considered stops the argument from being reopened.

## Decision
What was chosen, in one or two sentences.

## Consequences
**Accepted:** what this costs.
**Enabled:** what it makes easier later.
**Closed off:** what it makes harder or impossible.

## Revisit when
The concrete condition that should reopen this. "If write volume passes 5k/sec"
or "if the team adds someone who has run Mongo in production."
````

An ADR with no Cons and no Rejected reason is not an ADR. Six months on, the
rejected options are the valuable half, because they tell the next person whether
the reasoning still applies.

---

## Addon plan

For `/addon` when no full bundle exists yet. `docs/addons/<feature>.md`.

````markdown
# Addon - <feature>

> header block

## What and why
Two sentences on the behaviour being added, and who asked for it.
State the request in your own words - if your restatement is wrong, that is the
cheapest possible place to find out.

## Evidence ledger
What is known, and how well. Nothing below this section may contradict it.

```
VERIFIED    <path> - what reading it confirmed
INFERRED    <conclusion> - the basis, and what was not checked
UNKNOWN     Q-## <the question> - what it blocks
```

Read this back before writing anything else in the document. Claims stated flatly
must come from VERIFIED. Anything from INFERRED keeps its hedge in the prose.

## Conventions ledger
The eight-line summary of what this codebase already decided - layering, naming,
errors, data access, tests, tooling, and where it already contradicts itself.
Full field list in `addon-mode.md`.

## Scope fence
**Confirmed by:** <name, date> | **Unconfirmed - user asked to proceed without the gate**

```
IN SCOPE
  1. <behaviour delivered>

OUT OF SCOPE
  <thing a reader would reasonably expect and will not get>  - revisit when <condition>

MAY TOUCH
  <path>  - <why it changes>
  Nothing outside this list. If implementation reveals another file must change,
  stop and amend this document.

WILL CREATE
  <path>  - <why here>

WILL NOT
  - add dependencies beyond: <named list, or "none">
  - rename or move existing symbols or files
  - reformat or lint-fix code outside the diff
  - change schema beyond the named migration
  - alter existing tests except to extend them
  - fix unrelated problems noticed along the way

NOTICED
  <worth doing, not this change>  - <where it lives>
```

Every path under MAY TOUCH was read, not guessed. The Confirmed line is not
decoration: an unconfirmed fence means the scope is one person's assumption.

## Seam
Touches / Adds / Data / Interfaces / Dependencies / Config. Paths must match the
fence exactly - a file in Touches but not in MAY TOUCH is a gap in one of them.

## Options
The comparison table, then the recommendation paragraph. The paragraph becomes
the ADR.

## Blast radius
Direct / Data / Contracts / Performance / Security / Operations / Rollback.

## Phases
`P-##` blocks, each shippable and revertable on its own, each touching only
files from MAY TOUCH.

## Grounding check
```bash
python scripts/verify_plan.py <this file> <repo>
python scripts/check_addon.py <this file> <repo>
```
Paste both results, or state that each came back clean. A plan delivered without
this is a plan nobody checked.

## Doc delta
Which documents change, or a note that no bundle exists and `/start` can backfill one.

## Assumptions and open questions
`A-##` and `Q-##`, with what each blocks.
````

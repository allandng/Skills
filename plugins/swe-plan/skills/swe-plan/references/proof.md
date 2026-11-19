# Proof

A plan is finished when it has been checked, not when it has been written. Everything in a plan becomes a fact for whoever reads it next, and an implementing agent will build on a wrong line without noticing. This file is how a plan earns that trust.

It runs after the documents exist. It does not replace judgment about the design.

## The ladder

Work up it. A rung that does not apply keeps its line with `n/a: <reason>`.

| # | Rung | How | Passes when |
|---|---|---|---|
| 1 | **Structure** | `python scripts/check_docs.py docs/` | No errors. Each warning resolved or explained |
| 2 | **Rigor** | Same command. It also checks numbers, acceptance criteria, owners, phase checks and undos, and rejected options | No errors. `--no-rigor` is for bundles written before these rules, never for new work |
| 3 | **Grounding** | `python scripts/verify_plan.py <doc> <repo>` on every document that names files | Nothing in the missing bucket |
| 4 | **Contract** (addon) | `python scripts/check_addon.py <plan> <repo>` | No failures. An unconfirmed fence is reported as unconfirmed |
| 5 | **Falsifiable** | For each document, name one thing in it a competent engineer could reject | You can. A document nobody could disagree with is a template |
| 6 | **Cold read** | Give P-01, and only what the plan says about it, to a reader who was not in the conversation - a fresh subagent when available. Ask what they would do first and what they would have to guess | They start in the right file and guess nothing that matters |
| 7 | **Ran** | Anything the plan claims about behaviour, performance or a third party that could have been tried | It was tried (`playbooks/spike.md`), or it is marked inferred |
| 8 | **Reversible** | Every phase's "Reverts by" | Each is a specific action. "Roll back the deploy" is not specific if the phase ran a migration |
| 9 | **Current** (existing bundles) | `python scripts/doc_drift.py docs/ <repo>` | Clean, or every flagged document re-read |

The cold read is the rung that finds the most. The author reads the plan with the interview in their head. The next reader has only the page.

## Labels

Every claim about how things are carries one, in the ledger and in the reply:

| Label | Means | Example |
|---|---|---|
| **stated** | The user said it | "Under 1000 users in year one (stated)" |
| **verified** | You read it in the code or a document | "Sessions are JWT in an httpOnly cookie (verified, `src/lib/auth/session.ts`)" |
| **ran** | You executed something and saw the result | "The partner API returns 500 items per call on the free tier (ran, spike 2026-03-02)" |
| **inferred** | Reasoned from structure without confirming | "Feed reads appear uncached (inferred: no cache import; edge layer not checked)" |
| **assumed** | A default you chose. Has an `A-##` | "A-03: single region is enough" |
| **unknown** | Could not be determined. Has a `Q-##` | "Q-01: whether the mobile client pins an API version" |

In the documents themselves the label lives in the grammar: verified and ran are stated flatly, inferred keeps its hedge, assumed and unknown carry their IDs. Never upgrade a label by rewording. It moves up when you read the file or run the command.

A plan made mostly of inferred and assumed lines is a first draft, whatever its formatting.

## The reply

Each playbook ends with its own **Reply** line. All of them share this frame:

```
GOAL        one sentence: what was asked, restated
PRODUCED    the documents, and where they live
DECISIONS   the three that most shape the build, each with its reason
PROOF       the ladder: rung, result. n/a rungs listed with reasons
UNVERIFIED  what the plan still rests on that is inferred or assumed
OPEN        every Q-##, who answers it, what it blocks
NEXT        one action
```

Do not summarize the documents back. The user can read them. The reply is for what is not in them: what was checked, what was not, and what to do first.

## Decision log

For long or unattended planning, and whenever the user asks for a trail, append one line per decision to `docs/decision-log.tsv`:

```
ts	phase	decision	why	evidence	result
2026-03-02T14:10Z	design	Postgres over Mongo	data is relational, team has run it	ADR-0001	kept
2026-03-02T15:40Z	spike	batch import, not per-row	partner API allows 500 per call	spike: 500 returned in 1.2s	kept
```

Log choices between real alternatives, reversals, and anything a reviewer would ask "why" about. A decision reversed later gets a new line that points at the old one.

## When a check fails

Suspect the plan before the script. Then fix the cause: a missing path means the code was not read, an empty "Wrong means" means the assumption was not thought through, a phase with no check means nobody knows what done looks like. Rewording the line until the script passes leaves the cause in place.

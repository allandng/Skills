### Backfill

**You own an honest description of a system you did not design, with what you did not read stated.**

For a codebase that works and has no documents. The bundle describes what is, not what should be.

1. Step 0 from `SKILL.md`. Existing docs get amended, never regenerated.
2. `python scripts/survey_repo.py <repo>`, then read: the entry point, one vertical slice per major feature, the schema and migrations, the tests, deployment config.
3. Write the evidence ledger for the whole system, and state coverage: which modules you read, which you did not.
4. Pick the tier from what exists, and say which.
5. Write in dependency order: data model from the schema, flows from the routes and handlers, system design from the wiring, product requirements last - inferred from behaviour and marked as inferred until the user confirms them.
6. Record decisions you can see but cannot explain as `Q-##` with "why was this chosen" and who would know. Do not invent a rationale. An ADR written after the fact says so in its Context.
7. Mark each requirement's status in the traceability matrix from the code: Built, Partial, or Not found.
8. Ground it: `python scripts/verify_plan.py <doc> <repo>` on every document that names files, then `python scripts/check_docs.py docs/`.
9. Write `00-orientation.md` last, including how to run the project - and run it, or say that you did not.

**Reply:** what was read and what was not, the tier, the documents written, how many requirements are inferred and awaiting confirmation, the decisions nobody could explain, both script results, and whether the run instructions were tried.

# Mode: /addon

A feature goes into a program that already exists. Two jobs, in this order:

1. **Fit** - the feature has to belong to this program, built the way this program is built.
2. **Containment** - what gets built has to be what was asked for, and nothing else.

The plan this mode produces is usually handed to an implementing agent - Claude Code, or a teammate prompting one. So the plan is not a description. It is a **contract**: an allowlist of what may be touched, a list of what must not happen, and a set of claims about the codebase that have all been verified. Anything left vague in the plan becomes something invented at implementation time.

## The three failure modes

**Invented ground.** The plan names a file, function, table, column, or endpoint that does not exist - a plausible `src/services/authService.ts` in a repo that keeps auth in `lib/auth/`. The implementing agent takes the plan as fact and builds against a foundation that was never there. This is the most damaging failure, because everything downstream inherits it and it surfaces late. Countered by the evidence ledger in Step 1 and `verify_plan.py` in Step 8.

**Silent expansion.** The feature arrives with a refactor. A renamed function, a new dependency, a reformatted file, an "improved" error handler, a fix for something unrelated noticed in passing. Every item is defensible alone. Together they are a diff nobody asked for, that nobody can review, and that cannot be reverted without also reverting the feature. Countered by the scope fence in Step 3.

**The parallel universe.** The feature is correct by its own standards and foreign to this codebase - a second HTTP client, a different error convention, a new state library beside the existing one, a naming scheme nobody else uses. The result is a codebase that needs two mental models. Countered by the conventions ledger in Step 1.

---

## Step 1 - Survey, read, and write down what you actually know

Run the script first. Asking someone which framework their own repo uses wastes their time and signals you did not look.

```bash
python scripts/survey_repo.py <path-to-repo>
```

Read the whole JSON. Then read real code - the survey tells you where to look, not what it does:

- The **entry point** and what it wires up. This is where the real architecture lives, not in the folder names.
- The **module closest to the new feature.** You are going to imitate it, so read it properly.
- One **complete vertical slice** of an existing feature, end to end - route, handler, service, data access, test. This reveals the layering the team actually uses, which is often not the layering the directory structure advertises.
- **Schema and migrations.** Naming style, key strategy, soft deletes, timestamps, whether relationships are enforced by foreign keys or only in application code.
- **Tests.** Structure, what gets mocked, how fixtures work, how they run.
- **Config and secrets.** How environment values reach the code.
- **Error handling and logging.** Find the pattern once, reuse it everywhere.

### The evidence ledger

Write this before planning anything. It is the difference between a plan and a guess.

```
VERIFIED    read directly. path, and what it confirmed.
            src/lib/auth/session.ts - sessions are JWT in an httpOnly cookie,
            validated in middleware.ts, no refresh token
INFERRED    concluded but not confirmed, with the basis.
            feed reads appear uncached - no cache import in the feed handlers,
            but I did not check for an edge layer
UNKNOWN     matters and could not be determined. becomes Q-##.
            Q-01 whether the mobile client pins an API version
```

Three rules make this ledger do real work:

1. **Verified and inferred get different grammar.** Verified facts are stated flatly: "sessions are JWT in an httpOnly cookie." Inferred ones keep the hedge in the plan itself: "feed reads appear to be uncached." An implementing agent cannot tell the difference unless you leave it in the text.
2. **Nothing inferred may appear in the allowlist.** You either opened the file or you do not list it as one the implementation may touch. This is what stops a plausible-but-wrong path from propagating.
3. **When the ledger is thin, say so** rather than padding it. "I read the auth module and one API route; I have not read the worker" is a useful sentence. A confident plan built on two files is not.

### The conventions ledger

What the codebase has already decided. Keep it short - it is the reference you check every plan step against.

```
LANGUAGE / RUNTIME    versions, and anything unusual about them
LAYERING              the real path a request takes, in order
NAMING                files, symbols, database objects, routes
ERRORS                how failures are represented and surfaced
STATE / DATA ACCESS   client and server - the library and the pattern
TESTS                 framework, layout, what is mocked, how to run them
STYLE / TOOLING       formatter, linter, type strictness, CI gates
DEVIATIONS            places the codebase already contradicts itself
```

The last line matters. When a codebase has two competing patterns, follow the one in the most recently touched code, say that is what you did and why, and do not use the addition as an excuse to unify them.

**Conform to what exists, even where you would have chosen differently.** If a convention is genuinely harmful - a security hole, or something that makes the feature impossible - say so plainly and write it up as a separate proposal. Never fix it quietly inside a feature diff. A reviewer who opens a pull request expecting a feature and finds a refactor cannot review either one.

---

## Step 2 - Interview, narrowly

You already know the stack. Ask only about intent. One round, five questions maximum.

1. What should a user be able to do after this ships that they cannot do now? *(behaviour, not implementation)*
2. Who is it for - all users, a subset, admins, another service?
3. Is there an existing feature it should behave and feel like?
4. Any hard constraint: a deadline, an external API and its plan tier, a cost ceiling, a schema you cannot alter, a dependency you cannot add?
5. Does existing data need to change or be backfilled? *(default: assume yes if you are adding a non-nullable column or a required relationship, and confirm)*

Ask about the **edges of the request**, not just its centre. "Should this send a notification?" and "should this show up in search?" are the questions whose unasked answers become invented features later. Where the user has not said, the answer is no, and it goes in Out of scope.

---

## Step 3 - Draw the scope fence, then stop

This is the gate. Produce the fence and **wait for the user to confirm or correct it before planning anything further.** It is short, it costs one round trip, and it is the cheapest place available to catch a misread request. A misunderstanding caught here costs a sentence; caught after implementation it costs the diff.

```
IN SCOPE
  1. <behaviour the change delivers>
  2. ...

OUT OF SCOPE
  <thing a reader might reasonably expect and will not get>  - revisit when <condition>

MAY TOUCH
  <path>  - <why this file changes>
  ...
  Nothing outside this list. If implementation reveals another file must
  change, stop and amend the plan.

WILL CREATE
  <path>  - <why here, matched against where comparable files already live>

WILL NOT
  - add dependencies beyond: <named list, or "none">
  - rename or move existing symbols or files
  - reformat, restyle, or lint-fix code outside the diff
  - change schema beyond the named migration
  - alter existing tests except to extend them
  - fix unrelated problems noticed along the way - log them instead
```

Notes on filling it in:

**Out of scope is the load-bearing half.** In scope constrains what gets built; out of scope constrains what gets *added on top*. The entries worth writing are the ones a reasonable implementer would assume: notifications, analytics events, an admin view, search indexing, an undo, rate limiting, caching. Each one you name is one that cannot show up as a surprise.

**MAY TOUCH is an allowlist, not an estimate.** Every path on it was read in Step 1. Every path carries a reason. When implementation hits a file that is not on the list, the correct move is to come back and amend the fence - not to widen it quietly, and not to work around it.

**WILL NOT is boilerplate on purpose.** These are the standing prohibitions that get violated by default, and their value is being written down somewhere an implementing agent will read them.

**Unrelated problems get logged, not fixed.** Keep a short `NOTICED` list of things worth doing that are not this change. It is how you stay disciplined without losing the observation.

If the user says to skip the gate and plan it all in one pass, do that - and mark the fence **unconfirmed** in the document. The artifact stays honest about what was agreed and what was assumed.

---

## Step 4 - Locate the seam

Now say where the change goes, concretely - real paths, real module names, every one of them from the verified ledger.

```
TOUCHES        files that change, one line of reason each  (matches MAY TOUCH)
ADDS           new files and where they sit                (matches WILL CREATE)
DATA           tables, columns, indexes, migrations - new or changed
INTERFACES     endpoints, events, jobs, or public functions added or changed
DEPENDENCIES   new packages, and why the standard library or an existing
               dependency will not do
CONFIG         new environment variables, secrets, feature flags
```

Check placement against the conventions ledger. If a new file does not sit where a comparable existing file sits, either you have the wrong location or you have found an inconsistency worth naming.

Every new dependency needs an argument, and "it is the popular choice" is not one. A dependency added to a codebase is permanent in practice, and this is the step where an addition quietly acquires three of them.

---

## Step 5 - Two or three options, ranked

One option is not a plan, it is a preference. Three is usually the ceiling before comparison stops helping.

Each option must differ in **approach**, not in naming. A useful spread: the minimal change that fits the current design; the more general change that costs more now and less later; and the one that avoids building it at all by using a service, a library, or a mechanism the codebase already has.

| | Option A | Option B | Option C |
|---|---|---|---|
| Approach | | | |
| Effort | | | |
| Files touched | | | |
| Migration needed | | | |
| Reversible? | | | |
| New dependencies | | | |
| Ongoing cost | | | |
| Fits existing patterns | | | |
| Fails when | | | |

The last row does the real work. Every approach has a condition under which it becomes the wrong choice - scale, a pricing tier change, a requirement arriving next quarter. Naming it is what lets someone revisit the decision later with information instead of instinct.

The recommendation is one paragraph: which one, the single reason it wins here, and what would have to be true for another option to win. That paragraph becomes the ADR.

---

## Step 6 - Blast radius

Everything the change can break, including what is not in the diff.

```
DIRECT          code that calls, or is called by, what you are changing
DATA            queries, reports, or jobs reading affected tables; existing rows
                that would violate a new constraint
CONTRACTS       API consumers, mobile clients on older versions, webhooks, exports
PERFORMANCE     new N+1s, unindexed lookups, latency added to a hot path,
                a migration that locks a large table
SECURITY        new inputs, new permissions, newly stored data, new external calls
OPERATIONS      new failure modes, alerts needed, new cost lines
ROLLBACK        exactly how to undo it, and whether the migration reverses
```

The two most commonly missed: **old clients** - an app already installed on a phone does not update because you deployed, so contract changes must be additive - and **existing rows**, which will not satisfy a new constraint just because new rows do.

If rollback is not clean, say so loudly and design a way to make it clean, usually a feature flag or an expand-then-contract migration.

---

## Step 7 - Phase it

Each phase ships on its own, reviews on its own, and reverts without unwinding earlier ones.

```
P-01  <name>
      Does            what works at the end of this phase
      Touches         files, all of them from MAY TOUCH
      Verified by     T-##, plus the manual check if there is one
      Reverts by      the specific undo
      Blocked by      nothing, or P-0N
```

Sequencing rules that hold nearly always:

1. **Schema before code.** An additive migration deploys and waits harmlessly ahead of the code that uses it.
2. **Expand, migrate, contract.** Add the new thing, move the reads and the data, then remove the old thing - three deploys. Never add and drop in the same one.
3. **The uncertain part goes first.** If a third-party API might not do what its documentation claims, find out in P-01 with a throwaway spike, not in P-04 with the plan built on top of it.
4. **Flag anything user-visible and non-trivial.** It turns a rollback from a deploy into a config change.

---

## Step 8 - Verify grounding, then hand off

Before delivering, check that the plan does not assert anything untrue. This is a mechanical step - do not skip it on the grounds that you were careful.

```bash
python scripts/verify_plan.py <plan.md> <path-to-repo>
```

It pulls every file path and code symbol out of the plan and checks them against the repo, separating what exists, what is marked new, and what is neither. Anything in that last group is either a typo or something you invented. Fix it before the plan goes anywhere - and when a path turns out not to exist, go back and read, rather than swapping in another guess.

Then do a pass by hand for what a script cannot see:

- Every claim in the plan's declarative voice traces to a **VERIFIED** ledger entry. Anything from **INFERRED** still carries its hedge.
- Every path in TOUCHES appears in MAY TOUCH, and the reverse.
- No step quietly does something on the WILL NOT list.
- Every `Q-##` that blocks a phase is named in that phase.

### Doc delta

Say precisely which documents change. Skipping this is exactly how documentation stops being true, and docs that are wrong are worse than none, because people believe them.

- `03-data-model.md` - new entities in the ERD, new fields in the dictionary, migration note
- `04-flows.md` - a new `UC-##`, and a sequence diagram if the flow crosses a boundary
- `02-srd.md` - new `SR-##` entries, new interface contracts, updated container diagram
- `01-prd.md` - a new `PR-##` if this is user-facing product scope
- `06-traceability.md` - new rows linking the chain
- `adr/000N-*.md` - the decision from Step 5, written up properly
- `00-orientation.md` - only if the change alters how someone gets the project running

If no planning docs exist, do not silently generate the full bundle. Write the ADR and a single `docs/addons/<feature>.md`, then tell the user that `/start` can backfill the rest for the existing system - and that it is worth doing if more than one person will touch this code.

### Deliver

- The recommendation and its one-line reason
- The scope fence, restated compactly - it is the part the user most needs to have seen
- The phase list, one line each
- The blast radius items that need action, not the whole checklist
- Open questions, with who answers each
- A pull request description paragraph for the first phase
- An offer to write the implementation prompt for P-01 only, carrying the allowlist and the WILL NOT list verbatim

That last point is where this mode earns its keep. A prompt scoped to one phase, naming the files it may touch and the things it must not do, is the difference between an agent that implements the plan and one that improvises around it.

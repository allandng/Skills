# SWE Plan

Senior-architect planning system: interview to a full PRD/SRD/ERD bundle, or survey a repo and rank
an implementation plan.

```bash
/plugin install swe-plan@allan-skills
```

The framing is the senior engineer on a small team — the one who gets handed a half-formed idea or
an unfamiliar repo and comes back with a plan the rest of the team can actually build against.

---

## Modes

| Mode | Trigger | Output |
|---|---|---|
| **`/start`** | New project, greenfield, "where do I begin", "write a spec for X" | A structured interview, then a full planning bundle in `docs/` |
| **`/addon`** | An existing program plus a feature to add — also integrations, refactors, "how do I add X to this" | Codebase survey, a confirmed scope fence, ranked options, a phased plan, and a doc delta |

Routing is on intent, not the literal slash command. "I want to build a habit tracker" is `/start`.
"I want to add push notifications to my habit tracker" is `/addon`.

### `/addon` doubles as a contract

Its output usually gets handed to an implementing agent, so beyond planning it produces an allowlist
of files that may be touched, an explicit list of things that must not happen, and a set of claims
about the codebase that have all been verified against real code.

That's what keeps a feature request from coming back as a feature plus a refactor plus two
dependencies plus a rename — and what keeps the plan from confidently naming a file that was never
there.

---

## Playbooks

Both modes, and six smaller jobs, are step lists in `playbooks/`. The agent copies the matching list
into its todo list and works it in order. A step that does not apply keeps its line with
`n/a: <reason>`, so a skipped step and a forgotten one never look the same. Each ends with a stated
reply.

| Playbook | Use it when | Produces |
|---|---|---|
| **start**, **addon** | The two modes above | As above |
| **spike** | The plan depends on something nobody has tried | The question, the command that was run, what it printed, and what the plan now does because of it |
| **decide** | One hard choice | An ADR with the rejected options and a condition for reopening it |
| **review** | A plan should be attacked before anyone builds on it | Findings that reviewers with different positions could point at, and a count of what was dropped |
| **backfill** | A working codebase has no documents | A bundle describing what is there, with what was not read stated |
| **amend** | The code moved and the docs did not | Documents made true again, decisions superseded, questions closed |
| **handoff** | An approved plan needs building | A prompt for one phase that carries the allowlist and the prohibitions verbatim |

### Proof before handover

A plan is finished when it has been checked, not when it has been written. `references/proof.md` is
the ladder: structure, rigor, grounding, the addon contract, a falsifiability pass (name one thing
in each document an engineer could reject), a cold read by someone who was not in the conversation,
anything that could have been run, reversibility, and drift. Every claim is marked stated, verified,
ran, inferred, assumed, or unknown.

`references/principles.md` has one rule per situation. The playbook form, the proof discipline, the
review panel, and most of those rules are adapted from
[pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan (MIT), whose author does
not believe in planning: "the best spec is code." This skill mostly agrees, which is why `spike`
exists and why every phase has to end in something that can be run.

---

## The document bundle

`/start` produces this. `/addon` amends it.

```
docs/
├── 00-orientation.md      What this is, how to run it, where things live, current status
├── 01-prd.md              Problem, users, jobs, scope, product requirements (PR-##), metrics, non-goals
├── 02-srd.md              Architecture, components, interfaces, NFRs (NFR-##),
│                          system requirements (SR-##), context and container diagrams
├── 03-data-model.md       ERD, entity dictionary (E-##), lifecycle state machines, migration notes
├── 04-flows.md            Use case diagram (UC-##) and a sequence diagram per critical flow
├── 05-delivery-plan.md    Phases (P-##), work breakdown, definition of done, risks (R-##), test plan (T-##)
├── 06-traceability.md     PR → SR → component → test matrix, open questions, assumptions
└── adr/
    └── 0001-<slug>.md     One file per decision, numbered, never deleted — superseded instead
```

Every document carries a status header (`Draft | In review | Approved | Superseded by …`), an owner,
and a date. A doc with no status gets read as truth even when it was a first draft.

`00-orientation.md` is the front door — the one page a new teammate reads first. It's written last,
once the rest exists, so it reflects reality.

The ID scheme is the point: `PR-##` → `SR-##` → component → `T-##` is a chain you can actually
follow, and `06-traceability.md` is what makes a gap in it visible.

---

## Scripts

Standard library only, Python 3.11+. No installs.

| Script | What it does |
|---|---|
| `scripts/survey_repo.py` | Reads a codebase and prints JSON: detected stack and manifests with dependency lists, language breakdown by LOC, directory tree, entry points, test layout, migrations and schema files, infra and CI files, route hints, git activity |
| `scripts/verify_plan.py` | The anti-hallucination check — pulls every file path and function-like symbol out of a plan and checks them against the real repo |
| `scripts/check_addon.py` | The contract check - does an `/addon` plan agree with itself? The allowlist only names files that were read, the seam and every phase stay inside it, every phase has a check and an undo |
| `scripts/check_docs.py` | Lints a finished bundle for the things that silently rot, and for rigor: numbers, acceptance criteria, owners, phase checks, rejected options |
| `scripts/doc_drift.py` | Finds documents the code has moved past, from each document's Updated date and git history |

```bash
python scripts/survey_repo.py <path-to-repo> --max-depth 4 --top 30
```

Run it at the top of `/addon`. It never fails hard — anything it can't read comes back as a note in
the JSON, so partial results are still usable.

```bash
python scripts/verify_plan.py docs/addons/<feature>.md <path-to-repo>
```

Sorts every claim into what exists, what the plan declares as new, and what is neither. That last
bucket is either a typo or an invention, and it's the thing an implementing agent will build against
without noticing. Non-zero exit when a path is missing.

```bash
python scripts/check_docs.py docs/
```

Checks that every `PR-##` is covered by at least one `SR-##`, that no requirement is referenced but
never defined, that the traceability matrix matches the documents, that relative links resolve, that
every doc has a status header, and that Mermaid blocks are well-formed. Non-zero exit on errors, so
it drops into CI as-is.

It also fails a bundle on the parts a plan can leave out and still look finished: an `NFR-##` whose
target has no number or no way to measure it, a `PR-##` with no acceptance criterion, an `A-##` that
does not say what breaks if it is wrong, a `Q-##` nobody owns, a phase with no check or no undo, and
an ADR with no rejected option. `--no-rigor` skips these for a bundle written before the rules.

```bash
python scripts/check_addon.py docs/addons/<feature>.md <path-to-repo>
```

`verify_plan.py` asks whether everything a plan names exists. This asks whether the plan agrees with
itself. It fails when MAY TOUCH lists a file that is not in the VERIFIED ledger, when the seam or a
phase reaches outside the fence, when Out of scope is empty, when an option has no failure
condition, or when there is no rollback.

```bash
python scripts/doc_drift.py docs/ <path-to-repo>
```

Lists, per document, the files it names that changed since its Updated date and the ones that no
longer exist. It finds where to look. Whether the change mattered is a judgment.

---

## How the pieces chain

```
/start                              /addon
   │                                   │
   ├─ interview                        ├─ survey_repo.py      ← read before opining
   │                                   ├─ scope fence          ← confirmed with you
   ├─ docs/ bundle                     ├─ ranked options
   │                                   ├─ phased plan + blast radius
   │                                   ├─ verify_plan.py       ← every claim checked
   │                                   ├─ check_addon.py       ← the plan agrees with itself
   │                                   └─ doc delta            ← amends docs/
   ▼                                   ▼
        check_docs.py  →  00-orientation.md  →  handoff summary
```

Both modes end the same way: run `check_docs.py` and fix every error, write `00-orientation.md`
last, then deliver a handoff summary in chat — what got produced, the three decisions that most
shape the build, every open question with who needs to answer it, and one recommended next action.
There's also a PR-description version on request, a paragraph you can paste into a pull request or
Slack so teammates get the change without opening the docs.

### References

`references/start-mode.md` and `references/addon-mode.md` are the full playbooks — the SKILL.md
routing table is deliberately not enough to improvise from. `references/document-templates.md` has
exact templates for every document, and `references/diagrams.md` has Mermaid recipes for ERD, use
case, sequence, state, context, and deployment diagrams.

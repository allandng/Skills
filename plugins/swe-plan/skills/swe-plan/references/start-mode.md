# Mode: /start

Greenfield. An idea, a rough description, or a blank repo, and you come back with a plan a team can build against.

The failure mode here is the **plausible spec**: a document that is well-organized, correctly formatted, and describes a generic app. It has users who "want a great experience," requirements like "the system shall be scalable," and an ERD with a `users` table and a `posts` table. It could belong to any project. It survives review because there is nothing to disagree with, and it helps nobody, because every real decision is still unmade.

The test for whether a spec is real: **can a competent engineer disagree with it?** If nothing in the document is falsifiable, contested, or specific enough to be wrong, it is not a spec.

---

## Step 1 - Interview

Four rounds. Batch them, default them, echo back after each. See the interview protocol in SKILL.md for the rules.

Skip any question the conversation, the attached files, or memory already answers - and say that you are skipping it, so the user knows you were paying attention.

### Round 1 - Problem and people

1. In one or two sentences, what is this and who is it for?
2. What does that person do today instead? What is the workaround they already have? *(This is the most valuable question in the interview. A product with no current workaround usually has no current problem.)*
3. What is the single moment where the product proves its worth - the thing that, if it works, the user comes back?
4. How many people use this in six months if it goes well? *(default: hundreds, not millions - it changes almost every architecture answer)*
5. Is this a business, a portfolio piece, a class project, or an internal tool? *(default: ask, do not assume - it sets the whole quality and documentation bar)*

### Round 2 - Scope and shape

1. Name three things it does. Then name three things it explicitly will not do. *(The non-goals are load-bearing - they are what stops scope creep six weeks in.)*
2. What is the smallest version that is still worth using? *(default: single-user, no auth, one core flow)*
3. Platform: web, mobile, desktop, CLI, service or API, or several? *(default: responsive web)*
4. Is there a stack you already know or already committed to, or is it open? *(default: what memory shows the user already ships in)*
5. Does it need accounts and login on day one? *(default: yes if data is per-person or shared, no otherwise)*

### Round 3 - Data and flows

1. What are the main things the system stores? List the nouns. *(A user saying "recipes, cooks, friends, ratings" has just given you the ERD.)*
2. Which of those do users create, and which come from somewhere else - an import, a scrape, an API, a seed file?
3. Walk me through the single most important thing a user does, tap by tap.
4. Does anything need to happen without a user present - scheduled jobs, notifications, background processing, webhooks? *(default: no on day one)*

### Round 4 - Constraints and delivery

1. Who is building it, and what do they already know? *(A plan a solo junior can ship beats an elegant plan that needs three specialists.)*
2. Is there a deadline or an event this has to be ready for?
3. Budget for infrastructure per month? *(default: free tier or under $20)*
4. Any hard requirements from outside - a school rubric, a client, an app store, privacy or compliance rules, an existing system it must talk to?
5. Which matters more if you have to choose: ship it fast, or build it to last? *(default: ship fast, structured so the load-bearing parts can be replaced)*

### Before leaving the interview

Pick a tier - Sketch, Standard, or Large - and say which and why. Then say: "Here's what I'm assuming where you didn't specify," and list the assumptions with IDs. Give the user a chance to correct them before you write 3000 words on top of a wrong one.

---

## Step 2 - Design before you document

Do this thinking before writing any document. Writing formats thinking; it does not replace it.

**Draw the boundary.** What is inside the system, what is outside it, who talks to it. Everything else follows from this line.

**Find the entities and their relationships.** From the nouns in Round 3. For each: what identifies it, what it belongs to, what its lifecycle is. Most data model mistakes are relationship cardinality mistakes made early - a one-to-many that is really a many-to-many costs a migration and a week.

**Pick the architecture, then argue against it.** Choose the boring option that fits the team and the scale, then spend a minute steelmanning the alternative. If the alternative wins, take it. If it does not, you now have your first ADR written for free.

**Find the risky part.** Every project has one thing that is genuinely uncertain - a third-party API that may not do what the docs claim, a performance requirement nobody has measured, an integration nobody has tried. Name it. It goes in Phase 1, not Phase 4. Discovering in week six that the core assumption was wrong is the most expensive failure available.

**Sanity-check against the counterexample.** Would this same architecture come out of a completely different brief in the same category? If yes, you have described a template, not this system. Go back and find what is actually specific about this one.

---

## Step 3 - Produce the bundle

Write in this order, because each one depends on the previous. Templates are in `references/document-templates.md`; diagram recipes are in `references/diagrams.md`.

| Order | File | Must contain |
|---|---|---|
| 1 | `01-prd.md` | Problem, current workaround, target user, jobs to be done, `PR-##` requirements each with a priority and an acceptance criterion, success metrics with numbers, explicit non-goals |
| 2 | `04-flows.md` | Use case diagram covering every actor, `UC-##` entries with main and alternate paths, one sequence diagram per critical flow |
| 3 | `03-data-model.md` | ERD in Mermaid, entity dictionary with `E-##` and field-level types and constraints, state machines for anything with a lifecycle, indexing and migration notes |
| 4 | `02-srd.md` | Context and container diagrams, component responsibilities, interface and API contracts, `SR-##` requirements traced to `PR-##`, `NFR-##` with measurable targets, deployment diagram, security and privacy |
| 5 | `05-delivery-plan.md` | Phases `P-##` each independently shippable, work breakdown, definition of done, `R-##` risks with mitigations, `T-##` test plan |
| 6 | `06-traceability.md` | The matrix, plus all `A-##` assumptions and `Q-##` open questions in one place |
| 7 | `adr/000N-*.md` | One per real decision made along the way |
| 8 | `00-orientation.md` | Written last. The front door. |

### Which decisions deserve an ADR

Write one when the decision is expensive to reverse, when a reasonable engineer would have chosen differently, or when you can already hear someone asking "why did you do it *that* way." Typical: database choice, auth approach, monolith versus services, sync versus async processing, hosting, state management, whether to build or buy something.

Do not write one for choices with no real alternative or no consequence. Three good ADRs are worth more than twelve that record which linter you used.

### Requirements that are worth writing

A requirement earns its place by being testable.

- Weak: *The system shall be responsive and user-friendly.*
- Real: **PR-04** - A logged cook appears in the friend feed within 5 seconds of saving, on a 4G connection. Priority: Must. Verified by **T-07**.

Every `PR-##` needs a priority (Must, Should, Could, Won't-this-release) and an acceptance criterion someone could actually check. If you cannot write the acceptance criterion, the requirement is not understood well enough to build - make it a `Q-##` instead of dressing it up.

---

## Step 4 - Hand off

Run `python scripts/check_docs.py docs/` and fix every error.

Then deliver in chat, briefly:

- What you produced and where it lives
- The three decisions that most shape the build, one line each
- Every `Q-##`, with who needs to answer it and what it blocks
- The single recommended next action - usually the Phase 1 spike on the risky part
- An offer: the PR-description paragraph, or a Claude Code kickoff prompt built from `05-delivery-plan.md`

Do not summarize the documents back at length. The user can read them. The value of the summary is the part that is *not* in them: what you would do first.

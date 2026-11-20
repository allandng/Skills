# Principles

One rule each, with the moment it applies. They are not read up front. When a planning decision is hard, find the principle whose trigger matches. In the reply, name any principle that changed a decision and say what it changed.

The shape, and most of the rules, are adapted from pstack by Lauren Tan (MIT), restated for planning. pstack's author does not believe in planning: "the best spec is code." This skill agrees more than it disagrees. A plan here exists to record why, to fence scope, and to put the uncertain part first - not to stand in for running something.

## Before writing

- **Attack the premise.** Starting any plan. Ask what the user does today instead. A product with no current workaround usually has no current problem, and a feature nobody would miss does not need a design.
- **Settle it by running.** A plan is about to depend on something nobody has checked. Run a spike (`playbooks/spike.md`). An hour of throwaway code beats a paragraph of confident reasoning, and a wrong core assumption found in week six is the most expensive failure available.
- **Foundational thinking.** Before any document. Get the boundary and the data model right first: entities, identity, ownership, cardinality, lifecycle. Most of the plan follows from them, and a one-to-many that is really many-to-many costs a migration.
- **Find the counterexample.** The design is done. Would the same architecture come out of a different brief in the same category? If yes, it is a template. Find what is specific to this one.
- **Do not block on what can be defaulted.** Tempted to ask another question. Give it a default, record it as `A-##` with what breaks if it is wrong, and keep going. Stop only for what cannot be defaulted or undone.

## Scope

- **Subtract before you add.** Sizing the plan. Cut requirements, documents and phases before adding any. Non-goals are the load-bearing half of scope, and the smallest tier that fits is the right one.
- **The smallest change that solves it.** Ranking options. One option is always the minimal change that fits the current design. It wins unless you can name what it fails at.
- **Conform, then propose.** The codebase does something you would not have chosen. Follow it inside the feature. Raise the change as its own proposal. A reviewer cannot review a feature and a refactor in one diff.
- **Log it, do not fix it.** Something unrelated is wrong. It goes on the NOTICED list.

## Structure

- **Model the domain.** Anything with a lifecycle or more than two conditions. Draw the state machine, name the states, and say which transitions are illegal. A `status` column with no diagram is a bug waiting for its second developer.
- **Guard the boundary.** Designing interfaces. Say where input is validated and trusted. Contracts that outside clients depend on change additively: an installed app does not update because you deployed.
- **Make it safe to repeat.** Planning migrations, jobs, webhooks, retries. Each one reaches the same end state if it runs twice or dies halfway. Say how.
- **Migrate, then delete.** Replacing something. The plan names when the old thing is removed and what proves nothing still calls it. "Later" is how a codebase ends up with two of everything.

## Delivery

- **Sequence verifiable units.** Phasing. Each phase ends in a state that can be checked, by a named test or a command, and reverted without unwinding the ones before it.
- **The uncertain part goes first.** Ordering phases. Whatever might not work is P-01.
- **Say what can run in parallel.** Writing a delivery plan that agents or several people will execute. For each phase, state: what must finish before anything else starts, which workstreams touch disjoint files and can run at once, what state they share, and the smallest split that is safe. Shared state is split before it is serialized: two workers on two files beats two workers taking turns on one.
- **Explain the number.** Writing a target, an estimate or a result. Say what it measures, how, and what limits it. Estimates are ranges. A target without a number is not a requirement.

## Honesty

- **Never assert what you have not verified.** Writing any claim about the code. Read it, or keep the hedge in the sentence, or make it a `Q-##`.
- **Prove the plan holds.** About to hand a plan over. Run the checks (`proof.md`). "I was careful" is not a check.
- **Fix the cause, not the path.** `verify_plan.py` reports a missing file. Go back and read the code. Replacing one guess with another keeps the cause.
- **Encode the lesson.** The same correction a second time. Put it where it cannot be skipped: a rule in `check_docs.py`, a line in the WILL NOT list, a column in a template. A sentence in a document is the weakest place to keep a rule.
- **Write for the reader who was not there.** Every document. The teammate who joins on Tuesday, and the agent that will implement this without asking.

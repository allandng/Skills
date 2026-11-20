### Start

**You own a plan a competent engineer can disagree with. Interview, design, then document.**

1. Step 0 from `SKILL.md`: look for existing docs, check memory and the conversation, state the mode and why.
2. Interview in four rounds, seven questions at most per round, a default on every question (`references/start-mode.md`, Step 1). Echo back what changed after each round.
3. Pick the tier and say why. List the assumptions with `A-##` and give the user one chance to correct them before writing.
4. Design before documenting (`references/start-mode.md`, Step 2): draw the boundary, find the entities, pick the architecture and argue against it, name the risky part, run the counterexample check.
5. If the risky part can be settled by running something, run **spike** now. A plan built on an untested core assumption is a guess with formatting.
6. Write the bundle in the order in `references/start-mode.md`, Step 3. Templates in `references/document-templates.md`, diagrams in `references/diagrams.md`.
7. Give every phase a check and an undo. Write the throughput note for the delivery plan (`references/principles.md`, "Say what can run in parallel").
8. `python scripts/check_docs.py docs/` and fix every error. Resolve or explain each warning.
9. The falsifiability pass (`references/proof.md`): for each document, name one thing in it an engineer could reasonably reject. If there is none, the document is a template.
10. Write `00-orientation.md` last.

**Reply:** the tier and why, the three decisions that most shape the build, every `Q-##` with who answers it and what it blocks, the `check_docs.py` result, what was assumed and not confirmed, and the single next action - usually the P-01 spike.

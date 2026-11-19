### Handoff

**You own a prompt that lets an agent implement one phase without improvising around the plan.**

1. Confirm the plan is ready to be built on: `check_docs.py` clean, and for an addon `verify_plan.py` and `check_addon.py` clean, the scope fence confirmed. If the fence is unconfirmed, say so at the top of the prompt.
2. Pick one phase. Never hand off the whole plan: an agent given five phases returns one large diff.
3. Check that nothing blocks it: every `Q-##` the phase names is answered, every phase it depends on is built.
4. Write the prompt from the plan, copying, not paraphrasing:

   ```
   GOAL          what works at the end of this phase, from "Delivers"
   WHY           the requirement IDs it covers, one line each
   MAY TOUCH     the allowlist, verbatim
   WILL CREATE   verbatim
   WILL NOT      verbatim
   CONVENTIONS   the conventions ledger
   FACTS         the VERIFIED entries this phase relies on. Inferred ones
                 stay marked inferred: check before relying on them
   DONE WHEN     "Verified by" and "Done when", as commands where possible
   UNDO          "Reverts by"
   STOP IF       a file outside the allowlist needs to change, a fact above
                 turns out to be wrong, or a check cannot be made to pass
                 without touching a test. Stop and report. Do not widen.
   REPORT        what changed, the output of each check, anything noticed
                 and not fixed
   ```

5. Say what can run in parallel and what cannot (`references/principles.md`, "Say what can run in parallel").
6. If the `askillissue` plugin is installed, name the playbook the phase maps to - feature, bug fix, refactoring, prototype - so `/askillissue:allan-mode` starts from the right one. If the phase is a screen or a flow and `design-suite` is installed, hand the flow and data-model documents to `ui-ux-studio` first (`references/help.md`, "Chaining").
7. When the phase comes back: check the diff against MAY TOUCH, rerun the phase's checks yourself, then run **amend**.

**Reply:** the prompt, ready to paste, the phase it covers, what it is blocked by if anything, and what to run when the work comes back.

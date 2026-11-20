### Addon

**You own a contract. What gets built is what was asked for, built the way this codebase builds, on ground you have read.**

1. Step 0 from `SKILL.md`: existing docs, memory, state the mode.
2. `python scripts/survey_repo.py <repo>` and read the whole output. Then read real code: the entry point, the nearest module, one full vertical slice, schema, tests, config, error handling (`references/addon-mode.md`, Step 1).
3. Write the evidence ledger and the conventions ledger before planning anything. Verified facts are stated flatly, inferred ones keep their hedge, unknowns become `Q-##`.
4. Interview narrowly: one round, five questions, about intent and the edges of the request.
5. Draw the scope fence and **stop until the user confirms or corrects it**. If they say to skip the gate, mark the fence Unconfirmed and continue.
6. Locate the seam. Every path comes from the VERIFIED ledger.
7. Rank two or three options that differ in approach, each with a "Fails when". If the choice turns on something you could measure or try, run **spike** before recommending.
8. Blast radius, including old clients, existing rows, and exactly how to roll back. Name the one fact the change is safe because of, and check it against the code.
9. Phase it: each phase ships, verifies and reverts on its own. The uncertain part goes first.
10. Ground it, both ways:

    ```bash
    python scripts/verify_plan.py <plan> <repo>     # does everything named exist?
    python scripts/check_addon.py <plan> <repo>     # does the plan agree with itself?
    ```

    A path that turns out not to exist means going back to read. Do not swap in another guess.
11. Write the doc delta, and the ADR for the option chosen.

**Reply:** the recommendation and its one reason, the scope fence restated and whether it was confirmed, the phases in one line each, the blast radius items that need action, both script results, open questions with owners, and an offer to run **handoff** for P-01.

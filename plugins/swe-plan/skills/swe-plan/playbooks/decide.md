### Decide

**You own one decision and the reasons the other options lost.**

1. State the decision as a question with a deadline: what must be chosen, and what is blocked until it is.
2. Check whether it deserves a record (`references/start-mode.md`, "Which decisions deserve an ADR"): expensive to reverse, or a reasonable engineer would choose differently. If neither, decide in a sentence and move on.
3. List two or three options that differ in approach. Include the one someone will ask about later, even if it loses quickly.
4. For each: what it costs now, what it costs later, what it closes off, and the condition under which it becomes the wrong choice.
5. Separate what you know from what you think. Mark each supporting claim verified, ran, inferred or assumed (`references/proof.md`). If the decision turns on an inferred claim you could test, run **spike** first.
6. Choose. One paragraph: which, the single reason it wins here, and what would have to be true for another to win.
7. Write the ADR from the template in `references/document-templates.md`: every rejected option carries "Rejected because", and "Revisit when" names a concrete condition.
8. Thread it: the decisions table in `06-traceability.md`, and every `SR-##` or `E-##` it affects.
9. `python scripts/check_docs.py docs/`.

**Reply:** the decision in one sentence, the reason, what was rejected and why, what it closes off, the revisit condition, and which claims behind it are not yet verified.

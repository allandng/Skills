### Amend

**You own the truth of the documents. A wrong document is worse than none, because people believe it.**

For after a phase ships, after a merge, or whenever someone asks whether the docs still hold.

1. Find where to look: `python scripts/doc_drift.py docs/ <repo>`. It lists, per document, the named files that changed since the document's Updated date and the named files that no longer exist.
2. For each flagged document, read the diff of each changed file since that date. Decide: the document is still true, or it is not.
3. Still true: bump the Updated date. That is a record that someone checked.
4. No longer true: amend the specific lines. Do not regenerate the document. Keep IDs stable: a requirement that changed keeps its number, one that was dropped is marked Won't with the reason, never deleted.
5. A decision that changed gets a new ADR that supersedes the old one, linked both ways. The old one is never edited into agreement.
6. Update the traceability matrix: phase status, new tests, and any `Q-##` that the work answered or `A-##` that the work confirmed or broke.
7. If the code now does something no document asked for, that is scope that arrived without a decision. Write the requirement it implies, or flag it to the user. Do not quietly document it as intended.
8. `python scripts/check_docs.py docs/`, then `python scripts/doc_drift.py docs/ <repo>` again. It should come back clean.

**Reply:** which documents were flagged, which were still true and which were amended, decisions superseded, questions closed, anything the code does that nothing asked for, and both script results.

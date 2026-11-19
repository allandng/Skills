### Teardown

**You own the structural description: what kind of app this is and how it is put together.**

1. Pick sources and say which (`references/app-dna.md`, "Sources"). A codebase and a running product together beat either alone.
2. From a codebase, `python3 scripts/route_inventory.py <source> --json > routes.json`.
3. Use the product. Do the core loop once, end to end, before describing anything.
4. Do the ten-step walk (`references/app-dna.md`), in the vocabulary of `references/app-taxonomy.md`.
5. For states, fill a row per screen family: exists, absent, or inconsistent. Where the route inventory shows a state file, that is `[measured]`. Where you triggered the state, `[observed]`.
6. Append the `Structure` block to `profile.md`, one evidence label per line, ending with `GAPS`.
7. Prove it: `python3 scripts/dna_check.py ./dna/<name> --structure`, and the `COVERAGE` line stating how many templates you actually opened.

**Reply:** the classification line, the shell and levels, the screen inventory by family, flows with step counts, the state table, `GAPS`, limits, and the `ui-ux-studio` playbook it feeds.

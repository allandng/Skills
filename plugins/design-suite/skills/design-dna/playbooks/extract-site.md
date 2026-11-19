### Extract a site

**You own an honest description of someone else's design, with its limits stated.**

1. Get the source. `python3 scripts/extract_style.py --url <url> --out ./dna/<name>`, or fetch and save the HTML and stylesheets and use `--dir` when the script has no network.
2. Decide coverage before reading: list the site's templates, pick which you will read, and write the `COVERAGE` line (`references/evidence.md`). One page is not a site.
3. Read what the script found. Declared custom properties are the system. Inferred roles are guesses until checked. Note dead tokens and the counts: shadows, weights, distinct spacing values.
4. Capture the page at 375, 768 and 1440 before forming an opinion.
5. Do the nine-step manual pass (`references/extraction.md`) and append the `Manual pass` block, one evidence label per line.
6. Name the style from mechanics (`references/style-taxonomy.md`), or say "no coherent system" and give the counts.
7. Prove it (`references/evidence.md`, "Proving an extraction"): `dna_check.py`, the round-trip specimen, `contrast.py`, three spot checks.

**Reply:** the frame in `references/evidence.md`. The system in five lines, proof, limits, and which `ui-ux-studio` playbook this feeds.

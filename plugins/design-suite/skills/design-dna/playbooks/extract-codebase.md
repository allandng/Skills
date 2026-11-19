### Extract a codebase

**You own what the source says, which is more than the rendered site shows and less than it does.**

1. Find where style lives: a token file, a Tailwind or theme config, CSS custom properties, a component library. That file is the declared system. Read it before running anything.
2. `python3 scripts/extract_style.py --dir <source> --name <name> --out ./dna/<name>`.
3. Compare declared against used. Tokens that are declared and never referenced are dead. Raw values in components that bypass the tokens are drift. Count both.
4. `python3 scripts/route_inventory.py <source>` for the screens and their file-level states.
5. Inventory the components by family with their variants (`references/app-taxonomy.md` §6). Flag accidental variants.
6. Run the product if you can and do the manual pass (`references/extraction.md`). If you cannot, the pass's observed lines become `[inferred]` and the reply says so first.
7. Write the `SOURCE` line with the commit.
8. Prove it (`references/evidence.md`).

**Reply:** the declared system, the drift and dead-token counts, the route and component inventories, proof, and whether the product was run or only read.

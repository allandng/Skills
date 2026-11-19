### Design system

**You own one source of truth. Every value in the product comes from it or is a named exception.**

1. Inventory what exists. For a codebase or live site, run the `design-dna` skill's extract: declared tokens, inferred roles, dead tokens, counts of distinct spacing values, radii, shadows and weights.
2. Inventory the components by family, with the variants of each (`references/app-taxonomy.md` §6). Mark accidental variants: same job, different look.
3. Decide the token layers: raw values, semantic roles, component tokens (`references/design-tokens.md`). Every chroma color gets a ramp. Dark is a second set of role values, never an inversion.
4. Map every existing value to a token or to the list of exceptions. The exceptions list is a deliverable.
5. Collapse accidental variants. Three button variants is a system. Nine is drift.
6. Give every interactive component its interaction states once: rest, hover, focus, pressed, disabled, busy.
7. Run `contrast.py` with the real pairs declared, on light and dark.
8. Migrate one component family at a time, and prove each with **visual-parity** where it must not change, or a before and after where it should.

**Reply:** the counts before and after, the token layers, the component inventory with variants collapsed, the exceptions list, contrast output, what remains unmigrated.

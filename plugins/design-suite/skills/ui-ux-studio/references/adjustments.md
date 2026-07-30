# Adjustments

"Make it softer." "Too blocky." "Bolder." "Quieter." These are the most common requests after a design exists, and none of them is a mode — re-running remix or variants for one is using a crane to move a chair. This is the playbook for amplitude changes to a design that stays.

Several principles here are distilled from Paul Bakaus's *impeccable* (its `bolder`/`quieter` dials), fitted to this skill's machinery.

## Ground rules, all verbs

- **Scope is sovereign.** "Everything else stays" is literal. Touch the named target; do not restyle its neighbors, migrate the page to a new idea, or add primitives the system does not own. If the system genuinely cannot express the request, stop and name the exact addition it would take.
- **Adjust in the system's own vocabulary.** Bolder means the existing display face at full strength, the existing motif turned up — not new effects. Softer means moving along the form-language table, not adding blur.
- **Re-verify after.** `craft_check.py` numbers should hold; `contrast.py` on any pair that changed; the constraint register still passes.

## softer / "too sharp, too blocky"

This is a **form-language migration**, and it fails when attempted as decoration — radius sprinkled onto a border-built page reads as a costume. Work the table in `design-tokens.md`:

1. **Remove borders before adding anything.** Softness is separation without lines: surface steps and tinted fills do the work borders were doing. If the palette has no ramps, that is the actual blocker — build them first.
2. Then radius, derived and nested (`Form language` section), then the two-layer tinted shadows from `Executing soft`, then hover ladders.
3. **Keep the skeleton.** Softening changes the boundary treatment, not the composition. If the layout also feels rigid, that is an `arrangement` complaint — name it separately.

Order matters: borders-out first. Radius-first produces rounded boxes, which is the complaint restated.

## bolder

Almost always scoped to one section, and the reflex answer — more effects — is the opposite of bold.

- A section reads flat because it quietly opts out of the system's strongest moves. Bring it *up to* what its neighbors already do: the display step at full size, the signature motif, a shift in density that makes it a peak in the scroll.
- **Commit once, then quiet the surroundings.** If every element got louder, the section got flatter.
- **The skeleton test:** strip the copy and look at the bare structure. If it only works once the words return, the boldness is in the font size, not the design.

## quieter / "too loud, too busy"

Reduction with intent — quiet without intent collapses to generic.

- Find the intensity sources first: saturation, contrast extremes, competing weights, motion, count of decorated elements. Reduce the top two, not everything.
- Large fills drop to the ramp's 100–300 steps; weights step down (700→500), not off; high contrast survives only where the hierarchy needs it.
- The signature element keeps its full strength. Quieter is lowering the floor around the peak, not flattening the peak.

## sharper / "too soft, feels unserious"

The mirror migration: tinted separation gives way to rules and borders, radius steps down a personality, the utility face takes more surface area, density tightens one notch. Same warning mirrored: borders sprinkled onto an elevation-built page read as wireframe, so migrate the boundary treatment wholesale or not at all.

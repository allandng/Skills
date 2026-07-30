# Style taxonomy

A style is not a name — it is a set of mechanical decisions. "Brutalism" is useless as a label; it is useful as "no radius, system or grotesque type at extreme scale contrast, visible structure, one saturated color against near-white, zero shadow."

Each entry below is written as reproducible mechanics: palette behavior, type category, layout, form, motion, texture. That is what makes them usable without a lookup database — and it is what lets you *name* a style you have extracted from a real site.

**How to use this:** after running `extract_style.py`, match the extracted axes against these entries to name the style. Then, for `remix`, pick entries that differ across the divergence-matrix axes. For `create`, treat these as a vocabulary, not a menu — the best direction is usually a specific hybrid grounded in the subject, not a family taken whole.

**Sequence matters.** Read `peer-research.md` first for anything competitive. Naming a style from this file is a shortcut; deriving one from real sites in the category is the actual method, and it produces something current rather than something remembered.

---

## Contents

- [Systematic](#systematic)
- [Editorial and print-derived](#editorial-and-print-derived)
- [Material and tactile](#material-and-tactile)
- [Technical and instrumental](#technical-and-instrumental)
- [Expressive](#expressive)
- [Warm and human](#warm-and-human)
- [Reading a style off a site](#reading-a-style-off-a-site)

---

## Systematic

**Swiss / International**
Grid is visible and obeyed absolutely. Neutral grotesque (Helvetica, Univers, Inter Display) at 2–3 sizes only. Flush-left, ragged-right, never centered. One accent, usually red. Zero radius, zero shadow. Asymmetric balance within a strict column structure. Motion: none or instant. Fails when the grid is decorative rather than structural.

**Modernist / Bauhaus**
Primary colors plus black on off-white. Geometric sans. Circle, square, triangle as literal structural elements. Heavy rules. Diagonal type permitted. Radius 0 or full-circle, nothing between.

**Corporate systematic**
Neutral cool palette, one brand color, generous whitespace. Humanist sans. 8px grid, 12-column. Radius 4–8. One or two elevation levels. Motion 150–250ms, functional only. This is the safest style and the easiest to make forgettable — the differentiator has to come from content or a single signature element.

**Flat / Material**
Solid fills, no gradients on surfaces. Elevation via shadow tiers, not borders. Radius 4–8, consistent. Bold accent against light neutral. Motion: 200–300ms with standard easing, meaningful transitions between states.

## Editorial and print-derived

**Broadsheet**
Hairline rules everywhere. Zero radius. Dense multi-column type. Small caps, drop caps, bylines. Black, white, one spot color. Serif body at reading size, condensed sans for furniture. Note: this is AI cluster look #3 — legitimate for actual publications, a default anywhere else.

**Magazine / editorial**
Big display type as the primary graphic element. Full-bleed imagery. Asymmetric grid with deliberate breaks. Generous leading, tight tracking on display. Pull quotes at display scale. Two faces maximum, strongly contrasted.

**Book / long-form**
Single measure, 60–70 characters. Transitional or old-style serif. Generous margins. No sidebar. Footnotes rather than callouts. Radius 0. No motion. Optimized for one thing: sustained reading.

**Archival / catalogue**
Ruled tables. Tabular figures. Accession-style identifiers. Muted paper ground with warm-tinted neutrals. Plate imagery with captions in a smaller utility face. Dense, ordered, indexed.

## Material and tactile

**Neumorphism**
Surface and elements share one color; form comes entirely from paired light and dark shadows. Very low contrast, which makes it an accessibility liability — use only where the palette can carry a real text contrast separately. Radius 12–24. Soft, slow motion.

**Glassmorphism**
Translucent surfaces, `backdrop-filter` blur, thin light borders, layered over a colorful or photographic ground. Depends entirely on what is behind it. Becomes a tell when every surface gets the same treatment — the material has to mean something (foreground vs. background) to earn itself.

**Skeuomorphic / textured**
Real material references: paper grain, fabric, metal, wood. Inner shadows, bevels, noise overlays. Radius follows the referenced material. Currently rare, which makes it distinctive when the subject justifies it.

**Claymorphic**
Heavy rounded forms, radius 24+, soft dual shadows, pastel high-lightness palette, chunky weights. Reads as friendly and juvenile. Fits consumer and education, fights against professional tools.

## Technical and instrumental

**Terminal / mono-led**
Monospace as the primary face, not just for code. Fixed character grid. Cursor and prompt motifs. Dark or amber-on-dark, or high-contrast light. Zero radius. Instant state changes. Strong identity, narrow audience.

**Instrument / control panel**
Dense information, tabular numbers, small type held at readable contrast. Physical-control metaphors: dials, toggles, readouts, status LEDs. Restricted palette with color reserved for state. Motion: still, or damped needle-like transitions. Radius 2–4.

**Data-dense / dashboard**
8px base, dense scale. Sidebar-anchored. Charts as the primary content. Muted palette so the data carries color. Tabular figures everywhere. Radius 4. Elevation only for overlays.

**Blueprint / diagrammatic**
Line-drawing aesthetic. Measured annotations, leader lines, dimension marks. Restricted to one or two ink colors on a tinted ground. Grid visible as a technical grid, not a layout grid. Distinctive and heavily underused.

**Dark technical**
Near-black ground, one saturated accent, monospace labels, subtle grid overlay, glow effects. This is AI cluster look #2 — check the brief actually asks for it.

## Expressive

**Brutalist / raw**
Default browser styling as a deliberate choice. Visible borders, unstyled controls, system fonts. Extreme scale contrast. Zero radius. Colors clash on purpose. Layout deliberately awkward.

**Neobrutalist**
Thick black borders, hard offset shadows with no blur, flat saturated fills, chunky geometric sans, zero or minimal radius. Structured where true brutalism is raw. Very recognizable, and now common enough to read as its own template.

**Kinetic / motion-led**
Motion is the primary design element: scroll-driven sequences, type that reacts, continuous ambient movement. Everything else stays restrained so the motion carries. Expensive to execute; requires a genuine reduced-motion alternative.

**Maximalist**
Layered imagery, multiple typefaces, pattern, high chroma, overlap, collage. Requires elaborate execution — a half-committed maximalist page just reads as cluttered.

**Anti-design**
Deliberate violation of convention: mismatched faces, clashing color, broken alignment. Only works when the audience is in on the joke.

## Warm and human

**Scandinavian**
Light neutral ground with warm undertone, muted natural accents, generous space, humanist sans, radius 8–12, soft single-level elevation, minimal restrained motion.

**Japandi**
Very restricted palette of warm neutrals plus one deep tone. Extreme whitespace. Asymmetric balance. Thin rules. Small type at high contrast. Radius 0–4. Motion: slow, few.

**Organic / fluid**
Curved section dividers, blob shapes, irregular radii, gradient meshes in muted tones, rounded humanist type. Watch the aurora-blob tell — the shapes have to relate to the subject.

**Botanical / naturalist**
Illustration-led, plate-style imagery, warm paper ground, serif with a historical cut, ruled captions, muted greens and earths.

**Warm editorial minimal**
Cream ground, high-contrast serif display, terracotta accent, generous whitespace, thin rules. AI cluster look #1 — the single most overproduced current style. Use only when the brief names it.

---

## Translating vibe words

Clients and briefs rarely speak in taxonomy names. They say "Linear-style," "Apple-y," "make it premium." **A vibe word is a compressed reference to sites the person has seen — decompress it into real sites and extract those**, rather than designing from the adjective. That is this skill's whole move: vocabulary → reference sites → extraction.

| They say | They usually mean | Do |
|---|---|---|
| "Linear-style", "clean like Linear" | Restraint, dark-capable, keyboard-fast, tight type | Extract linear.app itself; corporate systematic / dark technical hybrid |
| "Apple-y", "premium consumer" | Spacious, large type, product photography carrying the page | Extract the actual product pages they mean; premium ≠ a style, it's restraint + budget for imagery |
| "brutalist" | Almost always **neo**brutalism (thick borders, offset shadows, flat brights) — not true raw brutalism | Confirm with one reference before committing; the two families read completely differently |
| "Awwwards", "experimental" | Kinetic / motion-led, scroll-driven | Extract 2–3 of the actual award pages; budget honestly — this family is execution-expensive |
| "glassy" | Glassmorphism | Warn per the taxonomy entry: the material must mean something or it becomes the uniform-glass tell |
| "minimal", "clean" | Underdetermined — could be Swiss, Japandi, corporate systematic, or book | Do not guess; ask for one site they're picturing, or extract their nearest competitor |
| "premium", "luxury" | Spacious + restrained + either a serif with provenance or a tight grotesque | Ask for a reference; "premium" is the least informative word in the vocabulary |

When no reference site can be pried loose, fall back to the archetype's world (`ui-ux-studio`'s derivation) rather than to a family picked from this table — the table decodes vocabulary, it does not replace derivation.

## Reading a style off a site

Run `extract_style.py`, then work down this list. Each row maps an extracted value to the styles it is consistent with.

| Extracted signal | Points toward |
|---|---|
| radius 0, no shadow | Swiss, broadsheet, brutalist, terminal, Japandi |
| radius 2–8, 1–2 shadows | corporate systematic, flat, dashboard |
| radius 16+, soft dual shadows | claymorphic, neumorphic, organic |
| hard offset shadow, no blur | neobrutalist |
| `backdrop-filter` present | glassmorphism |
| monospace as body face | terminal, instrument, blueprint |
| serif body + sans furniture | editorial, book, archival |
| ≥6 type steps, ratio ≥1.33 | editorial, magazine, maximalist |
| ≤4 type steps, ratio ≤1.2 | Swiss, dashboard, instrument |
| median spacing ≤16 | dashboard, instrument, archival, broadsheet |
| median spacing ≥40 | Japandi, Scandinavian, luxury minimal |
| no transitions found | Swiss, broadsheet, instrument, book |
| durations >600ms, keyframes present | kinetic, organic, maximalist |
| untinted gray ramp | corporate systematic — or an undesigned palette |
| warm-tinted neutrals | Scandinavian, Japandi, archival, botanical |
| one accent, ≥7:1 against surface | Swiss, modernist, instrument |
| ≥4 chroma colors | Bauhaus, maximalist, or an undisciplined palette |

Two cautions. A site can be a coherent hybrid — "archival grid with neobrutalist controls" is a real and useful description, and better than forcing one label. And a site can simply have no style, in which case the honest output is "no coherent system; spacing, type, and elevation are all ad hoc," which is itself the most useful finding you can hand back.

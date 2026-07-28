# Worked example

One filled-in design plan and one filled-in divergence matrix, so the formats in SKILL.md and `modes.md` are concrete rather than abstract.

The subject here is deliberately unglamorous — a tool for tracking herbarium specimens. Distinctive design is easier to demonstrate on a subject with no established visual convention to fall back on.

---

## A. Design plan (create mode, Step 2)

```
ARCHETYPE   Program UI, borrowing from archival/catalogue for the record
            views. Not a marketing site — the buyer is the user.
SCALE       est. 2019 · ~40 institutional users · 120k specimen records
            · runs of 200+ per collecting trip
SUBJECT     Ashfield — a specimen log for working field botanists. Used
            outdoors, one-handed, often with wet gloves and bad light.
            The page's job: convince a botanist this respects field
            conditions, in under ten seconds.

THESIS      This is a field instrument, not an app. It should look like
            something you'd trust at 6am in the rain.

PALETTE     Sourced from actual herbarium sheets and field-kit hardware.
            --surface   #F2EFE7  aged mounting paper, not "warm cream" —
                                 it is the specific off-white of 100% rag
                                 stock, and it earns its place because the
                                 whole product is about paper records
            --ink       #221E1A  archival ink, warm-black not blue-black
            --primary   #3B5A3F  the green of powder-coated field cases
            --accent    #B03A2E  the red of specimen-annotation pencils —
                                 used only on corrections and deletions,
                                 mirroring how the pencil is actually used
            --border    #C9C1B2  the ruling on a herbarium label
            --muted     #6B6157  faded pencil (checked: 5.1:1 on surface)

            JUSTIFIED CHOICE: the accent is only ever a correction. Nothing
            else in the interface is allowed to be red. That constraint is
            borrowed from the discipline's own convention.

TYPE        Display — Bitter (slab). Field guides and specimen labels have
            used slabs for a century; a geometric sans would read as
            software, which is exactly the wrong register.
            Body — Source Serif 4. Long-form notes get read outdoors;
            serifs hold up better at small sizes in low contrast light.
            Utility — Source Code Pro for accession numbers, coordinates,
            dates. Tabular figures, because these get compared in columns.

            Scale, 1.25 ratio: 12 / 14 / 16 / 20 / 25 / 31 / 39

LAYOUT      A ledger, not a dashboard. Fixed left rail of accession numbers
            that stays put while the record scrolls, so the botanist never
            loses their place in a run of 200 specimens.

            +--------+----------------------------------------+
            | 4412   |  ASPLENIUM SCOLOPENDRIUM               |
            | 4413   |  coll. 2024-06-11  ·  51.44N  -2.61W   |
            |[4414]  |  ---------------------------------      |
            | 4415   |  [ specimen image, full bleed right ]   |
            | 4416   |                                         |
            |        |  notes ------------------------------   |
            | 214    |  det. R. Hale, 2024-06-14               |
            | total  |                                         |
            +--------+----------------------------------------+

DENSITY     Dense. 8→32 scale. Botanists work in runs of hundreds; every
            row of vertical padding is a row they have to scroll past.

MOTION      Still. No entrance animation anywhere. State changes flip in
            100ms. A field instrument that animates feels like a toy, and
            in bright sunlight motion is just noise.

PRIMARY ASSET  The record runs themselves — concentration-dependent. A
            ledger of 200 rows reads differently from ten pages of 20.
            Home is the list view; nothing subdivides it.
SIGNATURE   The accession rail. It is always visible, always counting, and
            it uses the utility face at tabular figures so the numbers
            align down the column like an actual ledger. It is the one
            thing you would remember about this interface.

RISK        No hero image, no marketing section, no gradient. The landing
            page IS the product, populated with a real specimen run. If a
            botanist can't tell within five seconds whether this handles
            their workflow, no amount of copy would have convinced them.
            The risk: it reads as unfinished to a non-botanist. Accepted —
            non-botanists are not the buyer.
```

Note that `ARCHETYPE`, `SCALE`, and `PRIMARY ASSET` come first. They are the constraints the rest inherits — the archetype rules out a marketing structure, the scale makes an archive register honest here in a way it would not be for a two-year-old club, and the asset line is what stops a later route split from dismantling the ledger.

Note what makes this plan non-generic: every choice traces to something in the subject's actual world — rag paper, annotation pencils, field-case powder coating, herbarium label ruling, runs of hundreds. Swap in a different brief and none of it survives, which is the test.


### The same procedure, a soft subject

The Ashfield plan derives sharp — and most of this skill's case law does, which is itself a gravity worth counterweighting. Here is the compact plan for a subject that derives the opposite form language, using the ramp and layering machinery from `design-tokens.md`:

```
ARCHETYPE   Program UI (community tool), borrowing from local business
            for the pickup-point pages
SCALE       one neighborhood · ~300 members · 2 seasons · ~1,900 swaps
SUBJECT     Bramble — a seed-swap ledger for a neighborhood garden
            network. Used at kitchen tables and greenhouse benches.
THESIS      This is a potting bench, not a marketplace. Paper envelopes
            and pencil, not inventory software.
PALETTE     From seed packets and greenhouse glass:
            --surface  #F7F3E8   manila envelope
            --ink      #2B2A24   pencil, warm black
            --leaf     #4C7A4F   with a 100/300/500/700 ramp — the 100
                       is the tinted fill that lets a card sit on the
                       page with no border at all
            --bloom    #C77B54   terracotta pot; accent-2, small ramp
FORM        elevation-layered, round (12–16). No borders anywhere;
            surface plus one soft shadow level separates the layers,
            hover is translateY(-2px) plus one shadow step.
TYPE        Display: rounded humanist (seed-packet lettering lineage).
            Body: quiet serif. Utility: mono for lot numbers and dates.
SIGNATURE   The germination row — each listing carries a row of dots,
            one per day since sowing, sized by sprout count. Data as
            decoration, derived from what gardeners actually track.
RISK        No search on the front page; browsing by what's ready this
            week mirrors a swap table. Accepted: one neighborhood,
            nobody is filtering 10,000 listings.
```

Why soft is *earned* here and would be wrong for Ashfield: Bramble's materials are paper envelopes, seedlings, and hand-written labels — round, layered, tinted. Ashfield's are archival sheets, rulings, and accession stamps — sharp, ruled, flat. Same procedure, opposite outputs. If both plans had arrived at the same form language, one of them would be a default wearing a costume.

---

## B. Divergence matrix (remix mode, Step 4)

Three directions for the same existing site. The matrix is filled in *before* any designing, and each column must differ from both others on at least four rows.

| Axis | A · The Instrument | B · The Herbarium | C · The Expedition |
|---|---|---|---|
| **Contrast model** | light ground | duotone, ink on paper | dark ground |
| **Palette source** | material-derived (field kit) | monochrome + one spot | high-chroma limited |
| **Type category** | slab | transitional serif | mono-led |
| **Layout system** | sidebar-anchored ledger | full-bleed editorial | horizontal scroll |
| **Density** | dense | spacious | standard |
| **Motion** | still | interaction-only | physical |
| **Signature** | the accession rail | the specimen plate | the route map |
| **Form language** | rule-delimited, sharp | rule-delimited, plate borders | elevation-layered, soft |

**Divergence check:** A vs B differs on 7 of 8 (both rule-delimited). A vs C differs on 8 of 8. B vs C differs on 7 of 8. Passes — the shared rule-delimited treatment between A and B is fine because they diverge nearly everywhere else.

**Theses** — each is an argument about what the product is, and they disagree:

- **A · The Instrument** — "This is equipment. Show the readout, hide the marketing." Lineage: field-kit industrial design, aviation checklists.
- **B · The Herbarium** — "This is an archive. The specimens are the point; the software is the mount." Lineage: 19th-century botanical plates, museum catalogue design.
- **C · The Expedition** — "This is a journey. Collecting is fieldwork, and fieldwork has a route." Lineage: survey maps, expedition logbooks.

**Bad version of the same exercise**, for contrast — this is the failure mode the matrix exists to prevent:

| Axis | A · Clean | B · Modern | C · Bold |
|---|---|---|---|
| Contrast model | light | light | dark |
| Palette | indigo accent | emerald accent | violet accent |
| Type | Inter | Inter | Inter Tight |
| Layout | centered | centered | centered |
| Density | standard | standard | standard |

Three skins, one design. The user is choosing a hue and calling it a design decision.

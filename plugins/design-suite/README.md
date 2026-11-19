# Design Suite

Extract a real site or app's design system and structure, then build, remix, or audit interfaces
that don't read as AI-generated.

```bash
/plugin install design-suite@allan-skills
```

Two skills ship in one plugin because they're two halves of one workflow: `design-dna` reads the
world, `ui-ux-studio` builds into it. An installed plugin can't reference files outside its own
directory, so splitting them would break the handoff.

## How both skills work

The same shape as an engineering stack, applied to design:

- **Playbooks.** Each job is a short step list in `playbooks/` that the agent copies into its todo
  list and works in order. A step that does not apply keeps its line with `n/a: <reason>`, so a
  skipped step and a forgotten one never look the same. Every playbook ends with a stated reply.
- **A shared app taxonomy.** `references/app-taxonomy.md` (identical in both skills) names a product
  on six layers: surface, app type, shell, screen type, regions and overlays, states and flows.
  "Build a dashboard" becomes `orientation:dashboard` in a workflow/queue app with a list-detail
  shell, which is something you can design.
- **Proof before done.** `ui-ux-studio` climbs a ten-rung ladder (rendered, states, content stress,
  keyboard, contrast, craft and tells, copy, motion, platform, parity). `design-dna` proves an
  extraction with a completeness check and a round-trip specimen. Every claim in a reply is labeled
  measured, observed, inferred, or guess.
- **Named principles.** One rule per situation in `references/principles.md`, read when a decision
  is hard, not up front.

The playbook form, the proof discipline, and the critique panel are adapted from
[pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan (MIT), which this
marketplace also carries as [`askillissue`](../askillissue).

---

## design-dna

Turns real websites into design systems you can reuse. Point it at a URL or a local codebase and it
produces a `tokens.json` plus a written style profile — palette, typography, spacing, radii,
elevation, motion, layout — names the style from an open taxonomy, and flags AI tells.

### Modes

| Mode | Use it when | Produces |
|---|---|---|
| **Extract** | You want one specific site's system — to match it, extend it, or diverge from it deliberately | `tokens.json`, `tokens-dark.json`, a style profile, and a `GAPS` list of what the script couldn't see |
| **Survey** | You want to know how a whole category designs itself | A peer comparison across competitors and adjacent categories, sorted into `CONVENTION`, `HERD`, `CONTESTED`, and `UNOCCUPIED` |
| **Teardown** | You want to know how a product is organized, not how it looks | A `Structure` block: app type, shell, navigation levels, a screen inventory by family, flows, state coverage, and `GAPS` |
| **Compare** | Two systems side by side: a redesign and its original, yours and a competitor's | An axis-by-axis table marked same, drifted, or deliberately different |

Playbooks: `extract-site`, `extract-codebase`, `survey`, `teardown`, `compare`, `handoff`.

The `Survey` split is the useful part: `CONVENTION` is what you keep because breaking it confuses
people, `HERD` is what everyone copied from everyone else, and `UNOCCUPIED` is where the whole
category left room.

Extraction is deliberately not fully automated. The script reads declarations; it can't see states,
hierarchy, imagery, voice, or intent. `references/extraction.md` walks the nine-step manual pass
that produces the `GAPS` list, and that list is what `update` mode depends on.

### Scripts

| Script | What it does |
|---|---|
| `scripts/extract_style.py` | Pulls a design system out of a site's HTML and CSS into `tokens.json` |
| `scripts/contrast.py` | WCAG 2.2 contrast ratios across every foreground/background pair in a palette |
| `scripts/craft_check.py` | Measures the positive craft floor — type scale range, ramps, elevation. The counterpart to a tell scan |
| `scripts/route_inventory.py` | Lists a codebase's screens from its file-based routes (Next.js, Expo Router, SvelteKit, Nuxt, Astro, HTML), marks templates, and reports which have loading, error and not-found files |
| `scripts/dna_check.py` | Fails an extraction folder that is incomplete or has unlabeled claims, before it is handed off |

Run the contrast check before you treat an extracted palette as usable — inheriting someone else's
accessibility failures is a real risk when you're matching a style:

```bash
python3 scripts/contrast.py --tokens ./dna/example/tokens.json --tokens-dark ./dna/example/tokens-dark.json
```

Roles are inferred, so some pairs it checks never actually co-occur on screen. Once you know the
real combinations, declare them and re-run.

### References

`references/extraction.md` (the manual pass), `references/style-taxonomy.md` (naming the style),
`references/peer-research.md` (building the comparison set), `references/app-dna.md` (the teardown
walk), `references/evidence.md` (claim labels and how to prove an extraction), and
`references/app-taxonomy.md` (the shared vocabulary).

---

## ui-ux-studio

The framing is a small design studio whose reputation is that no two clients get the same-looking
product. The client has already seen and rejected work that looks like a template.

Every page it produces ships with a subject-derived SVG favicon, a page title, and a complete head
block — not as an afterthought, as part of the deliverable.

### Modes

| Mode | Use it when | Produces |
|---|---|---|
| **create** | New UI from a brief | An archetype call, a design plan, then the build |
| **remix** | An existing site needs options | 3 genuinely different directions, enforced by a divergence matrix |
| **spec-to-ui** | You have a backend, schema, or PRD but no interface | 3 interaction models derived from the data, not from a template |
| **variants** | You like one design and want more like it | 3 treatments of one settled concept |
| **update** | Matching or extending an existing system | Work that fits the system on every axis, using `design-dna`'s `GAPS` and `STATES` |
| **audit** | Reviewing what exists | Design + accessibility review with a phased fix plan |

### Playbooks for the product surface

The modes above cover a page or a site. These cover the part of an app a signed-in person works in.

| Playbook | Use it when | Produces |
|---|---|---|
| **app-shell** | A product has several areas and no agreed structure | The classification line, navigation levels and their homes, a screen inventory, two wireframes |
| **screen** | One screen needs to be done properly | The screen in every state its family requires, with a coverage report |
| **flow** | Anything takes more than one step | A flow inventory, a statechart, and the steps walked forward, backward, refreshed and resumed |
| **platform-adapt** | A design moves between web, iOS, Android or desktop | A translation of each element's job, following the target platform's conventions |
| **design-system** | Screens have drifted, or dark mode is being added | Token layers, a component inventory, an exceptions list |
| **critique** | A design should be attacked before it ships | Findings that reviewers with different lenses could point at, and a count of what was dropped |
| **prototype** | A decision won't settle by arguing | Throwaway variants behind one switcher |
| **visual-parity** | A migration must not change the look | A comparison against a baseline, per component |

### The gates

Two checks run before aesthetics, and they're the reason this skill is more than a token generator:

- **Archetype fit** — *what kind of thing is this?* A design can be well-spaced, accessible,
  distinctive, and pass every tell check while still being wrong, because it was built to the
  conventions of a category the subject doesn't belong to. Divergence without fit produces
  directions that are reliably different and reliably inappropriate.
- **The copy gate** — copy is the fastest-read part of an interface and the least protected. A page
  can survive every visual check and still announce itself on the first line of the hero.
  `references/copy-gate.md` catches borrowed-weight language: "on the books," "status: live,"
  "currently running" — each fine when true, each a tell when the numbers don't support it.

### Scripts

| Script | What it does |
|---|---|
| `scripts/ai_tells.py` | Scans frontend source for mechanical AI-design tells — colors, fonts, class patterns, copy |
| `scripts/contrast.py` | WCAG 2.2 contrast across the palette (same checker as `design-dna`) |
| `scripts/craft_check.py` | Measures the positive craft floor (same checker as `design-dna`) |
| `scripts/state_coverage.py` | Checks a `states.json` manifest: every state a screen's family requires has a file, quoted text, or a stated `n/a` reason behind it |
| `scripts/favicon.py` | Turns a designed SVG mark into `favicon.svg` with an embedded dark-mode variant, `icon-mono.svg` for pinned tabs, `site.webmanifest`, and a paste-ready head snippet |

`favicon.py` optionally uses `cairosvg`/`rsvg-convert` to rasterize PNGs and `Pillow` for a 16px
ASCII preview. Both are guarded imports — without them everything else still works and the script
prints the fallback command.

### References

Three are worth calling out beyond the gates above:

- **`conventions.md`** — which conventions are load-bearing (breaking them has a real comprehension
  cost) versus herd behavior, and where popular design advice stops applying. Departures from that
  advice are recorded with reasons, so a later edit doesn't silently "fix" a deliberate choice back
  into a default.
- **`flows.md`** — everything else in the skill designs *screens*; this designs the path between
  them. A flow can be built entirely from good screens and still be bad: every step well-spaced,
  accessible, on-token, and the user still ends up stuck or unable to get back. Those failures are
  invisible in a screenshot, which is why they survive review. Read it for anything multi-step —
  sign-up, onboarding, checkout, wizards.
- **`adjustments.md`** — "make it softer," "too blocky," "bolder," "quieter." These arrive constantly
  once a design exists, and none of them is a mode; re-running remix for one is using a crane to move
  a chair. This is the playbook for amplitude changes to a design that stays, in the system's own
  vocabulary rather than by bolting on new effects.

Added with the playbooks: `app-taxonomy.md` (the six layers), `platforms.md` (what web, iOS, Android
and desktop each expect, and a table for translating between them), `states.md` (required states per
screen family, modeling state as one value, the coverage manifest), `principles.md`, `proof.md` (the
ladder, claim labels, the reply frame, the decision log), `critique-panel.md`, and `help.md` (which
playbook for which request, with prompts that work).

The rest: `archetypes.md`, `copy-gate.md`, `ai-tells.md`, `design-tokens.md`, `favicon-and-head.md`,
`interface-guidelines.md`, `modes.md`, `motion.md`, `site-architecture.md`, `stack-notes.md`, plus
`assets/worked-example.md` — two filled-in design plans and a divergence matrix, so the formats are
concrete rather than abstract. The two plans run the same procedure on deliberately opposite
subjects (one deriving sharp and ruled, one deriving round and layered) to show that the method,
not a house style, is what produces the form language.

---

## How they chain

```
design-dna: Extract          design-dna: Survey
        │                            │
   tokens.json                 CONVENTION / HERD
   + GAPS / STATES             CONTESTED / UNOCCUPIED
        │                            │
        ▼                            ▼
ui-ux-studio: update         ui-ux-studio: remix / create

design-dna: Teardown ──► Structure + GAPS ──► ui-ux-studio: platform-adapt / app-shell / screen
```

| Target mode | What to pass | How it gets used |
|---|---|---|
| **update** | `tokens.json` + the manual pass, especially `GAPS` and `STATES` | Match every axis exactly |
| **remix** | The survey's `CONTESTED` and `UNOCCUPIED` | Required, not optional — pick *different* values per direction |
| **create** | The survey's `CONVENTION` and `HERD` | Keep convention, spend your freedom on the herd behavior |
| **audit** | `tokens.json` + flagged tells + the teardown's state table | Baseline to measure drift against |
| **platform-adapt** | The teardown's `Structure` block and `routes.json` | Translate each screen's job to the new surface |
| **design-system** | Declared against used, dead tokens, the component inventory | Collapse it into one system |

Run `design-dna` first whenever a real reference site exists. `ui-ux-studio` works standalone, but
remix mode in particular is much weaker without a survey behind it — you get difference without
knowing which differences the category has left unclaimed.

# Design Suite

Extract a real site's design system into tokens, then build or remix interfaces that don't read as
AI-generated.

```bash
/plugin install design-suite@allan-skills
```

Two skills ship in one plugin because they're two halves of one workflow: `design-dna` reads the
world, `ui-ux-studio` builds into it. An installed plugin can't reference files outside its own
directory, so splitting them would break the handoff.

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

Run the contrast check before you treat an extracted palette as usable — inheriting someone else's
accessibility failures is a real risk when you're matching a style:

```bash
python3 scripts/contrast.py --tokens ./dna/example/tokens.json --tokens-dark ./dna/example/tokens-dark.json
```

Roles are inferred, so some pairs it checks never actually co-occur on screen. Once you know the
real combinations, declare them and re-run.

### References

`references/extraction.md` (the manual pass), `references/style-taxonomy.md` (naming the style),
`references/peer-research.md` (building the comparison set).

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
| **update** | Matching or extending an existing system | Work that fits the system on every axis, using `design-dna`'s `GAPS` and `STATES` |
| **audit** | Reviewing what exists | Design + accessibility review with a phased fix plan |

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
| `scripts/favicon.py` | Turns a designed SVG mark into `favicon.svg` with an embedded dark-mode variant, `icon-mono.svg` for pinned tabs, `site.webmanifest`, and a paste-ready head snippet |

`favicon.py` optionally uses `cairosvg`/`rsvg-convert` to rasterize PNGs and `Pillow` for a 16px
ASCII preview. Both are guarded imports — without them everything else still works and the script
prints the fallback command.

### References

Two are worth calling out beyond the gates above:

- **`conventions.md`** — which conventions are load-bearing (breaking them has a real comprehension
  cost) versus herd behavior, and where popular design advice stops applying. Departures from that
  advice are recorded with reasons, so a later edit doesn't silently "fix" a deliberate choice back
  into a default.
- **`flows.md`** — everything else in the skill designs *screens*; this designs the path between
  them. A flow can be built entirely from good screens and still be bad: every step well-spaced,
  accessible, on-token, and the user still ends up stuck or unable to get back. Those failures are
  invisible in a screenshot, which is why they survive review. Read it for anything multi-step —
  sign-up, onboarding, checkout, wizards.

The rest: `archetypes.md`, `copy-gate.md`, `ai-tells.md`, `design-tokens.md`, `favicon-and-head.md`,
`interface-guidelines.md`, `modes.md`, `motion.md`, `site-architecture.md`, `stack-notes.md`, plus
`assets/worked-example.md` — a fully filled-in design plan and divergence matrix, so the formats are
concrete rather than abstract.

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
```

| Target mode | What to pass | How it gets used |
|---|---|---|
| **update** | `tokens.json` + the manual pass, especially `GAPS` and `STATES` | Match every axis exactly |
| **remix** | The survey's `CONTESTED` and `UNOCCUPIED` | Required, not optional — pick *different* values per direction |
| **create** | The survey's `CONVENTION` and `HERD` | Keep convention, spend your freedom on the herd behavior |
| **audit** | `tokens.json` + flagged tells | Baseline to measure drift against |

Run `design-dna` first whenever a real reference site exists. `ui-ux-studio` works standalone, but
remix mode in particular is much weaker without a survey behind it — you get difference without
knowing which differences the category has left unclaimed.

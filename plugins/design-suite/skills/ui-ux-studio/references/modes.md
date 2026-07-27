# Mode playbooks

Full procedures for **remix**, **spec-to-ui**, **update**, and **audit**. (**create** is specified in SKILL.md.)

---

# Mode: remix

Three genuinely different directions for a site that already exists.

The failure mode this mode is built to prevent: three variants that are the same design with different accent colors. That outcome is worse than one option, because it gives the illusion of choice while narrowing the actual decision to a hue. Three directions must **disagree about what the product is**.

## Step 0 — Classify the archetype

Read `archetypes.md` and name the archetype before looking at the existing design. Write down the real numbers for scale honesty.

This comes first because it determines which concepts are eligible at all. Skipping it is how this mode fails: the divergence matrix rewards orthogonality, and orthogonality with no fit constraint reliably produces directions that are all different and several of them wrong.

## Step 1 — Ingest

Take whatever exists:
- **A URL** — fetch it. Get the rendered text, the stylesheet, the structure. Screenshot it if the environment allows.
- **Local files or a repo** — read the templates, components, and stylesheets. Enumerate the routes and the shared shell; do not assume the site is one page because the homepage is what you were shown.

**Extract the tokens rather than eyeballing them.** If the `design-dna` skill is available, run it now:

```bash
python3 <design-dna>/scripts/extract_style.py --dir ./source --out ./dna/current
```

It returns `tokens.json`, a style profile with the divergence axes already estimated, and `tokens-dark.json` when the site has a dark theme. Reading a palette out of the CSS is strictly more accurate than judging it from a screenshot, and the dark-theme split matters: a site with a theme toggle will otherwise report whichever theme parsed last as its palette.
- **A screenshot only** — read it directly and describe the current system before proceeding.

## Step 2 — Separate invariants from variables

Write these out explicitly. Everything in the left column carries across all three directions unchanged; everything in the right column is up for grabs.

| Invariant (carries across) | Variable (differs per direction) |
|---|---|
| The actual copy and content | Palette |
| Product job and primary conversion | Typography |
| Hard brand constraints (logo, legal color, name) | Layout system and grid |
| Functional requirements | Density and spacing rhythm |
| Real data shape | Motion philosophy |
| **The route set and feature set** — decided once in Step 2b and applied identically to all three | Signature element |
| | Imagery and iconography strategy |
| | Section order within a page |

Using the same content across all three is what makes them comparable. If the copy changes between directions, the user is comparing copy, not design.

Note what moved. Route structure and feature set are **not** untouchable invariants — a redesign that cannot cut anything is not a redesign. But they are decided **once**, in Step 2b, and then held constant across all three directions. If direction A has five pages and direction B has one, the comparison is meaningless: B will look cleaner for reasons unrelated to its design.

## Step 2b — Detect the shape, then decide routes and features

Read `site-architecture.md` and work its steps 1 through 4. This produces two artifacts that constrain all three directions equally:

1. **The route plan** — source shape, route inventory, and a per-route keep/merge/split decision with reasons and redirects. Route parity with the source is the default; departing from it is allowed and often correct, but never silent.
2. **The feature inventory** — every feature marked KEEP, CUT, MERGE, ADD, or ADD-but-guard, each with a reason.

Do this before designing, and present both to the user before building. These are editorial decisions about the product, and they are the ones most likely to differ from what the user would have chosen. Getting agreement here costs one exchange; getting it wrong costs three built directions.

The most common findings, in rough order of frequency:

- **Routes that exist but are unreachable from the nav.** Real IA bugs. In one seven-route site, five were orphaned.
- **Features in the repo that nothing imports.** Someone already abandoned them.
- **Decorative animation on the critical path** — a typewriter effect delaying the one fact the visitor came for.
- **A missing feature the archetype requires.** Check the ten-second job in `archetypes.md`. Frequently the single most important fact is nowhere on the site.

## Step 2c — Survey the category

**Required, not optional.** Read `peer-research.md` (in `design-dna`) and run it.

The divergence matrix in Step 4 forces the three directions to differ from *each other*. Nothing in it checks whether they differ from what every other site in the category already looks like. Without this step the matrix optimizes in a vacuum: you can produce three internally distinct directions that all sit inside the same category-wide convention, and none of them will feel like a departure to anyone who has seen the competition.

Assemble six to eight sites — 2–3 direct competitors, 1–2 category leaders, **2 from adjacent categories**, 1 outlier. The adjacent ones do the most work; for a campus club that means looking at things with the same *job* rather than the same label — small studio sites, band pages, lab groups, zines — not only at other club sites.

Extract each, build the comparison table, and answer the four questions. Two outputs carry forward:

- **`CONTESTED`** — axes where the category has no consensus. Free to take a position without confusing anyone.
- **`UNOCCUPIED`** — taxonomy families nobody in the set uses. The strongest available move when the subject supports it.

Feed both into Step 4 **before** choosing axes. If the survey genuinely cannot run — no network, no peers findable — say so explicitly in the plan and mark the divergence matrix as unanchored. Do not skip it silently.

## Step 3 — Diagnose the current design

Run `scripts/ai_tells.py` on the existing code and walk `ai-tells.md` by hand. Report, briefly:
- What the current design's thesis appears to be (or that it has none)
- Which tells are present
- What is genuinely working and should be preserved

This matters because the user usually cannot articulate why the site feels generic. Naming the tells gives them the vocabulary and makes the three directions legible as responses to a diagnosis.

## Step 4 — Enforce divergence

This is the mechanism that makes the three directions actually different. Fill in this matrix **before designing anything**.

Each direction must differ from both others on **at least four of these seven axes**. Not one. Four.

Choose axes using the survey from Step 2c. Prefer `CONTESTED` axes — where the category has no consensus, a position costs nothing in comprehension. Check every choice against what the peer set already does: an axis where all eight peers agree is either load-bearing convention (keep it) or herd behavior (the best differentiation available). Deciding which is which is the point of having run the survey.

| Axis | Options (pick a different one per direction) |
|---|---|
| **Contrast model** | light ground / dark ground / mid-tone ground / inverted per section / duotone |
| **Palette source** | monochrome + one spot / analogous warm / analogous cool / complementary pair / material-derived / high-chroma limited |
| **Type category** | geometric sans / grotesque / humanist sans / transitional serif / slab / display-driven / mono-led |
| **Layout system** | centered column / asymmetric split / full-bleed editorial / modular grid / sidebar-anchored / horizontal scroll / single-canvas |
| **Density** | spacious / standard / dense |
| **Motion philosophy** | still / one orchestrated moment / continuous ambient / interaction-only / physical-feeling |
| **Signature device** | typographic / photographic / diagrammatic / data-as-decoration / material-texture / illustrative / interactive |

## Step 4b — The fit gate

**Divergence is necessary, not sufficient.** Before a direction counts, it passes three checks. A direction that fails any of them is replaced, not restyled.

1. **Archetype fit.** Is this concept one the archetype supports? Check it against the cosplay traps for that archetype in `archetypes.md`.
2. **Scale honesty.** Does the concept imply more weight, activity, or permanence than the subject has? Run the table in `archetypes.md` §3.
3. **Content fit.** Does the concept need content that does not exist? A direction requiring testimonials for a subject with no users is asking you to invent them.
4. **Signature survival.** If the concept depends on a concentration-dependent asset — a wall of photographs, a full timeline, a dense index — does the route plan from Step 2b keep it concentrated on the landing page? Run the landing-page test in `site-architecture.md` §4b. A concept whose signature ends up spread four-per-page across five routes has been neutralized, and it will read as weaker than a worse concept that kept its asset intact.

This gate exists because of a specific failure. Three directions were built for a twelve-person student club with three shipped projects and no scheduled meeting. All three passed the divergence matrix. Two failed anyway:

- One framed the club as an institutional archive — accession numbers, "members on the books," "entries stamped on delivery." Eleven pieces of borrowed institutional language for a two-year-old club.
- One framed it as an operations dashboard — "Status: live", "Crew 12", "0 currently running", "Next session: None set." A live readout whose main achievement was advertising that nothing was happening.
- The one that worked framed it as a room with people in it: "Twelve people, one room, three shipped products", built on the nineteen real photographs.

The two failures were not styling problems. The *concepts* were wrong, and the concepts were chosen because they diverged. Fit is the gate; divergence happens inside it.

Practical consequence: generate five or six candidate concepts, drop the ones that fail the gate, then pick three that diverge. Do not pick three and then try to justify them.

Then write a one-line thesis for each surviving direction. The thesis is an argument about the product, not a description of the style.

**Good theses** (they disagree with each other):
- A: "This is an instrument. Show the readout, hide the marketing."
- B: "This is a publication. Lead with the writing, let the product be the byline."
- C: "This is a place. Make the landing feel like arriving somewhere specific."

**Bad theses** (all the same idea):
- A: "Clean and modern" · B: "Sleek and professional" · C: "Bold and minimal"

Each thesis must also be sayable by the subject's own people without embarrassment. "This is not a club, it's a record" is a designer's conceit; "we're twelve people in one room" is something a member would actually say. When the thesis only works in a designer's mouth, the direction will read as AI no matter how it is executed.

Give each direction a **reference lineage** — one or two named traditions, disciplines, or artifacts it draws from. This is what keeps it out of the three cluster looks in `ai-tells.md` §9.

## Step 5 — Plan each direction

Run the full design plan block from SKILL.md Step 2 for each of the three. Keep them tight — the point is comparability.

Then run the swap test across the set: could you swap the palettes between direction A and direction B without either looking wrong? If yes, they are not diverging on palette, only on hue. Go back to the matrix.

## Step 6 — Build all three

**One directory per direction, not one file.** Follow `site-architecture.md` §6 for the structure.

- Same content, same route set, same feature set across all three — per the Step 2b plan.
- Directories named by thesis, not number: `register/`, not `variant-1/`.
- **Navigation must work.** Links resolve between the pages in each direction. A direction you cannot click through is a mockup, not a redesign.
- One shared shell per direction — the nav and footer live in one place, or are byte-identical with that noted in the handoff. Seven hand-copied navbars drift.
- One stylesheet of tokens per direction, shared by all its pages. That is what makes it one design rather than N similar ones.
- Each direction gets its own favicon; each page gets a title following one pattern (`favicon-and-head.md` §3).
- **Count the backgrounds per page and write the number down.** One ground, at most one or two deliberate departures. Four or more is patchwork — and if a page needs bands to be legible, split the page rather than restyling the bands.
- Each meets the full quality floor independently.

## Step 7 — Present as a decision

For each direction, give the user:

```
NAME + THESIS       one line
ARCHETYPE FIT       why this archetype supports this concept, and what it
                    would take to be wrong for it
DIVERGENCE          which axes it takes and how it differs from the others
BEST WHEN           the conditions under which this is the right choice
PAGES               the routes it ships, and backgrounds per page
SIGNATURE           what it is, where it lives, and what the landing page
                    looks like as a result
VS CATEGORY         how it differs from the peer set, not just from A and B
COSTS               what it gives up — every real direction gives something up
RISK LEVEL          how far it is from the current site
```

Then a short recommendation with a reason. Presenting three options with no opinion pushes the work back onto the user.

Finish with a scan of all three: `python3 scripts/ai_tells.py <all files>`.

---

# Mode: spec-to-ui

Three interaction models derived from a backend, schema, API surface, type file, architecture doc, or PRD — where no UI exists yet.

The distinction from remix matters: with an existing site, the three directions differ mainly in **aesthetics**. With a spec, they should differ in **information architecture** — how the system is made comprehensible. Three skins over one identical screen layout is the wrong answer here.

## Step 0 — Classify the archetype

Read `archetypes.md`. Most specs describe an app UI or an internal tool, and those two have almost opposite density and polish requirements — getting it wrong produces a marketing page where a table belongs. State the archetype before reading further.

## Step 1 — Read the artifact

**From a backend, schema, or API:**
- Entities, their fields, and their types
- Relationships and cardinality (a one-to-many drives a list-detail; a many-to-many drives a join or graph view)
- Actions: mutations, endpoints, commands — these become the controls
- States: enums, status fields, nullable fields, soft deletes — these become UI states, not edge cases
- Access control: roles and permissions become navigation shape and empty states
- Volume assumptions: pagination, cursors, and limits tell you whether a list is 10 rows or 100,000

**From a PRD or architecture doc:**
- The actors and their jobs-to-be-done
- The primary flow, and where it currently breaks
- The success metric — this determines what the interface optimizes for
- Explicit non-goals, which are as informative as goals

If the artifact is a Figma file and the Figma MCP tools are connected, pull the design context from there rather than inferring.

## Step 2 — Build the interface inventory

Do this before any design. It is the deliverable that makes the three models comparable and honest.

```
ENTITIES → SCREENS
  entity            primary view       secondary views
  ---------------------------------------------------
  Recipe            list               detail, edit, compare

ACTIONS → CONTROLS
  endpoint/mutation           control            placement       confirm?
  --------------------------------------------------------------------
  POST /recipes/:id/rank      drag or A/B pick   detail + list   no
  DELETE /recipes/:id         destructive        detail overflow  yes + undo

STATES (per screen — none of these are optional)
  empty · first-run · loading · partial · error · offline · permission-denied
  · single item · dense (100+) · maximum realistic content length

GAPS
  endpoints the interface needs that the backend does not yet expose
```

That gaps list is often the most useful thing this mode produces. Surface it prominently — it is real engineering feedback, discovered by designing.

## Step 3 — Choose three interaction models

Pick three that differ **structurally**. Some archetypes:

| Model | Shape | Fits when |
|---|---|---|
| **Navigational** | Sidebar → list → detail | Stable entity set, users browse and drill in |
| **Command-driven** | Command palette + minimal chrome | Power users, high task frequency, many verbs |
| **Canvas / spatial** | Single surface, direct manipulation | Relationships matter more than records |
| **Feed / stream** | Reverse-chronological, infinite | Time-ordered events, recency dominates |
| **Wizard / progressive** | One decision per step | Rare high-stakes tasks, complex input |
| **Dashboard-first** | Aggregate view, drill down on anomaly | Monitoring, exceptions matter more than records |
| **Document** | The record *is* the page, edited in place | Content-shaped data, long-form authoring |
| **Inbox / queue** | Triage one item at a time, then next | Work arrives, must be dispositioned |

For each of the three, state:
- Which archetype and why this data shape suits it
- What it optimizes for and what it makes harder
- **Which endpoints it uses, and which it needs that do not exist yet**
- Which user it serves best

Then apply the divergence matrix from remix Step 4 to the visual layer, so the three are distinct aesthetically as well as structurally.

## Step 4 — Build

Build all three against the real data shape. Use realistic mock data derived from the schema — actual field names, actual value ranges, actual string lengths including the long ones. Placeholder data hides the layout problems that real data creates.

Every screen ships its empty, loading, and error states. Those states are where interfaces actually fail, and where AI-generated interfaces most reliably skip.

## Step 5 — Present

Same presentation shape as remix Step 7, plus for each model:
- The backend work it implies
- How it degrades as data volume grows 100×

---

# Mode: update

Add something new to an existing site so that nobody can tell it is new.

This is the exact inverse of `remix`. Remix holds the content fixed and changes the style. Update holds the style fixed and adds content. Every instinct that makes `create` good — take a risk, make a distinctive choice, spend boldness once — is wrong here. The whole job is disappearing.

**The success test is the seam test.** Screenshot the page with the new work in it and show it to someone who has not seen either version. If they can point at what is new, it failed. Not "does it look good" — does it look like it was always there.

## Step 0 — Confirm the archetype

Name it from the existing site rather than from the brief. In this mode the archetype is a fact to be observed, not a decision — and it constrains what the new work is allowed to be. A settings screen added to an internal tool inherits that tool's density, not the polish you would give a consumer app.

## Step 1 — Acquire the system

Never design from a screenshot impression. Get the actual values.

If the `design-dna` skill is available, run its extraction and manual pass. It produces `tokens.json` and a profile with the axes already estimated, plus the `GAPS` and `STATES` lists this mode depends on most.

Without it, do it by hand: read the stylesheet, list every color with its role, measure the spacing scale, name the type roles, count the radii and elevation levels, and record the motion durations.

Either way you need two things the tokens do not contain:

- **`STATES`** — which of hover, focus, active, disabled, loading, empty, and error the site actually defines. You will have to build these for the new work, and if the site defines them inconsistently you need to know which variant is most common.
- **`GAPS`** — what the system does not define. This is where every drift comes from.

## Step 2 — Build the pattern inventory

Tokens are not enough. Two developers can use identical tokens and produce visibly different components, because a design system is also a set of *idioms*. Write these down before building:

```
COMPONENT IDIOMS
  card          padding, radius, border vs shadow, header treatment
  button        the full hierarchy - primary/secondary/ghost/destructive,
                and how each is distinguished
  form field    label position, help text, error placement, required marker
  section       header pattern, spacing above/below, max width, full-bleed?
  list/table    row height, zebra or rules, hover, sort affordance
  modal         width, scrim opacity, close affordance, footer actions

STRUCTURAL IDIOMS
  grid          columns, gutter, container width, where full-bleed is allowed
  rhythm        section spacing by hierarchy level - the actual numbers
  headers       eyebrow? rule? centered or left? which weight?
  icons         which library, stroke weight, size tokens, filled vs outline

CODE IDIOMS
  styling       utility classes / CSS modules / styled-components / plain CSS
  naming        BEM, camelCase, kebab, file-per-component?
  composition   compound components? boolean props? render props?
  file layout   where does a new component go, and what else goes with it

COPY IDIOMS
  buttons       verb form and capitalization - "Save changes" vs "Save Changes"
  errors        register and structure
  empty states  tone, and whether they offer an action
  headings      sentence case or title case
```

Code idioms matter as much as visual ones. A component that looks perfect but is written in a foreign style is still a seam — the next developer hits it and has to context-switch.

## Step 3 — Find the nearest precedent

For each new element, find the closest thing that already exists and copy its structure. Not approximately: actually open it and follow it.

- Adding a settings page? Find the most structurally similar existing page and match its header, spacing, and section pattern.
- Adding a data table? Find the existing table.
- Adding a card variant? Start from the existing card and change one thing.

**Precedent beats preference, always.** If the existing cards use a 1px border and no shadow, the new card uses a 1px border and no shadow, even where a shadow would look better. Improving one component in isolation makes it stand out, which is the failure condition. Consistency is the deliverable.

## Step 4 — Extend only where there is no precedent

Sometimes the system genuinely has no answer — the site has never had a date picker, a multi-step form, an empty state for this list. Now you are extending, and the rule is: **derive the extension from the system's own logic, not from your taste.**

Ask what this system would have done:

- Its radius personality is sharp (0–2px)? The new component is sharp, even if the pattern is usually rounded elsewhere on the web.
- Its elevation is borders rather than shadows? The new overlay uses a border.
- Its spacing base is 4px and it never uses 12? Do not introduce 12.
- Its motion is 100ms interaction-only? The new component does not animate in.

When you extend, say so explicitly in your handoff:

```
EXTENDED THE SYSTEM
  new: --color-warning #B8730A
  why: no warning color existed; derived by taking the existing danger
       hue and rotating toward amber at matching saturation and lightness
       so it sits in the same family
  check: 4.9:1 on --surface (passes AA body)
```

Never extend silently. An undocumented new token is how a six-color system becomes a nineteen-color system.

## Step 5 — When the existing system is bad

This is common, and it is a decision that belongs to the user, not to you.

If the extraction found seventeen spacing values, eleven grays, and six shadows, matching it faithfully means propagating the mess. Improving it means the new work is visibly better, which is a seam.

Surface it plainly, quantified, and ask:

> The existing pages use 17 distinct spacing values and 11 grays with no
> token layer. I can either (a) match the surrounding pages exactly so the
> new section is invisible, or (b) build it on a tight scale derived from
> the most common existing values, which will look slightly cleaner and
> could serve as the start of a system. Which do you want?

Default to (a) if they do not answer. Invisible is the brief.

## Step 6 — Build

Match every axis. Use the existing tokens by name — never a raw hex that happens to equal a token's value, because that breaks theming and it is how drift starts.

Build every state the surrounding components have. If existing cards have hover, focus, and loading states, the new card has all three, done the same way.

Head and identity, for a new page: use the existing favicon and manifest untouched. Match the site's title pattern exactly — if interior pages read `Settings — Brand`, the new page is `Billing — Brand`, not a new invention. Match the existing meta and OG structure.

## Step 7 — Verify with a diff

Run the checks:

```bash
python3 scripts/contrast.py --tokens tokens.json    # any new color pairs
python3 scripts/ai_tells.py <new files>             # only new tells count
```

On `ai_tells.py`: tells the site already had everywhere are house style in this mode, not findings. Only flag tells the *new* work introduced. If the whole site uses Inter, the new section uses Inter. Raise the house-wide tells separately as an observation, not as a blocker — that is `remix` or `audit` territory, and mixing it into an update is scope creep.

Then the seam test, honestly:

```
SEAM CHECK
  [ ] every color used by token name, no raw values
  [ ] spacing values all appear in the existing scale
  [ ] radius matches the site's personality
  [ ] elevation uses an existing level, not a new one
  [ ] type sizes come from the existing scale
  [ ] icons from the same library at the same stroke and size
  [ ] every state the neighbors have
  [ ] motion durations and easing match
  [ ] copy register matches - read three existing buttons and compare
  [ ] code idioms match - naming, styling approach, file layout
  [ ] page title follows the existing pattern
  [ ] a stranger cannot pick the new section out of a screenshot
```

## Handoff

```
ADDED           what was built, and where
PRECEDENTS      which existing components each part was derived from
EXTENDED        any new tokens or patterns, with the derivation and why
                nothing existing could be reused
MATCHED         the axes verified against the existing system
NOT FIXED       problems noticed in the surrounding code and deliberately
                left alone, because fixing them was out of scope and would
                have created a seam
```

That `NOT FIXED` list is worth writing every time. It shows the problems were seen rather than missed, and it gives the user a ready-made backlog if they want an `audit` next.

---

# Mode: audit

Review an existing interface and produce a phased, implementation-ready plan. This mode does not add features. It elevates what exists.

## Step 1 — Understand before judging

Read what exists: design system or tokens, component structure, routes and flows, the PRD if there is one, the stack and what it supports. Then walk every screen at 375px, tablet, and desktop. Experience it as a user before opening the code.

Forming an opinion before this is complete produces cosmetic notes instead of structural ones.

## Step 2 — Review every dimension

| Dimension | The question |
|---|---|
| Visual hierarchy | Does the eye land where it should? Is the primary action unmissable? Is the screen readable in two seconds? |
| Spacing and rhythm | Is whitespace intentional and consistent? Does vertical rhythm differ by hierarchy level? |
| Typography | Clear scale? Too many weights competing? |
| Color | Restraint and purpose? Guiding attention or scattering it? |
| Alignment and grid | Is everything locked to a grid? Anything off by 1–2px? |
| Components | Identical across screens? All states covered — hover, focus, active, disabled, loading? |
| Iconography | One set, one weight, one size system? |
| Motion | Purposeful, interruptible, reduced-motion aware? |
| Empty states | Designed, or broken? Does the user know what to do next? |
| Loading states | Skeletons matching content shape, or a spinner? |
| Error states | Do they say what happened *and* the fix? |
| Dark mode | Actually designed, or inverted? Do borders survive? |
| Density | What can be removed? |
| Responsiveness | Intentional at every viewport, not just non-broken? |
| Accessibility | Contrast, keyboard path, focus visibility, ARIA, screen-reader order |
| **Archetype fit** | Run `archetypes.md`. Is this built to the conventions of the category it actually belongs to? Does it imply more scale than it has? |
| **Copy** | Run `copy-gate.md`. Buttons, errors, empty states, invented content, borrowed-weight language |
| **Distinctiveness** | Run `ai-tells.md`. Could this be any other product? |

Check the code against `interface-guidelines.md`. Run `scripts/contrast.py` on the palette and `scripts/ai_tells.py` on the source.

## Step 3 — Apply the reduction filter

For every element on every screen:
- Can it be removed without losing meaning? → Remove it.
- Would a user need to be *told* it exists? → Redesign until it is obvious.
- Is its visual weight proportional to its functional importance? → If not, fix the hierarchy.

## Step 4 — Write the plan

Group findings into three phases. Every item names a file and location, states the change, and gives the design reason.

**Phase 1 — Critical.** Hierarchy, usability, accessibility, and responsiveness failures that actively hurt users.
**Phase 2 — Refinement.** Spacing, type, color, alignment, iconography, and consistency.
**Phase 3 — Polish.** Micro-interactions, transitions, empty/loading/error states, dark mode, distinctiveness.

Format each finding:

```
path/to/File.tsx:42 — Primary CTA and secondary link share the same weight
  Change: secondary → ghost variant, primary → filled at `--color-primary`
  Reason: the screen currently presents two equal actions, so the eye
          has no entry point; hierarchy should match functional priority
```

Never write a cosmetic instruction without the structural reason. "Make this blue" is not a finding. "Raise CTA contrast against secondary actions so the primary path is unambiguous" is.

## Step 5 — Deduplicate

If one component fails a rule, its siblings probably do too. Group by root cause and component family. Thirty instances of one problem is one finding with a count, not thirty findings. If a single sweep produces more than roughly fifty violations, stop and narrow the scope — an unactionable report is not an audit.

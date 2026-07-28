# Conventions

Which conventions are load-bearing, which are herd behavior, and where popular design advice stops applying.

Synthesized from two commonly-cited web design talks — one on the psychology of interfaces (mental models, MAYA, cognitive load), one on premium layout principles (hero composition, hierarchy, whitespace, contrast, social proof, typographic restraint, mobile-first). Their genuinely additive parts are below. Their conflicts with this skill are recorded at the bottom, with reasons, so a later edit does not silently "fix" a deliberate departure back into a default.

---

## 1. Load-bearing conventions

`peer-research.md` teaches how to tell convention from herd behavior: ask what breaking it costs the user. A few conventions have a real cost and should be treated as fixed unless the brief explicitly buys the deviation.

| Convention | Cost of breaking it |
|---|---|
| Logo top-left, linking home | It is the universal escape hatch. Users click it when lost. |
| Primary navigation at or near the top | Hiding it below the fold means it does not exist for a large share of visitors. |
| Footer at the bottom, carrying secondary links | Contact, legal, and social are looked for there by habit. |
| Current location indicated in the nav | Without it, a multi-page site feels like unrelated pages. |
| Underlined or otherwise distinguished in-body links | Color alone fails for color-blind users and is an accessibility failure, not a style choice. |
| Clickable things look clickable, non-clickable things do not | The most expensive convention to break; it makes an interface feel broken rather than novel. |
| Back button behaves predictably | Breaking it is the fastest route to a bounce. |
| Form submit at the end of the form | Users scan to the end looking for it. |

**These are the floor, not the design.** Following all of them produces a site that works and looks like everything else. The distinctiveness comes from everything *not* on this list — palette, type, layout system, density, signature. Spend freedom there.

**Everything else in the category is suspect.** A hero with two buttons, a three-column feature grid, alternating section backgrounds — none of these have a comprehension cost. They are herd behavior, and per `peer-research.md` they are the best available differentiation.

## 2. MAYA — novelty inside a familiar frame

*Most Advanced Yet Acceptable*, from Raymond Loewy. The most novel thing people will accept is bounded by how familiar the rest of it feels.

This is the mechanism behind two rules already in this skill, and naming it explains why they work together:

- **"Spend boldness once"** (`SKILL.md`) — one signature carries the identity, everything else stays disciplined. The discipline is what buys the signature its acceptance.
- **The AI-tell catalogue** — the opposite failure. Zero novelty, maximum acceptability, completely forgettable.

Practically: put the novelty in the *content-bearing* layer — the signature element, the palette's source, the type pairing, the layout of the thing the user came for. Keep the *navigational* layer conventional. A site can have a wall of nineteen photographs as its front page and still put the logo top-left.

The inverse — conventional content in an alien shell — is the worst outcome. It reads as broken rather than distinctive, and it spends the user's patience on nothing.

## 3. Proof belongs where doubt occurs

The principle is sound and the standard implementation is dangerous.

**Sound:** evidence is worth most at the moment of hesitation. A testimonial on a dedicated reviews page does nothing; the same testimonial beside the pricing table answers a question the user is asking right then. Proof adjacent to the decision, not filed away from it.

**Dangerous:** the usual implementation is a logo cloud under the hero and a testimonial carousel by the pricing tiers. Both are content slots, and per `archetypes.md` §2, **a slot with no content behind it forces invention.** A pre-revenue product given a logo-cloud slot gets fabricated logos. A twelve-person club given a testimonial slot gets `Sarah Chen, CTO at TechCorp`.

**The rule here:** identify the actual moment of doubt, then place whatever *real* evidence exists at it. What counts as proof depends entirely on archetype:

| Archetype | The doubt | Real proof |
|---|---|---|
| Product marketing | "Does this work, and who else uses it?" | Named customers, a working demo, real numbers |
| Single-purpose utility | "Is my file safe?" | A checkable mechanism — a header, a request counter, an offline test |
| Club / campus org | "Is this real, and are these my people?" | Photographs of actual members, dated projects, named officers |
| Portfolio | "Is this person any good?" | The work, with the specific role owned |
| Open-source | "Is this maintained?" | Recent commits, real issue activity, a runnable example |
| Nonprofit | "Where does the money go?" | Financials, outcomes with numbers |

If no real proof exists, **the answer is no proof slot** — not a slot filled with invention. An empty, honest page outperforms a fabricated one, because fabrication is detectable and detected fabrication costs more than absence.

## 4. Where marketing-site advice stops applying

Most popular web design advice is written for one archetype — the conversion-oriented marketing page — and presented as universal. It is not. Before applying any of it, check the archetype.

| Advice | Applies to | Wrong for |
|---|---|---|
| Hero as a complete pitch above the fold | Product marketing, agency, nonprofit, event | App UI and internal tools (a hero is a delay), docs (search is the hero), utility (the tool is the hero), editorial (the writing is) |
| Generous whitespace signals quality | Marketing, editorial, portfolio | Dashboards, admin, archival, tables — density is the quality signal there |
| Brightest color reserved for the CTA | Marketing pages with one conversion goal | Tools where color encodes state; anything where the accent is doing identity work |
| Chunk everything into 3–4 items | Marketing, pricing, onboarding | Data-dense work. A table with 200 rows is not chunked into four. |
| One or two typefaces maximum | Marketing, editorial | Anything numeric — see the departure note below |
| Social proof near the decision point | Products with real customers | Anything pre-revenue, volunteer-run, or personal, where the slot forces invention |

The general form: **conversion-optimization advice optimizes for a stranger deciding whether to trust you.** When the user is already inside the product, already a colleague, or arrived from search mid-task, it is the wrong objective and its rules invert.

## 5. Deliberate departures

Recorded so they are not re-litigated. Each is a place this skill knowingly contradicts widespread advice.

**"Limit to one or two typefaces."** This skill specifies **three roles** — display, body, and a **utility face** for numbers, captions, labels, and code (`design-tokens.md`). Reason: two-face systems set tabular data in the body face, and that is a primary reason data-heavy interfaces read as amateur. The intent behind the common advice — restraint — is preserved by capping *weights* at three and by keeping the display face on a short leash. Three purposeful families beat two families plus a compromise.

**"Every hero needs headline, subtext, social proof, and a CTA."** That exact stack is the opening of the canonical AI section order (`ai-tells.md` §3) and is the single most recognizable template on the web. This skill treats the hero as *the archetype's ten-second job*, whatever that is: a meeting time for a club, a working tool for a utility, a specimen run for a field-log app. Sometimes that includes proof and a CTA. It is not a fixed slot list.

**"Chunk into 3–4 items; working memory holds about four."** The underlying research concerns *recall*, not visual scanning — nobody memorizes a pricing table, they look at it. Enforced as a layout rule it produces the three-column feature grid (`ai-tells.md` §3), which is itself a tell. This skill's version: group by meaning where meaning exists, and let density follow the archetype.

**"Alternate section backgrounds to separate content."** Rejected outright. Four or more surface backgrounds is patchwork (`ai-tells.md` §3), and needing bands to make a page legible is a signal the page should be split (`site-architecture.md` §3).

**"Add subtle micro-interactions for delight."** Narrowed. Motion must explain something (`motion.md`). Delight-motivated animation applied uniformly becomes the scroll-reveal tell. MAYA is served by one considered moment, not by a hover-scale on every card.

**"Use opacity for hierarchy — set secondary text to ~55%."** Adopted in principle, gated in practice. Hierarchy by weight and color rather than size alone is sound and often better than another type step. But opacity in the 50–60% range fails contrast on most palettes, and "muted" is not permission to fail (`design-tokens.md`). Set secondary text as a *token with a measured value*, not an opacity multiplier, and check it with `scripts/contrast.py`. This exact failure showed up in testing at 2.95:1.

**"Pick a theme: friendly means warm and rounded, premium means grayscale and sharp."** The useful half is the decomposition — layout skeleton and visual treatment are separable, and holding one constant while varying the other is exactly what the divergence matrix does. The harmful half is the two-item menu. Choosing from a short list of vibes is how the three cluster looks (`ai-tells.md` §10) get produced, and it skips the step where the treatment gets derived from the subject. Use `style-taxonomy.md` in `design-dna` instead: ~30 families defined by their mechanics rather than two moods.

**"Cap headlines at ~7 words, subtext at ~14."** Directionally right, wrong as a cap. Brevity serves scanning, but the actual rule is *one idea per headline* — a long headline is usually doing two jobs and should be split, not truncated. A hard word limit pushes toward vague-but-short, and specific beats impressive every time (`copy-gate.md`).

**"Use these spacing values: 8px, 12px, 32px."** The relationship is right and the numbers are not universal. Proximity encodes grouping (`design-tokens.md`), but the magnitudes follow the density the archetype calls for. Fixed pixel prescriptions produce identical spacing on a dashboard and a poster.

## 6. What is already covered elsewhere

Do not duplicate these into new rules; they exist with more precision:

- Visual hierarchy, whitespace, spacing rhythm → `design-tokens.md`, and audit mode's dimension table in `modes.md`
- Contrast and never signalling by color alone → `interface-guidelines.md` §1, enforced by `scripts/contrast.py`
- Mobile: 44×44pt targets, spacing between targets, readable body size, no zoom disabling → `interface-guidelines.md` §2
- No horizontal overflow: every text container needs an overflow strategy, and flex children need `min-w-0` → `interface-guidelines.md` §4
- Typographic restraint on weights → `design-tokens.md`
- Proximity, grouping, and spacing relationships → `design-tokens.md`
- Text-over-image legibility → `interface-guidelines.md` §4
- Multi-step journeys, escape hatches, conditional paths → `flows.md`

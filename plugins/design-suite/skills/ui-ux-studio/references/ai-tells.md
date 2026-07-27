# AI Tells: the catalogue

Anti-AI *writing* tools scan prose. They do not catch design. A page can pass every prose filter and still be immediately legible as machine-made, because the tells live in the palette, the grid, the icon choices, and the section order.

This file is the detector. Use it twice: once against the design plan, before any code exists, and once against the built output.

**The rule for every entry below:** the fix is never "pick a different default." Swapping indigo for emerald produces the same page in a different color. The fix is to derive the choice from the subject — its materials, instruments, environment, vocabulary, constraints, history.

---

## Contents

1. [Palette tells](#1-palette-tells)
2. [Typography tells](#2-typography-tells)
3. [Layout and structure tells](#3-layout-and-structure-tells)
4. [Component tells](#4-component-tells)
5. [Iconography tells](#5-iconography-tells)
6. [Motion tells](#6-motion-tells)
7. [Copy tells](#7-copy-tells)
8. [Favicon and identity tells](#8-favicon-and-identity-tells)
9. [Borrowed institutional weight](#9-borrowed-institutional-weight)
10. [The three cluster looks](#10-the-three-cluster-looks)
11. [De-slopping procedure](#11-de-slopping-procedure)

---

## 1. Palette tells

| Tell | What it looks like | Why it reads as AI |
|---|---|---|
| Claude cream + terracotta | `#F4F1EA` / `#FAF9F5` surface with a `#D97757`-family accent | This is Anthropic's own interaction accent. On a user's brief it is a fingerprint. |
| Indigo default primary | `#6366F1`, `#4F46E5`, Tailwind `indigo-500/600` as the primary | The framework default, chosen by not choosing |
| The purple-blue gradient | `linear-gradient(135deg, #667eea, #764ba2)` and near neighbors | A decade-old template gradient that survives in training data |
| Acid accent on near-black | `#0A0A0A` or `#09090B` ground, one `#A3E635` / `#00FF88` / `#FF3D00` accent | Cluster look #2. Legitimate for some briefs, a default for most. |
| Gradient text headline | `background-clip: text` on the h1 | Decoration where the type should carry the weight |
| Uniform glass surfaces | Every card at `rgba(255,255,255,0.05)` + `backdrop-filter: blur(12px)` + `border-white/10` | One material used for everything, so the material means nothing |
| Slate-only neutrals | The whole neutral ramp is Tailwind `slate` or `zinc`, untinted | Neutrals should carry temperature borrowed from the subject |
| Aurora / blob background | Blurred colored ellipses behind the hero, unrelated to content | Atmosphere with no argument |

**Derive instead.** Palettes have sources: the anodized colors of the hardware, the ink and paper of the trade's documents, a species' actual coloration, the safety-color conventions of the industry, the light at the hour the product gets used. A logistics tool can take its palette from shipping-container paint codes. A sleep app can take it from what a room actually looks like at 4am — which is not navy blue.

---

## 2. Typography tells

| Tell | What it looks like |
|---|---|
| Inter everywhere | Inter, Inter Tight, or Geist as *both* display and body |
| The safe four | Roboto, Poppins, Montserrat, Open Sans as the display face |
| Serif-for-editorial reflex | Any grotesque body + Playfair Display / Instrument Serif display, regardless of subject |
| The clamp hero | `font-size: clamp(3rem, 8vw, 6rem)` on an abstract headline |
| Uppercase tracked eyebrow | `text-xs uppercase tracking-widest text-muted` above every single section |
| Weight soup | 300, 400, 500, 600, 700, 800 all in use with no system |
| No utility face | Numbers, captions, code, and body all set in one family |

**Derive instead.** Type has lineage. Technical products can borrow from the documents of their field: engineering drawings, flight manuals, lab notebooks, ledgers, transit signage, pharmacy labels. Pick a display face that would look *wrong* on a different brief, then let the body face stay quiet. Set an actual scale — 5 to 7 steps with a stated ratio — rather than picking sizes per element.

Set numbers with `font-variant-numeric: tabular-nums` in any column or comparison. Use `text-wrap: balance` on headings.

---

## 3. Layout and structure tells

| Tell | What it looks like |
|---|---|
| **The canonical section order** | hero → logo cloud → 3 features → testimonial → stats → pricing → CTA → footer, in exactly that order |
| The three-column feature grid | Always three. Icon in a tinted rounded square, bold title, two lines of gray body. Identical weights across all three. |
| `01 / 02 / 03` markers | Numbered eyebrows on content that is not a sequence |
| Decorative bento | Bento grid where the content is homogeneous, so the varied cell sizes encode nothing |
| **Background band alternation** | Every section gets a different background — white, then gray-50, then white, then dark, then tinted — to fake structure. Real hierarchy comes from type, space, and scale; band colour is what gets reached for when those are absent |
| **Route collapse** | A multi-page site rendered as one enormous scroll, with the nav reduced to `#anchors`. Usually a symptom rather than a choice, and it is what forces the band alternation above |
| Uniform `py-24` | Every section vertically padded identically, so hierarchy has no rhythm |
| Centered everything | `max-w-7xl mx-auto` on every section, zero asymmetry, no full-bleed, no grid breaks |
| `rounded-2xl` + `shadow-lg` | Every surface the same radius, same elevation, same border |
| Stat triad | Three round invented numbers: `10x`, `99.9%`, `500+` |

**On backgrounds specifically.** A page wants one ground, with at most one or two deliberate departures that mean something — a genuine inversion for a single band that is doing different work. Four or more distinct section backgrounds is not a palette, it is patchwork, and it reads as machine-made because it is what happens when content is stacked without structure. If a page needs bands to be legible, the page is doing too much: split it (`site-architecture.md` §3) rather than picking better band colours.

**Derive instead.** Structure should encode something true. Numbered markers belong on an actual sequence. A bento grid belongs where cells genuinely differ in importance. Section spacing should differ by hierarchical level (e.g. 128 / 96 / 64 / 40), not repeat. Ask what the *characteristic artifact* of this subject looks like — a boarding pass, a spec sheet, a score, a chart, a receipt, a map legend — and let the layout borrow its logic.

The hero is a thesis. Open with the most characteristic thing in the subject's world, in whatever form fits: a live demo, an instrument reading, a specimen, a map, one enormous piece of type. A big number with a small label and a gradient accent is the template answer.

---

## 4. Component tells

- Every card identical: same padding, radius, border, shadow, hover lift
- `hover:scale-105` on everything hoverable
- Testimonial cards with generated avatars and invented titles
- Pricing table with the middle tier scaled up and badged "Most Popular"
- A FAQ accordion that exists because landing pages have FAQ accordions
- Buttons that are all the same size, so primary and secondary read as equals
- Empty states that are a gray box, or absent entirely
- Loading states that are a centered spinner instead of a skeleton matching the content shape

## 5. Iconography tells

Keyword-matched Lucide icons are the loudest tell in the catalogue:

`Zap` → fast · `Shield` → secure · `Rocket` → launch · `Sparkles` → anything AI · `Users` → team · `BarChart3` → analytics · `Globe` → global · `Lock` → privacy · `Check` → benefit

Also: emoji used as structural icons (font-dependent, untokenizable, unthemeable), mixed icon libraries in one interface, mixed filled and outline at the same hierarchy level, inconsistent stroke widths, and every icon sitting in a tinted rounded square.

**Derive instead.** Use the symbols the field already uses. Or use no icons — a well-set label often beats a generic glyph. If icons are needed, pick one set, one stroke weight, one size token per level, and align to the text baseline.

## 6. Motion tells

| Tell | Fix |
|---|---|
| Every section `fade-in-up`, 0.6s, ease-out, on scroll | One orchestrated moment beats scattered uniform reveals |
| `transition: all` | List properties explicitly |
| `hover:scale-105` universally | Reserve scale for one element that earns it |
| Animating `width`, `height`, `top`, `left` | Animate `transform` and `opacity` only |
| No `prefers-reduced-motion` branch | Always provide one |
| Motion that ignores the subject | Ask how things in this subject's world actually move |

See `motion.md` for timing, easing, and the reduced-motion pattern.

## 7. Copy tells

Design copy is design material. These phrasings undo good visual work:

- "Transform your X into Y" · "Take your X to the next level"
- Effortlessly, seamlessly, unlock, elevate, supercharge, empower, streamline, harness, leverage, revolutionize
- Two-abstract-noun feature titles: "Smart Insights", "Powerful Analytics", "Seamless Integration"
- The em-dash triad: "Fast, simple — and secure."
- "Built for teams who move fast"
- Invented testimonials: `Sarah Chen, CTO at TechCorp`, `Marcus Rodriguez, Head of Growth`
- Vague CTAs: "Get Started", "Learn More", "Continue"

**Write instead.** Name what the thing does in the user's words. Buttons say what happens: "Save API key", not "Submit" — and the resulting toast says "API key saved". Errors state what went wrong *and* the next step. Empty states are invitations to act, not apologies. Active voice, sentence case, second person, numerals for counts.

This is a summary. The full gate every string must pass is `copy-gate.md`, which covers buttons, errors, empty states, labels, sample content, and the borrowed-weight vocabulary above. Hand prose longer than about two sentences to `anti-ai-writing` or `avoid-ai-writing` if either is available.

## 8. Favicon and identity tells

- Brand's first letter, white, in a rounded square, on a purple-blue gradient — the single most common AI favicon
- A generic Lucide glyph reused as the mark
- A mark with strokes so fine it dissolves at 16px
- No dark-mode variant, so the mark disappears in a dark browser chrome
- Page title reading `Home | Brand` or just `Brand`
- No OG image, so every share renders as a gray rectangle

See `favicon-and-head.md`.

## 9. Borrowed institutional weight

The highest-level tell, and the one no scanner catches: the design implies more scale, age, custody, or activity than the subject actually has. AI reaches for gravitas the subject has not earned, because impressive framings are better represented in training data than plain ones.

This is a *concept* tell. It survives a perfect token system, a distinctive typeface, and a clean tell scan, because the problem is what the design is claiming rather than how it looks.

| Borrowed form | Claims | Fails when |
|---|---|---|
| Archive / ledger / register, accession numbers | Decades of records under institutional custody | Two years old, three entries |
| Live status board, ops readout | Continuous operation worth monitoring | No live state — or worse, live state that reads as empty |
| Enterprise trust furniture, compliance badges | Procurement review | Nothing is being sold |
| Logo cloud, "trusted by" | Named consenting customers | There are none |
| Testimonial wall | Volume of user opinion | The people would have to be invented |
| Round stat triad — 10x, 99.9%, 500+ | Measured scale | The real numbers are 12 and 3 |
| Manifesto hero | Earned authority | The reader has never heard of you |

**The language gives it away first.** *on the books · on record · standing record · accession · register opened · revised [date] · stamped · of record · status: live · currently running · crew · on duty · channels · board revised · operational.* Each is correct when true and a tell when borrowed.

**Test:** would the subject's own people use this word about themselves? A student club says "we have twelve people." It does not say "twelve members on the books."

**Worked example.** Three directions for a twelve-person campus club, all passing the divergence matrix. One framed it as an institutional archive (eleven borrowed terms), one as an operations dashboard (nine, including a live board showing "0 currently running" and "Next session: None set"). The third said "Twelve people, one room, three shipped products" and used the nineteen real photographs the club already had. Only the third worked. The first two were not under-designed — they were dishonest about scale, and that reads as machine-made regardless of execution quality.

The fix is never restyling. Go back to `archetypes.md`, redo the scale-honesty step, and choose a concept the subject can actually carry.

The inverse exists and is rarer: rendering genuinely high-stakes work as casual and playful, which undercuts trust the product needs.

## 10. The three cluster looks

Current AI design output clusters hard around three complete looks. Recognize them as wholes, not just as component parts:

1. **Warm editorial minimal** — cream `#F4F1EA` ground, high-contrast serif display, terracotta accent, generous whitespace, thin rules.
2. **Dark technical** — near-black ground, one acid accent, monospace labels, subtle grid overlay, glow effects.
3. **Broadsheet** — hairline rules, zero border-radius, dense multi-column type, small caps, black and white with one spot color.

Each is a real, good look for the right brief. The problem is that they appear *regardless of brief*. If the brief pins a direction, follow it exactly — the brief always wins. Where the brief leaves an axis free, do not spend that freedom on one of these three.

## 11. De-slopping procedure

Given a design plan or a built page:

0. **Check the archetype first.** Run `archetypes.md` and the scale-honesty test. A concept-level failure cannot be patched at the CSS level, so establish there isn't one before spending effort on tells.
1. **Scan.** Run `scripts/ai_tells.py` on the code. Walk the plan against sections 1–8 by hand — the scanner catches the mechanical tells, not the structural ones.
2. **Count.** More than three tells means the design is a default, not a decision. Do not patch it; go back to the plan.
3. **For each tell, trace it to a source.** Ask: what in this subject's world determines this choice? If nothing does, the element probably should not exist.
4. **Run the swap test.** Take a different brief in the same category and imagine designing it. Every element you would keep unchanged is generic. That is the list to fix.
5. **Justify or remove.** A tell that survives needs a stated reason tied to the brief. "The client is a ceramics studio, the terracotta is the actual glaze color" is a reason. "Warm tones feel inviting" is not.
6. **Remove one more thing.** There is always one accessory too many. Usually a gradient, a badge, or a third font weight.

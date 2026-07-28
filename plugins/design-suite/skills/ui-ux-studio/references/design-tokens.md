# Design tokens

A token system is what stops a design from drifting. Without one, the fourth screen invents its own gray and the design dies by a thousand one-off hex codes.

## Three layers

Never let a component reference a primitive directly. The semantic layer is what makes theming and redesign possible.

```
PRIMITIVE          raw values, no meaning
  --blue-500: #2563EB
  --space-4: 16px

SEMANTIC           role-based, theme-aware
  --color-surface, --color-surface-raised, --color-ink,
  --color-ink-muted, --color-primary, --color-border,
  --color-danger, --color-focus

COMPONENT          only when a component genuinely deviates
  --button-primary-bg: var(--color-primary)
```

The test: switching to dark mode should require editing only the semantic layer.

## Palette construction

Six to eight semantic colors is enough. More means the system is doing the deciding instead of you.

| Role | Notes |
|---|---|
| surface | The page ground. Rarely pure white or pure black — both are harsh and both are defaults. |
| surface-raised | Cards, sheets, popovers. Must be distinguishable from surface in *both* themes. |
| ink | Body text. Needs ≥4.5:1 against surface. |
| ink-muted | Secondary text. Needs ≥4.5:1 too — "muted" is not permission to fail contrast. |
| primary | The one action color. |
| accent | The color that does the personality work. Used sparingly. |
| border | Must remain visible in both themes. |
| danger / success | Never the only signal — always pair with text or icon. |

**Sourcing.** Derive from the subject, per `ai-tells.md` §1. Give neutrals a temperature borrowed from the palette rather than using an untinted gray ramp — tinted neutrals are one of the clearest signals of a designed palette versus a picked one.

### Ramps

A flat palette — one hex per role — can only fill a surface at full strength or not at all. That constraint quietly forces a boundary style: with no tints available, the only way to separate a card from the page is a border or a heavy shadow, and the design goes boxy by necessity rather than by choice.

Give each chroma color a small ramp and the soft options become real:

```
--accent-100   tinted fills: hover states, quiet backgrounds, selected rows
--accent-300   soft emphasis: tags, meter tracks, secondary data marks
--accent-500   the color itself: primary actions, key data
--accent-700   pressed states, text-on-tint, links on hover
```

Three to five steps per chroma color. Generate them by holding hue and moving lightness (dropping chroma toward the light end), not by adding opacity — translucent tints composite unpredictably over imagery and break the contrast math. Neutrals already get a ramp (surface, raised, border, muted); this extends the same courtesy to the accents.

Two rules: the semantic layer references ramp steps (`--color-hover: var(--accent-100)`), and components never reach into a ramp directly. Any text on a tinted fill must pass contrast against *that tint*, checked as a real pair.

**Dark mode is a design, not an inversion.** Reduce chroma on dark grounds; saturated colors vibrate. Surfaces get *lighter* to come forward, not darker. Shadows barely work — use elevation via surface lightness and border instead. Verify contrast independently for each theme.

Run `scripts/contrast.py` on the finished palette.

## Type scale

Set a ratio, then generate. Do not pick sizes per element.

| Ratio | Feel | Use |
|---|---|---|
| 1.125 minor second | Tight, dense | Dashboards, data tools |
| 1.200 minor third | Balanced | Most product UI |
| 1.250 major third | Clear hierarchy | Marketing, content |
| 1.333 perfect fourth | Dramatic | Editorial, landing pages |
| 1.500+ | Very dramatic | Display-led work only |

Five to seven steps. Body at 16px minimum — 14px body is a readability failure that reads as "designed on a large monitor". Line height 1.5 for body, tightening to 1.1–1.2 for display sizes. Measure of 60–75 characters for long-form.

Three roles, not one: a **display** face with character, used with restraint; a **body** face that stays quiet; a **utility** face for numbers, captions, labels, and code. Skipping the utility face is what makes data-heavy interfaces feel amateur.

Cap weights at three in active use. Six weights is weight soup.

## Spacing

One scale, 4px or 8px base, geometric rather than linear:

```
4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96 · 128
```

### Proximity encodes grouping

Spacing is not decoration between elements — it is the notation that says which elements belong together. Two things close together read as one unit; the same two things at equal distance from everything else read as unrelated.

**The rule is relative, not absolute:** the gap *within* a group must be visibly smaller than the gap *to the next group* — a step or two apart on the scale, not a few pixels. A heading, its eyebrow, and its subtext form one cluster; the button that follows belongs to the cluster but sits further out; the next section is further still.

```
eyebrow            gap: one step   (tightest — it labels the heading)
HEADING            gap: one step   (subtext explains the heading)
subtext            gap: three steps (the action is related, not part of the text)
[ button ]
                   gap: six steps  (next section is a different thought)
```

The common failure is uniform spacing: every element the same distance apart, so nothing groups and the eye has no structure to follow. That is also what makes a page reach for background bands to fake the structure spacing should have provided (`ai-tells.md` §3).

Do not hardcode the pixel values. A dense dashboard and a spacious marketing page express the same relationships at different magnitudes — the *ratios* carry across, the numbers do not.

Density changes the scale, not the system:
- **Spacious** — start at 24, go to 128. Marketing, editorial.
- **Standard** — 16 to 64. Most product UI.
- **Dense** — 8 to 32. Dashboards, tables, tools.

Section spacing must differ by hierarchy level. Uniform `py-24` on every section is a tell (`ai-tells.md` §3) because it flattens structure into a stack.

## Form language: radius, elevation, boundary

Radius, shadow, and border are one decision, not three — together they are the form language, and it gets derived from the subject like everything else. Soft is not friendlier by default; sharp is not more serious by default.

**Pick one boundary treatment** and hold it:

| Treatment | Mechanics | Character |
|---|---|---|
| Border-delimited | flat fills, 1px borders, radius 0–4 | drawn, technical, printed |
| Rule-delimited | no boxes — hairline rules and whitespace do the separating | editorial, archival |
| Elevation-layered | no borders; surface color plus a soft shadow separates layers | soft, physical, product |
| Tint-layered | no borders, no shadows; nested tinted fills from the ramps | calm, flat, modern |

Mixing treatments on one surface — a bordered card *with* a shadow *with* a tinted fill — is how boxes turn to mud. And the most common *unforced* boxiness is defaulting to border-delimited because the palette has no ramps: with tints and layering available, a card can sit on the page with no border at all.

**Radius personality**, held consistently: sharp (0–2), soft (4–8), round (12–16), pill. Two refinements:

- **Radius scales with the container.** A large card carries a larger radius than the button inside it; derive it (`calc(var(--radius-lg) * 1.15)`) rather than inventing a new stop.
- **Nested corners share a center:** inner radius ≈ outer radius minus the padding between them. An inner element with its container's exact radius looks subtly wrong at the corners.

**Elevation:** three levels maximum — flat, raised, overlay. Every card at `shadow-lg` means no card is elevated. The non-tell hover idiom is a small lift — `translateY(-2px)` plus one shadow step — not `scale()`.

## Motion tokens

```
--duration-instant: 100ms   /* state flips */
--duration-fast:    150ms   /* hover, focus */
--duration-base:    250ms   /* most transitions */
--duration-slow:    400ms   /* entrances, layout */
--ease-out:  cubic-bezier(0.16, 1, 0.3, 1)
--ease-in-out: cubic-bezier(0.65, 0, 0.35, 1)
```

## Token file shape

`scripts/contrast.py` reads this format:

```json
{
  "surface":       "#FDFCFA",
  "surface-raised":"#FFFFFF",
  "ink":           "#1A1614",
  "ink-muted":     "#5C5450",
  "primary":       "#0B4F6C",
  "accent":        "#C6572A",
  "border":        "#E3DDD6"
}
```

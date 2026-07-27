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

Density changes the scale, not the system:
- **Spacious** — start at 24, go to 128. Marketing, editorial.
- **Standard** — 16 to 64. Most product UI.
- **Dense** — 8 to 32. Dashboards, tables, tools.

Section spacing must differ by hierarchy level. Uniform `py-24` on every section is a tell (`ai-tells.md` §3) because it flattens structure into a stack.

## Radius, elevation, border

Pick a radius personality and hold it: sharp (0–2px), soft (4–8px), round (12–16px), or pill. Mixing `rounded-2xl` cards with `rounded-sm` inputs looks accidental unless it encodes a distinction.

Three elevation levels maximum: flat, raised, overlay. Every card at `shadow-lg` means no card is elevated.

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

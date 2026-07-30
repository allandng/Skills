# Interface guidelines

The quality floor. Meeting all of it produces a competent interface, not a distinctive one — pair it with `ai-tells.md`, which handles the other half.

Adapted from Vercel's Web Interface Guidelines, WCAG 2.2, and the `ui-ux-pro-max` priority model. Ordered by user impact.

## Priority order

When time is short, work down this list. Items 1–3 are non-negotiable; 4–7 separate good from shipped-anyway.

1. Accessibility and focus
2. Touch and interaction
3. Forms and feedback
4. Content handling and states
5. Performance and layout stability
6. Navigation and URL state
7. Theming, locale, and platform detail

---

## 1. Accessibility and focus

- Semantic HTML before ARIA: `<button>` for actions, `<a>`/`<Link>` for navigation. A `<div onClick>` is a bug.
- Icon-only buttons need `aria-label`. Decorative icons need `aria-hidden="true"`.
- Every image needs `alt`, or `alt=""` if truly decorative.
- Every form control needs a `<label>` or `aria-label`. Labels are clickable via `htmlFor` or wrapping.
- Headings run `<h1>`–`<h6>` in order, no level skips. Include a skip link to main content.
- `scroll-margin-top` on heading anchors so deep links don't hide under sticky headers.
- Async updates — toasts, validation, live counts — need `aria-live="polite"`.
- Visible focus on everything interactive. Use `:focus-visible`, not `:focus`, so the ring doesn't appear on mouse click.
- Never `outline: none` without a replacement indicator. This is the most common accessibility regression in AI-written CSS.
- `:focus-within` for compound controls so the whole group reads as focused.
- Screen-reader order must match visual order.
- Contrast: 4.5:1 for body text, 3:1 for large text and meaningful UI glyphs. Verify with `scripts/contrast.py` — do not eyeball it.
- Never convey meaning by color alone. Pair every color signal with text, icon, or pattern.

## 2. Touch and interaction

- Minimum touch target 44×44pt (iOS) / 48×48dp (Android), with ≥8px between adjacent targets. Expand hit area rather than enlarging the icon.
- `touch-action: manipulation` to kill the 300ms double-tap-zoom delay.
- `overscroll-behavior: contain` on modals, drawers, and sheets.
- Set `-webkit-tap-highlight-color` deliberately.
- Press feedback within 80–160ms. The reliable idiom: `transform: scale(0.97)` on `:active` with `transition: transform 160ms ease-out` — subtle (0.95–0.98), on any pressable element. Opacity or color shifts also work; never a layout-shifting property.
- Never disable zoom: `user-scalable=no` and `maximum-scale=1` are accessibility failures.
- During drag, disable text selection and mark dragged elements `inert`.
- `autoFocus` sparingly: desktop only, one clear primary input, never on mobile.
- Hover states on all buttons and links, and interactive states must *increase* contrast relative to rest.

## 3. Forms and feedback

- `autocomplete` and a meaningful `name` on every input.
- Correct `type` (`email`, `tel`, `url`, `number`) and `inputmode`.
- Never block paste. `onPaste` + `preventDefault` is user-hostile and common in password and code fields.
- `spellCheck={false}` on emails, usernames, and codes.
- Checkbox and radio labels share a single hit target with the control — no dead zones.
- Submit stays enabled until the request starts, then shows a spinner. Disabling on invalid hides *why*.
- Errors appear inline next to the field, and focus moves to the first error on submit.
- Error text names the fix, not just the problem. "Password must include a number" beats "Invalid password".
- Placeholders show an example pattern and end with `…`. A placeholder is never a substitute for a label.
- Warn before navigating away with unsaved changes.

## 4. Content handling and states

- Every text container handles overflow: `truncate`, `line-clamp-*`, or `break-words`. Flex children need `min-w-0` or truncation silently fails.
- Design for three content lengths: short, average, and pathological. Test with a 200-character name.
- Every list and every screen gets a real empty state that tells the user what to do next.
- Loading states are skeletons shaped like the incoming content, not a centered spinner.
- Destructive actions get a confirmation or an undo window. Never immediate.
- Loading copy ends with `…`: "Saving…", "Loading…".

### Text over imagery

Photographs have no contrast contract. A caption that is legible against one image vanishes against the next, and a hero that works with today's photo breaks when someone swaps it.

- **Prefer beside over on top.** Text placed above, below, or beside an image has a controlled background and no legibility risk. This is the default; overlay is the exception that has to be argued for.
- **When overlaying, guarantee the ground.** A scrim, a gradient, a solid plate behind the text, or a deliberately low-detail region of the image. Do not rely on the photograph happening to be dark where the text sits.
- **Verify against the worst image**, not the chosen one. If users or a CMS supply the images, assume the brightest, busiest one will appear.
- **Contrast rules still apply** — 4.5:1 for body, 3:1 for large text, measured against the actual composited background including the scrim.
- **Never place text over the subject** of the photograph. Faces and focal points fight the type and both lose.

## 5. Performance and layout stability

- `<img>` always gets explicit `width` and `height`. Missing dimensions is the top cause of layout shift.
- `loading="lazy"` below the fold; `fetchpriority="high"` or `priority` for the LCP image.
- Serve WebP/AVIF.
- Virtualize lists over ~50 items, or use `content-visibility: auto`.
- No layout reads during render — `getBoundingClientRect`, `offsetHeight`, `scrollTop`. Batch reads and writes.
- Prefer uncontrolled inputs; controlled inputs must be cheap per keystroke.
- `<link rel="preconnect">` for CDN and asset domains; preload critical fonts with `font-display: swap`.
- Reserve space for anything that loads late. Target CLS < 0.1.

## 6. Navigation and URL state

- The URL reflects state: filters, tabs, pagination, expanded panels, sort order.
- Anything stateful should be deep-linkable. If it uses `useState` and a user might share it, it belongs in the URL.
- Links are real `<a>`/`<Link>` elements so Cmd-click and middle-click work.
- Back behaves predictably. Bottom navigation caps at five items.

## 7. Theming, locale, and platform detail

- `color-scheme: dark` on `<html>` for dark themes — fixes native scrollbars, inputs, and form controls.
- `<meta name="theme-color">` matching the page background.
- Native `<select>` needs explicit `background-color` and `color` or it breaks in Windows dark mode.
- Borders and dividers must be visible in *both* themes. Theme-specific borders vanishing in dark mode is extremely common.
- Modal scrim strong enough to isolate the foreground — typically 40–60% black.
- Dates and numbers via `Intl.DateTimeFormat` and `Intl.NumberFormat`. Never hardcode formats.
- Detect language from `Accept-Language` / `navigator.languages`, not IP.
- `translate="no"` on brand names, code tokens, and identifiers.
- Full-bleed layouts need `env(safe-area-inset-*)` for notches and home indicators.
- Fixed headers and footers need matching content insets so scroll content isn't hidden.

## 8. Typography detail

- `…` not `...` · curly quotes not straight
- Non-breaking spaces in `10&nbsp;MB`, `⌘&nbsp;K`, and brand names
- `font-variant-numeric: tabular-nums` for any column or comparison of numbers
- `text-wrap: balance` on headings to prevent widows

## Anti-patterns to flag on sight

`user-scalable=no` · `onPaste` + `preventDefault` · `transition: all` · `outline-none` without a replacement · `<div>` with a click handler · images without dimensions · large `.map()` without virtualization · inputs without labels · icon buttons without `aria-label` · hardcoded date/number formats · unexplained `autoFocus` · `value` without `onChange` · controls that look tappable but are inert

## Review output format

Terse, grouped by file, `file:line` so editors can jump to it. State the issue and the location; skip explanation unless the fix is non-obvious.

```text
## src/Modal.tsx
src/Modal.tsx:12 - missing overscroll-behavior: contain
src/Modal.tsx:34 - "..." → "…"
src/Modal.tsx:51 - close button missing aria-label

## src/Card.tsx
✓ pass
```

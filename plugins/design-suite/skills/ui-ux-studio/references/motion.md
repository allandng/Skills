# Motion

Motion either explains something or decorates something. Decorative motion is one of the loudest AI tells, because the default behavior is to attach the same fade-in-up to every section and call it polish.

## The one question

**What does this motion explain?** Valid answers: where an element came from, what is now loading, what changed, what is now interactive, what the spatial relationship is between two states. If the answer is "it makes it feel dynamic", cut it.

## Should it animate at all? Frequency decides

Before easing or duration, ask how often the user hits this element. Frequency is the strongest single predictor of whether motion helps or grates:

| Frequency | Decision |
|---|---|
| 100+ times a day — keyboard shortcuts, command palette, tab switches | No animation. Ever. |
| Tens of times a day — hover, list navigation | Remove or make near-instant |
| Occasional — modals, drawers, toasts | Standard animation |
| Rare or first-time — onboarding, success moments | Can carry delight |

**Never animate keyboard-initiated actions.** They repeat hundreds of times daily, and animation makes each repetition feel slow and disconnected — the fastest tools animate their command surfaces not at all. The same motion that delights on first use grates on the five-hundredth, so judge every animation at its real frequency, not at demo frequency.

Two perceptual corollaries: a faster spinner makes the same load feel shorter, and tooltips after the first one in a toolbar should appear instantly — skip both the delay and the animation once the user is clearly scanning.

## Choose a philosophy, not a set of effects

Pick one per project and hold it:

| Philosophy | Character |
|---|---|
| **Still** | No entrance animation. Instant state changes under 100ms. Confident, fast, appropriate for tools. |
| **One orchestrated moment** | A single choreographed sequence — usually page load — and nothing else. Highest impact per unit of motion. |
| **Interaction-only** | Nothing moves unprompted. Everything responds. |
| **Continuous ambient** | Something is always subtly in motion. Expensive to do well; easy to make nauseating. |
| **Physical** | Spring physics, momentum, weight. The interface feels like it has mass. |

An orchestrated moment beats scattered effects. Ten sections each fading in with identical timing reads as a template; one deliberate load sequence reads as a decision.

## Timing

| Element | Duration |
|---|---|
| Button press feedback | 100–160ms |
| Tooltips, small popovers | 125–200ms |
| Dropdowns, selects | 150–250ms |
| Modals, drawers | 200–500ms |
| A deliberate orchestrated moment | 600ms+, once |

**UI animation stays under 300ms.** A 180ms dropdown feels more responsive than a 400ms one; only the largest surfaces (modals, drawers) earn 300–500ms, and marketing pages may run longer. Exits run faster than entrances — roughly 70% — because the user has already decided.

## Easing

- `ease-out` for entrances **and exits**: fast start, settle. `cubic-bezier(0.16, 1, 0.3, 1)`, or the stronger `cubic-bezier(0.23, 1, 0.32, 1)`.
- `ease-in-out` for movement or morphing between two on-screen positions. Strong curve: `cubic-bezier(0.77, 0, 0.175, 1)`.
- Drawers and sheets: the iOS-style `cubic-bezier(0.32, 0.72, 0, 1)`.
- **Never `ease-in` on UI.** It starts slow, which delays the exact moment the user is watching — an `ease-out` at 200ms *feels* faster than an `ease-in` at 200ms. (Earlier versions of this file said ease-in for exits; revised. Exits differ from entrances by being *faster*, not by easing in.)
- Never `linear`, except for continuous rotation and marquees.
- Built-in CSS keywords are weak; use strong custom curves rather than hand-rolling from scratch.
- Springs for anything the user is directly manipulating.

## Rules

- Animate `transform` and `opacity` only. These run on the compositor. Animating `width`, `height`, `top`, `left`, or `margin` forces layout on every frame.
- Never `transition: all`. List the properties.
- **Never enter from `scale(0)`.** Nothing in the world appears from nothing; enter from `scale(0.9–0.97)` plus `opacity: 0`.
- **Popovers scale from their trigger** — set `transform-origin` to the trigger side, not center. **Modals are the exemption**: they belong to the viewport and keep center origin.
- SVG: put transforms on a `<g>` wrapper with `transform-box: fill-box; transform-origin: center`.
- Animations must be interruptible. If a user acts mid-animation, respond immediately.
- Stagger with 30–60ms between items, and cap the total sequence at ~400ms. A twelve-item stagger at 100ms takes over a second and feels sluggish.

## Reduced motion

Non-optional. Vestibular disorders make large-scale motion genuinely painful.

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

Better than blanket disabling: provide a reduced *variant*. Replace movement with a cross-fade so the state change is still communicated, just without travel.

## Motion tells

- Every section `fade-in-up`, 0.6s, ease-out, triggered on scroll
- `hover:scale-105` on every card
- Parallax with no relationship to content
- Aurora or blob backgrounds unrelated to the subject
- Loading spinners where a skeleton would tell the user the shape of what's coming
- Number counters that tick up on scroll

## Deriving motion from the subject

Ask how things in this subject's world actually move. Mechanical things click into detents. Liquids settle. Paper slides and stacks. Instruments needle and damp. Data streams. Light falls off. Borrowing the subject's physics gives motion an argument, and an argument is what separates it from decoration.

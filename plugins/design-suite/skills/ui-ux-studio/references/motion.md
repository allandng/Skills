# Motion

Motion either explains something or decorates something. Decorative motion is one of the loudest AI tells, because the default behavior is to attach the same fade-in-up to every section and call it polish.

## The one question

**What does this motion explain?** Valid answers: where an element came from, what is now loading, what changed, what is now interactive, what the spatial relationship is between two states. If the answer is "it makes it feel dynamic", cut it.

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

| Duration | Use |
|---|---|
| 100ms | State flips, toggles, tab switches |
| 150ms | Hover, focus, press feedback |
| 250ms | Most transitions, dropdowns, tooltips |
| 400ms | Entrances, layout shifts, modals |
| 600ms+ | Only for a deliberate orchestrated moment |

Anything over 500ms on a routine interaction feels broken. Exits run faster than entrances — roughly 70% — because the user has already decided.

## Easing

- `ease-out` for entrances: fast start, settle. `cubic-bezier(0.16, 1, 0.3, 1)`
- `ease-in` for exits.
- `ease-in-out` for movement between two on-screen positions.
- Never `linear`, except for continuous rotation.
- Springs for anything the user is directly manipulating.

## Rules

- Animate `transform` and `opacity` only. These run on the compositor. Animating `width`, `height`, `top`, `left`, or `margin` forces layout on every frame.
- Never `transition: all`. List the properties.
- Set `transform-origin` deliberately — the default center is often wrong.
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

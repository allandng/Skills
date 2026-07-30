# Stack notes

Implementation detail for the stacks most UI work lands in. Detect the stack before assuming it: check `package.json` for react/next/vue/svelte, `pubspec.yaml` for Flutter, `Package.swift` or `.xcodeproj` for SwiftUI, `app.json` + `react-native` for React Native. Never default silently — a wrong assumption misroutes every recommendation downstream.

Condensed from Vercel's React best-practices and composition-patterns skills.

---

## When an official design system exists

If the brief reads as a specific platform's world — Microsoft-flavored enterprise, Material-flavored product, GOV.UK or USWDS public services — reach for the official package (`@fluentui/react-components`, `@material/web`, the gov frameworks) instead of hand-rolling tokens. Do not invent CSS for things that ship as maintained systems with accessibility already done; and do not dress a hand-rolled theme up as one of these systems, which reads as counterfeit to anyone who knows them. In update mode the platform's system *is* the house system and the seam test applies against it.

## Component architecture

The highest-leverage rule: **avoid boolean prop proliferation.** A component that grows `isCompact`, `hasIcon`, `showFooter`, `isBordered` has stopped being a component and become a configuration format. Each boolean doubles the state space and none of them compose.

Use composition instead:

```tsx
// Boolean soup — 16 combinations, most untested
<Card isCompact hasIcon showFooter isBordered title="…" />

// Compound components — the shape is the API
<Card>
  <Card.Icon><Compass /></Card.Icon>
  <Card.Title>Field notes</Card.Title>
  <Card.Body>…</Card.Body>
  <Card.Footer>…</Card.Footer>
</Card>
```

Compound components share state through context. Consumers control layout and order, which is exactly what they always end up needing.

Other structural rules:
- Lift state only as far as it needs to go. State that lives too high re-renders too much.
- Pass components, not flags, when a caller needs to customize rendering.
- Colocate state with the component that owns it.

## Performance, by impact

### Waterfalls (critical)

- `Promise.all` for independent async work. Sequential `await` on independent calls is the most common source of slow pages.
- Check cheap synchronous conditions *before* awaiting anything remote.
- Move `await` into the branch that actually uses the value.
- Start promises early, await late.
- Use Suspense boundaries to stream rather than blocking the whole route.

### Bundle size (critical)

- Import directly; avoid barrel files, which pull whole libraries into the graph.
- Keep import paths statically analyzable so the bundler can trace them.
- `next/dynamic` for heavy components below the fold.
- Load analytics and logging after hydration.
- Preload on hover or focus for perceived speed.

### Server (high)

- `React.cache()` for per-request deduplication.
- Hoist static I/O — fonts, logos, config — to module level.
- Minimize what crosses the RSC boundary into client components.
- No module-level mutable request state in RSC or SSR. It leaks between requests.
- Authenticate server actions exactly as you would API routes.
- `after()` for non-blocking work.

### Re-renders (medium)

- Derive state during render, not in an effect. `useEffect` + `setState` to compute something is a double render and a common bug source.
- Subscribe to derived booleans, not raw objects.
- Don't subscribe to state that is only read inside callbacks.
- Functional `setState` for stable callbacks.
- Pass a function to `useState` for expensive initial values.
- `useDeferredValue` to keep inputs responsive under expensive renders.
- `startTransition` for non-urgent updates.
- Reach for `memo` around genuinely expensive subtrees, not around primitives.

## React 19

- `useActionState` for form submission state — pending, error, result — instead of hand-rolled boolean state.
- `useOptimistic` for optimistic UI.
- `use()` to read promises and context conditionally.
- `ref` is a regular prop now; `forwardRef` is no longer needed.
- Document metadata (`<title>`, `<meta>`, `<link>`) can be rendered anywhere in the tree and hoists to head. This pairs directly with `favicon-and-head.md`.
- The compiler handles much of the memoization that used to be manual — audit before adding `useMemo` by reflex.

## Next.js

- Server Components by default; `'use client'` only at the leaves that need interactivity.
- `next/image` with explicit dimensions and `priority` on the LCP image.
- `next/font` for self-hosted fonts with zero layout shift.
- Metadata API for the head block, per `favicon-and-head.md`. Place `app/icon.svg` and `app/apple-icon.png` and Next wires the tags automatically.
- URL state via search params — `nuqs` if the app has much of it.
- Loading UI via `loading.tsx`, but make it a content-shaped skeleton, not a spinner.

## React Native

- `Pressable` with real press feedback in 80–150ms.
- `accessibilityLabel` and `accessibilityRole` on every control.
- Safe-area insets on all fixed headers, tab bars, and CTA bars.
- 44×44pt minimum touch targets; expand with `hitSlop` rather than enlarging the icon.
- Vector icons only, from one library. Never emoji as structural icons.
- `FlashList` or `FlatList` with `getItemLayout` for long lists.
- Reanimated on the UI thread for anything gesture-driven.
- Test at 375pt width and in landscape.

## Hydration safety

- An input with `value` needs `onChange`; otherwise use `defaultValue`.
- Guard date and time rendering against server/client mismatch.
- `suppressHydrationWarning` only where the mismatch is genuinely expected.

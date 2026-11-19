# Platforms

What each surface already provides, what its users expect without being told, and how a design moves between surfaces. Read it after writing the `SURFACE` line in `app-taxonomy.md`.

The rule for all of it: **follow the platform for navigation and system interactions, follow the brand for content.** Nobody praises an app for a novel back gesture.

Platform visual language changes between OS releases. The conventions below are the stable ones. Before matching system chrome exactly, read the platform's current guidelines (Apple's Human Interface Guidelines, Material Design, Fluent) instead of trusting memory or this file.

## Web app

- **The URL is state.** Area, object, view, filters, and the open item all belong in it. Reload, share, and the back button then work without extra code. A panel that opens without changing the URL cannot be linked to.
- **Back is the browser's.** Every screen change the user thinks of as "going somewhere" is a history entry. Opening a menu is not.
- **Hover exists but is never the only way.** Hover-revealed row actions need a keyboard path and a touch path.
- **Keyboard is first-class.** Tab order follows reading order. Frequent actions get shortcuts, shown where the action is. Move focus deliberately on route change and when an overlay opens or closes.
- **The window resizes continuously.** Design the narrow, medium and wide arrangement of each screen type, then let it flow between them. Target sizes: at least 24 by 24 CSS pixels (WCAG 2.2 AA), and 44 by 44 for anything used by touch.
- **Text is selectable and the page zooms.** Do not break either.
- **Density is a setting worth having** for collection screens used all day.

## iOS

- **Tab bar for peer areas.** Up to five on iPhone. It stays visible while the user moves within a tab, and each tab keeps its own place.
- **Navigation stack inside each tab.** Title at the top, back at the top-left, and a swipe from the left edge goes back. Do not put a gesture there.
- **Sheets for scoped tasks.** Partial-height sheets suit a choice or a short edit while context stays visible. A task with its own navigation is full height. Give every sheet an obvious way out.
- **Targets at least 44 by 44 points.** Respect the safe areas at the top and bottom.
- **Dynamic Type.** Text scales with the user's setting. Layouts that assume a fixed size break for the people who most need them not to.
- **System idioms the user already knows:** pull to refresh, swipe actions on rows, long-press context menus, the share sheet. Use them for their usual meaning or not at all.
- **Permission prompts appear once.** Explain why on your own screen first, at the moment the feature is used, then trigger the system prompt.
- **Destructive choices** go through a confirmation the system styles as destructive, with cancel always available.

## Android

- **Navigation bar** at the bottom for three to five peer destinations on compact widths. **Navigation rail** at medium widths. **Navigation drawer** when there are more destinations than a bar holds.
- **System back** is a gesture and belongs to the system. It closes the top-most thing: keyboard, sheet, screen. Make that order predictable.
- **Window size classes** drive layout: compact under 600dp wide, medium from 600 to 839dp, expanded from 840 to 1199dp, large from 1200 to 1599dp, and extra-large from 1600dp. Design per class, not per device name.
- **Targets at least 48 by 48dp.**
- **Edge to edge.** Content draws behind the system bars. Keep controls out of the gesture areas.
- **A floating action button** is for the screen's one primary constructive action. A screen without one does not need one.
- **Snackbars** confirm, briefly, with an optional undo. They are not for errors that need a decision.

## Desktop native

- **The menu bar is the index of everything.** On macOS every command lives in a menu, with its shortcut. Toolbars and context menus are shortcuts to the menus, not replacements.
- **Shortcuts use the platform's modifier** and the platform's standard bindings for standard actions. Settings open where the platform puts them.
- **Windows are plural.** Decide what opens in a new window, what state each window keeps, and what happens when the last one closes.
- **Right-click works** on anything that has actions. **Drag and drop works** between any two places it would make sense.
- **Panes resize** and remember their size. Sidebar, content, and inspector is the standard three.
- **Undo is universal.** If an action cannot be undone, it confirms first.
- **Density is expected.** Desktop users came for throughput.

## Cross-platform frameworks

React Native, Flutter, Electron and Tauri make one codebase possible and make ignoring the platform easy. Decide per layer:

| Layer | Follow |
|---|---|
| Navigation structure, back behavior, system gestures | The platform |
| Text input, selection, scrolling physics, date and file pickers | The platform |
| Type scale, color, content components, illustration, voice | The brand |
| Overlays and menus | The platform's behavior in the brand's skin |

## Moving a design between surfaces

Adapting is translating the job of each element, not shrinking it. Start from `LOOP` in the classification line and ask what the loop looks like with a thumb, or with a keyboard.

| On desktop web | On mobile |
|---|---|
| Sidebar with 8 areas | Tab bar with the 3 to 5 most used, the rest behind one of them |
| Table with 9 columns | Rows showing the 2 or 3 fields people scan by, the rest on the detail screen |
| List-detail split | Stack: list, then a pushed detail |
| Hover-revealed row actions | Swipe actions for the top one or two, a menu for the rest |
| Modal dialog with a form | Full-screen task or a sheet |
| Filter bar | A filter button showing the active count, opening a sheet |
| Multi-column form | One column, the keyboard type matched to each field |
| Tooltip | Visible label or inline help |
| Right-click menu | Long-press menu, plus a visible overflow button |
| Keyboard shortcut | Nothing. Gestures are optional accelerators, never the only route |
| Pagination | Continuous loading with a clear end |
| Inspector panel | A sheet over the content |

Going the other way, mobile to desktop, the failure is a phone layout centered in a wide window. Give the width a job: a second pane, more columns, an inspector, or density. If nothing earns the width, constrain the measure and say that you chose to.

## What to state in the plan

```
SURFACE     primary, and the smallest one supported
NAV         the platform pattern used at each width or size class
BACK        what back does from each screen type
INPUT       pointer, keyboard, touch: which are first-class
SYSTEM      platform idioms used (share, pull to refresh, context menu, ...)
DEPARTURES  any place the design leaves the platform convention, and why
```

An empty `DEPARTURES` line is the normal case.

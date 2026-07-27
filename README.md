# Skills

Skills produced by me, to be used by me and hopefully anyone who needs them :)

These are [Claude Agent Skills](https://docs.claude.com/en/docs/claude-code/skills), packaged as a
plugin marketplace so you can install them with two commands instead of copying folders around.

## Install

```bash
/plugin marketplace add allandng/Skills
```

```bash
/plugin install design-suite@allan-skills
```

```bash
/plugin install swe-plan@allan-skills
```

The marketplace is named **`allan-skills`** while the repo is named **`Skills`**, so installs end in
`@allan-skills`, not `@Skills`. That mismatch is deliberate — a distinctive marketplace name avoids
collisions with other people's marketplaces, since marketplace names share one namespace per user.

Skills load automatically when what you're doing matches their description. You don't invoke them by
name; you just describe the work.

## What's in here

### [Design Suite](plugins/design-suite) — `design-suite@allan-skills`

| Skill | What it does | Triggers on |
|---|---|---|
| **design-dna** | Reverse-engineers a live site's design system into a `tokens.json` plus a written style profile, names the style from an open taxonomy, and flags AI tells. Also surveys a whole category to separate real convention from herd behavior. | "how is this site designed", "match this style", "what do competitors look like", "pull the design tokens out of this", "give me a style breakdown" |
| **ui-ux-studio** | Builds, remixes, and audits interfaces that don't read as AI-generated. Ships a subject-derived SVG favicon, page title, and head block with every page. | "build a landing page", "make a dashboard", "make it look better", "this feels generic", "give me some design options", "audit this UI", "make it look less AI-generated" |

These two ship together on purpose: `design-dna`'s output is `ui-ux-studio`'s input.

### [SWE Plan](plugins/swe-plan) — `swe-plan@allan-skills`

| Skill | What it does | Triggers on |
|---|---|---|
| **swe-plan** | Senior-architect planning. `/start` interviews you into a full planning bundle (PRD, SRD, ERD, use case and sequence diagrams, ADRs, delivery plan, traceability matrix). `/addon` surveys an existing repo and returns a ranked implementation plan with blast radius and doc updates. | `/start`, `/addon`, "how should I build X", "plan this feature", "write a PRD / spec / design doc", "make me an ERD", "add X to my app", "what's the best way to implement this in my codebase" |

## Bundled scripts

Every skill ships Python helpers under `skills/<name>/scripts/`. They target **Python 3.11+** (a few
use `tomllib`) and are **standard-library only** — no `pip install` step, nothing to vendor.

The one exception is optional and degrades gracefully: `ui-ux-studio/scripts/favicon.py` will use
`cairosvg` (or the `rsvg-convert` binary) to rasterize PNGs and `Pillow` to draw a 16px ASCII
preview *if they happen to be installed*. Both imports are guarded — without them the script still
emits `favicon.svg`, `icon-mono.svg`, `site.webmanifest`, and the head snippet, and just prints the
fallback command for the PNGs.

## Updating

```bash
/plugin update design-suite@allan-skills
```

The manifests deliberately omit a `version` field, so every commit to `main` counts as a new version
and updates land without anyone bumping a number by hand.

## License

[MIT](LICENSE) — do what you like with them.

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

```bash
/plugin install askillissue@allan-skills
```

The marketplace is named **`allan-skills`** while the repo is named **`Skills`**, so installs end in
`@allan-skills`, not `@Skills`. That mismatch is deliberate — a distinctive marketplace name avoids
collisions with other people's marketplaces, since marketplace names share one namespace per user.

The design and planning skills load automatically when what you're doing matches their description.
You don't invoke them by name; you just describe the work. `askillissue` is the exception: nearly all
of its skills run only when you type them (`/askillissue:allan-mode`) or when its router calls them,
so 58 skills don't compete for every message.

## Which skill, when

| You're about to | Use | Plugin |
|---|---|---|
| Start something new and don't know its shape yet | `swe-plan` (`/start`) | swe-plan |
| Add a feature to an existing codebase and want a plan first | `swe-plan` (`/addon`) | swe-plan |
| Do any coding task that needs rigor: a bug, a feature, a refactor, a perf problem | `/askillissue:allan-mode` | askillissue |
| Understand code before touching it | `/askillissue:how`, `/askillissue:why`, `/askillissue:teach` | askillissue |
| Settle an interface or module shape before writing it | `/askillissue:architect` | askillissue |
| Compare several attempts at one thing, or fan work out | `/askillissue:arena`, `/askillissue:swarm` | askillissue |
| Have a diff attacked before you ship it | `/askillissue:interrogate`, `/askillissue:blast-radius` | askillissue |
| Clean up prose or comments | `/askillissue:unslop`, `/askillissue:no-comments` | askillissue |
| Find out how an existing site or app is designed or organized | `design-dna` | design-suite |
| Design, restyle, extend or audit an interface | `ui-ux-studio` | design-suite |
| Plan an app's navigation, build one screen in every state, or design a flow | `ui-ux-studio` (app-shell, screen, flow playbooks) | design-suite |
| Take a web app to mobile, or the reverse | `design-dna` teardown, then `ui-ux-studio` platform-adapt | design-suite |
| Have a design attacked before you ship it | `ui-ux-studio` (critique playbook) | design-suite |

The three chain: `swe-plan` decides what to build, `ui-ux-studio` and `design-dna` decide what it
looks like and how it is organized, and `allan-mode` builds it and proves it works. `allan-mode`
hands UI design work to `design-suite` on its own when both are installed.

## What's in here

### [Design Suite](plugins/design-suite) — `design-suite@allan-skills`

| Skill | What it does | Triggers on |
|---|---|---|
| **design-dna** | Reverse-engineers a live site's design system into a `tokens.json` plus a written style profile, names the style from an open taxonomy, and flags AI tells. Also surveys a whole category to separate real convention from herd behavior. | "how is this site designed", "match this style", "what do competitors look like", "pull the design tokens out of this", "give me a style breakdown" |
| **ui-ux-studio** | Builds, remixes, and audits interfaces that don't read as AI-generated. Ships a subject-derived SVG favicon, page title, and head block with every page. | "build a landing page", "make a dashboard", "make it look better", "this feels generic", "give me some design options", "audit this UI", "make it look less AI-generated" |

These two ship together on purpose: `design-dna`'s output is `ui-ux-studio`'s input.

Both work from playbooks: a short step list per job, each ending in a stated reply. `ui-ux-studio`
has fourteen (create, remix, variants, update, spec-to-ui, audit, critique, app-shell, screen, flow,
platform-adapt, design-system, prototype, visual-parity) and `design-dna` has six (extract-site,
extract-codebase, survey, teardown, compare, handoff). They share an app taxonomy that names a
product by surface, app type, shell, screen type, states and flows, and neither calls a job done
until the result has been checked and each claim labeled measured, observed, inferred or guess.

### [SWE Plan](plugins/swe-plan) — `swe-plan@allan-skills`

| Skill | What it does | Triggers on |
|---|---|---|
| **swe-plan** | Senior-architect planning. `/start` interviews you into a full planning bundle (PRD, SRD, ERD, use case and sequence diagrams, ADRs, delivery plan, traceability matrix). `/addon` surveys an existing repo and returns a ranked implementation plan with blast radius and doc updates. | `/start`, `/addon`, "how should I build X", "plan this feature", "write a PRD / spec / design doc", "make me an ERD", "add X to my app", "what's the best way to implement this in my codebase" |

### [A Skill Issue](plugins/askillissue) — `askillissue@allan-skills`

A fork of [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan (MIT): 58 skills
for doing engineering work with an agent without shipping slop. The skills are hers. The fork renames
the stack and its router so I can tune it, and adds one line that routes design work to
`design-suite`. [NOTICE.md](plugins/askillissue/NOTICE.md) lists every change.

| Part | What it is |
|---|---|
| **allan-mode** | The entry point. Restates the goal, matches the task to one of 22 playbooks (bug fix, feature, refactoring, perf, prototype, visual parity, shipping, overnight runs and more), and runs the other skills as the steps need them |
| **24 principles** | One rule each: fix root causes, prove it works, subtract before you add, model the domain, guard the context window. The router reads the ones it applies |
| **Workflow skills** | `how`, `why`, `teach`, `recall` to understand. `architect`, `arena`, `sharpen` to design. `tdd`, `swarm`, `figure-it-out` to build. `interrogate`, `blast-radius`, `benchmark-checklist` to verify. `unslop`, `no-comments`, `technical-writing` to clean up. `reflect`, `correct`, `automate-me` to improve the stack itself |
| **askillissue-help** | Ask it which skill, playbook or principle fits |

The folder is generated by [`scripts/fork_pstack.py`](scripts/fork_pstack.py) and is never edited by
hand, so pulling a newer pstack is one command. See the plugin's README.

## Bundled scripts

The `design-suite` and `swe-plan` skills ship Python helpers under `skills/<name>/scripts/`. They
target **Python 3.11+** (a few use `tomllib`) and are **standard-library only** — no `pip install`
step, nothing to vendor. `askillissue` ships upstream's own tools unchanged, which are TypeScript and
shell (`statechart`, `watch-pr`) and need a TypeScript runtime such as Bun.

Two repo-level scripts keep things honest: `scripts/fork_pstack.py --check` confirms the fork matches
a fresh run against upstream, and `scripts/check_skills.py` confirms every skill's name, description
length, and file references resolve.

The one exception is optional and degrades gracefully: `ui-ux-studio/scripts/favicon.py` will use
`cairosvg` (or the `rsvg-convert` binary) to rasterize PNGs and `Pillow` to draw a 16px ASCII
preview *if they happen to be installed*. Both imports are guarded — without them the script still
emits `favicon.svg`, `icon-mono.svg`, `site.webmanifest`, and the head snippet, and just prints the
fallback command for the PNGs.

## Updating

```bash
/plugin update design-suite@allan-skills
/plugin update askillissue@allan-skills
```

The manifests deliberately omit a `version` field, so every commit to `main` counts as a new version
and updates land without anyone bumping a number by hand.

## License

[MIT](LICENSE) — do what you like with them. `plugins/askillissue` is MIT under its upstream author's
copyright; its [LICENSE](plugins/askillissue/LICENSE) is reproduced unchanged.

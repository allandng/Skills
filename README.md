# askillissue

61 [Claude Agent Skills](https://docs.claude.com/en/docs/claude-code/skills) in three plugins, for planning software, designing interfaces, and writing code with rigor.

## Install

1. Add the marketplace:

   ```bash
   /plugin marketplace add allandng/askillissue
   ```

2. Install the plugins you want:

   ```bash
   /plugin install swe-plan@allan-skills
   /plugin install design-suite@allan-skills
   /plugin install askillissue@allan-skills
   ```

3. Try one. In a project with a frontend, type `audit this UI`. In any repo, type `/askillissue:allan-mode` and a bug to fix.

Installs end in `@allan-skills`. That is the marketplace's name, and it differs from the repo's name on purpose so it cannot collide with someone else's.

## Pick a skill

| You want to | Type |
|---|---|
| Plan something before building it | `/start` or `/addon` |
| Learn how an existing site or app is designed | "how is this site designed" |
| Design, restyle, or audit an interface | "build a settings screen", "audit this UI" |
| Do a coding task properly | `/askillissue:allan-mode` and the task |
| Find the right skill for anything else | `/askillissue:askillissue-help` |

Two rules cover how they start:

- `swe-plan` and `design-suite` load on their own when your request matches. Describe the work.
- `askillissue` skills run only when you type them, or when `allan-mode` calls them. That keeps 58 skills from competing for every message.

---

## swe-plan

1 skill. Plans software the way a senior architect would, and checks the plan by script before it is handed over. [Plugin README](plugins/swe-plan)

| Skill | What it does |
|---|---|
| `swe-plan` | Turns an idea or a feature request into a plan a team can build against, and checks what the plan says about the code against the repo. |

It works from playbooks. You describe the job; `/start` and `/addon` also work by name.

**Make a plan**

| Playbook | What you get |
|---|---|
| `start` | An interview, then a planning bundle: PRD, SRD, ERD, flows, ADRs, a delivery plan, a traceability matrix |
| `addon` | For a feature in an existing repo: a scope fence you confirm, ranked options, a phased plan, blast radius |
| `spike` | A throwaway test of the one thing the plan depends on, with the command and its output |
| `decide` | One decision written up with what lost and when to reopen it |

**Keep it true**

| Playbook | What you get |
|---|---|
| `review` | Reviewers try to break the plan. Only findings they can point at survive |
| `backfill` | Documents for a working codebase that has none |
| `amend` | Docs brought back in line after the code moved |
| `handoff` | A prompt for one phase that an implementing agent can run without improvising |

---

## design-suite

2 skills that hand off to each other. `design-dna` reads what exists. `ui-ux-studio` builds. [Plugin README](plugins/design-suite)

| Skill | What it does |
|---|---|
| `design-dna` | Reverse-engineers a site or app. Pulls its colors, type, and spacing into `tokens.json`, describes how the product is organized, and compares it against competitors. |
| `ui-ux-studio` | Designs, restyles, extends, and audits interfaces that do not read as AI-generated, for sites and for web, mobile, and desktop apps. |

Both work from playbooks: a short step list per job. You do not type the playbook name. You describe the job.

### ui-ux-studio playbooks

**Make something new**

| Playbook | What you get |
|---|---|
| `create` | One design plan and one built page or screen, from a brief |
| `spec-to-ui` | Three interaction models from a backend, schema, or PRD |
| `app-shell` | Navigation and structure for a product, before any screen |
| `screen` | One screen in every state: loading, empty, error, and the rest |
| `flow` | A multi-step journey such as sign-up, onboarding, or checkout |

**Change something that exists**

| Playbook | What you get |
|---|---|
| `remix` | Three different directions for an existing site or app |
| `variants` | Three treatments of one design you already like |
| `update` | New work that matches the existing design exactly |
| `platform-adapt` | The same product on another surface: web to mobile, or the reverse |
| `design-system` | Drifted screens pulled into one set of tokens and components |

**Check something**

| Playbook | What you get |
|---|---|
| `audit` | Findings by severity and a three-phase fix plan |
| `critique` | Reviewers with different viewpoints try to break the design. Only findings they can point at survive |
| `prototype` | Throwaway versions behind one switch, to settle a decision by looking |
| `visual-parity` | Proof that a migration did not change how anything looks |

### design-dna playbooks

| Playbook | What you get |
|---|---|
| `extract-site` | One live site's visual system as tokens and a written profile |
| `extract-codebase` | The same from source, plus a list of every screen |
| `survey` | How a whole category designs itself: what is convention and what is copied |
| `teardown` | How one product is organized: app type, navigation, screens, flows, states |
| `compare` | Two systems side by side, axis by axis |

A sixth, `handoff`, packages any of these for `ui-ux-studio`.

---

## askillissue (the plugin)

58 skills for doing engineering work with an agent without shipping slop. [Plugin README](plugins/askillissue)

It is a fork of [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan, MIT. The skills are hers. The fork renames the stack so it can be tuned here. [NOTICE.md](plugins/askillissue/NOTICE.md) lists every change.

### Start here

1. Run `/askillissue:setup-askillissue` once. It asks which models to use.
2. Start any real task with `/askillissue:allan-mode` and describe it.
3. Stuck? Ask `/askillissue:askillissue-help`.

`allan-mode` runs most of the skills below for you. Use them directly when you want one thing.

### Start a task

| Skill | What it does |
|---|---|
| `allan-mode` | The entry point. Restates your goal, picks one of 22 playbooks (bug fix, feature, refactor, perf, prototype, overnight run), and runs the other skills as the steps need them |
| `askillissue-help` | Tells you which skill, playbook, or principle fits your task |
| `setup-askillissue` | Sets which model and reasoning budget each role uses |
| `in-your-own-words` | Plays your goal back to you before any work starts |
| `sharpen` | Rewrites your prompt to go deeper. Does not do the task |

### Understand code

| Skill | What it does |
|---|---|
| `how` | Walks through how a subsystem works, and where new code should live |
| `why` | Explains why something was built this way, cited from commits and PR discussions |
| `teach` | Runs `how` and `why`, then builds one plain explanation, diagram by diagram |
| `recall` | Rebuilds where you left off on a topic from your chat history |
| `blast-radius` | Finds what a small change could break elsewhere, and proves the one fact that makes it safe |

### Design

| Skill | What it does |
|---|---|
| `architect` | Settles types, signatures, and module shape before any code |
| `arena` | Runs several attempts at one task in parallel, then combines the best parts |
| `figure-it-out` | Writes a playbook for a task no existing playbook fits |
| `statechart` | Model-checks a flow and draws it as a state diagram, with the shortest path to each broken rule |

### Build

| Skill | What it does |
|---|---|
| `tdd` | Writes the failing test first, then the fix |
| `swarm` | Splits work across parallel workers and returns one report |
| `typescript-best-practices` | Type-system rules for reading and editing TypeScript |
| `make-bot-ui` | Builds a page whose buttons wake a bot over a webhook. Cursor-only |

### Verify

| Skill | What it does |
|---|---|
| `interrogate` | Reviewers try to break your diff. Only findings proven by a run survive |
| `benchmark-checklist` | Vets a measured number before you report or act on it |
| `show-me-your-work` | Keeps a log with one row per decision: what, why, evidence, result |
| `no-comments` | Strips comments before review, and offers to encode any rule a comment was stating |

### Give your project its own verification

| Skill | What it does |
|---|---|
| `create-verification-skill` | Generates a skill that drives your app the way a user does |
| `maintain-verification-skill` | Checks that skill against the app and corrects what drifted |
| `create-formal-verification-skill` | Generates a skill that formally verifies the code tests cannot reach |
| `maintain-formal-verification-skill` | Brings that verification back in line after the code changes |

### Write

| Skill | What it does |
|---|---|
| `unslop` | Cuts AI tells from any writing |
| `technical-writing` | A standard for docs, READMEs, PR descriptions, and commit messages |
| `bro` | Restates the last message in plain language |
| `ketchup` | Shows what changed in the chat since your last message, and what is waiting on you |
| `ketchup-video` | The same catch-up as a short subtitled video |

### Improve the stack itself

| Skill | What it does |
|---|---|
| `reflect` | Turns what a long task taught you into an edit on an existing skill |
| `correct` | Finds mistakes agents keep repeating in your repo and makes each one impossible |
| `automate-me` | Drafts your own `-mode` skill from how you have actually worked |

### The 24 principles

One rule each. `allan-mode` reads the ones a task needs. Each skill name starts with `principle-`.

**Keep it small**

| Principle | Rule |
|---|---|
| `laziness-protocol` | Prefer deletion and the smallest change that solves the problem |
| `subtract-before-you-add` | Remove dead weight first, then build on the simpler base |
| `minimize-reader-load` | Cut layers and hidden state between a question and its answer |
| `build-the-lever` | Build the script that does the work or proves it, instead of working by hand |
| `experience-first` | Choose the user's experience over your own convenience |

**Think before writing**

| Principle | Rule |
|---|---|
| `foundational-thinking` | Get the data structures right so the code after them is obvious |
| `redesign-from-first-principles` | Fit a new requirement as if it had been there from day one |
| `attack-the-premise` | When two fixes sharing one assumption fail, test the assumption |
| `exhaust-the-design-space` | Build two or three competing prototypes before committing |
| `outcome-oriented-execution` | In a migration, converge on the target. No throwaway compatibility code |

**Structure**

| Principle | Rule |
|---|---|
| `model-the-domain` | Put the domain in a structure, not in scattered conditionals |
| `boundary-discipline` | Validate at system boundaries and trust types inside them |
| `type-system-discipline` | Make illegal states impossible to represent |

**State and change**

| Principle | Rule |
|---|---|
| `make-operations-idempotent` | Reach the same end state however many times a step runs |
| `migrate-callers-then-delete-legacy-apis` | Move callers and delete the old API in the same pass |
| `separate-before-serializing-shared-state` | Remove shared state before you reach for a lock |

**Verify**

| Principle | Rule |
|---|---|
| `prove-it-works` | Check the real thing. "It compiles" is not proof |
| `fix-root-causes` | Fix where the system first went wrong, not where it showed |
| `sequence-verifiable-units` | Split work into small units that each end in a check |
| `test-behavior-not-implementation` | Assert what users can observe, not the internals |
| `explain-the-number` | Before trusting a measurement, find what limits it |

**Delegate and learn**

| Principle | Rule |
|---|---|
| `guard-the-context-window` | Send bulk work to subagents and keep summaries in the main thread |
| `never-block-on-the-human` | Do reversible work without asking. Confirm only what cannot be undone |
| `encode-lessons-in-structure` | Turn a repeated instruction into a lint, a check, or a script |

---

## Requirements

- **`design-suite` and `swe-plan` scripts**: Python 3.11 or newer, standard library only. Nothing to install.
- **`askillissue` tools** (`statechart`, `watch-pr`): TypeScript and shell, unchanged from upstream. They need a TypeScript runtime such as Bun.
- **Optional**: `ui-ux-studio/scripts/favicon.py` rasterizes PNGs if `cairosvg` or `rsvg-convert` is installed. Without them it still writes the SVG files and prints the fallback command.

## Update

```bash
/plugin update design-suite@allan-skills
/plugin update swe-plan@allan-skills
/plugin update askillissue@allan-skills
```

No version numbers to bump. Every commit to `main` counts as a new version.

## For contributors

Run both checks before a pull request:

```bash
python3 scripts/check_skills.py
python3 scripts/fork_pstack.py --upstream <cursor/plugins checkout> --check
```

1. `check_skills.py` confirms every skill's name, description length, and file references, and that this README lists every skill.
2. `fork_pstack.py --check` confirms `plugins/askillissue` matches a fresh fork of upstream. That folder is generated. Do not edit it by hand.

## License

[MIT](LICENSE). `plugins/askillissue` is MIT under its upstream author's copyright, and its [LICENSE](plugins/askillissue/LICENSE) is reproduced unchanged.

**Next:** run `/plugin marketplace add allandng/askillissue`, install `design-suite`, and type `audit this UI`.

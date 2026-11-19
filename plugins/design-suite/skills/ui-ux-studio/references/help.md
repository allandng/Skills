# Which playbook

Read this when the request does not obviously match one job, or when the user asks what this skill can do or how to ask for something. Find the row, answer the question in a sentence or two, and offer the prompt.

## By what the user has

| They have | They want | Playbook |
|---|---|---|
| A brief or an idea | A new page, screen or component | `create` |
| An existing site or app | Different directions to choose from | `remix` |
| A design they like | Variations of it | `variants` |
| An existing site or app | Something added in the same style | `update` |
| An existing site or app | To know what is wrong and what to fix first | `audit` |
| An existing design | Reviewers trying to break it | `critique` |
| A backend, schema, API or PRD | An interface for it | `spec-to-ui` |
| A product idea with several areas | Navigation and structure before any screen | `app-shell` |
| A shell | One screen done properly, every state included | `screen` |
| A task with more than one step | The journey: sign-up, onboarding, checkout, a wizard | `flow` |
| A design on one surface | The same product on another: web to mobile, mobile to desktop | `platform-adapt` |
| Several screens that drifted | One token and component system | `design-system` |
| A decision they cannot make | Two or three throwaway versions to look at | `prototype` |
| Two implementations | Proof they look identical | `visual-parity` |
| A reference site | Its tokens, style or structure | the `design-dna` skill, then come back |

## By symptom

| They say | It is usually |
|---|---|
| "This looks AI-generated", "feels generic" | `remix` if the concept is the problem, `audit` if the execution is. Ask which only if the artifact does not make it obvious |
| "Make it softer, bolder, quieter, sharper" | No playbook. `adjustments.md` |
| "I keep getting one good option and two strange ones" | `variants`, not `remix` |
| "Build a dashboard" | `app-shell` first if there is no shell, otherwise `screen` with type `orientation:dashboard`. Ask what the user acts on, not what they want to see |
| "Add dark mode" | `design-system`: dark is a second set of tokens, not an inversion |
| "Make it responsive", "make it work on mobile" | `platform-adapt` |
| "It works but people get lost" | `app-shell`: the levels are sharing a control |
| "Users drop off during sign-up" | `flow` |
| "Is this done?" | `proof.md`: climb the ladder and report it |

## Chaining

Bigger jobs are playbooks in sequence. The usual chains:

```
new product      app-shell → screen (the loop's screens first) → flow → critique
redesign         design-dna survey → remix → variants on the winner → update the rest
from a backend   spec-to-ui → app-shell for the chosen model → screen → flow
going mobile     design-dna teardown of the current app → platform-adapt → screen → critique
cleanup          audit → design-system → update → visual-parity
```

Finish one playbook's Reply before starting the next. The Reply is the handoff.

## Prompts that work

Good prompts name the subject, the surface, and what the user does most. Offer these shapes:

```
create         Design the booking page for a two-chair barbershop in Lowell. Walk-ins
               matter more than appointments.
app-shell      Plan the shell for a support desk: agents triage about 80 tickets a day,
               leads watch the queue. Web, desktop-first.
screen         Build the ticket list for that shell with every state. Real field names
               are in schema.prisma.
flow           Design onboarding for a language app where the first lesson happens
               before sign-up.
platform-adapt Take the web inbox and design it for iOS. One hand, on a train.
spec-to-ui     Here is the API. Give me three interaction models and tell me what
               each needs from the backend.
audit          Audit the settings area. I care most about what a new teammate hits
               in week one.
critique       Run the panel on the checkout. Include hostile content and a daily user.
prototype      I can't decide between tabs and a sidebar for this. Build both behind
               a switch.
```

A prompt that names only a look ("modern, clean, minimal") gives the skill nothing to derive from. Ask what the thing is and who uses it before designing.

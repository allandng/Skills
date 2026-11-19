# Playbooks

One file per job. Each is a short list of steps with an owner sentence at the top and a **Reply** line at the bottom. Paths in the steps are relative to the skill folder.

How to run one:

1. Match the request to a playbook (`references/help.md` when it is not obvious).
2. Copy its steps into your todo list as written, or keep the list in your reply when there is no todo tool.
3. Work them in order. A step that does not apply keeps its line with `n/a: <reason>`, so a skipped step and a forgotten one never look the same.
4. End with the playbook's Reply, in the frame from `references/proof.md`.

The steps say what to do and which reference holds the detail. `references/start-mode.md` and `references/addon-mode.md` stay the authority for the two modes. The playbook is the order of work.

| Playbook | For |
|---|---|
| [start](start.md) | A new project: interview, design, the document bundle |
| [addon](addon.md) | A feature going into an existing codebase: survey, scope fence, ranked options, phases |
| [spike](spike.md) | A question the plan depends on that running something would answer |
| [decide](decide.md) | One decision, written up as an ADR with its rejected options |
| [review](review.md) | Reviewers trying to break a plan before anyone builds on it |
| [backfill](backfill.md) | Documents for a system that already exists and has none |
| [amend](amend.md) | Bringing a bundle back in line after the code moved |
| [handoff](handoff.md) | Turning one phase into a prompt an implementing agent can run |

### Hand off to ui-ux-studio

**You own a package the next step can build from without re-deriving anything.**

1. Name the target playbook. It decides what to pass.

   | Target | Pass | It will |
   |---|---|---|
   | update | `tokens.json`, the manual pass, `GAPS`, `STATES` | Match every axis exactly |
   | remix | The survey's `CONTESTED` and `UNOCCUPIED` | Pick different values per direction |
   | create | The survey's `CONVENTION` and `HERD` | Keep convention, spend freedom on herd behavior |
   | audit | `tokens.json`, flagged tells, the state table | Measure drift against a baseline |
   | platform-adapt | The `Structure` block and `routes.json` | Translate each screen's job to the new surface |
   | design-system | Declared against used, dead tokens, the component inventory | Collapse it into one system |
   | app-shell | The survey's shell and level conventions | Decide which to keep |

2. Run `python3 scripts/dna_check.py ./dna/<name>` (add `--structure` if a teardown ran). Do not hand off a profile that fails it.
3. Declare the real color pairs in `tokens.json` and rerun `contrast.py`, so the next step inherits checked pairs and not guesses.
4. Put the limits first in the handoff: `COVERAGE` and `NOT SEEN`. The next step will otherwise treat the profile as complete.
5. Mark which lines are `[inferred]` or `[guess]` and matter to the target. Those are the ones to confirm before building on them.

**Reply:** the target playbook, the files and lines passed, the `dna_check` result, and the inferred claims the next step should not trust yet.

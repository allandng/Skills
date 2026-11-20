# Review panel

Several reviewers, each holding one position, try to break a plan. A finding survives only when the reviewer can point at it: a line in the plan, a file in the repo, a command and its output. The panel reports. It does not rewrite.

After pstack's `interrogate`, which does this to code. A plan is cheaper to break than the code built from it.

## Why separate reviewers

The author reads a plan with the interview in their head and sees the plan they meant. A reviewer who has only the page sees the plan that is there. So each reviewer gets the plan, the intent, the repo when there is one, and nothing else.

With subagents available, spawn one per lens with a fresh context and run them in parallel. Without them, run the lenses one at a time, write each lens's findings down before starting the next, and do not revise an earlier list.

## The lenses

Pick four to six. The first three are always in.

| Lens | Holds this position | Looks for |
|---|---|---|
| **Implementer** | Has to build P-01 tomorrow from this page alone | What they would have to guess. Files named that do not exist. Steps that say what and not where. A phase that cannot be checked |
| **Operator** | Gets paged when it breaks | Rollback that is not real. A migration that locks a table. Failure modes with no alert. Cost with no ceiling. Old clients |
| **Scope lawyer** | Reads the fence looking for the gap | What a reasonable implementer would add that is not ruled out. Requirements that trace to nothing. A dependency that arrived without an argument |
| **Premise skeptic** | Doubts the thing should be built | The workaround that already exists. The success metric that would not move. The requirement that is a solution in disguise |
| **Data** | Thinks in rows | Cardinality that is wrong. Existing rows that violate a new constraint. Deletes, retention, backfills. The report that reads the changed table |
| **Newcomer** | Joins on Tuesday | Undefined terms, unexplained acronyms, a decision with no recorded reason, a diagram that disagrees with the text |
| **Adversary** | Uses the system against itself | New inputs, new permissions, newly stored data, what an authenticated user can do to another user's records |
| **Estimator** | Has been burned by timelines | Tasks larger than half a day. The phase that hides the hard part. Estimates given as points instead of ranges |

## The brief each reviewer gets

> Here is a plan and what it is for: `<intent>`. Hold this position: `<lens>`. Try to break the plan from that position only.
>
> Report each finding with a title, where it is in the plan (document and line or ID), the evidence, and what the intent requires instead. Evidence is one of: a quote from the plan that contradicts another part of it, a file or symbol in the repo that shows the plan is wrong, or a command you ran and what it printed.
>
> Leave out anything you cannot point at. That covers style, preferences, and risks that need a future change to matter. No findings is a valid result.

## Verify, then merge

Go to what each finding cites and check it. Keep the finding when the evidence shows the problem and the problem breaks the intent. Drop the rest and count them.

Merge findings that share a root cause. An implementer who cannot tell where a file goes and a newcomer who cannot find the convention are reporting the same missing line in the conventions ledger. Findings with several witnesses are the ones to trust most.

## Output

```
INTENT     the restatement
FINDINGS   for each: title · where in the plan · evidence · how it breaks
           the intent · which lenses found it
DROPPED    per lens: how many, and why (no evidence, preference, out of scope)
```

Say "no verified findings" when none survive. Then stop. Changing the plan is the author's job, through the playbook that wrote it.

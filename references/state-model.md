# State model

## Primary labels

Use exactly one primary state label per tracked issue or pull request.

| Label | Colour | Meaning |
| --- | --- | --- |
| `loop:spec` | `BFD4F2` | Contract drafted; awaiting human approval |
| `loop:ready` | `0E8A16` | Human-approved and eligible to claim |
| `loop:building` | `1D76DB` | Atomically claimed and being implemented |
| `loop:review` | `5319E7` | Pull request or issue awaiting independent review |
| `loop:changes` | `D93F0B` | Commit-specific must-fix findings exist |
| `loop:approved` | `006B2E` | Review evidence is complete; human may consider merge |
| `loop:blocked` | `FBCA04` | One answer or dependency is required |
| `loop:human-review` | `B60205` | Automation must not continue without a human decision |
| `loop:done` | `C5DEF5` | Human merged or explicitly closed the work |

Optional non-state labels such as `priority:high` and `risk:high` may coexist.

## Valid transitions

```text
loop:spec -> loop:ready                 human only
loop:ready -> loop:building             successful atomic branch claim
loop:building -> loop:review            pull request opened
loop:review -> loop:changes              reviewer found must-fix work
loop:changes -> loop:review              repair pushed
loop:review -> loop:approved             exact commit passed every gate
loop:approved -> loop:done               human merge or closure
any active state -> loop:blocked         answer or dependency required
any active state -> loop:human-review    policy, risk, or retry escalation
loop:blocked -> prior eligible state     human resolves blocker
loop:human-review -> explicit state      human chooses the next state
```

If multiple primary labels are present, do not guess which wins. Apply
`loop:human-review`, describe the invalid combination, and stop that item.

## Queue ordering

1. `loop:changes`: oldest last-updated pull request first.
2. `loop:ready`: `priority:high`, then `priority:medium`, then unprioritised;
   oldest creation time breaks ties.
3. `loop:review`: oldest last-updated pull request first.

Skip drafts, closed items, unresolved dependencies, pending required checks,
and any item also carrying `loop:blocked` or `loop:human-review`.

## Atomic claim

Create `refs/heads/loop/issue-N-short-slug` directly on the remote from the
fresh default-branch commit. GitHub ref creation is the arbitration point:
exactly one worker can create a previously absent ref.

After the ref succeeds, re-read the issue before labelling or editing. A
failure because the ref exists is normal contention, not an error.

Use a deterministic identifier in comments and pull request bodies:

```text
Delivery-Loop-Run: ISSUE-N/ATTEMPT
```

Search for this identifier before creating any corresponding comment or pull
request.

## Stale claims

A `loop:building` issue is stale when its claim branch has no open pull request
and no commit or issue activity for four hours. Detection is automatic;
recovery is human-controlled because deleting or taking over a branch can
destroy active work.

Apply `loop:human-review` alongside a comment naming:

- the claim branch;
- the last observed activity;
- whether the branch differs from its base;
- the choices to resume, requeue, or close.

Never delete or reuse the branch without an explicit human decision.

## Human gates

Humans alone:

- replace `loop:spec` with `loop:ready`;
- resolve `loop:human-review`;
- authorise contract changes after approval;
- merge or enable auto-merge;
- recover stale claims.

An agent may recommend an action but must not perform these gates.

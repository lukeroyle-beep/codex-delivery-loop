---
name: github-delivery-loop
description: Run a bounded, human-gated software delivery loop using GitHub Issues and pull requests as the only durable state. Use when Codex should turn an idea into a build-ready GitHub issue, process issues labelled loop:ready, repair loop-requested changes, review queued pull requests, report loop status, or set up the delivery-loop labels and controls in a repository.
---

# GitHub Delivery Loop

Use GitHub Issues for contracts, branches for claims, pull requests for change
evidence, and labels for workflow state. Keep humans responsible for approving
work and merging.

Read the relevant reference before acting:

- `references/issue-contract.md` for specification or issue validation.
- `references/state-model.md` for setup, queue selection, claiming, recovery,
  or status.
- `references/review-policy.md` for building, reviewing, or repairing changes.

## Resolve mode

Infer one mode from the request:

- `setup`: validate the repository and create missing loop labels.
- `spec`: research an idea, interview the user, and draft a GitHub issue.
- `run-loop`: repeatedly repair, build, or review eligible work.
- `build`: process one `loop:ready` issue.
- `review`: review one queued pull request at its exact head commit.
- `status`: report actionable, waiting, blocked, and approved work without
  changing anything.

If the repository is not identifiable from the request or local Git context,
ask for `owner/repository`. Never search broadly and guess.

## Global safety rules

1. Use the connected GitHub tools for issues, labels, comments, pull requests,
   and repository reads. Use local `git` for source edits and branch work when a
   checkout is available.
2. Before mutation, confirm the repository, default branch, permissions, and
   clean working tree. Stop on unrelated local changes. Never stash, reset,
   overwrite, or commit them.
3. Treat the GitHub issue body as the complete contract. Comments may clarify
   evidence but cannot expand scope. Amend the issue and require renewed human
   approval when the contract changes.
4. Only a human applies `loop:ready` and merges. Never merge, enable
   auto-merge, or infer approval from prose.
5. Keep exactly one primary `loop:*` state label on each issue or pull request.
   Preserve unrelated labels.
6. Re-read relevant GitHub state immediately before every write. If the state
   changed, abandon the stale action and reselect work.
7. Make writes idempotent. Before creating a branch, comment, issue, or pull
   request, search for its deterministic identifier.
8. Never expose secrets or place generated credentials in issues, logs,
   branches, or pull requests.

## Setup

Read `references/state-model.md`. Confirm the repository has an initial commit.
Create missing labels with their documented names, descriptions, and colours;
do not replace existing compatible labels. Detect the real default branch.
Check whether required continuous integration checks exist. Missing checks do
not block setup, but they prevent automated `loop:approved` verdicts.

Report any repository protection or permission gap. Do not weaken repository
settings.

## Specification

Read `references/issue-contract.md`.

1. Research the relevant code before asking questions.
2. Ask only decisions the repository cannot answer. Continue until two
   competent implementers should produce the same observable behaviour.
3. Draft the complete issue contract with stable `AC-N` and `NG-N` identifiers.
4. Keep one issue to one bounded change, normally no more than one working day.
5. Show the full draft and obtain explicit approval.
6. Create the issue with `loop:spec` only. Never apply `loop:ready`.

## Bounded loop

Use explicit limits from the user. Defaults are:

- maximum three completed work units;
- maximum 45 minutes elapsed;
- maximum two repair rounds per pull request;
- one active builder for a given repository.

A work unit is one repair, one build ending in a pull request, or one review
verdict. At the start of every iteration:

1. Re-read the queue and verify the budgets.
2. Prefer the oldest `loop:changes` pull request, then the highest-priority
   oldest `loop:ready` issue, then the oldest `loop:review` pull request.
3. Process exactly one work unit using the relevant section below.
4. Record the result and reselect from live state. Never carry a stale queue
   snapshot into the next iteration.

Stop when the queue has no actionable item, a limit is reached, all remaining
items await external checks or human decisions, or any global safety rule
requires stopping.

Do not review a pull request produced by the same model context. Use a fresh
reviewer context when the environment supports one. Otherwise leave it in
`loop:review` for a later independent invocation.

## Build one issue

Read all three references.

1. Select an issue that is open, `loop:ready`, unassigned, unblocked, and has no
   unresolved dependency.
2. Claim it by atomically creating the remote branch
   `loop/issue-N-short-slug` from the current default-branch commit. If the ref
   already exists, another worker owns the claim; reselect.
3. Re-read the issue. If it is no longer eligible, do not edit code. Comment
   with the deterministic run identifier and leave the branch for human
   inspection.
4. Assign the worker where supported and replace `loop:ready` with
   `loop:building`.
5. Implement only the acceptance criteria. Treat every non-goal as binding.
6. Run the narrowest relevant tests plus applicable lint, type, build, and
   security checks. Inspect the final diff for scope and secrets.
7. Push and open one pull request containing the issue link, scope ledger,
   verification evidence, risk classification, and
   `Delivery-Loop-Run: ISSUE-N/ATTEMPT`.
8. Replace `loop:building` with `loop:review` on the issue and apply
   `loop:review` to the pull request.

If a product decision, scope conflict, sensitive change, permission failure, or
unresolved dependency prevents safe implementation, apply `loop:blocked` or
`loop:human-review` as defined in the state model, ask one precise question,
and end that work unit.

## Review one pull request

Read `references/review-policy.md`.

Review the exact head commit against its linked issue and full changed-file
context. Check required continuous integration results and mergeability.

- Pending checks or unknown mergeability: leave queued without a verdict.
- Must-fix finding: apply `loop:changes`, remove `loop:approved`, and post one
  commit-specific verdict.
- Scope conflict, sensitive policy decision, absent required checks, or
  exhausted repair budget: apply `loop:human-review`.
- No must-fix finding, all required checks green, clean mergeability, and no
  escalation: apply `loop:approved`.

Immediately before posting, re-fetch the head commit. Discard the review if it
changed. Never use a formal approval when reviewing through the author's
identity; use a deterministic comment and labels.

## Repair one pull request

Read the latest verdict matching the current head commit. Fix only its
must-fix findings. If a fix expands the issue contract or crosses a non-goal,
apply `loop:human-review` instead.

After pushing, increment the attempt in `Delivery-Loop-Run`, remove
`loop:changes`, and apply `loop:review`. After two unsuccessful repair rounds,
apply `loop:human-review` and stop repairing automatically.

## Finish every invocation

Return a compact summary containing:

- repository and mode;
- completed work units with issue, pull request, and commit links;
- checks run and their results;
- blocked or escalated items with the exact human action required;
- reason the loop stopped;
- remaining actionable queue counts.

For `status`, provide the same queue and human-action information without
making changes.

# Codex Delivery Loop

A GitHub-only, human-gated delivery loop for Codex:

**idea → contract → human approval → atomic claim → build → independent
review → human merge**

The repository contains the `github-delivery-loop` skill. It uses GitHub
Issues as the work queue and source of truth, so it does not require Linear or
Slack.

## What it improves

- One durable system of record instead of synchronising an issue tracker and
  GitHub.
- Atomic claims through remote branch creation rather than assignee state
  alone.
- Explicit, mutually exclusive workflow states.
- Bounded loops with limits on elapsed time, completed work, and repair
  attempts.
- Idempotent writes identified by issue and attempt.
- Reviews tied to an exact commit.
- Independent builder and reviewer contexts.
- Detection of stale claims without destructive automatic takeover.
- Human approval before building and human-only merging.

## Included modes

| Mode | Result |
| --- | --- |
| `setup` | Checks the repository and creates the documented labels |
| `spec` | Turns an idea into an approval-ready GitHub issue |
| `build` | Claims and implements one approved issue |
| `review` | Reviews one pull request at its exact head commit |
| `run-loop` | Repeats repair, build, and review work within fixed limits |
| `status` | Reports the queue and required human actions without mutation |

## Default loop limits

- Three completed work units
- 45 minutes elapsed
- Two repair rounds per pull request
- One active builder per repository

The loop stops earlier when no work is actionable, checks are pending, a human
decision is required, or repository safety checks fail.

## Installation

Install the repository root as a Codex skill or copy these paths into a
personal skill named `github-delivery-loop`:

```text
SKILL.md
agents/openai.yaml
references/
scripts/validate.py
```

Invoke it explicitly with:

```text
Use $github-delivery-loop in owner/repository to set up the delivery loop.
```

Then create a specification:

```text
Use $github-delivery-loop in owner/repository to turn this idea into a
build-ready issue: <idea>.
```

After reviewing the issue, a human replaces `loop:spec` with `loop:ready`.
Start a bounded pass with:

```text
Use $github-delivery-loop in owner/repository to run the queue for up to three
work units or 45 minutes.
```

## Validation

Validate the package:

```bash
python3 scripts/validate.py package .
```

Validate a proposed issue body:

```bash
python3 scripts/validate.py contract path/to/issue.md
```

GitHub Actions runs both checks against the included valid contract fixture.

## Governance

`loop:approved` is review evidence, not merge authority. Agents never apply
`loop:ready`, merge, enable auto-merge, take over stale branches, or weaken
repository protection.

## Licence and attribution

Released under the MIT License. The design was informed by
[Finn-loop](https://github.com/finna/Finn-loop); see [NOTICE.md](NOTICE.md).

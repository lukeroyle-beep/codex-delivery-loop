## Problem

Users need a bounded delivery loop that does not require repeated prompts.

## Acceptance criteria

- [ ] AC-1: A run stops after the configured work-unit or elapsed-time limit.
- [ ] AC-2: The run reports why it stopped and what work remains.

## Non-goals

- NG-1: The loop does not merge pull requests.
- NG-2: The loop does not take over stale branches automatically.

## Relevant files

- `SKILL.md`: Defines bounded execution.

## Verification

1. Run with a one-unit limit and confirm it stops after AC-1 is satisfied.
2. Confirm the final output reports the stop reason and remaining queue for
   AC-2.

## Risk

Low: this fixture changes no runtime system.

## Dependencies

- None.

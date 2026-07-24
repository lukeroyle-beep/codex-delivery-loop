# Issue contract

Use this exact structure:

```markdown
## Problem

One or two sentences describing the user or operational problem.

## Acceptance criteria

- [ ] AC-1: Observable, testable outcome
- [ ] AC-2: Observable, testable outcome

## Non-goals

- NG-1: Behaviour that must not change
- NG-2: Work explicitly excluded

## Relevant files

- `path/to/file`: why it matters

## Verification

1. Exact action and expected result covering AC-1.
2. Exact action and expected result covering AC-2.

## Risk

Low | Medium | High, with one-sentence justification.

## Dependencies

- None, or linked issues and the required relationship.
```

## Contract rules

- Keep `AC-N` and `NG-N` identifiers unique, sequential, and stable.
- Write acceptance criteria as observable outcomes, not implementation tasks.
- Make every verification step map to at least one acceptance criterion.
- Ensure no acceptance criterion requires violating a non-goal.
- State permissions, error behaviour, empty states, migration treatment, and
  compatibility where they affect observable behaviour.
- Keep implementation suggestions out unless the repository makes them
  architectural constraints.
- Split work that cannot reasonably be completed and reviewed within one
  working day.
- Use GitHub dependency links or explicit `Blocked by #N` entries for ordered
  work. A downstream issue cannot be `loop:ready` while its blocker is open.

## Approval

Create a drafted contract with `loop:spec`. A human reads the final issue and
changes the label to `loop:ready`. Editing acceptance criteria, non-goals, risk,
or dependencies after that approval returns the issue to `loop:spec`.

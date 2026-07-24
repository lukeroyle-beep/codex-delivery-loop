# Build and review policy

## Pull request contract

Every delivery-loop pull request must include:

```markdown
Closes #N

Delivery-Loop-Run: ISSUE-N/ATTEMPT

## Scope ledger

- AC-1: implementation and evidence
- NG-1: preservation evidence
- Other behaviour changes: None

## Verification

1. Manual step and observed result

## Checks

- Command or required check: result

## Risk

Low | Medium | High: justification
```

If `Other behaviour changes: None` is false, return the issue to
`loop:human-review` before opening or updating the pull request.

## Review categories

Every must-fix finding begins with exactly one category:

- `[AC-N]`: an acceptance criterion is not satisfied.
- `[DEFECT]`: implementation is broken within the approved scope.
- `[SECURITY]`: a material security issue prevents safe delivery.
- `[CI]`: a required continuous integration check failed.
- `[SCOPE AC-N ↔ NG-N]`: an acceptance criterion conflicts with a non-goal.

Do not inflate preferences, optional refactors, or unrelated improvements into
must-fix findings.

## Commit-specific verdict

Post one idempotent comment:

```markdown
Delivery-loop review of COMMIT_SHA

Required checks: passed | failed | pending | not configured
Mergeability: clean | conflicting | unknown

## Must fix before merge

None, or categorised findings with file and line evidence.

## Should fix soon

Non-blocking, in-scope observations only.

## Safe to consider for human merge

Yes | No, with the controlling reason.
```

Review the complete diff and changed files in context. Re-fetch the head commit
immediately before posting. If the same `Delivery-loop review of COMMIT_SHA`
already exists, update only when correcting a demonstrable review error;
otherwise do not duplicate it.

## Approval gates

`loop:approved` requires all of:

- every acceptance criterion satisfied;
- every non-goal preserved;
- all required checks passed;
- mergeability clean;
- reviewed head commit unchanged;
- no must-fix finding;
- no unresolved dependency or policy escalation;
- reviewer context independent from the builder context.

If required checks are not configured, use `loop:human-review`, not
`loop:approved`.

## Mandatory escalation

Use `loop:human-review` for:

- contract conflict or ambiguity requiring a product decision;
- exhausted repair budget;
- missing required checks;
- stale or conflicting workflow state;
- changes involving credentials, authentication, authorisation, billing,
  production data deletion, destructive migrations, deployment permissions,
  branch protection, or workflow trust boundaries;
- any requested action beyond the issue contract.

Human review can return the item to a valid state after recording the decision.

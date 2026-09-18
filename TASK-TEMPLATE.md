# Bounded Task Packet

## Task identity

- Evaluation/task ID:
- Date:
- Repository:
- Branch or committed baseline:
- Worktree:
- Owner:

## Objective

State one concrete outcome. Describe the behavior or artifact that must exist when the task is complete.

## Candidate route/model

- Preferred model:
- Provider:
- Why this route is appropriate:
- Escalation target:

## Owned paths

List the exact files or directories the worker may change.

- 

## Forbidden scope

The worker must not:

- Modify paths outside the owned set without authorization.
- Change production behavior when the task is test-only.
- Change dependencies, generated metadata, schemas, or deployment state unless explicitly listed.
- Commit, merge, push, reset, stash, clean, or delete existing work unless explicitly authorized.
- Read, expose, or store secrets.

## Dirty-worktree preservation

Record the starting dirty state. Preserve all pre-existing changes, screenshots, generated artifacts, local WIP, and prior tests. Do not use cleanup operations to make the task easier. If a pre-existing artifact conflicts with the task, stop and report it rather than deleting or hiding it.

## Required reading

List the authoritative files, contracts, architecture documents, source definitions, usages, and focused tests that must be read before editing.

- 

## Relevant context

- System-spine sections:
- Glossary terms:
- Contracts and invariants:
- Dependency/blast-radius notes:
- Optional intelligence integrations:

## Acceptance criteria

1. 
2. 
3. 

Each criterion must be observable and independently verifiable.

## Required verification commands

- Focused test:
- Package typecheck:
- Build, if applicable:
- Structural/map checks, if applicable:
- Runtime or live-state check, if applicable:
- `git diff --check`

Record exact commands, exit codes, and meaningful results.

## Escalation and stop conditions

Escalate after two materially unsuccessful repair attempts, or earlier when the dependency map reveals an unplanned public boundary, contract drift, or architecture ambiguity.

If the task exposes a concrete production defect outside the owned scope:

1. Stop implementation.
2. Preserve the current worktree and evidence.
3. Record the failing command and diagnosis.
4. Report the blocker and affected paths.
5. Do not broaden the task or patch production code without explicit authorization.

## Evidence handoff

- Resolved model/provider:
- Session/run ID:
- Start/end time, if trustworthy:
- Attempts:
- Repairs:
- Files read:
- Changed paths:
- Scope drift:
- Initial failures:
- Focused results:
- Typecheck/build results:
- Structural/runtime results:
- Owner corrections:
- Remaining gaps or blockers:
- Artifact and report paths:

## Acceptance status

- Worker status: Not accepted / Ready for review / Blocked
- Owner status: Not reviewed / Accepted / Rejected
- Notes:

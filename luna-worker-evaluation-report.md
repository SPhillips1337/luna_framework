# Luna Worker Evaluation Report

Date: 2026-09-16

## Scope

This evaluation used Luna as an explicitly routed worker for a bounded Echoes of Aion Phase 3 diplomacy task. It was not an implementation of the Luna framework itself.

Repository:

`C:/Users/steph/Documents/development/EchoesOfAion`

Branch:

`feature/aion-phase3`

Task:

Add one focused regression test proving that an active-war pair with opposing fleets co-located in one system can move from a valid prior `PROPOSE_PEACE` state to the exact current-turn `ACCEPT_PEACE` action before combat.

## Resolved route

- Model: `gpt-5.6-luna`
- Provider: `openai-codex`

## Worker constraints

The worker was instructed to:

- Preserve the pre-existing dirty worktree.
- Modify only `packages/server/tests/turn-resolution/turn-pipeline.test.ts`.
- Avoid production-code changes unless a concrete defect blocked the test.
- Avoid commits, merges, pushes, resets, stashes, generated-map changes, and deletion of existing artifacts.
- Read the repository contracts, architecture documents, turn pipeline, war resolver, combat resolver, order validator, and focused tests before editing.

## Implementation result

Added one regression test in:

`packages/server/tests/turn-resolution/turn-pipeline.test.ts`

The test:

1. Creates two empires with opposing fleets in the same system and an active war.
2. Uses the canonical `war:${empirePairKey(...)}` identifier.
3. Resolves a valid prior `PROPOSE_PEACE` action.
4. Submits the exact current-turn `ACCEPT_PEACE` action.
5. Verifies the war becomes `ended` before combat.
6. Verifies no combat report is produced.
7. Verifies both fleets survive.
8. Verifies both the original input state and the prior proposed state remain unchanged.

No production code or generated maps were changed.

## Verification evidence

Initial baseline before the edit:

- `pnpm exec vitest run packages/server/tests/turn-resolution/turn-pipeline.test.ts`
- Result: 20 tests passed, 0 failed.

Targeted regression:

- `pnpm exec vitest run packages/server/tests/turn-resolution/turn-pipeline.test.ts -t "accepts previously proposed peace before combat"`
- Result: 1 passed; 8 tests skipped in the package test file.

Focused pipeline file:

- `pnpm exec vitest run packages/server/tests/turn-resolution/turn-pipeline.test.ts`
- Result: 21 tests passed, 0 failed.

Server typecheck:

- `pnpm --dir packages/server run typecheck`
- Result: passed with exit code 0.

Agent-map verification:

- `pnpm run agent:map:verify`
- Result: passed; map fresh with 70 source files and 229 resolved internal edges.

Architecture and boundary fixture tests:

- `pnpm run test:agent-architecture`
- Result: generator and boundary checker fixture tests passed.

Boundary report:

- `pnpm run agent:boundaries`
- Result: completed successfully with no unresolved imports or boundary violations. It reported 12 existing report-only dependency cycles.

Whitespace validation:

- `git diff --check`
- Result: passed.

## Assessment

The task demonstrates that Luna can execute a tightly scoped repository change while respecting explicit file ownership, dirty-tree preservation, source-first contract discovery, and evidence-based verification.

It does not by itself establish a reusable Luna framework, orchestration protocol, benchmark suite, persistence layer, or multi-agent coordination system. Those would need to be designed and evaluated separately in this workspace.

## Potential next framework work

If this workspace is intended to become a Luna improvement framework, useful next slices would be:

- Define a standard task brief and worker handoff schema.
- Capture route, model, provider, changed paths, commands, exit codes, and blockers as machine-readable evidence.
- Add acceptance criteria and verification-ladder fields to each evaluation.
- Separate worker self-report from owner/adversarial acceptance.
- Add repeatable benchmark tasks covering code changes, test-only changes, failure recovery, and dirty-worktree preservation.
- Store evaluation results without copying secrets or unrelated repository artifacts.

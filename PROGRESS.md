# Progress

## Current state

- Framework documentation foundation: complete.
- Canonical TypeScript routing fixture: created at `fixtures/routing-benchmark-ts`.
- Controlled B1/B2/B3 evaluations: executed with explicit Luna and Terra dispatch routes.
- Launcher stability: root-caused and fixed (sandbox child-process spawn); matched re-runs B1/B2/B3 completed with normalized timing/cost capture and independent verification. See `RESULTS.md` "Stabilized matched re-runs".
- Echoes of Aion: untouched during fixture work.
- B4 ladder (A0 audit + A1–A4 execution slices): complete; see `RESULTS.md`.
- n=3 repeat track (b4r): closed, parent-adjudicated scores retained per run.
- Controlled-confirmation track (n=6/arm, b4c): complete and frozen — 12/12 valid runs; protocol label CONFIRMED, explicitly EXPLORATORY (revised scoring rule; order-entangled; not a model ranking). See `RESULTS.md` "B4 controlled-confirmation track" and `b4-repeat-track/` (73-entry SHA-256 manifest). Evidence bundle committed locally as the initial snapshot `8ae7387`; tag `b4-confirmation-frozen`.
- Current phase: none active. Any follow-up requires a separately pre-registered protocol; no reruns or scoring-rule changes against this frozen record.

## Completed work

### Framework foundation

- Documented the Luna/Terra model-fit hypothesis and the framework objective in `BRIEF.md`.
- Added `SPINE.md`, `GLOSSARY.md`, `TASK-TEMPLATE.md`, and `EVALUATION-PROTOCOL.md`.
- Added research and provenance links in `LINKS.md`.
- Created the canonical TypeScript fixture with domain, service, API, test, task-packet, and documentation layers.
- Added explicit baseline tags, isolated external worktrees, pinned dependencies, and reproducible package scripts.

### B1 — single-file regression

- Objective: lowercase and trim email normalization.
- Baseline tag: `benchmark-b1-baseline` → `361fb242ca3eedc0ac2f869dc12c6ddbd4f3f212`.
- Worktrees: `fixtures/fixture-runs/b1-luna-matched` and `fixtures/fixture-runs/b1-terra-matched`.
- Luna dispatch: `openai-codex:gpt-5.6-luna`; thread `01a0af7d-7e4e-7ca1-a436-acefc7ca8fa9`; JSONL `luna-b1-matched.jsonl`.
- Terra dispatch: `openai-codex:gpt-5.6-terra`; thread `01a0af8b-0647-7993-85e9-ed2673d1cd38`; JSONL `terra-b1-matched.jsonl`.
- Both changed only `src/domain/email.ts` and passed independent test, typecheck, and diff checks.
- Classification: independently verified behavior with a baseline-metadata caveat; exclude from strict matched-performance metrics.

### B2 — cross-layer revoked-access propagation

- Objective: propagate revoked status through domain and service behavior while preserving inactive API presentation and input immutability.
- Baseline tag: `benchmark-b2-baseline` → `5d600a591c00cc06a23863a26dfbdf6413d6074b`.
- Worktrees: `fixtures/fixture-runs/b2-luna-matched` and `fixtures/fixture-runs/b2-terra-matched`.
- Luna dispatch: `openai-codex:gpt-5.6-luna`; thread `01a0afdd-17e4-76f2-8b84-e34415ee2eee`; JSONL `b2-luna.jsonl`.
- Terra dispatch: `openai-codex:gpt-5.6-terra`; thread `01a0afe4-06d4-76c2-bb34-8fff0dd4f887`; JSONL `b2-terra.jsonl`.
- Both changed only `src/domain/access-grant.ts` and `src/services/access-service.ts`; the API presenter already satisfied the contract.
- Both passed independent `pnpm run test:b2`, `pnpm run typecheck`, and `git diff --check`.
- Classification: strongest matched boundary datapoint, without a model-superiority claim.

### B3 — expiry-time contract propagation

- Objective: make time-aware service authorization and API presentation honor strict expiry semantics.
- Baseline tag: `benchmark-b3-baseline` → `d4d470c21cb1630540334a26918999a25a4b9d14`.
- Worktrees: `fixtures/fixture-runs/b3-luna-matched` and `fixtures/fixture-runs/b3-terra-matched`.
- Luna dispatch: `openai-codex:gpt-5.6-luna`; thread `01a0b01a-bb69-73a3-9956-78fa2d410193`; JSONL `b3-luna.jsonl`.
- Terra dispatch: `openai-codex:gpt-5.6-terra`; thread `01a0b021-acda-7973-a9c6-d6fc1448b0fa`; JSONL `b3-terra.jsonl`.
- Both changed only `src/services/access-service.ts` and `src/api/access-presenter.ts`.
- The domain expiry helper was already correct in the baseline; B3 therefore measured propagation/synthesis, not implementation of all three layers.
- Both passed independent `pnpm run test:b3`, `pnpm run typecheck`, and `git diff --check`.
- Classification: matched modest multi-module datapoint, without a model-superiority claim.

## Evidence controls

- Each task used a committed failing/incomplete fixture baseline and fresh external worktrees.
- Baseline `HEAD` matched the task tag in both worktrees before dispatch.
- Routes were explicitly dispatched as `openai-codex:gpt-5.6-luna` and `openai-codex:gpt-5.6-terra`.
- Worker thread IDs and JSONL artifacts are recorded above and in `RESULTS.md`.
- Parent-side diff inspection and independent focused test, typecheck, and whitespace checks were required for acceptance.
- Worker self-report was treated as evidence, not final acceptance.

## Known limitations

- Earlier Windows/Vite `spawn EPERM` is resolved: the Codex `workspace-write` sandbox blocks Node child-process spawns (Vite `net use` probe, esbuild helper). Stabilized runs use `danger-full-access` on disposable external worktrees; the launcher-only baseline commits and dispatch harness are documented in `RESULTS.md`.
- Stabilized run timing/cost figures are single-sample per cell and warm-cache-contaminated; usable as raw evidence only, not as comparisons. Parent-shell timings must never be compared with worker-dispatch timings; the harness window spans only the `codex exec` call.
- Timing and cost data from the pre-stabilization runs must not be compared.
- B1 packet/baseline metadata was finalized after its original run artifacts; the stabilized B1 pair supersedes them for metrics once n>1 exists.
- B3's domain helper was already correct, reducing the realized change to service/API propagation; B4 must leave the domain layer incomplete.
- Some worker runtime reports did not expose provider/model/session metadata; explicit CLI dispatch plus JSONL `thread_id` is the route evidence.
- `luna_framework` itself is not a Git repository, so root-level documentation has no commit history and root-level `git diff --check` is unavailable.

## Current conclusions

- Luna and Terra both completed B2 and B3 correctly with bounded scope in these small fixtures.
- The evidence supports the task-packet, spine, glossary, baseline-tag, isolated-worktree, and independent-verification protocol as a correctness and scope-control mechanism.
- The evidence does not establish Luna-versus-Terra quality, speed, cost, or superiority.
- The recurring process failure is environmental: worker Vitest/Vite child-process execution and launcher timing need stabilization before quantitative routing claims.

## Next decision

Launcher stabilization is complete (step 1) and B2/B3 have been repeated with normalized capture (step 2, single-sample each). Remaining:

1. Build n>1 per cell: repeat stabilized B1–B3 arms in randomized dispatch order before any timing/cost reading.
2. Design B4 with an intentionally incomplete domain layer so true contract synthesis is measured.
3. Keep the operator-authorization addendum text in a version-controlled file rather than embedded in the harness.

Do not clean or remove the existing worktrees and JSONL artifacts before evidence review is complete.

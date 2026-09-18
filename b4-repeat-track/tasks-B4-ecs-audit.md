# B4-A0 — Ventralis monolith architecture audit (audit-only, scored)

## Route

- Intended route: judgment/audit slice — first B4 candidate; both arms evaluated against the same owner rubric.
- Comparison route: must be captured explicitly for every run.

## Baseline

- Repository: `fixtures/ecs-monolith-ts` (synthetic monolith motivated by the Echoes of Aion refactoring research question; it is NOT an Aion refactor — see README).
- Source baseline tag: `benchmark-ecs-baseline` (characterization suite green, typecheck clean).
- The dispatched worktree HEAD is the packet commit that adds this file on top of the source baseline; the benchmark operator certifies HEAD as the approved evaluation baseline. Where tag and HEAD disagree, HEAD is authoritative.
- Before dispatch, `git rev-parse HEAD` must equal `git rev-parse master` in the source repo at packet freeze time.

## Objective

Produce an architecture audit and migration plan for refactoring `src/main.ts` into a modular architecture **of the candidate design's choosing** (ECS is the motivating proposal, not a mandate — a justified hybrid that rejects ECS for specific concerns scores well). This task is scored on the plan only. **You must stop after the plan: zero source edits, zero file creation, zero renames, zero formatting changes.**

The stated refactoring goal (from the project owner's research note) is: file-level isolation, strict TypeScript interfaces, separation of logic (Systems) from state (Components), no single migrated file over 120 lines, and the rewritten entry point under ~80 lines. You may challenge any part of this with reasons.

## Deliverable (your final message)

A Markdown audit containing ALL of the following:

1. **State map table** — every module-level mutable binding in `src/main.ts` → classification: proposed Component data, retained runtime state (world/session), derived-on-read, or dead/redundant. Include the hidden ones (e.g. what `snapshot`/`restore` touch, RNG, save counters).
2. **Function map table** — every function → proposed destination (system / entity factory / type module / persistence adapter / debug surface / retained bootstrap).
3. **Side effects and dependencies table** — per function: reads/writes of globals, output emission, storage writes, RNG consumption, log coupling.
4. **Ownership and mutation boundaries** — who owns world state, the event queue, the persistence adapter, the clock, and the random source after migration; how systems mutate state (returned commands vs controlled direct mutation — pick one and justify).
5. **Not-ECS list** — concerns that must NOT become components/systems and why (at minimum justify or reject: persistence boundary, debug/HUD surface, scheduled-event queue, seeded RNG).
6. **Hidden-coupling register** — every non-obvious coupling you found, with file:line evidence. The suite pins several legacy quirks (resource-mirror drift, secret recipe costs, double stone drop, KeyH re-equip, log-length affecting spawns); your plan must treat each as behavior to preserve, not fix.
7. **Proposed dependency graph** — Mermaid or ASCII, module-level, with arrow directions; must be acyclic and must show where `main.ts` sits relative to persistence and debug surfaces.
8. **Proposed file tree** for the migration, respecting the line budget above.
9. **Migration order** — the phase sequence a follow-up implementation task would execute, sliced so the characterization suite passes after each slice.
10. **Risk & verification plan** — how a later implementer proves behavioral preservation without editing tests; what would make you abandon ECS for a concern.

## Required reading

- `README.md`
- `src/main.ts` (full file)
- `tests/characterization.test.ts` (full file)

## Forbidden scope

- Do not edit or create ANY file under `src/` or `tests/`; do not create new files anywhere; do not touch package files, docs, configs, `.gitignore`, or dependencies.
- Do not run formatters or lint --fix. `git diff` must be empty at the end (ignoring untracked tooling caches).
- Read-only commands are allowed (including running the test suite).
- Do not commit, push, merge, reset, stash, clean, or delete.

## Acceptance criteria

1. Zero source/test diffs at completion (`git status --short` shows nothing under `src/`/`tests/`; `git diff --check` clean).
2. All ten deliverable sections present.
3. State map covers every `let` binding in `src/main.ts` (there are 15 module-level bindings) plus the exported `monsters` array.
4. Hidden-coupling register identifies at least: the resource-mirror vs inventory double-accounting, craft side effects on `attackBonus`/`torchBuffTicks` and secret wood consumption, RNG consumption order dependence, log-length dependence in spawn logic, `decideUseStorage` gating of periodic saves, and the KeyH re-equip quirk.
5. Dependency graph is acyclic and consistent with the proposed file tree.
6. Plan states explicitly that `tests/characterization.test.ts` is the acceptance oracle and must not be edited.

## Verification (report exact results)

- `git status --short`
- `git diff --check`
- `pnpm run test` (must remain green — read-only run)
- `pnpm run typecheck`

## Handoff

Record model/provider, session/thread ID, attempts, changed paths (must be none), each verification command with exit code, initial failures, and remaining blockers. Your final message is the graded artifact: include the complete audit in it, not a summary of a file.

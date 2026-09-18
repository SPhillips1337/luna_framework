# B4-A0 Owner Rubric — Ventralis monolith audit (plan-only, 100 pts)

Owner-side scoring file. NEVER included in a dispatch worktree; workers see only `tasks/B4-ecs-audit.md`.

| # | Dimension | Pts | Scored by |
|---|---|---|---|
| 1 | State coverage: all 15 module-level `let` bindings + exported `monsters` classified with a defensible destination | 15 | table inspection vs `grep -c '^let' src/main.ts` |
| 2 | Function coverage: every function mapped; no `TODO/unknown` escapes | 10 | table inspection vs `grep -c '^function' src/main.ts` |
| 3 | Hidden couplings found (each 2 pts): mirror-vs-inventory double accounting; craft side effects on `attackBonus`/`torchBuffTicks`/secret wood; RNG order dependence; log-length spawn coupling; `decideUseStorage` save gating; KeyH re-equip | 12 | presence with file:line evidence |
| 4 | Not-ECS judgment: persistence, debug/HUD, event queue, seeded RNG each explicitly kept/converted with reasons; blanket "everything becomes a component" scores 0 here | 15 | reasons evaluated, not positions |
| 5 | Dependency graph: present, acyclic, consistent with proposed tree, main/bootstrap at the leaves not the root | 10 | graph inspection |
| 6 | Ownership/mutation contract: one coherent answer for world ownership + system mutation mechanism (commands vs controlled mutation), applied to persistence + RNG | 10 | internal consistency |
| 7 | Migration order: sliced so characterization suite stays green after each slice; names the oracle and forbids editing it | 8 | plan inspection |
| 8 | Quirk discipline: legacy behaviors treated as preserve-not-fix (drift, double drop, re-equip) | 8 | explicit statements |
| 9 | Clean stop: zero source/test diffs; tests still green; `git diff --check` exit 0; audit in final message | 7 | parent verification (hard gate: violation caps total at 40) |
| 10 | Line-budget handling: addresses 120-line cap and bootstrap size; challenges or accepts with reasons | 5 | plan inspection |

Grading procedure per run:
1. Parent-verify worktree: `git status --short` (no tracked changes under src/tests), `pnpm run test` (21/21), `pnpm run typecheck`, `git diff --check`.
2. Parse JSONL: one `turn.completed`, record thread_id, codex_exit, elapsed.
3. Extract the final assistant message (the graded artifact) from the JSONL, not from any file the worker might have created.
4. Score dimensions 1–10; record per-dimension notes in RESULTS.md. A dimension with missing required content scores 0, not "partial credit by vibe".

Interpretation guardrails:
- n=1 per arm is a qualitative signal only; no superiority claim until n>1 in randomized order.
- The audit tests architectural judgment; it does not by itself validate that either arm can execute the migration (A1–A4 slices follow).

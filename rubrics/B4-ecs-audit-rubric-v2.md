# B4-A0 Owner Rubric v2 — Ventralis monolith audit (plan-only, 100 pts)

Owner-side scoring file. NEVER included in a dispatch worktree; workers see only
`tasks/B4-ecs-audit.md`. v2 changes per n=1 round findings (2026-09-18):
dimension 3 expanded from 6 to 10 required couplings (the four extra planted traps Terra's
first audit caught); new dimension 11 for false-positive risk (behavior-breaking refactor
proposals); points rebalanced to keep total 100.

| # | Dimension | Pts | Scored by |
|---|---|---|---|
| 1 | State coverage: all 15 module-level `let` bindings + exported `monsters` classified with a defensible destination | 12 | table inspection vs `grep -c '^let' src/main.ts` |
| 2 | Function coverage: every function mapped; no `TODO/unknown` escapes | 8 | table inspection vs `grep -c '^function' src/main.ts` |
| 3 | Hidden couplings found (each 2 pts, 10 total): (a) mirror-vs-inventory double accounting; (b) craft side effects on `attackBonus`/`torchBuffTicks`/secret wood; (c) RNG order dependence; (d) log-length spawn coupling; (e) `decideUseStorage` save gating; (f) KeyH re-equip; (g) unused `MonsterInstance.attack` vs hardcoded per-kind damage; (h) equality-only (`===`) due-event matching — `<=`/priority-queue would change semantics; (i) restore appends its log entry at the RESTORED tick; (j) `resetGame` deliberately leaves `worldRef` intact | 20 | presence with file:line evidence |
| 4 | Not-ECS judgment: persistence, debug/HUD, event queue, seeded RNG each explicitly kept/converted with reasons; blanket "everything becomes a component" without per-concern reason scores 0 here | 12 | reasons evaluated, not positions |
| 5 | Dependency graph: present, acyclic, consistent with proposed tree, main/bootstrap at the leaves not the root | 8 | graph inspection |
| 6 | Ownership/mutation contract: one coherent answer for world ownership + system mutation mechanism (commands vs controlled mutation), applied to persistence + RNG | 7 | internal consistency |
| 7 | Migration order: sliced so characterization suite stays green after each slice; names the oracle and forbids editing it | 7 | plan inspection |
| 8 | Quirk discipline: legacy behaviors treated as preserve-not-fix (drift, double drop, re-equip) | 7 | explicit statements |
| 9 | Clean stop: zero source/test diffs; tests still green; `git diff --check` exit 0; audit in final message | 7 | parent verification (hard gate: violation caps total at 40) |
| 10 | Line-budget handling: addresses 120-line cap AND file readability intent (no logic-cramming loophole); challenges or accepts with reasons | 2 | plan inspection |
| 11 | False-positive risk: no proposed "fix" that would silently break pinned behavior (dedup mirror/inventory, `<=` scheduler, unify init/save storage paths, reassign monsters array, add restore validation/defaults, drop secret wood cost). Any behavior-breaking proposal caps this dimension at 2 AND is recorded as a named qualitative finding regardless of total score | 10 | proposals checked against the trap list; absence = full marks |

Grading procedure per run:
1. Parent-verify worktree: `git status --porcelain` empty under src/tests, `pnpm exec vitest run
   tests/characterization.test.ts` (21/21), `pnpm run typecheck`, `git diff --check` exit 0.
2. Parse JSONL: one `turn.completed`, record thread_id, codex_exit, elapsed, token envelope.
3. Extract the final assistant message (the graded artifact) from the JSONL, not from any file
   the worker might have created.
4. Verify cited file:line references resolve against the frozen baseline `src/main.ts`
   (programmatic spot-check; stale/fabricated citations = the finding does not count for dim 3).
5. Edge-parse any dependency graph programmatically for acyclicity + no edge into `main`
   from lower layers.
6. Score dimensions 1–11; per-run notes preserved, NOT averaged away. A dimension with missing
   required content scores 0, not "partial credit by vibe".
7. Aggregate per arm: mean, median, range, and per-trap detection counts (a/b/…/j) across runs.

Interpretation guardrails:
- Repeat track tests whether the n=1 register-depth difference replicates. If it does:
  replicated qualitative evidence, not proof of superiority. If it vanishes: sampling noise.
- Timing/token columns recorded, never ranked unless sample design supports it.
- A0 judgment scores and A1–A4 execution outcomes measure different capabilities; never merge
  into one ranking.

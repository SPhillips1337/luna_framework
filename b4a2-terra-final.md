Completed combat extraction.

Files changed:

- [src/main.ts](C:\Users\steph\Documents\development\luna_framework\fixtures\fixture-runs\b4a2-terra\src\main.ts)
- [src/systems/combat-system.ts](C:\Users\steph\Documents\development\luna_framework\fixtures\fixture-runs\b4a2-terra\src\systems\combat-system.ts)

Coupling traps:

- Attack RNG/order: `attackRoll()` remains inside combat system; it draws once through `nextRandom()` before hit resolution.
- Stone double-drop: kill path performs both `session.resources.stone += 2` and `session.inventory.items.stone += 2`.
- Live-array identity: exported `monsters` is the direct `session.monsters` alias; combat uses `push`/`shift`, while restore retains `length = 0`.
- Tick spawn RNG: `main.ts` retains the original `%20` and event-log parity guard, then calls `nextRandom()` only inside that guarded branch.

Verification run:

- `pnpm exec vitest run tests/characterization.test.ts` — exit 0; 21/21 passed.
- `pnpm run typecheck` — exit 0.
- Line check — `combat-system.ts: 0` lines over 120 columns. `main.ts` has 10 pre-existing, untouched over-120 lines.
- `git diff --check` — exit 0.
- `git status --porcelain` — `M src/main.ts`, `?? src/systems/combat-system.ts`.
- `git diff --name-only` — `src/main.ts`.
- `git ls-files --others --exclude-standard` — `src/systems/combat-system.ts`.

Model/provider: Codex / OpenAI. Session/thread ID: not visible. Attempts: 1 implementation pass; repairs: split two written glue lines and corrected one PowerShell verification interpolation error. Scope drift: none. Initial failures: verification command parser error only; no code/test/typecheck failures. Remaining blockers: none.

Intentional deviations: none.
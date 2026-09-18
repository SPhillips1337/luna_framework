Implemented B4-A4 tick-loop extraction.

Files:

- Modified `src/main.ts`
- Created `src/systems/tick-system.ts` (50 lines)

Bootstrap tick order:

1. Increment tick
2. Starvation
3. Torch buff decrement
4. Strict-equality event selection
5. Event application/removal
6. Live-array monster damage pass
7. Parity-gated spawn/RNG draw
8. `saveIfDue()`

Hard-failure traps remain in `tick-system.ts`: `===`/`!==` event matching, parity-gated RNG draw, live `monsters` iteration, and save immediately after spawn.

Verification:

- `pnpm exec vitest run tests/characterization.test.ts` — exit 0, 21/21 passed
- `pnpm run typecheck` — exit 0
- `git diff --check` — exit 0
- New file width proof — 0 lines over 120 columns
- Added `main.ts` hunk width proof — all lines within 120 columns
- Path audit — only `src/main.ts` and `src/systems/tick-system.ts`

Attempts: 2. Initial proof command had a PowerShell interpolation parse error; corrected and reran successfully.

Model/provider and session/thread ID: not visible.

Scope drift: none. Intentional deviations: none. Remaining blockers: none.
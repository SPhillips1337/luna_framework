Implemented B4-A3 persistence extraction.

Files:

- `src/systems/persistence-system.ts` — added
- `src/main.ts` — modified

Pins preserved:

- Snapshot key order, omissions, shallow copies, and log truncation.
- Live monster-array identity during restore.
- Restore attribution uses restored tick.
- Direct init restore vs gated save asymmetry.
- Counter increments only before gated tick-10 writes.
- No RNG consumption in persistence paths.

Verification:

- `pnpm exec vitest run tests/characterization.test.ts` — exit 0, 21/21 passed
- `pnpm run typecheck` — exit 0
- `git diff --check` — exit 0
- New-file lines over 120: 0
- Added `main.ts` lines over 120: 0
- Owned paths confirmed: `src/main.ts`, `src/systems/persistence-system.ts`

Attempts/repairs: one PowerShell line-length proof command initially had interpolation syntax errors; corrected and reran successfully.

Model/provider and session/thread ID were not visible. Scope drift: none. Remaining blockers: none.

Intentional deviations: none.
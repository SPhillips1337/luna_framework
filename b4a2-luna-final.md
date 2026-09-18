Implemented B4-A2 combat extraction.

Model/provider: GPT-5 / OpenAI  
Session/thread ID: not visible  
Attempts: 2 patch attempts; corrected one failed line-check probe.

Files changed:

- `src/main.ts`
- `src/systems/combat-system.ts`

Scope drift: none.

Verification:

- `pnpm exec vitest run tests/characterization.test.ts` — exit 0, 21/21 passed
- `pnpm run typecheck` — exit 0
- Line-length check — combat system max 87 columns; `main.ts` retained 7 pre-existing overlong lines
- `git diff --check` — exit 0
- `git status --porcelain` / `git diff --name-only` — only owned paths changed

Coupling traps:

- Attack roll order and bonuses remain in `combat-system.ts`
- Stone double-drop updates both mirror and inventory
- `monsters` remains the live `session.monsters` alias
- RNG calls remain only in combat roll and guarded spawn logic
- Persistence, HUD/input, event filtering, and tick internals remain in `main.ts`

Intentional deviations: none.
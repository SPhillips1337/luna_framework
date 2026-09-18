Implemented ordered tick-loop extraction.

Files changed:

- `src/main.ts`
- `src/systems/tick-system.ts` (74 lines)

Bootstrap order in `runTickSystems()`:

1. increment tick
2. starvation
3. torch-buff decrement
4. due-event application and `!==` removal
5. monster damage
6. parity-gated spawn
7. persistence save

Hard-failure safeguards:

- Strict event matching/removal: `event.at === tickCount` and `event.at !== tickCount`
- RNG draw is inside the `%20` plus even-log-parity gate
- Monster damage iterates the exported `monsters` reference, backed by the live `session.monsters` array
- Persistence remains immediately after spawn processing

Verification results:

- `pnpm exec vitest run tests/characterization.test.ts` — exit 0; 21/21 passed
- `pnpm run typecheck` — exit 0
- `git diff --check` — exit 0
- Line/width proof:
  - `src/systems/tick-system.ts`: 74 lines; max width 86; 0 lines over 120
  - added `src/main.ts` hunk: 4 lines; max width 87; 0 lines over 120
- `git diff --name-only`: `src/main.ts`
- `git ls-files --others --exclude-standard src`: `src/systems/tick-system.ts`
- `tests/` untouched

Intentional deviations: none.  
Scope drift: none.  
Initial failures: none.  
Attempts: 1 implementation attempt; 1 structural refinement to make the ordered phases explicit.  
Remaining blockers: none.  
Model/provider: GPT-5 / Codex. Session/thread ID: not visible.
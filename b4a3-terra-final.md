Implemented persistence extraction.

Files changed:

- `src/systems/persistence-system.ts` (created)
- `src/main.ts` (modified)

Pin locations:

- Key order, omissions, copies/truncation: `snapshot()` in persistence system.
- Monster array identity: clears and pushes into `session.monsters` in `restore()`.
- Save-time gating: `decideUseStorage()` / `persist()` in persistence system.
- Counter timing: increment immediately before gated write in `persist()`, called only at tick `% 10`.
- Log attribution: `restore()` assigns restored tick before calling main’s `say("save restored")`.
- RNG neutrality: persistence functions do not consume RNG.

Verification run:

- `pnpm exec vitest run tests/characterization.test.ts` — exit 0; **21/21 passed**
- `pnpm run typecheck` — exit 0
- Line proof:
  - `src/systems/persistence-system.ts`: 0 lines >120; 55 total lines
  - Added diff lines in `src/main.ts`: 0 lines >120
  - `git diff --check` — exit 0
- `git diff --name-only` + `git ls-files --others --exclude-standard src`:
  - `src/main.ts`
  - `src/systems/persistence-system.ts`

Initial failures/repairs:

- First test run failed because the extracted restore function required a logging callback when invoked through `api.restore`; repaired with a minimal main bootstrap wrapper. Final test run passed.
- One audit helper command had a PowerShell interpolation parse error; corrected before audit execution.

Model/provider: Codex / OpenAI (GPT-5).  
Session/thread ID: not visible.  
Attempts: 2 implementation/test attempts.  
Scope drift: none.  
Intentional deviations: none.
# Evaluation Results Registry

## Status legend

- **Exploratory** — useful for hypothesis formation or protocol design; not a strict model comparison.
- **Matched** — satisfies the common-baseline, isolated-worktree, identical-task, route-capture, and independent-verification controls.
- **Incomplete** — evidence is insufficient for acceptance or comparison.

## Echoes of Aion Luna/Terra pilot

- Status: **Exploratory**
- Repository: `C:\Users\steph\Documents\development\EchoesOfAion`
- Branch: `feature/aion-phase3`
- Pilot area: diplomacy and turn-resolution boundary
- Evaluation ledger: `C:\Users\steph\Documents\development\EchoesOfAion\.agent\evaluations\2026-09-luna-terra-pilot.md`
- Task packets: `C:\Users\steph\Documents\development\EchoesOfAion\.agent\tasks\`
- Architecture plan: `C:\Users\steph\Documents\development\EchoesOfAion\.hermes\plans\2026-09-16_140000-agent-legible-architecture-pilot.md`
- Comparison status: **Not comparable**

### Recorded datapoints

| Task | Route | Outcome | Comparison status |
|---|---|---|---|
| Task 03 — accepted peace | Explicit `openai-codex:gpt-5.6-luna` | Passed first attempt; independently verified | Luna datapoint only |
| Task 04 — legacy diplomacy compatibility | Explicit `openai-codex:gpt-5.6-luna` | Passed first attempt; independently verified | Luna datapoint only |
| Task 05 — duplicate-edge normalization | Explicit `openai-codex:gpt-5.6-terra` | Passed first attempt; independently verified | Terra tooling datapoint; not matched |

The ledger also records earlier exploratory tasks, including a route-uncertain delegated run and a task executed from a Terra-context session. Those are not strict model datapoints.

### Pilot conclusion

The pilot supports only a tentative routing hypothesis: Luna is promising for tightly bounded, contract-driven work, while Terra is promising for broader tooling or architecture work. The sample is small and unmatched; no performance or superiority claim is justified.

## Controlled fixture preparation

- Fixture: `C:\Users\steph\Documents\development\luna_framework\fixtures\routing-benchmark-ts`
- Initial intentionally failing code commit: `44d136f2b0a9332f215cc5c7a2265090ea01506a`
- B1 baseline tag: `benchmark-b1-baseline` → `361fb242ca3eedc0ac2f869dc12c6ddbd4f3f212`
- B2 baseline tag: `benchmark-b2-baseline` → `5d600a591c00cc06a23863a26dfbdf6413d6074b`
- B3 baseline tag: `benchmark-b3-baseline` → `d4d470c21cb1630540334a26918999a25a4b9d14`
- Dependency setup: pinned TypeScript 5.9.3, Vitest 1.6.1, and Node types 20.19.39; lockfile committed.
- Explicit dispatch routes: `openai-codex:gpt-5.6-luna` and `openai-codex:gpt-5.6-terra`.
- Worker-reported provider/model metadata was unavailable in some runs; explicit CLI dispatch is the route evidence.
- Baseline verification: each task reproduced its intended focused failure in both fresh worktrees and passed typecheck before dispatch.
- B1 worktrees: `../fixture-runs/b1-luna-matched` and `../fixture-runs/b1-terra-matched`.
- B2 worktrees: `../fixture-runs/b2-luna-matched` and `../fixture-runs/b2-terra-matched`.
- B3 worktrees: `../fixture-runs/b3-luna-matched` and `../fixture-runs/b3-terra-matched`.

## Matched B1 run evidence

- Status: **Independently verified behavior; baseline-metadata caveat**
- Task: B1 single-file email normalization regression.
- Luna route: `openai-codex:gpt-5.6-luna`; thread `01a0af7d-7e4e-7ca1-a436-acefc7ca8fa9`; one attempt, zero repairs.
- Terra route: `openai-codex:gpt-5.6-terra`; thread `01a0af8b-0647-7993-85e9-ed2673d1cd38`; two test attempts, one code repair.
- Actual changed path in both: `src/domain/email.ts` only.
- Independent verification in both: `pnpm run test:b1`, `pnpm run typecheck`, and `git diff --check` passed.
- Initial worker test runs in both hit environment `spawn EPERM`; parent reruns passed. This is an environment/tooling caveat, not counted as a reasoning retry.
- Control caveat: the run artifacts were created before the final packet-control commit and are retained as independently verified explicit-route evidence, not a strict matched performance comparison.

## B2 run evidence

- Status: **Matched; independently verified behavior**
- Task: B2 cross-layer revoked-access contract propagation.
- Baseline tag: `benchmark-b2-baseline` → `5d600a591c00cc06a23863a26dfbdf6413d6074b`.
- Worktrees: `../fixture-runs/b2-luna-matched` and `../fixture-runs/b2-terra-matched`; both started clean at the same tag/commit.
- Luna route: `openai-codex:gpt-5.6-luna`; thread `01a0afdd-17e4-76f2-8b84-e34415ee2eee`; one implementation attempt, zero repairs.
- Terra route: `openai-codex:gpt-5.6-terra`; thread `01a0afe4-06d4-76c2-bb34-8fff0dd4f887`; one implementation attempt, zero repairs.
- Actual changed paths in both: `src/domain/access-grant.ts` and `src/services/access-service.ts` only. `src/api/access-presenter.ts` already satisfied the contract and remained unchanged.
- Independent verification in both: `pnpm run test:b2`, `pnpm run typecheck`, and `git diff --check` passed.
- Focused test acceptance covers revoked status, denied access, inactive presentation, and original-grant immutability.
- Worker-side focused test runs hit Windows/Vite `spawn EPERM`; parent reruns passed. This is recorded as environment noise, not an implementation retry.
- No timing/cost comparison is claimed; elapsed capture was not normalized.

## B3 run evidence

- Status: **Matched; independently verified behavior**
- Task: B3 modest multi-module expiry-time contract propagation.
- Baseline tag: `benchmark-b3-baseline` → `d4d470c21cb1630540334a26918999a25a4b9d14`.
- Worktrees: `../fixture-runs/b3-luna-matched` and `../fixture-runs/b3-terra-matched`; both started clean at the same tag/commit.
- Luna route: `openai-codex:gpt-5.6-luna`; thread `01a0b01a-bb69-73a3-9956-78fa2d410193`; one implementation attempt, zero repairs.
- Terra route: `openai-codex:gpt-5.6-terra`; thread `01a0b021-acda-7973-a9c6-d6fc1448b0fa`; one implementation attempt, zero repairs.
- Actual changed paths in both: `src/services/access-service.ts` and `src/api/access-presenter.ts` only. The domain helper already enforced the strict expiry boundary and remained unchanged.
- Independent verification in both: `pnpm run test:b3`, `pnpm run typecheck`, and `git diff --check` passed.
- Focused test acceptance covers pre-expiry access, access denial at expiry, inactive API presentation, and input immutability.
- Worker-side focused test runs hit Windows/Vite `spawn EPERM`; parent reruns passed. This is recorded as environment noise, not an implementation retry.
- No timing/cost comparison is claimed; elapsed capture was not normalized.

## Launcher-stability infrastructure (recorded explicitly; not model work)

Date: 2026-09-18. These changes are evaluation infrastructure. They are identical for both arms, live in the fixture baseline before any worker dispatch, and never appear in a worker solution diff.

- Root cause of the recurring worker `spawn EPERM`: the Codex `workspace-write` sandbox blocks Node child-process spawns. Two independent paths hit it: Vite 5's `windowsSafeRealPathSync` (spawns `net use` via cmd during module resolution) and esbuild's helper service process. Parent-shell reruns always passed because the parent environment can spawn children.
- Vite 6 has the same call, so version upgrade does not help. Fixture-side `resolve.preserveSymlinks: true` (new committed `vitest.config.ts`) skips the `net use` probe, but a TS config load itself spawns esbuild, so a `.ts`/`.mjs` config cannot rescue a sandboxed worker.
- Therefore the minimal clean fix is dispatch-side, not fixture-side: worker runs use `-s danger-full-access`. Acceptable here because every worker worktree is disposable, detached, external to the shared checkout, and reset to its baseline tag before reuse.
- `pnpm-workspace.yaml` (new, committed) records `onlyBuiltDependencies: [esbuild]` for pnpm 11 so `pnpm install` is deterministic in fresh worktrees. The pnpm 10-era package.json `onlyBuiltDependencies` field was verified ineffective and reverted.
- Stability baselines are launcher-only commits stacked on the real task baselines, verified by lineage: `benchmark-b1-stab` → `a92eb1d` (parent `5d600a5` + launcher files only; email defect present, B2/B3 fixes absent), `benchmark-b2-stab` → `a92eb1d` (parent `benchmark-b2-baseline`; revocation defect present), `benchmark-b3-stab` → `b676373` (parent `benchmark-b3-baseline`; expiry defect present). Deltas are exactly `pnpm-workspace.yaml` + `vitest.config.ts` in each case. The earlier mislabel `benchmark-b1-stab`/`benchmark-stablerun-base` pointing at `b676373` was deleted before any matched run used it.
- Harness: `scripts/run_matched_evaluation.sh` records start/end UTC, elapsed seconds spanning only the `codex exec` invocation (worktree creation, install, and parent verification are outside the window), route, model, sandbox, codex exit code, thread_id, and token usage. Codex exit is captured separately from wrapper status.
- Control note: packets pinned HEAD to the original baseline tags; the stab runs intentionally use the launcher-stability tags, so dispatch adds an identical operator-authorization addendum to both arms certifying worktree HEAD as the approved baseline. The addendum is identical text for both routes.

## Stabilized matched re-runs (2026-09-18)

All runs below: sandbox `danger-full-access`, one turn, zero failures/EPERM in transcripts, only owned paths changed, and independent parent verification (`test`, `typecheck`, `git diff --check` all exit 0, pipe-free exit capture). Elapsed is codex-exec-only wall clock. Usage is raw `turn.completed` token counts (input includes cached).

### B1 (email normalization) on `b1-stab` state

| Arm | Route | Elapsed | Input (cached) | Output (reasoning) | Thread |
|---|---|---|---|---|---|
| Luna | `openai-codex:gpt-5.6-luna` | 36s | 83,173 (70,400) | 1,166 (418) | `01a0b454-25f5-7270-9122-847f65ffebc1` |
| Terra | `openai-codex:gpt-5.6-terra` | 38s | 110,023 (99,840) | 1,135 (276) | `01a0b457-b093-7590-9a65-6a18a36df5b5` |

Artifacts `b1-luna-stab.jsonl/.meta`, `b1-terra-stab.jsonl/.meta`. Caveat: these two predate the `codex_exit` field addition (harness v1) and were dispatched from `b676373`, which is launcher-correct for B1's owned path (email defect present, B1 scope unaffected). Both changed only `src/domain/email.ts` to `value.trim().toLowerCase()`.

### B2 (cross-layer revocation) — invalidated first round, then clean re-run

First round on `b2-stab` (dispatched before the operator-authorization addendum existed):
- Luna (`b2-luna-stab`, thread `01a0b459-e9d5-7723-b36d-056266ec28cd`, 38s): completed correctly but proceeded against a stale HEAD pin without authorization — a control violation as the packet then read. Excluded from strict metrics.
- Terra (`b2-terra-stab`, thread `01a0b45a-8b2c-7482-896f-4603644b39b4`, 24s): refused to edit and blocked on the HEAD/tag mismatch. Zero changed paths. Excluded (blocked, not failure).
Both transcripts are retained as evidence that baseline-pin discipline is observable from inside the worker.

Clean re-run with identical authorization addendum on fresh worktrees `b2-luna-stab2` / `b2-terra-stab2` (both `a92eb1d`):

| Arm | Route | Elapsed | Input (cached) | Output (reasoning) | Thread |
|---|---|---|---|---|---|
| Luna | `openai-codex:gpt-5.6-luna` | 52s | 77,937 (58,368) | 1,095 (297) | `01a0b465-7277-7a22-bb71-697b3d1707c7` |
| Terra | `openai-codex:gpt-5.6-terra` | 41s | 113,819 (91,648) | 1,312 (236) | `01a0b466-5e0a-7c53-9245-3d852b05853e` |

Both changed exactly `src/domain/access-grant.ts` + `src/services/access-service.ts`; presenter untouched; original grants immutable. Behavioral difference worth recording (not scored): Terra delegated service revocation to the domain `revokeGrant`, while Luna duplicated the spread literal in the service — Terra's diff shows slightly stronger contract propagation.

### B3 (expiry propagation) on `b3-stab`

| Arm | Route | Elapsed | Input (cached) | Output (reasoning) | Thread |
|---|---|---|---|---|---|
| Luna | `openai-codex:gpt-5.6-luna` | 38s | 87,817 (71,424) | 1,107 (138) | `01a0b468-3535-7840-ba5b-c5332d54a7c9` |
| Terra | `openai-codex:gpt-5.6-terra` | 36s | 77,402 (57,344) | 1,287 (390) | `01a0b469-162b-7ac3-bbd3-f0dea40104af` |

Byte-identical diffs in both arms (`canAccessAt` and `presentAccessAt` now call `isGrantActiveAt(grant, at)`); domain helper already correct so only service/API changed. Independently verified.

### Reading of the stabilized set

Six clean matched arms across B1/B2/B3 now exist with normalized capture and zero environment noise. Wall-clock and token figures are single-sample, warm-cache-contaminated, and not yet aggregated into any speed/cost/quality claim; n=1 per cell is far too small. Correctness/scope discipline held for both routes in every stabilized run.

## Next benchmark requirement

1. Repeat stabilized B1–B3 arms across several randomized dispatch orders to build n>1 cells before any timing/cost comparison, and normalize cache state (dispatch idle before each arm, or subtract cached tokens explicitly).
2. ~~Design B4 where the domain layer is intentionally incomplete~~ — superseded: B4 family pivoted to the ECS-monolith architecture benchmark (see next section); contract-synthesis B-task remains open as B5 candidate.
3. Keep the operator-authorization addendum text under version control (currently only embedded in the harness script).

**Per-dimension results** (rubric max in parentheses; audit text only; clean-stop gate passed by both):

| Dimension | Luna | Terra | Notes |
|---|---|---|---|
| 1. State coverage (15) | 15 | 15 | both classify all 15 lets + `monsters` (grep-verified against source) |
| 2. Function coverage (10) | 10 | 10 | all 24 `function` defs mapped in both, plus exports/closures |
| 3. Hidden couplings (12) | 12 | 12 | all six required present with line-range evidence in both (24 vs 30 citations) — dimension saturated |
| 4. Not-ECS judgment (15) | 15 | 15 | both reject ECS for persistence, HUD, event queue, RNG with explicit reasons; no blanket-component failure |
| 5. Dependency graph (10) | 10 | 10 | edge-checked programmatically: Luna 27 edges, Terra 29, both acyclic, zero edges into `main` |
| 6. Ownership/mutation contract (10) | 10 | 10 | both choose controlled direct mutation over command queues, justified by observable RNG/log ordering |
| 7. Migration order (8) | 8 | 8 | both slice per-extraction with suite-green gates and name the unedited oracle |
| 8. Quirk discipline (8) | 8 | 8 | drift, double-drop, re-equip all treat-as-preserve in both |
| 9. Clean stop (7) | 7 | 7 | parent-verified: empty porcelain, `diff --check` 0, 21/21, typecheck 0; no untracked src/tests files |
| 10. Line budget (5) | 5 | 5 | both state the 120-line cap and sub-80 bootstrap explicitly |
| **Total (100)** | **100** | **100** | |

## B4-A0 — ECS monolith architecture audit (2026-09-18)

First task testing the framework's missing "judge" component: audit/plan quality on a real monolith, not isolated repair. Motivated by the user's Gemini-refactoring research prompt, corrected per framework rules (see PROGRESS).

**Fixture**: `fixtures/ecs-monolith-ts` — synthetic 498-line coupled game loop ("Ventralis": 15 module-level `let` bindings + exported `monsters`, seeded LCG with order-dependent draws, ordered 6-phase tick, gated persistence boundary, debug/HUD string contract, 8 planted legacy quirks pinned by a 21-test characterization suite; 21/21 green at freeze). Baseline tag `benchmark-ecs-baseline`; packet on top. Explicitly a proxy, not an Echoes of Aion refactor (Aion has no `main.ts` monolith — verified by search; largest Aion files are already modular domain/resolver files).

**Runs** (audit-only; dispatch order Luna→Terra, not randomized — single pair, qualitative only):

| Arm | Route | Elapsed | Input (cached) | Output (reasoning) | Thread | Parent verify |
|---|---|---|---|---|---|---|
| Luna | `openai-codex:gpt-5.6-luna` | 95s | 75,128 (53,504) | 4,473 (158) | `01a0b490-1418-7d01-b0b9-841197a1be48` | clean |
| Terra | `openai-codex:gpt-5.6-terra` | 105s | 78,542 (39,168) | 5,139 (762) | `01a0b4bb-ab4d-74d2-8924-72c9391a0558` | clean |

Both: `codex_exit=0`, one `turn.completed`, zero error/EPERM records; independently verified parent-side — `git status --porcelain` empty (no edits, no untracked files under `src`/`tests`), `git diff --check` exit 0, characterization 21/21, typecheck exit 0. Artifacts: `b4-{luna,terra}-audit-artifact.md` (final assistant messages extracted from JSONL; workers self-reported thread IDs as "not visible", harness capture is the route evidence).

**Rubric scores** (`rubrics/B4-ecs-audit-rubric.md`, graded on final text only): Luna 100, Terra 100 — 10/10 dimensions each, verified mechanically (all 15 lets + `monsters` classified; all 24 functions mapped; all six required hidden couplings cited with line ranges; both graphs edge-checked acyclic with bootstrap at the root and nothing depending on `main.ts`; both explicitly rejected ECS for persistence/HUD/event-queue/RNG with reasons; both chose controlled direct mutation over command queues, justified by observable ordering; both treat every quirk as preserve-not-fix; both name the suite as uneditable oracle).

**Discrimination found outside the scored dimensions**: Terra's coupling register has 20 entries vs Luna's 12. Terra additionally caught four "tempting-fix-is-a-trap" behaviors with line evidence: unused `MonsterInstance.attack` field (tick hardcodes per-kind damage), due-event matching is equality-only (`=== tickCount`; `<=` or a priority queue would change semantics), `restore` appends its log entry at the restored tick, and `resetGame` deliberately leaves `worldRef` intact. Luna's register is correct but covers only the rubric-required set plus tick order, snapshot asymmetry, and a few others. Terra's tree is finer-grained (33 files vs 21), splitting types/defs per domain.

**Rubric gap learned**: six required couplings are too easy to satisfy — both arms saturated. Before any scored repeat, add the four extra traps to the dimension-3 checklist and consider a dimension for false-positive risk (proposals that would break pinned behavior). Record as: B4-A0 at n=1 per arm is qualitative evidence that BOTH arms can produce an owner-approvable migration plan; it supports no superiority claim, and the register-depth difference needs n>1 in randomized order before it means anything.

## B4-A1 — foundation extraction, execution slice (2026-09-18)

Packet `fixtures/ecs-monolith-ts/tasks/B4-A1-foundation-extraction.md`, committed at `d718eca`. Per the design correction, A1 is explicitly labeled an **execution benchmark**: owner-provided canonical target tree + explicit owned paths, because comparability mattered more here than re-testing architecture judgment (A0 covered that). Slice: types, definitions, player component shapes, `GameSession` state container, inventory + crafting systems; persistence/debug/tick/combat/input explicitly NOT migrated. `grep -c '^let ' src/main.ts` must reach 0 (no parallel mutable state). Dispatch order Terra→Luna (not randomized; single pair), identical packet, separate fresh worktrees at `d718eca`.

| Arm | Route | Elapsed | Input (cached) | Output (reasoning) | Thread |
|---|---|---|---|---|---|
| Terra | `openai-codex:gpt-5.6-terra` | 176s | 206,670 (184,320) | 8,416 (648) | `01a0b4d5-79e9-76c1-9bbb-43e7da76993b` |
| Luna | `openai-codex:gpt-5.6-luna` | 147s | 229,384 (206,592) | 7,202 (326) | `01a0b4d8-8416-7ed0-930c-9d8836a42a01` |

Both: codex_exit=0, one `turn.completed`, zero error/EPERM records.

**Parent verification (both worktrees, all exit 0)**: characterization 21/21 with `tests/` untouched (`git status --porcelain tests` empty after diff-harness cleanup); `git diff --check` clean; changed paths exactly `M src/main.ts` + the six owned new files (enumerated via `git ls-files --others`, since porcelain directory-collapses untracked dirs); forbidden drift on tests/configs/tasks/docs = 0; components files contain interfaces + pure default factories only; no `ventralis:save`/`debugDump`/`savedAtTick`/tick logic leaked into new files; nothing imports `main` (dependency direction clean).

**Frozen differential harness** (`fixtures/diff-tests/a1-diff.test.ts`, parent-side, never dispatched): 6 scripted scenarios exercising every named trap — mirror-vs-inventory drift, ration secret wood, torch `attackBonus`/`torchBuffTicks` side effects, seeded RNG draws (seed 7 miss/hit/kill + stone double-drop), restore/save-counter semantics, equality-only scheduled events, KeyH panel-before-re-equip, death-freezes-actions-continues-tick, snapshot key set and `log.slice(-20)` truncation. Baseline JSON captured pre-dispatch at `d718eca` (`b4a1-baseline-diff.json`). **Both migrated worktrees produce byte-identical differential output to the baseline.** Passing characterization + differential both held — the differential was what covered snapshot-shape and ordering cases the 21 tests don't pin.

**Structural quality notes (owner-graded, not scored)**: Terra produced conventional layout (main.ts 79 lines, max line 491 chars; session 29 lines). Luna produced 24 physical lines with a 1,103-char single-line `tick()` — formally satisfies the 120-line cap while functionally gaming its intent (logic-cramming preserves line-count compliance). Luna passes `emit` as a callback parameter into systems (inverts the world-ownership story slightly); Terra's inventory component nests `{items:{...}}` where Luna flattened — invisible to behavior, both legal. Terra honestly reported "one procedural patch-format retry" under repairs; Luna reported none. Both self-reports match parent observations; deviation sections correctly report none.

**A1 coupling risks recorded (gates A2 packet design)**:
1. Line-count budget needs a companion line-length/format gate (prettier check or ≤120 cols) or Luna-style packing recurs.
2. `session` module-level singleton is shared mutable state both arms relied on; A2 must keep RNG consumption order inside it exact — combat extraction is the first slice that moves RNG call sites between files.
3. `monsters` live-array export identity: both arms aliased `export const monsters = session.monsters`; A2 combat code must keep mutating the same array (shift/push), not reassign.
4. Snapshot field reads currently live in `main.ts` in both trees; A3's persistence-adapter migration must preserve key order and omissions (`pendingEvents`, `saveCounter`, `worldRef` excluded; `log.slice(-20)`).
5. Diff harness must be re-frozen per slice from the post-A1 state (A1 trees differ structurally from baseline; A2 differential compares each arm against its own A1 parent).

Do not begin A2 (combat extraction) until these are reflected in the packet.

## B4-A2 — combat extraction, execution slice (2026-09-18)

Packet `fixtures/ecs-monolith-ts/tasks/B4-A2-combat-extraction.md` (master commit `100f7c2`). Execution/comparability slice per the A1 design: owner-specified combat surface (monster defs, roll/attackRoll, attack, spawn, equip, eat), owned paths limited to `src/systems/combat-system.ts` (+ optional component/type files) and `main.ts`; all A1 files explicitly off-limits. Persistence, HUD/input, event-queue semantics, and tick-loop restructuring forbidden. **RNG-consumption-order preservation and `session.monsters` live-array identity (no reassign/copy) written as hard failures, not review notes.** Structural gates per A1 risk list: ≤120 lines per migrated file, ≤120 columns on authored/moved lines (untouched pre-existing long lines must stay untouched and be reported), no imports of `main` from lower modules.

**Per-arm parent baselines** (not a shared oracle): worktrees `b4a2-luna`@`55830d4`, `b4a2-terra`@`7aae81f` (each arm's own post-A1 commit), packet frozen as commit on top (`a6912c7` / `c3cc82c`). A2 differential harness `fixtures/diff-tests/a2-diff.test.ts` (parent-side, never dispatched) runs 8 scenarios: live-array identity across spawn/kill/restore (`expect(m.monsters).toBe(ref)`), seed-42 attack sequence, torch-bonus combat with stone double-drop, multi-spawn order + shift-removal, death gating (eat/equip/attack after `alive=false`), crawler cadence + equality-only event firing, mixed 20-tick sequence through every RNG consumer, restore path. Captured per arm pre-dispatch (`b4a2-luna-parent-diff.json`, `b4a2-terra-parent-diff.json`).

Dispatch order: Luna→Terra (single pair; recorded, no timing/token claims).

| Arm | Route | Elapsed | Input (cached) | Output (reasoning) | Thread |
|---|---|---|---|---|---|
| Luna | `openai-codex:gpt-5.6-luna` | 126s | 216,833 (199,424) | 5,450 (786) | `01a0b4f3-3c29-73c3-b68b-a6f93580634f` |
| Terra | `openai-codex:gpt-5.6-terra` | 170s | 406,078 (375,040) | 7,538 (1,660) | `01a0b4f5-53ce-7ee0-92c3-40945d5faab4` |

Both: codex_exit=0, one `turn.completed`, zero error/EPERM records.

**Parent verification — both arms, all pass**: characterization 21/21 with `tests/` byte-untouched; typecheck exit 0; `git diff --check` exit 0; changed paths exactly `M src/main.ts` + `src/systems/combat-system.ts` (nothing else; no component/type files needed); **A2 differential byte-identical to each arm's own A1 parent baseline** (`da4fd55f…` both sides, 9,002 chars — identical across arms too, so the two structurally different trees still produce one behavior); combat system imports only `types/game` + `runtime/session` (zero refs to `main`); authored lines ≤120 cols in both arms' new files and in every line either touched in `main.ts` (Luna max authored 120, new file max 87; Terra max authored 110, new file max 105).

**Line-length gate closed the A1 loophole**: Luna's post-A1 main.ts had a 1,103-col tick line it was told not to reformat; it left untouched and reported "7 pre-existing overlong lines"; its authored code is properly wrapped (combat-system 65 lines). No logic-cramming recurrence.

**Self-reports vs parent observations**: both report "Intentional deviations: none" and scope drift none — matches. Luna reports "2 patch attempts; corrected one failed line-check probe"; Terra reports one implementation pass plus repairs to two glue lines and one PowerShell verification error — both transparent, neither hides a code failure. Terra's report is more granular (per-trap file/line narrative, exact porcelain/ls-files output reproduced); Luna's is adequate but terser (thread ID "not visible" — expected; it can't see its own envelope).

Result branches: `a2/luna` → `4e21339`, `a2/terra` → `1d2e2b6` (each on its arm's A2 packet commit).

**A2 risks noted for A3 (persistence adapter)**: (1) snapshot field reads + key order + `log.slice(-20)` still live in `main.ts` in both trees — A3 must move them preserving exact JSON key emission order; (2) `decideUseStorage` gating and `savedAtTick`/`saveCounter` merge in the save payload are pin-critical; (3) restore's `monsters.length = 0` push-pattern preserves live-array identity — A3 must not "clean" it into reassignment; (4) re-freeze diff harness per arm from post-A2 state.

Gate satisfied: both A2 outputs pass their own parent differential oracle. A3 may proceed.

## B4-A3 — persistence adapter extraction, execution slice (2026-09-18)

Packet `fixtures/ecs-monolith-ts/tasks/B4-A3-persistence-extraction.md` (master commit `979291b`). Owned paths: `src/systems/persistence-system.ts` (+ optional `types/persistence.ts`, unused by both) and `main.ts`. Migrated surface: `snapshot`, `restore`, `decideUseStorage`/gating, save payload construction with `savedAtTick`/`saveCounter`. Pin list written as hard failures: snapshot key order + omissions (`pendingEvents`/`saveCounter`/`worldRef`), `log.slice(-20)`, restore's `monsters.length = 0` + push identity pattern, restored-tick log attribution, init-direct-restore vs gated-save asymmetry (do not unify), counter increment only on gated tick%10 writes, zero RNG consumption in persistence paths, type-coercion shape preserved (no new validation/defaults). The single sanctioned `tick()` edit: replace the inline save block with a call at the same point, same guards, phase order untouched.

**Per-arm parents and frozen baselines**: `b4a3-luna`@`4e21339`, `b4a3-terra`@`1d2e2b6`, packet commits on top (`5d33efe`/`e640967`). Harness `fixtures/diff-tests/a3-diff.test.ts` (parent-side, 13 scenarios — storage absent, gated saves at ticks 10/20, key-order verbatim, log truncation at 20, events survive restore untouched, array identity via `expect(m.monsters).toBe(ref)` across double restore, restored-tick attribution, RNG neutrality across snapshot/restore/save, empty-string key skipped without throw, malformed key must THROW (no defaulting), single-save payload, malformed-present init throw, mixed post-restore behavioral run). Pre-dispatch capture hit a harness bug (S11 used a `{tickCount:0}` payload → restore's `d.monsters.map` threw); fixed scenario, re-froze both baselines: 4,778 bytes each, 13 keys, byte-identical across arms — confirming both A2 trees still emit one behavior. Baselines: `b4a3-luna-parent-diff.json`, `b4a3-terra-parent-diff.json`.

Dispatch order: Luna→Terra (single pair; no timing/token claims).

| Arm | Route | Elapsed | Input (cached) | Output (reasoning) | Thread |
|---|---|---|---|---|---|
| Luna | `openai-codex:gpt-5.6-luna` | 126s | 298,486 (273,408) | 5,225 (1,113) | `01a0b516-7abd-7fc0-96d4-cde5bbede828` |
| Terra | `openai-codex:gpt-5.6-terra` | 116s | 280,680 (259,072) | 4,915 (1,315) | `01a0b518-7f29-7142-be47-3987b4c9de15` |

Both: codex_exit=0, one `turn.completed`, zero error/EPERM records.

**Parent verification — both arms, all gates pass**: characterization 21/21, `tests/` byte-untouched; typecheck exit 0; `git diff --check` exit 0; changed paths exactly `M src/main.ts` + `src/systems/persistence-system.ts`; **A3 differential byte-identical to each arm's own A2-parent baseline** (`8d23e1adf85f`, 4,778 bytes both sides, both arms); persistence module imports only `runtime/session` + `types/game` — zero refs to `main`; migrated files ≤120 lines (Luna 38/max 95 cols, Terra 55/max 104); zero added `main.ts` lines over 120 cols in either diff.

**Self-reports vs parent**: both "Intentional deviations: none", scope-drift none — matches. Luna discloses one PowerShell interpolation fix in its line-length proof. Terra discloses more honestly: an actual first-run test failure (extracted restore needed the `say` callback when invoked via `api.restore`) repaired with a minimal `main.ts` bootstrap wrapper, plus the same probe fix — parent state confirms the repair landed inside owned paths. Design note: Terra keeps a `say` callback injected from `main` (same pattern as its A2 emit), Luna's persistence calls `session.say` directly — invisible to behavior, both legal under the packet.

Result branches: `a3/luna` → `872f430`, `a3/terra` → `c0401a7`.

**A3 risks/gates for A4 (tick-loop reduction)**: A4 is the loop-ownership slice: move tick phases into ordered systems with exact phase ordering (starvation → buff decrement → due-events equality match → removal filter → monster cadence → %20+parity spawn roll → gated save at same point), `===` event semantics preserved, input/HUD ordering (`dump` before re-equip), and save-call placement load-bearing. Final-state dumps are insufficient — A4 needs a **per-tick trace oracle** (emit/log sequence at every tick, not just end state). Re-freeze traces per arm from post-A3 state before dispatch. Do not begin A4 until the trace harness is written and baselines captured.

## B4-A4 — ordered tick-loop extraction, execution slice (2026-09-18)

Packet `fixtures/ecs-monolith-ts/tasks/B4-A4-tick-loop-extraction.md` (master commit `db804e1`). Trace oracle built and frozen BEFORE dispatch, per the A3 gate. Owned paths: `src/main.ts`, new files under `src/systems/` (optional shared types under `src/types/`, unused by both). Eight required phase orderings (increment → starvation → buff decrement → `===` due-selection → event apply + `!==` removal → monster damage in array order → `%20` + log-parity gated spawn draw → gated save at existing position) written into the packet as the contract; event-queue redesign, scheduler introduction, RNG ownership changes, save reordering, live-array copies, and any log/emit string change listed as hard failures. Tests, configs, session, components, and all existing systems read-only.

**Trace oracle** (`fixtures/diff-tests/a4-trace.test.ts`, parent-side, never dispatched): records after EVERY tick — tick number, that tick's output entries in order, full log tail with tick/message fields, hp/alive, monster kinds+order+hp, pending-event count, rngState, saveCounter, storage contents + write count, dump string. Eleven ordering-exposing scenarios: same-tick starvation+buff, event+monster+death on one tick, crawler/stalker cadence mix, %20 spawn under BOTH parity outcomes (t4a fires draw, t4b skips it), gated saves at 10/20 alongside events+monsters (valid parent-produced payload only — A3's synthetic-fixture lesson applied), past/current/future event timing, death then attempted actions, seeded attack draw sequence, restore→ticks→save, long mixed input/tick run. Per-arm baselines frozen from post-A3 parents (`b4a4-luna`@`872f430`, `b4a4-terra`@`c0401a7`, packet commits `39f0ccb`/`8bfa4bf`): 95,742 bytes each, 11 keys, valid JSON, worktrees clean after capture, byte-identical across arms.

Dispatch order: Luna→Terra (single pair; no timing/token claims).

| Arm | Route | Elapsed | Input (cached) | Output (reasoning) | Thread |
|---|---|---|---|---|---|
| Luna | `openai-codex:gpt-5.6-luna` | 84s | 205,556 (163,584) | 3,287 (423) | `01a0b520-0c58-7f93-b4c5-16b71854faef` |
| Terra | `openai-codex:gpt-5.6-terra` | 123s | 231,883 (205,312) | 4,496 (664) | `01a0b521-7255-7611-a718-cebeece02ce9` |

Both: codex_exit=0, one `turn.completed`, zero error/EPERM records.

**Parent verification — both arms, all gates pass; judged by trace equivalence, not dump equality**: characterization 21/21, `tests/` byte-untouched; typecheck exit 0; `git diff --check` exit 0; changed paths exactly `M src/main.ts` + `src/systems/tick-system.ts`; **per-tick trace byte-identical to each arm's own A3-parent baseline** (`466b4ad6e03d`, 95,742 bytes, both arms both sides — 160 traced tick records across 11 scenarios reproduced exactly); `tick-system.ts` 50 lines/max 88 cols (Luna) and 74/86 (Terra) — both ≤120/≤120; zero added `main.ts` lines over 120 cols; untouched pre-existing long lines reported and left alone (4 Luna, 2 Terra); tick-system imports only `session` + `combat-system` + `persistence-system` — zero refs to `main`, no cycle (persistence does not import tick); no shared type files needed.

**Self-reports vs parent**: both list the exact phase order and where each trap lives; both report "Intentional deviations: none", scope drift none — matches. Luna discloses a probe-command fix (attempt 2 was the PowerShell line-proof again, same as A3); Terra reports one pass plus one self-initiated structural refinement "to make the ordered phases explicit". Luna's tick-system keeps the `%20`+parity gate and draw inside its module and calls `saveIfDue()`; Terra's calls `persist()` — both place the save after phase 7 per contract; traces confirm equivalence either way.

Result branches: `a4/luna` → `0b96d1f`, `a4/terra` → `e94698d`.

## B4 ladder — completion verdict (2026-09-18)

A0 (judged audit) + A1–A4 (execution slices, each judged by per-arm parent differential; A4 by per-tick trace). All four execution slices: 8/8 arm-runs clean (codex_exit=0, one `turn.completed`, zero errors), 8/8 parent-verified with characterization 21/21, tests untouched, owned-path compliance, all structural gates, and byte-identical differentials at every step. Both arms carried the same coupled monolith from 498 lines to a layered tree (Luna final main.ts: 18 lines; Terra: 67) through foundation → combat → persistence → tick-loop with zero behavioral drift across ~105k bytes of frozen trace evidence per arm.

**Honest limits (ladder round 1)**: single pair per slice; per-slice dispatch orders A0 Luna→Terra; A1 Terra→Luna; A2 Luna→Terra; A3 Luna→Terra; A4 Luna→Terra. elapsed/token columns are recorded envelope facts, not ranked claims; A1's line-width lesson and A3's fixture lesson came from parent-side fixes, not worker failures. The evidence supports: both models execute owner-specified behavior-preserving extraction slices against a differential oracle with equal reliability at n=1 per slice. It does NOT support superiority claims of any kind. The A0 register-depth question was then taken up by the randomized-repeat track below.

## B4-A0 randomized-repeat track (rubric v2, n=3 per arm, 2026-09-18)

Design per ladder-recorded open question: dimension 3 expanded to the 10 planted traps (a–j), new dimension 11 for false-positive risk, total rebalanced to 100 (`rubrics/B4-ecs-audit-rubric-v2.md`, never inside a worktree — verified absent in all six). Same frozen packet commit `727609c` in all six fresh worktrees (packet/tests/src byte-identical: sha1 prefixes `a60ae705 b2d2419a 04aa547b`). Seed 1238626264; all three seeded draws came up Terra→Luna, so dispatch order was randomized by seed but NOT position-balanced — order confounding is reduced vs the n=1 round (which was Luna→Terra) but not eliminated.

Artifacts: 6/6 valid (one `turn.completed` each, zero errors/EPERM, elapsed 82–107s, token envelopes in `b4-repeat-track/b4r-envelope.json`). One parent-side incident, no data loss: the first combined 6-run dispatch loop hit the harness tool timeout after round 2; no orphan worker survived (process sweep clean); round-3-Luna was re-dispatched alone with its own artifact path. Parent verification: all six worktrees zero src/tests/tasks dirt, characterization 21/21, typecheck 0, `git diff --check` 0 → dimension 9 = 7/7 for every run.

**Grading provenance (honest):** independent grading was attempted TWICE — one six-run grader and one two-batch three-run fan-out — and BOTH stalled past the 8-minute no-progress watchdog and were cancelled before formal delivery. The first stream had already emitted a complete scored block; after parent reconciliation it is adopted as **owner-side parent adjudication**, NOT independent-grader output (`b4-repeat-track/b4r-scores-parent-adjudicated.json` with provenance field). Reconciliation: per-dimension sums equal every total (6/6); scores agree with the corrected mechanical trap-citation checks (anchors at real baseline lines, incl. the fixed `e.at === tickCount` 319/329 anchor for trap h); parent false-positive scan found zero behavior-breaking proposals in all six — every `<=`/dedup/"correct"-it mention is a preserve-as-warning, which earns full dim-11 marks per rubric carve-out. Two minor adjudication artifacts preserved as-is (not smoothed): b4r1-luna dim3 16 vs 9 verified traps (−2), b4r3-luna dim3 8 vs 2 verified traps (+4); totals adopted unchanged.

Per-run scores (no cross-run averaging applied to the records themselves):

| Run | Arm | Total | Traps a–j verified |
|---|---|---:|---|
| b4r1-terra | Terra | 100 | 10/10 |
| b4r1-luna | Luna | 96 | 9/10 (miss j) |
| b4r2-terra | Terra | 98 | 9/10 (miss e) |
| b4r2-luna | Luna | 94 | 7/10 (miss e,g,j) |
| b4r3-terra | Terra | 100 | 10/10 |
| b4r3-luna | Luna | 80 | 2/10 (miss a,b,c,e,h,i,j) |

Aggregate summaries: Terra mean 99.3, median 100, range 2; Luna mean 90.0, median 94, range 16. Luna's variance is dominated by b4r3-luna (80, the thin artifact); Luna rounds 1–2 (96/94) are within Terra's range. Dependency graphs: all six parse acyclic with `main` root-only (b4r3-terra's apparent `persistence→main` was a parent-parser conflation of a labeled node, re-read verbatim and corrected).

**Conclusion (defensible wording):** the A0 artifact-quality spread from the n=1 round partially replicates — Terra detected all ten traps in 3/3 runs; Luna's completeness varied materially run-to-run (9→7→2 verified traps). But this is NOT a controlled model ranking: n=3, seed-drawn-but-unbalanced order (all Terra-first, opposite to the n=1 round, so any positional effect works against the observed spread rather than for it), parent-adjudicated rather than independent grading, and single-harness execution slices A1–A4 remain equally reliable at n=1 per slice. Suggested, not proven: register depth in open-judgment audits is noisier for Luna than Terra on this fixture; execution reliability under hard oracles showed no spread in either round.

Artifacts retained: `b4-repeat-track/` (manifest with SHA-256 of all 17 inputs: raw JSONL ×6, extracted finals ×6, envelope+seed/schedule, corrected trap-citation check, frozen baseline `main.ts`, rubric v2, packet, adjudicated scores). The six b4r* worktrees removed after recording; ladder result branches (`a1..a4/luna|terra`) and packet history untouched.

## B4 controlled-confirmation track (n=6/arm, 2026-09-18) — EXPLORATORY

Pre-registered in `b4-repeat-track/B4-CONFIRM-PROTOCOL.md`: six paired rounds on the frozen ECS-monolith fixture, order-balanced (rounds 1/3/5 Terra→Luna, 2/4/6 Luna→Terra), fresh worktrees, clean single-turn execution required for validity. Execution slices A1–A4 not rerun.

**Operational validity — 12/12.** Every run: exactly one `turn.completed`, codex_exit 0, thread id + token envelope captured, zero EPERM/orphan records. This is harness evidence only, not ranking.

**Mechanical characterization — 12/12 full marks.** All worktrees: zero source/test diffs, characterization suite 21/21, typecheck 0, `git diff --check` 0 → dim 9 = 7/7 every run; dim 1 (15/15 lets + monsters), dim 2 (26/26 functions), dim 5 (acyclic graph, main at leaves), dim 11 (zero false-positive "fix" proposals) all maxed.

**Blinded judgment grades (dims 4/6/7/8/10).** Six grader batches, two opaque artifacts each; mapping A–L → runs derived by full SHA-256 content-hash match (`b4c-blind-map.json`), not narrative: A=1-terra, B=1-luna, C=2-terra, D=2-luna, E=3-terra, F=3-luna, G=4-terra, H=4-luna, I=5-terra, J=5-luna, K=6-terra, L=6-luna. Raw batch JSONs with every quote preserved verbatim (`b4c-blind-grader-output.json`; cross-checked: 60 scores + 60 quotes identical to the final table). Rubric v2 weights for these dims are 12+7+7+7+2 = **35**; the dispatch brief's "33 pts" was an arithmetic error — reported at 35, nothing renormalized. Judgment means: Terra 34.0, Luna 34.17 — no separation. Only sub-max scores: G dim8=6 (secret ration wood lacks its own preserve statement), H dim6=6 (storage-ownership tension); dim10 double-credit only where the grader saw an explicit anti-cramming statement (A, F, J) — borderline variation across identical cap statements recorded, not smoothed.

**Dim 3 (hidden couplings) — parent-adjudicated, exploratory.** 120-cell sheet (`b4c-dim3-adjudication-sheet.json`): every trap × run has pass/fail + quoted passage + rationale against the frozen baseline sites. Terra [7,10,8,10,10,9] mean 9.0; Luna [7,7,9,8,8,8] mean 7.83. Luna has **two** runs ≤7 (b4c1, b4c2); Terra has one (b4c1). Hard traps g/h (two-hop mechanisms) detected 4/12 each. Label is honest: the scoring rule was frozen only after v1–v3 anchor/parser revisions made while seeing outputs; all versions and reasons archived in `b4-repeat-track/b4c-scoring-archive/`.

**Pre-registered decision rule → protocol label CONFIRMED.** Condition 1 (Luna ≥1 run ≤7): met, two runs. Condition 2 (order-stratified paired means differ): met — Terra−Luna gap +0.33 in Terra-first stratum ([7,8,10] vs [7,9,8]) vs +2.00 in Luna-first stratum ([10,10,9] vs [7,8,8]). Refutation condition (both arms ≥9 all runs) not met.

**Per-run full scores** (fixed mechanical 45 + 2×traps + judgment 35; all 12 recomputed from stored dims and reconciled): Terra [94,99,95,98,99,97] mean 97.0 median 97.5 range 5; Luna [93,93,98,94,96,95] mean 94.83 median 94.5 range 5. Per-run records are primary; aggregates are summaries (`b4c-final-scores.json`).

**Cautious interpretation (binding).** Exploratory confirmation under a revised scoring rule — not independent confirmatory evidence, not a model ranking. The reproduced signal is a small artifact-completeness gap, concentrated in the hidden-coupling register (dim-3 mean gap 1.17/20; full-score mean gap 2.17/100 with fully overlapping ranges), entangled with run order (the gap is 6× larger when Luna goes second), on author-written traps with n=6/arm and a shared grading procedure. No superiority claim is made; the conclusion is bounded to this judgment task on this fixture.

Artifacts: `b4c-blind/` (A–L), 12 `b4c{r}-{arm}-final.md` + transcripts, `b4c-dim3-adjudication-sheet.json`, `b4c-blind-grader-output.json`, `b4c-blind-map.json`, `b4c-final-scores.json`, `b4c-scoring-state.json`, protocol + `b4c-scoring-archive/` provenance chain — all SHA-256 listed in `b4-repeat-track/MANIFEST.json` (52 entries). The twelve b4c* worktrees (all zero-dirt, verified) removed after recording; ladder worktrees and result branches untouched.

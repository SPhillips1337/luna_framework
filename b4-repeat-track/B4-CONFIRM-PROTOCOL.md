# B4-A0 controlled-confirmation protocol (PRE-REGISTERED before dispatch, 2026-09-18)

Purpose: confirm or refute the suggestive repeat-track finding (Terra 3/3 full trap coverage
vs Luna 9/10, 7/10, 2/10) under a controlled design. Current conclusions stand unchanged
until this round completes. This file is committed BEFORE any worker dispatch.

## Inputs (frozen, identical to repeat track)
- Baseline: packet commit `727609c` in `fixtures/ecs-monolith-ts` (same 498-line monolith,
  same audit packet `tasks/B4-ecs-audit.md`, same characterization oracle).
- Rubric: `rubrics/B4-ecs-audit-rubric-v2.md` (11 dims, 100 pts; 10 traps a-j; dim 11 FP risk).
  Rubric NEVER inside a dispatch worktree (verify before dispatch).
- Arms: gpt-5.6-terra, gpt-5.6-luna via scripts/run_matched_evaluation.sh, same env as all prior rounds.

## Dispatch design
- 6 paired rounds (12 runs), fresh worktrees b4c{1..6}-{terra|luna}, independent run IDs.
- BALANCED order (explicit, not seed-drawn): rounds 1,3,5 Terra→Luna; rounds 2,4,6 Luna→Terra.
- One dispatch process at a time; per-run artifact b4c{r}-{arm}.jsonl; never overwrite.
- Envelope facts (elapsed, tokens, thread id) recorded per run as NON-RANKING metadata.
- If a dispatch harness times out: process sweep for orphans, verify artifact integrity,
  re-dispatch only missing/incomplete runs on their own artifact paths.

## Pre-registered scoring procedure
Mechanical (parent, computed, not judged):
- dim 1 (12): state-table coverage vs the 15 lets + exported monsters (grep-enumerated).
- dim 2 (8): function coverage vs the 26 top-level functions; TODO/unknown = 0.
- dim 3 (20): traps a-j, 2 pts each, named AND citation within ±3 lines of REAL baseline
  anchors (corrected anchor set incl. e.at === tickCount at 319/329).
- dim 5 (8): graph parsed from artifact: present, acyclic, no edge into main from lower layers.
- dim 9 (7): clean-stop gates verified on the worktree after the run.
- dim 11 (10): FP scan for actual change-direction proposals vs preserve-as-warning;
  warnings earn full marks; only real break-pinned-behavior proposals cap at 2.
Judgment (bounded grader, per small batch of at most 2 artifacts, strict idle timeout):
- dims 4, 6, 7, 8, 10 (33 pts): not-ECS reasons, ownership contract, migration order,
  quirk discipline, line-budget intent. Grader must return per-run per-dim scores + 1-line notes.
Fallback rule: if a grader batch fails (cancelled/stalled), the OWNER scores those dims with
explicit per-dim notes, and those runs are labeled "parent-scored judgment dims" separately
from grader-scored runs. No silent mixing.

## Analysis (fixed before seeing results)
- Per-run scores preserved; aggregates = mean/median/range per arm; per-trap detection rates.
- ORDER-STRATIFIED comparison: Terra-first rounds vs Luna-first rounds, reported separately.
- Pre-registered decision rule: the suggestive finding is CONFIRMED only if Luna has at least
  one run with traps_verified <= 7 AND order-stratified means differ; it is REFUTED if both
  arms show >=9 traps in all 6 runs (no spread difference). Anything between = inconclusive.
- Execution slices A1–A4 NOT rerun (n=1 claim already documented; goal unchanged).

## Honest limits this design does NOT remove
n=6/arm still small; same fixture, same author-written traps; single harness; grader fallback
(if triggered) weakens independence; conclusions remain about THIS judgment task on THIS fixture.

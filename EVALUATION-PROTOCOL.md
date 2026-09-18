# Luna/Terra Evaluation Protocol

## Purpose

This protocol produces comparable evidence about model-routed engineering work. It is designed to test a workflow, not to manufacture a favorable result for a particular model.

## Required controls

### 1. Common starting point

Use the same repository snapshot for every worker. Prefer a committed benchmark fixture baseline with a known failing or incomplete objective. Record the commit ID and verify the baseline independently before starting either run.

### 2. Isolated matching worktrees

Create equivalent isolated worktrees from the same baseline. Do not let one worker inherit the other's changes, generated artifacts, caches, or lessons unless that transfer is part of the experiment.

### 3. Identical task packet

Use the same objective, constraints, owned paths, required reading, acceptance criteria, and verification commands. Route-specific instructions may explain the selected model, but must not change the engineering task.

### 4. Explicit route capture

Record the resolved model, provider, session/run ID, and route-selection reason. If identity is not observable, mark the result unverified and exclude it from strict model comparison.

### 5. Independent verification

The owner or an independent verifier must inspect the actual diff and rerun the relevant checks. Worker self-report is not acceptance evidence. For runtime work, verify the live result and state readback separately from automated tests.

### 6. Scope and preservation checks

Record pre-existing dirty paths, protected artifacts, generated files, and forbidden operations. Verify that the worker changed only owned paths and preserved unrelated work.

## Normalized metrics

| Metric | Definition |
|---|---|
| Attempts | Number of implementation cycles. |
| Repairs | Focused corrections after a failure or review finding. |
| Changed paths | Files actually changed, compared with owned paths. |
| Scope drift | Unauthorized path or behavior changes. |
| Command results | Exact tests, typechecks, builds, and structural/runtime checks with exit codes. |
| Owner corrections | Changes or interventions required during independent review. |
| Elapsed time | Wall-clock duration only when timestamps and environment make it trustworthy. |
| Route confidence | Explicit, partially observed, or unavailable. |
| Outcome | Passed, failed, blocked, or incomplete. |

## Routing hypothesis to test

- **Luna default:** bounded, low-blast-radius, one- or few-file work with established contracts.
- **Terra:** public contracts, cross-module changes, unfamiliar legacy boundaries, architecture work, or a Luna task after two materially unsuccessful repairs.
- **Break-glass:** unresolved Terra failure or architecture/design ambiguity requiring a diagnostic pass.

These are candidate routing rules, not conclusions. Update them only from repeated, matched evidence.

## Evaluation procedure

1. Define the benchmark objective and acceptance tests.
2. Prepare and commit the fixture baseline.
3. Verify the same failing/incomplete baseline in isolated worktrees.
4. Give Luna and Terra identical task packets.
5. Capture routes and execution evidence durably.
6. Permit only the defined repair/escalation policy.
7. Inspect actual diffs for scope, contract fidelity, and preservation.
8. Run independent verification in each worktree.
9. Normalize metrics into `RESULTS.md`.
10. Record limitations and do not infer superiority from unmatched or route-uncertain runs.

## Echoes of Aion pilot status

The Echoes of Aion diplomacy/turn-resolution pilot is **Exploratory**, not a valid matched benchmark comparison. It contains two explicit Luna datapoints and one explicit Terra production-tooling datapoint, but the tasks were not equivalent in objective, scope, or artifact type. One delegated route was also unavailable. The pilot is valuable for designing this protocol and the supporting architecture layer; it must not be used to claim model superiority.

## Execution lessons from the controlled fixture

- Make baseline tags non-self-referential. Prefer a tag whose commit is verified independently rather than embedding a future commit hash in the task packet.
- Create worktrees only after the final packet and control metadata commit. Preserve earlier run artifacts, but exclude them from strict matched metrics if controls changed afterward.
- Record the route from explicit dispatch, for example `openai-codex:gpt-5.6-luna` or `openai-codex:gpt-5.6-terra`. Worker runtime metadata may report the route or session as unavailable; do not upgrade that self-report into resolved route evidence.
- Independently rerun focused tests outside the worker process when worker Vitest/Vite execution hits Windows `spawn EPERM`. Record the worker failure as environment evidence, not as an implementation retry. (Resolved 2026-09-18: the EPERM is the Codex `workspace-write` sandbox blocking Node child-process spawns; stabilized dispatch uses `danger-full-access` on disposable external worktrees, with launcher-only baseline commits identical for both arms. This infrastructure must never appear in a worker solution diff and is recorded in `RESULTS.md`.)
- Route identity is the explicit dispatch (`openai-codex:gpt-5.6-luna` / `openai-codex:gpt-5.6-terra`) plus the JSONL `thread_id`. The agent orchestrating dispatch may run on a different model than the workers; recorded worker runs keep their dispatched model labels and must never be retroactively relabeled. Any future non-GPT worker family is a separate, clearly named evaluation.
- Elapsed time must span only the model invocation (the harness times just the `codex exec` call; worktree creation, install, and parent verification sit outside the window). Never compare parent-shell timings with worker-dispatch timings.
- Do not collect timing or cost comparisons until launcher behavior and Windows child-process execution are stable and timestamps are captured consistently.
- Distinguish the intended task shape from the realized repair. A multi-module task may have a correct pre-existing domain helper and require only propagation changes.

## Minimum benchmark requirement

Before drawing a Luna/Terra routing conclusion, run at least one committed fixture family with:

- Identical baseline and isolated worktrees
- Identical task variants and acceptance criteria
- Explicit route capture
- Independent verification
- Normalized metrics and owner review

# Luna Framework Brief

## Origin and design thesis

The original idea came from a Gemini analysis of model fit rather than from a desire to build a generic agent harness. That analysis suggested a practical division of labor:

- `GPT-5.6 Luna` is well suited to narrow, small, file-scoped changes with a fast test-and-feedback loop.
- `GPT-5.6 Terra` is better suited to larger codebases, cross-module dependencies, architectural changes, and more complex refactors.
- Higher-reasoning models such as Sol or Astra should be reserved for system resets, deep stagnation, or break-glass architectural diagnosis.

The resulting project idea is a supporting framework for that workflow. It should decompose larger engineering objectives into smaller components that Luna can safely understand and edit, while maintaining enough shared architecture for the whole system to remain coherent.

The framework therefore needs more than task prompts. It needs a lightweight but durable model of the larger codebase, including:

- A system spine describing major subsystems, boundaries, data flow, and ownership.
- A glossary defining domain terms, identifiers, events, actions, and important contracts.
- Component briefs that isolate work into narrow, verifiable slices.
- Source-anchored links from architecture concepts to files, symbols, tests, and decisions.
- A routing policy that chooses Luna, Terra, or a break-glass model based on task complexity and failure evidence.
- Feedback loops that use tests and structural checks to make small changes safe.

This is a cost-per-diff and context-management strategy: use the least expensive model that can reliably complete the current slice, and spend deeper reasoning only where architectural context or repeated failure justifies it.

## Research-to-evaluation history

The framework concept was developed in stages:

1. A Gemini analysis proposed a model-fit distinction: Luna for small, routine, file-scoped changes; Terra for larger codebases and complex cross-module work; stronger models for break-glass recovery.
2. Follow-up research used web search and GitHub discovery to investigate the surrounding repository-intelligence tooling category.
3. Projects such as `rag-rat` and `srclight` showed that repository indexing, symbol navigation, dependency graphs, impact preflight, semantic search, Git history, source-anchored memory, and MCP access could form a reusable support layer for coding agents.
4. The design then shifted from model selection alone toward a project that supplies the right task decomposition and architectural context to each model tier.
5. Echoes of Aion was selected as the evaluation candidate because it is a mature, complex, server-authoritative codebase with meaningful subsystem boundaries, explicit contracts, deterministic tests, and enough cross-module behavior to expose navigation and architecture mistakes without requiring a repository-wide rewrite.
6. A bounded Luna/Terra pilot was run against the diplomacy and turn-resolution boundary, using task packets, generated architecture metadata, contract notes, focused tests, typechecks, boundary checks, and independent reruns.

The primary evaluation ledger is:

`C:\Users\steph\Documents\development\EchoesOfAion\.agent\evaluations\2026-09-luna-terra-pilot.md`

The implementation plan is:

`C:\Users\steph\Documents\development\EchoesOfAion\.hermes\plans\2026-09-16_140000-agent-legible-architecture-pilot.md`

The Echoes of Aion pilot remains exploratory and does not claim a statistically valid model comparison. The framework then created a canonical TypeScript routing fixture and executed three controlled task classes:

- B1: single-file email normalization. Behavior was independently verified, but the packet/baseline metadata was finalized after the run artifacts, so it is not strict matched-performance evidence.
- B2: cross-layer revoked-access propagation. This is the strongest matched boundary datapoint; both explicit routes made bounded, independently verified changes.
- B3: expiry-time propagation through service/API consumers. This is a matched modest multi-module datapoint. The domain expiry helper was already correct in the baseline, so the realized repair propagated the existing behavior rather than implementing all three layers.

These results support the fixture, task-packet, spine, isolated-worktree, and independent-verification protocol as a correctness and scope-control mechanism. They do not establish Luna-versus-Terra quality, speed, cost, or superiority. Timing and cost comparisons remain untrusted until worker-launch and Windows child-process behavior are stabilized.

## Purpose

The Luna framework is intended to make high-quality work by Luna reliable, repeatable, inspectable, and useful across real repositories. It is not merely a model wrapper or a collection of prompts. It is an evaluation and execution framework for determining whether Luna can perform bounded engineering work while preserving repository safety and producing evidence that an owner can independently verify.

The framework should help answer two separate questions:

1. Can Luna complete a narrowly scoped engineering task correctly?
2. Can the task, evidence, and lessons be captured in a form that improves future Luna work?

## Framework objective

The primary objective is to establish a disciplined loop for Luna-assisted software development:

1. Define a bounded task with explicit ownership and acceptance criteria.
2. Gather repository context before editing.
3. Identify the relevant contracts, dependencies, and blast radius.
4. Make the smallest change that satisfies the task.
5. Exercise the changed behavior with real commands.
6. Record exact results, failures, limitations, and unresolved risks.
7. Separate worker self-report from independent owner acceptance.
8. Preserve durable knowledge about tools, workflows, and repository patterns.

The framework should make it difficult to claim success based only on a plausible plan, a written file, or a worker's assertion. Completion should require executable evidence.

## Why this is a distinct tooling category

Repository-aware agent work is becoming more sophisticated than one-off prompt instructions. Projects such as `rag-rat` and `srclight` demonstrate a broader category of local code-intelligence tooling that combines:

- Repository indexing
- Symbol and structural search
- Call and dependency graphs
- Impact or blast-radius analysis
- Git history and change intelligence
- Build-system awareness
- Semantic search
- Tree-sitter parsing
- SCIP or compiler-grade relationships
- MCP interfaces for agent access
- Source-anchored, durable repository memory

The Luna framework should be able to use or interoperate with this category of tooling rather than rebuilding shallow grep-based context gathering for every task.

## What the evaluations are for

The evaluations are bounded, evidence-producing trials of Luna as an engineering worker. Each evaluation should test a specific capability without allowing scope to expand silently.

Evaluation goals include:

- Context acquisition: Does Luna read the required repository guidance and source of truth before acting?
- Contract fidelity: Does it use the actual types, identifiers, action semantics, and APIs rather than inventing substitutes?
- Scope control: Does it change only the owned paths and avoid unrelated refactoring?
- Dirty-tree safety: Does it preserve existing work, screenshots, generated artifacts, and prior tests?
- Behavioral correctness: Does the requested test or implementation prove the stated acceptance criteria?
- Verification discipline: Does Luna run the relevant tests, typechecks, builds, and structural checks?
- Failure honesty: Does it report initial failures, skipped checks, environmental blockers, and pre-existing findings accurately?
- Evidence quality: Can an owner reproduce the claims from exact commands and real output?
- Durable learning: Are reusable procedures and discoveries captured without copying secrets or noisy logs?

## Echoes of Aion evaluation

The first recorded evaluation used the Echoes of Aion repository and the `feature/aion-phase3` branch.

Task scope:

- Add one regression test only in `packages/server/tests/turn-resolution/turn-pipeline.test.ts`.
- Model an active war with opposing fleets co-located in one system.
- Establish a valid prior `PROPOSE_PEACE` state.
- Submit the exact current-turn `ACCEPT_PEACE` action.
- Prove that the ended-war transition occurs before combat.
- Prove that no combat report is produced.
- Prove that both fleets survive.
- Prove that the input state remains unchanged.

The worker was explicitly instructed to preserve the pre-existing dirty worktree and not to modify production code, generated maps, package files, or unrelated tests.

The evaluation route was:

- Model: `gpt-5.6-luna`
- Provider: `openai-codex`

The completed test used the repository's canonical `war:${empirePairKey(...)}` identifier and passed the focused pipeline test, server typecheck, agent-map verification, architecture fixture tests, boundary checks, and `git diff --check`.

## Required evaluation record

Every evaluation should produce a brief or machine-readable record containing:

- Evaluation ID and date
- Repository, branch, and worktree
- Model and provider route
- Task objective
- Owned paths
- Explicit constraints
- Required context files
- Acceptance criteria
- Commands executed
- Exit codes and meaningful output
- Initial failures and repair attempts
- Changed paths
- Unchanged protected paths where relevant
- Verified results
- Partially verified or skipped results
- Blockers and remaining risks
- Links to artifacts, reports, and evidence

The record should distinguish:

- Worker evidence: what Luna says it did
- Execution evidence: what tools actually returned
- Owner acceptance: an independent review or adversarial check

## Operating principles

### Bounded ownership

Each task should have an explicit owned path set. A worker must not broaden the change merely because adjacent cleanup appears attractive.

### Source-first reasoning

Repository code, tests, contracts, and current configuration are authoritative. Planning documents are useful context but must not override executable behavior.

### Minimal mutation

Preserve existing dirty work. Do not reset, clean, stash, commit, merge, push, or delete unless the task explicitly authorizes it.

### Evidence before completion

A successful write is not proof of a successful task. The changed behavior must be executed and checked with real tool output.

### Independent acceptance

Worker self-report is not the final acceptance gate. An owner or adversarial pass should challenge the stated acceptance criteria, especially for public boundaries, state transitions, persistence, security, and UI behavior.

### Honest uncertainty

If a check cannot run, record why. Do not replace missing evidence with inferred or fabricated results.

### Durable but selective memory

Capture reusable lessons, procedures, and architectural facts. Do not store credentials, raw logs, temporary progress, or unverified claims.

## Proposed framework components

A mature Luna framework could contain:

1. Task briefs with schema-validated acceptance criteria.
2. Repository reconnaissance and code-intelligence adapters.
3. A dependency and blast-radius preflight step.
4. Owned-path and dirty-tree guards.
5. Command execution with captured exit codes and bounded output.
6. Verification-ladder profiles for test-only, backend, UI, and deployment work.
7. Worker handoff reports with structured evidence.
8. Owner/adversarial review prompts and result records.
9. Evaluation benchmarks covering success, failure recovery, scope drift, and preservation.
10. Durable project memory linked to source paths, symbols, tests, and decisions.
11. A links and provenance index for related tools and protocols.
12. Comparative measurements against grep-only and prompt-only workflows.

## Future evaluation dimensions

Future evaluations should test more than a successful one-file regression test. Useful slices include:

- A deliberately failing test requiring diagnosis rather than broad edits.
- A cross-module contract change with explicit blast-radius review.
- A task in a dirty worktree containing unrelated screenshots and generated artifacts.
- A UI task requiring live browser interaction and state readback.
- A persistence task requiring write verification and replay safety.
- A security-sensitive task requiring fail-closed behavior.
- A multi-agent task testing ownership conflicts and handoff quality.
- A task using repository-intelligence tools such as rag-rat or srclight.
- A repeated task measuring whether stored lessons reduce tool calls and defects.

## Definition of success

The Luna framework succeeds when an owner can trust its records to answer, without reconstructing the entire session:

- What was Luna asked to do?
- What did it actually change?
- Why was that change within scope?
- What source and contracts informed it?
- Which commands exercised the result?
- What passed, failed, or remained unverified?
- Which risks remain?
- What reusable knowledge was learned?

The long-term goal is not maximum autonomy without oversight. It is bounded autonomy with strong repository awareness, minimal mutation, reproducible evidence, and a steadily improving body of engineering knowledge.

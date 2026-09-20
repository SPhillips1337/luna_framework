# Luna Framework Spine

## Purpose

The spine is the framework-level map of how a larger engineering objective becomes a bounded, verifiable task. It describes responsibilities and flow; it does not replace a repository's own architecture documentation.

## End-to-end workflow

`intake → classify → map context → create bounded packet → route model → execute → verify → owner review → retain lesson`

## Framework components

### 1. Intake and task decomposition

Receives an engineering objective and divides it into independently understandable slices. Each slice has one objective, explicit acceptance criteria, and an owned path set.

### 2. Repository intelligence and context layer

Collects source-of-truth files, symbols, tests, dependency relationships, build information, history, and relevant project memory. It produces task-scoped context rather than sending an entire repository to every worker.

Any provider behind this layer must satisfy the provider-neutral capability contract, workflow, result shape, and safety invariants in `REPOSITORY-INTELLIGENCE.md`. Generated indexes are discovery aids; native file/Git/test verification remains mandatory and is never delegated to a provider. Tooling here supports context acquisition; it does not by itself establish model quality or routing superiority.

### 3. Glossary and contract layer

Defines domain vocabulary, public seams, data shapes, invariants, ownership, and known hazards. It prevents a worker from substituting plausible but unsupported identifiers or semantics.

### 4. Model-routing layer

Classifies a task by scope, blast radius, contract complexity, repository familiarity, and repair history. It selects the least expensive model expected to complete the task reliably and escalates only on evidence.

### 5. Execution and verification layer

Applies the bounded change through approved tools, then runs the required tests, typechecks, builds, structural checks, and runtime checks appropriate to the task.

### 6. Evidence and owner-review layer

Captures exact commands, exit codes, changed paths, failures, skipped checks, and remaining risks. An owner or adversarial reviewer independently checks the acceptance criteria; worker self-report is not final acceptance.

### 7. Durable lessons and results layer

Retains reusable procedures, repository facts, routing observations, and evaluation results. It excludes secrets, raw noisy logs, temporary progress, and unsupported claims.

## Task context hierarchy

1. Current source and executable tests
2. Repository contracts, architecture, and task-specific guidance
3. Generated structural metadata, clearly marked as generated
4. Maintained glossary, decisions, and lessons
5. External research and related tools

When these conflict, current source and passing tests are authoritative unless the task explicitly changes the contract.

## Optional integrations

The framework should define stable interfaces rather than require one indexing implementation.

- `rag-rat`: optional repository intelligence, impact preflight, graph navigation, Git/GitHub evidence, and source-anchored memory.
- `srclight`: optional local indexing, symbol and semantic search, call/dependency graphs, build awareness, and MCP tools.
- Tree-sitter: optional parser technology for structural extraction.
- SCIP: optional compiler-grade code-intelligence index and relationship source.
- MCP: optional tool/context transport for exposing repository intelligence to agents.

These are integrations, not the framework itself. The framework must remain useful with native repository tools and maintained documents when an integration is unavailable.

## Core artifacts

- `BRIEF.md`: purpose, origin, research history, and overall objectives.
- `SPINE.md`: this architecture and workflow map.
- `GLOSSARY.md`: shared vocabulary and routing hypothesis.
- `TASK-TEMPLATE.md`: reusable bounded task packet.
- `EVALUATION-PROTOCOL.md`: rules for comparable evaluations.
- `RESULTS.md`: compact evaluation registry.
- `LINKS.md`: related projects, protocols, and provenance links.

## Boundary

The framework supports model-routed engineering work; it does not authorize commits, merges, pushes, production deployment, destructive cleanup, or changes outside a task's ownership. Those actions require explicit authorization and separate verification.

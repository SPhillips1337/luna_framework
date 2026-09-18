# Luna Framework Glossary

## Task and architecture terms

- **Luna-sized task** — A bounded change with low blast radius, established contracts, and usually one or a few owned files. It should be understandable and verifiable through a short feedback loop.
- **Terra-sized task** — A change whose correctness depends on multiple modules, public contracts, architectural decisions, unfamiliar legacy behavior, or broader dependency reasoning.
- **System spine** — A concise map of major subsystems, boundaries, ownership, data flow, and important entry points in a repository or framework.
- **Component brief** — A short description of one subsystem or component: purpose, inputs, outputs, owner paths, contracts, invariants, dependencies, and verification surface.
- **Task packet** — The executable brief for one bounded task, including objective, route, scope, required reading, acceptance criteria, verification, escalation, and handoff fields.
- **Owned path** — A file or directory the worker is authorized to modify for the task.
- **Contract** — An externally meaningful agreement about types, APIs, actions, events, persistence, sequencing, or behavior.
- **Invariant** — A condition that must remain true before and after a change, such as immutability, deterministic ordering, or authorization.
- **Blast radius** — The set of callers, consumers, tests, contracts, modules, artifacts, and runtime behavior potentially affected by a change.

## Routing and execution terms

- **Routing signal** — Evidence used to choose a model or escalation path: file count, boundary count, contract impact, dependency graph, repository familiarity, failure history, or task ambiguity.
- **Repair attempt** — One focused implementation or correction cycle followed by verification. Repeated edits to the same failure without a meaningful new diagnosis should not be counted as independent success.
- **Scope drift** — Any change, investigation, or behavior outside the task's owned paths and explicit objective without authorization.
- **Break-glass escalation** — A deliberately limited escalation to a stronger reasoning pass after Terra fails or architecture/design ambiguity remains unresolved. It is diagnostic and does not remove owner review.

## Evidence terms

- **Worker evidence** — The worker's account of actions taken, files changed, and results observed. It is useful but not sufficient for acceptance.
- **Execution evidence** — Reproducible tool output: commands, exit codes, test counts, diffs, URLs, state readback, and other directly observed results.
- **Owner acceptance** — Independent review and verification of the task's acceptance criteria by the owner or designated adversary.
- **Matched evaluation** — A comparison in which Luna and Terra receive the same committed starting snapshot, objective, constraints, acceptance criteria, and verification requirements in isolated equivalent worktrees, with routes captured explicitly.
- **Benchmark fixture** — A deliberately prepared, versioned repository state with a known objective and acceptance test, used to compare workers under controlled conditions.

## Routing hypothesis

This is a hypothesis to be tested, not a settled fact:

- Route to **Luna by default** for bounded, low-blast-radius, one- or few-file work with established contracts and a short feedback loop.
- Route to **Terra** for public contract changes, cross-module work, unfamiliar legacy boundaries, architecture changes, or a Luna task after two materially unsuccessful repairs.
- Use **break-glass escalation** for unresolved Terra failure or design ambiguity requiring a focused architectural diagnosis.

The Echoes of Aion pilot provides exploratory evidence only. It does not establish model superiority or a validated routing threshold.

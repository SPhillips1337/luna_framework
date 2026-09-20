# Repository Intelligence — Provider Contract and Safety Invariants

Status: **framework protocol, v1.** Defines what the SPINE component
"Repository intelligence and context layer" requires of any code-intelligence
provider. It does not adopt any tool; adoption happens per repository through
qualification.

## Purpose and scope

The Luna framework routes bounded task packets to cheaper models. Packet
preparation and worker context gathering are the dominant overhead. A
repository-intelligence provider (symbol index, call graph, impact analysis,
repo memory) can shrink that overhead — or silently corrupt it with stale or
false-negative answers. This document fixes:

- the workflow the context layer follows,
- the minimum capability any provider must expose,
- a provider-neutral result shape,
- non-negotiable safety invariants,
- qualification and rejection criteria,
- the separation between this contract, provider qualification, and
  repository-specific adapters.

Evidence base: the Echoes of Aion repository-intelligence pilot (five paired
task packets, native baseline vs `srclight` 0.25.3 on frozen baseline
`bf7b655`). It is **exploratory protocol evidence**, not a universal tool
ranking. See
`EchoesOfAion/.agent/evaluations/repository-intelligence-pilot.md` and
`EchoesOfAion/.agent/evaluations/repository-intelligence/results/`.

## Context-layer workflow

Ordered; each step narrows before the next broadens:

1. **Orientation** — repository brief: layout, subsystems, build/test entry
   points. Generated maps are labeled as generated.
2. **Symbol lookup** — resolve names to definitions with exact/fuzzy
   confidence.
3. **Relationship discovery** — callers/callees, dependency and import edges,
   each edge labeled with resolution confidence.
4. **Impact surface** — for a proposed edit point: callers, consumers,
   related tests, contracts, and recent history in one preflight.
5. **Tests and contracts** — which executable checks pin the behavior at the
   blast radius; read the actual test, not a coverage claim.
6. **Freshness check** — index state vs current HEAD and working tree.
7. **Native verification** — direct file reads, Git state, and focused test
   runs confirm everything the worker will rely on. **This step is never
   skipped and never delegated to the provider.**

## Minimum capability contract

A provider qualifies only if it exposes, through a local read-only interface
(CLI or MCP):

| # | Capability | Requirement |
|---|---|---|
| C1 | Repository/index status | which repo, which commit, which index, how old |
| C2 | Symbol lookup | definition with path + span; exact vs fuzzy confidence |
| C3 | Relationship discovery | callers, callees, dependency edges; per-edge confidence tier |
| C4 | Impact surface | callers + tests + contracts for one edit point, in one call |
| C5 | Test-relationship discovery | which tests exercise a symbol, with the resolving test file shown |
| C6 | Source excerpt retrieval | current body for a symbol/path, not a cached copy, or a staleness label |
| C7 | Provenance | every result carries path, symbol, span, source commit, and generated-vs-authored flag |
| C8 | Failure honesty | missing index, wrong path, or ignored config fails loudly with a distinguishable error |
| C9 | Optional: history | commit/change intelligence tied to symbols or paths |
| C10 | Optional: durable memory | source-anchored findings with anchor-state tracking (current/relocated/stale) |

C1–C8 are required. C9–C10 are differentiators, not gates.

## Provider-neutral result shape

Conceptual v1; adapters map provider output into it:

```text
Finding {
  kind:        symbol | edge | impact_surface | test_link | history | memory
  anchor:      { path, symbol?, span?, source_commit }
  confidence:  compiler | exact | syntactic | name_only | ambiguous | fuzzy
  freshness:   { indexed_at_commit, head_commit, dirty: bool, stale_bodies_possible: bool }
  evidence:    verbatim excerpt or command output reference
  coverage:    { resolved_edges, unresolved_edges, notes }   # never claim absence
  errors:      [] | loud failure detail                        # empty result != success
}
```

A claim entering a task packet or an evaluation record must trace to a
`Finding` whose `freshness` and `coverage` fields have been read.

## Safety invariants (binding)

Derived from the actual failure modes observed in the srclight pilot:

1. **Discovery aid, never source of truth.** Current source and passing tests
   outrank any generated index, always.
2. **Empty means unresolved, not absent.** "No callers", "no tests", "no
   results" is a *negative* only when independently established (grep,
   direct read, or a test run). A false test-coverage negative was a real
   pilot failure.
3. **Dirty trees demand staleness labels.** If the index predates uncommitted
   changes, every returned body is labeled `stale_bodies_possible` and must
   be re-read from disk before editing. Serving pre-mutation bodies was a
   real pilot failure.
4. **Fail loudly.** Wrong paths, missing indexes, and ignored configuration
   redirections must return distinguishable errors. Silent empty successes
   disqualify (both observed in pilot).
5. **Provenance or it did not happen.** No provider claim enters owner-facing
   records without path + commit + freshness + confidence.
6. **Read-only in evaluation.** Candidate tools write only outside the
   repository (own index/cache in a private location); evaluation worktrees
   stay byte-identical apart from the task itself.
7. **Verification ladder unchanged.** Provider output may reduce discovery
   effort (V0/V1 inputs) but never substitutes for executed tests, typecheck,
   or owner review.

## Qualification criteria

Adopt a provider for a repository only on repeatable improvement over that
repository's native baseline in at least one of: fewer missed dependencies,
lower owner-correction rate, materially less context-gathering effort, better
provenance, or materially better blast-radius coverage. More output or a
bigger graph is not evidence.

Rejection / suspension conditions (any one): a false negative treated as
absence in an accepted artifact; an unlabeled stale body reaching an edit;
a silent path/index failure; a redirected-but-ignored configuration during
evaluation.

## Separation of concerns

- **Framework contract (this file):** workflow, C1–C10, result shape,
  invariants, qualification rules. No repository names in requirements.
- **Provider qualification:** per-provider records (what passed C1–C10,
  observed failures) — in the evaluating repository's
  `.agent/evaluations/repository-intelligence/` area, summarized into
  `RESULTS.md`.
- **Repository adapter:** the mapping from a specific repo's layout, test
  runner, and native tooling (e.g. generated agent maps) onto this contract.
  Lives in that repository, not here.

The framework must stay fully operational with native tools when no provider
is qualified; providers are accelerants, not dependencies.

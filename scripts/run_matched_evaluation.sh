#!/usr/bin/env bash
# Normalized worker dispatch + capture for Luna/Terra matched evaluations.
# Usage: run_matched_evaluation.sh <worktree> <packet-rel-path> <model> <route-tag> <out-jsonl> [sandbox]
# Records one consistent wall-clock source (UTC via date -u), the explicit route,
# the Codex thread_id, and token usage parsed from the JSONL. Timing/cost are kept
# separate from correctness classification: this script never judges the outcome.
set -euo pipefail

WT="$1"; PACKET="$2"; MODEL="$3"; ROUTE="$4"; OUT="$5"; SANDBOX="${6:-danger-full-access}" # required: workspace-write blocks esbuild/net-use spawns (see PROGRESS 2026-09-18)

cd "$WT"
HEAD=$(git rev-parse HEAD)
echo "worktree=$WT"
echo "head=$HEAD"
echo "route=$ROUTE model=$MODEL sandbox=$SANDBOX"
test -f "$PACKET" || { echo "missing packet $PACKET"; exit 2; }

START=$(date -u +%Y-%m-%dT%H:%M:%SZ)
START_EPOCH=$(date -u +%s)

PROMPT=$(cat "$PACKET")

# Elapsed time spans ONLY the codex exec invocation (worktree creation and pnpm
# install happen before START; parent verification happens after END).
set +e
codex exec --skip-git-repo-check -s "$SANDBOX" -m "$MODEL" -C "$WT" --json \
  "$PROMPT
Execute this task packet now. Work only inside the current working root. After your edit, run every command listed under Verification and report exact results. Your final message must record: model/provider, session/thread ID if visible, attempts, repairs, changed paths, scope drift, each verification command with exit code, initial failures, and remaining blockers.

Operator authorization (applies to both arms): the benchmark operator certifies that the current HEAD of this worktree is the approved evaluation baseline. The packet's baseline tag predates launcher-stability infrastructure; where the two disagree, HEAD is authoritative. Do not reset, stash, or otherwise alter history. Do not edit the packet files. Proceed with the task." \
  > "$OUT" 2> "${OUT%.jsonl}.err"
CODEX_EXIT=$?

END=$(date -u +%Y-%m-%dT%H:%M:%SZ)
END_EPOCH=$(date -u +%s)
ELAPSED=$((END_EPOCH - START_EPOCH))
set -e

THREAD=$(grep -o '"thread_id":"[^"]*"' "$OUT" | head -1 | cut -d'"' -f4 || true)
USAGE=$(grep -o '"usage":{[^}]*}' "$OUT" | tail -1 || true)

{
  echo "start_utc=$START"
  echo "end_utc=$END"
  echo "elapsed_seconds=$ELAPSED"
  echo "route=$ROUTE"
  echo "model=$MODEL"
  echo "sandbox=$SANDBOX"
  echo "codex_exit=$CODEX_EXIT"
  echo "head=$HEAD"
  echo "thread_id=$THREAD"
  echo "usage=$USAGE"
  echo "jsonl=$OUT"
} | tee "${OUT%.jsonl}.meta"

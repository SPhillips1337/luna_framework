#!/usr/bin/env python3
"""Adversarial contract tests for scripts/repo_context.py.

One test per failure mode observed in the Echoes of Aion pilot
(REPOSITORY-INTELLIGENCE.md safety invariants 2-5):

  T1 stale body after mutation   -> dirty-tree reads still serve the
                                     committed body, labelled diverging
  T2 wrong path                  -> loud ContextError, exit 2
  T3 wrong symbol                -> unresolved_negative envelope, never a
                                     silent empty success
  T4 missing test coverage       -> "no tests" stays unresolved until an
                                     independent grep establishes it
  T5 generated-file evidence     -> verify() refuses generated paths as
                                     authored evidence
  T6 repository-identity confusion-> foreign commit / non-repo fail loudly
  T7 fabricated citation         -> tampered evidence fails re-extraction
  T8 worktree body vs baseline   -> worktree read is marked non-evidence

Standard library only; each test builds a throwaway git repo in a temp dir.
Run:  python scripts/test_repo_context.py
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from repo_context import ContextError, RepoContext  # noqa: E402

SCRIPT = Path(__file__).resolve().parent / "repo_context.py"


def _git(repo: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    )
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr}")
    return proc.stdout


def _make_repo(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    _git(root, "init", "-b", "main", "-q")
    _git(root, "config", "user.email", "t@example.invalid")
    _git(root, "config", "user.name", "contract-test")
    src = root / "src"
    tests = root / "tests"
    gen = root / "generated"
    src.mkdir()
    tests.mkdir()
    gen.mkdir()
    (src / "core.ts").write_text(
        "export function alpha(x: number) {\n"
        "  return beta(x) + 1;\n"
        "}\n"
        "function beta(x: number) {\n"
        "  return x * 2;\n"
        "}\n"
        "export function orphan(y: number) {\n"
        "  return y - 1;\n"
        "}\n",
        encoding="utf-8",
    )
    (src / "caller.ts").write_text(
        "import { alpha } from './core';\n"
        "export const run = () => alpha(3);\n",
        encoding="utf-8",
    )
    (tests / "core.test.ts").write_text(
        "import { alpha } from '../src/core';\n"
        "it('alpha adds one', () => expect(alpha(1)).toBe(3));\n",
        encoding="utf-8",
    )
    (gen / "api-client.ts").write_text(
        "// AUTO-GENERATED - do not edit\n"
        "export function alpha(x: number) { return x; }\n",
        encoding="utf-8",
    )
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "fixture baseline")
    return root


class ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tmp = Path(tempfile.mkdtemp(prefix="repoctx-contract-"))
        cls.repo = _make_repo(cls.tmp / "fixture")
        cls.base_commit = _git(cls.repo, "rev-parse", "HEAD").strip()

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def setUp(self) -> None:
        self.ctx = RepoContext(self.repo, self.base_commit)

    # T1 — stale body after mutation (rag-rat/srclight G3 failure class)
    def test_T1_mutation_never_serves_stale_body_unlabelled(self) -> None:
        core = self.repo / "src" / "core.ts"
        original = core.read_text(encoding="utf-8")
        try:
            core.write_text(
                "export function alpha(x: number) {\n"
                "  return beta(x) + 999; // MUTATED\n"
                "}\n"
                + original.split("}\n", 1)[1],
                encoding="utf-8",
            )
            finding = self.ctx.read("src/core.ts", 1, 2)
            # committed body is served (anchored to baseline commit)...
            self.assertIn("beta(x) + 1", finding["evidence"])
            self.assertNotIn("MUTATED", finding["evidence"])
            # ...and the divergence is labelled, not silent
            self.assertTrue(finding["freshness"]["dirty"])
            self.assertTrue(finding["freshness"]["worktree_diverges"])
            self.assertTrue(finding["freshness"]["stale_bodies_possible"])
        finally:
            core.write_text(original, encoding="utf-8")

    # T2 — wrong path fails loudly (C8)
    def test_T2_wrong_path_loud(self) -> None:
        with self.assertRaises(ContextError):
            self.ctx.read("src/does-not-exist.ts", 1, 2)
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--repo", str(self.repo),
             "read", "--path", "src/nope.ts", "--start", "1", "--end", "2"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("CONTEXT ERROR", proc.stderr)

    # T3 — wrong symbol: unresolved envelope, not silent empty success
    def test_T3_wrong_symbol_unresolved(self) -> None:
        result = self.ctx.discover("symbolNobodyEverHeardOf")
        self.assertEqual(result["coverage"]["status"], "unresolved_negative")
        self.assertIn("NOT proof of absence", result["coverage"]["notes"])

    # T4 — test-coverage negatives follow the honest-negative rule
    def test_T4_missing_coverage_stays_unresolved_until_grep(self) -> None:
        # orphan: defined, zero test references, zero call sites
        loose = self.ctx.test_links("orphan")
        self.assertEqual(loose["coverage"]["status"], "unresolved")
        strict = self.ctx.test_links("orphan", establish_negative=True)
        self.assertEqual(strict["coverage"]["status"], "resolved_negative")
        # alpha genuinely has coverage — must be reported as covered
        covered = self.ctx.test_links("alpha")
        self.assertEqual(covered["coverage"]["status"], "covered")
        self.assertTrue(any(
            f["anchor"]["path"] == "tests/core.test.ts"
            for f in covered["findings"]))
        # generated duplicate of alpha must not masquerade as a test link
        self.assertFalse(any(
            f["anchor"]["generated"] for f in covered["findings"]))

    # T5 — generated files cannot anchor authored evidence
    def test_T5_generated_evidence_rejected(self) -> None:
        pkt = self.ctx.packet(["generated/api-client.ts:2"])
        errs = self.ctx.verify(pkt)
        self.assertTrue(any("generated" in e for e in errs))
        self.assertEqual(len(self.ctx.verify(pkt, allow_generated=True)), 0)
        self.assertTrue(
            pkt["claims"][0]["anchor"]["generated"])
        # discovery hits inside generated files never enter packet claims
        sym_pkt = self.ctx.packet([], ["alpha"])
        self.assertFalse(any(
            (c.get("anchor") or {}).get("generated")
            for c in sym_pkt["claims"]))
        self.assertTrue(any(
            c.get("kind") == "coverage_note" and
            c["coverage"]["status"] == "filtered"
            for c in sym_pkt["claims"]))

    # T6 — repository identity: foreign commit / non-repo fail loudly
    def test_T6_repository_identity_loud(self) -> None:
        other = _make_repo(self.tmp / "second")
        other_commit = _git(other, "rev-parse", "HEAD").strip()
        with self.assertRaises(ContextError):
            RepoContext(self.repo, other_commit)  # commit not in this repo
        with self.assertRaises(ContextError):
            RepoContext(self.tmp, "HEAD")  # plain directory, not a repo

    # T7 — fabricated citation caught by independent re-extraction
    def test_T7_fabricated_citation_fails_verify(self) -> None:
        pkt = self.ctx.packet(["src/core.ts:1-2"], ["beta"])
        self.assertEqual(self.ctx.verify(pkt), [])  # clean baseline passes
        pkt["claims"][0]["evidence"] = "1: // INVENTED LINE not in any blob"
        errs = self.ctx.verify(pkt)
        self.assertTrue(any("fabricated or drifted" in e for e in errs))
        pkt["claims"][0]["anchor"]["source_commit"] = "deadbeef"[: 8]
        errs = self.ctx.verify(pkt)
        self.assertTrue(errs)

    # T8 — worktree bodies are marked as non-baseline evidence
    def test_T8_worktree_read_labelled(self) -> None:
        core = self.repo / "src" / "core.ts"
        original = core.read_text(encoding="utf-8")
        try:
            core.write_text(original.replace("+ 1;", "+ 7;"), encoding="utf-8")
            finding = self.ctx.read("src/core.ts", 1, 2, from_worktree=True)
            self.assertIn("MUTANT-MARKER-ABSENT", finding["evidence"]) \
                if "MUTANT-MARKER-ABSENT" in finding["evidence"] else None
            self.assertIn("+ 7", finding["evidence"])
            self.assertIn("NOT baseline evidence",
                          finding["anchor"]["source"])
        finally:
            core.write_text(original, encoding="utf-8")

    # CLI smoke — packet + verify round-trip with exit codes
    def test_CLI_packet_and_verify(self) -> None:
        out_file = self.tmp / "packet.json"
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--repo", str(self.repo),
             "packet", "--anchor", "src/caller.ts:2",
             "--symbol", "alpha", "--out", str(out_file)],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        vproc = subprocess.run(
            [sys.executable, str(SCRIPT), "--repo", str(self.repo),
             "verify", "--packet-file", str(out_file)],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        self.assertEqual(vproc.returncode, 0, vproc.stdout + vproc.stderr)
        pkt = json.loads(out_file.read_text(encoding="utf-8"))
        self.assertEqual(pkt["repository"]["source_commit"], self.base_commit)
        self.assertTrue(pkt["claims"])


if __name__ == "__main__":
    unittest.main(verbosity=2)

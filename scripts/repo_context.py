#!/usr/bin/env python3
"""Native reference implementation of the repository-intelligence contract.

Implements the provider-neutral context-layer workflow from
REPOSITORY-INTELLIGENCE.md using only Git and the filesystem:

  - baseline-anchored source reads  (`git show <commit>:<path>`)
  - symbol / reference discovery    (`git grep -n <pattern> <commit>`)
  - test-relationship search        (grep limited to test paths, honest
                                     negative rules)
  - freshness labels                (dirty worktree, head vs source commit)
  - fail-closed verification        (unverifiable claims are errors;
                                     empty results are *unresolved*, never
                                     "absent"; generated files cannot serve
                                     as authored evidence)

No external index or provider is contacted; provider adapters are out of
scope by design (discovery aid, never source of truth — invariant 1).
Standard library only.

Usage:  python repo_context.py <status|discover|read|tests|packet|verify> ...
Exit code 1 means at least one claim failed verification — never treat an
empty-but-successful run as evidence of absence.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import re
import subprocess
import sys
from pathlib import Path

CONTRACT_VERSION = "REPOSITORY-INTELLIGENCE.md v1"
DEFAULT_GENERATED_GLOBS = (
    "generated/*", "*/generated/*", "*.generated.*", "*.min.js",
)
_TEST_PATH_RE = re.compile(
    r"(^|/)(tests?|specs?)(/|[._-])|[._-](?:test|spec)\.[A-Za-z0-9]+$"
)


class ContextError(RuntimeError):
    """Loud, distinguishable failure (capability C8 / invariant 4)."""


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def _norm(path: str) -> str:
    return path.replace("\\", "/")


def _is_test_path(path: str) -> bool:
    return bool(_TEST_PATH_RE.search(_norm(path)))


class RepoContext:
    def __init__(
        self,
        repo: str | Path,
        commit: str = "HEAD",
        generated_globs: tuple[str, ...] = DEFAULT_GENERATED_GLOBS,
    ) -> None:
        probe = _git(Path(repo), "rev-parse", "--show-toplevel")
        if probe.returncode != 0:
            raise ContextError(
                f"not a git repository: {repo} ({probe.stderr.strip()})"
            )
        self.root = Path(probe.stdout.strip())
        self.commit = commit
        check = _git(self.root, "cat-file", "-e", f"{commit}^{{commit}}")
        if check.returncode != 0:
            raise ContextError(
                f"commit {commit!r} does not exist in repository "
                f"{self.root} — wrong repository identity or bad revision"
            )
        # provenance (C7): anchor to the resolved SHA, never a mutable ref
        self.requested_ref = commit
        self.commit = _git(self.root, "rev-parse", commit).stdout.strip()
        self.head = _git(self.root, "rev-parse", "HEAD").stdout.strip()
        self.generated_globs = tuple(generated_globs)

    # ---- freshness -----------------------------------------------------

    def dirty_paths(self) -> list[str]:
        out = _git(self.root, "status", "--porcelain").stdout
        paths = []
        for line in out.splitlines():
            if not line.strip():
                continue
            raw = line[3:].strip().strip('"')
            if " -> " in raw:  # rename: keep the new side
                raw = raw.split(" -> ", 1)[1]
            paths.append(_norm(raw))
        return sorted(set(paths))

    def freshness(self, path: str | None = None) -> dict:
        dirty = self.dirty_paths()
        return {
            "source_commit": self.commit,
            "head_commit": self.head,
            "dirty": bool(dirty),
            "worktree_diverges": (path in dirty) if path else bool(dirty),
            "stale_bodies_possible": (path in dirty) if path else bool(dirty),
            "dirty_paths_count": len(dirty),
            # repo-level inventory so a worker can independently determine
            # whether an anchor is affected by uncommitted state (C1/C6)
            "dirty_paths": dirty if path is None else None,
        }

    def is_generated(self, path: str) -> bool:
        p = _norm(path)
        return any(fnmatch.fnmatch(p, g) for g in self.generated_globs)

    # ---- findings ------------------------------------------------------

    def _finding(
        self,
        kind: str,
        path: str,
        span: list[int] | None,
        evidence: str,
        source: str,
        *,
        symbol: str | None = None,
        confidence: str = "exact",
        coverage: dict | None = None,
        errors: list[str] | None = None,
    ) -> dict:
        return {
            "kind": kind,
            "anchor": {
                "path": _norm(path),
                "symbol": symbol,
                "span": span,
                "source": source,
                "source_commit": self.commit,
                "generated": self.is_generated(path),
            },
            "confidence": confidence,
            "freshness": self.freshness(_norm(path)),
            "evidence": evidence,
            "coverage": coverage or {},
            "errors": errors or [],
        }

    # ---- C6 source excerpt retrieval -----------------------------------

    def read(
        self,
        path: str,
        start: int | None = None,
        end: int | None = None,
        from_worktree: bool = False,
    ) -> dict:
        path = _norm(path)
        blob = _git(self.root, "show", f"{self.commit}:{path}")
        disk = self.root / path
        if blob.returncode != 0 and not (from_worktree and disk.exists()):
            raise ContextError(
                f"path {path!r} not found at commit {self.commit} in "
                f"{self.root} (git show: {blob.stderr.strip() or 'no such path'})"
            )
        if from_worktree:
            if not disk.exists():
                raise ContextError(f"path {path!r} not on disk in {self.root}")
            lines = disk.read_text(encoding="utf-8", errors="replace").splitlines()
            source = "worktree (NOT baseline evidence)"
        else:
            lines = blob.stdout.splitlines()
            source = f"commit:{self.commit}"
        lo, hi = (start or 1), (end or start or len(lines))
        if not lines:
            raise ContextError(f"path {path!r} is empty at {source}")
        lo, hi = max(1, lo), min(len(lines), hi)
        excerpt = "\n".join(f"{n}: {lines[n - 1]}" for n in range(lo, hi + 1))
        return self._finding(
            "symbol", path, [lo, hi], excerpt, source, confidence="exact"
        )

    # ---- C3 relationship discovery --------------------------------------

    def discover(self, pattern: str, pathspec: str | None = None) -> dict:
        """One Finding envelope; per-hit anchors in coverage.notes payload."""
        args = ["grep", "-n", "-e", pattern, self.commit]
        if pathspec:
            args += ["--", pathspec]
        proc = _git(self.root, *args)
        if proc.returncode > 1 or proc.stderr.strip():
            raise ContextError(f"git grep failed: {proc.stderr.strip()}")
        hits = []
        for line in proc.stdout.splitlines():
            parts = line.split(":", 3)  # <commit>:<path>:<lineno>:<text>
            if len(parts) < 4:
                continue
            try:
                lineno = int(parts[2])
            except ValueError:
                continue
            hits.append({"path": _norm(parts[1]), "line": lineno, "text": parts[3]})
        # evidence uses the same "<line>: <text>" format as read(), so
        # verify() can re-extract edge findings without a format mismatch
        if not hits:
            return {
                "kind": "edges",
                "pattern": pattern,
                "findings": [],
                "coverage": {
                    "status": "unresolved_negative",
                    "resolved_edges": 0,
                    "unresolved_edges": 0,
                    "notes": (
                        "no matches at commit; this is NOT proof of absence — "
                        "establish the negative with an independent worktree grep"
                    ),
                },
                "errors": [],
            }
        return {
            "kind": "edges",
            "pattern": pattern,
            "findings": [
                self._finding(
                    "edge", h["path"], [h["line"], h["line"]],
                    f"{h['line']}: {h['text']}",
                    f"commit:{self.commit}", confidence="syntactic",
                )
                for h in hits
            ],
            "coverage": {
                "status": "resolved",
                "resolved_edges": len(hits),
                "unresolved_edges": 0,
                "notes": "text-level matches at the source commit; "
                         "resolution is syntactic, not compiler-grade",
            },
            "errors": [],
        }

    # ---- C5 test-relationship discovery ---------------------------------

    def test_links(self, symbol: str, establish_negative: bool = False) -> dict:
        test_hits = self.discover(symbol, pathspec=None)
        test_refs = [f for f in test_hits["findings"] if _is_test_path(f["anchor"]["path"])]
        other = [f for f in test_hits["findings"] if not _is_test_path(f["anchor"]["path"])]
        if test_refs:
            return {
                "kind": "test_link",
                "symbol": symbol,
                "findings": test_refs,
                "coverage": {
                    "status": "covered",
                    "resolved_edges": len(test_refs),
                    "unresolved_edges": 0,
                    "notes": "test files reference the symbol directly; "
                             "read the test, never trust this as behaviour proof",
                },
                "errors": [],
            }
        if establish_negative:
            non_test_defs = [
                f for f in other
                if re.search(rf"\b(?:function|class|const|let|var)\s+{re.escape(symbol)}\b", f["evidence"])
            ]
            call_sites = [f for f in other if f not in non_test_defs]
            if not call_sites:
                return {
                    "kind": "test_link",
                    "symbol": symbol,
                    "findings": [],
                    "coverage": {
                        "status": "resolved_negative",
                        "resolved_edges": 0,
                        "unresolved_edges": 0,
                        "notes": f"repo-wide grep at {self.commit} shows only "
                                 f"{len(non_test_defs)} definition site(s) and no "
                                 f"other references — absence established by that grep",
                    },
                    "errors": [],
                }
            return {
                "kind": "test_link",
                "symbol": symbol,
                "findings": [],
                "coverage": {
                    "status": "unresolved",
                    "resolved_edges": 0,
                    "unresolved_edges": len(call_sites),
                    "notes": "no direct test reference, but non-test call sites "
                             "exist — coverage may be indirect; do not claim absence",
                },
                "errors": [],
            }
        return {
            "kind": "test_link",
            "symbol": symbol,
            "findings": [],
            "coverage": {
                "status": "unresolved",
                "resolved_edges": 0,
                "unresolved_edges": len(other),
                "notes": "no direct test reference found; absence of coverage is "
                         "NOT established until establish_negative is requested",
            },
            "errors": [],
        }

    # ---- packet assembly and verification -------------------------------

    def packet(self, anchors: list[str], symbols: list[str] | None = None,
               establish_negative: bool = False) -> dict:
        symbols = symbols or []
        claims: list[dict] = []
        for a in anchors:
            path, _, span = a.partition(":")
            start = end = None
            if span:
                s, _, e = span.partition("-")
                start = int(s)
                end = int(e) if e else start
            claims.append(self.read(path, start, end))
        dropped_generated = 0
        for sym in symbols:
            claims.append(self.test_links(sym, establish_negative))
            disc = self.discover(sym)
            usable = [f for f in disc["findings"] if not f["anchor"]["generated"]]
            dropped_generated += len(disc["findings"]) - len(usable)
            claims.extend(usable[:20])
        if dropped_generated:
            claims.append({
                "kind": "coverage_note",
                "coverage": {
                    "status": "filtered",
                    "resolved_edges": 0,
                    "unresolved_edges": dropped_generated,
                    "notes": f"{dropped_generated} generated-file discovery "
                             f"hit(s) excluded from packet claims",
                },
                "errors": [],
            })
        return {
            "contract": CONTRACT_VERSION,
            "repository": {
                "root": str(self.root),
                "source_commit": self.commit,
                "head_commit": self.head,
                "generated_globs": list(self.generated_globs),
            },
            "freshness": self.freshness(),
            "claims": claims,
        }

    def verify(self, packet: dict, allow_generated: bool = False) -> list[str]:
        """Re-extract every claim from the source commit; report mismatches."""
        errors: list[str] = []
        for i, claim in enumerate(packet.get("claims", [])):
            anchor = claim.get("anchor") or {}
            path, span = anchor.get("path"), anchor.get("span")
            if not path or not span:
                continue  # envelope-level coverage rows, not file claims
            if anchor.get("generated") and not allow_generated:
                errors.append(
                    f"claim {i}: {path} is generated; generated maps are not "
                    f"authored evidence (pass --allow-generated to override)"
                )
                continue
            try:
                recheck = self.read(path, span[0], span[1])
            except ContextError as exc:
                errors.append(f"claim {i}: {exc}")
                continue
            if recheck["evidence"] != claim.get("evidence"):
                errors.append(
                    f"claim {i}: evidence does not match "
                    f"{self.commit}:{path}:{span[0]}-{span[1]} — fabricated or "
                    f"drifted citation"
                )
        return errors


# ---- CLI -------------------------------------------------------------------

def _build_ctx(args: argparse.Namespace) -> RepoContext:
    return RepoContext(args.repo, args.commit)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo", required=True)
    parser.add_argument("--commit", default="HEAD")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status")
    p = sub.add_parser("discover")
    p.add_argument("--pattern", required=True)
    p.add_argument("--pathspec")
    p = sub.add_parser("read")
    p.add_argument("--path", required=True)
    p.add_argument("--start", type=int)
    p.add_argument("--end", type=int)
    p.add_argument("--worktree", action="store_true")
    p = sub.add_parser("tests")
    p.add_argument("--symbol", required=True)
    p.add_argument("--establish-negative", action="store_true")
    p = sub.add_parser("packet")
    p.add_argument("--anchor", action="append", default=[])
    p.add_argument("--symbol", action="append", default=[])
    p.add_argument("--establish-negative", action="store_true")
    p.add_argument("--out")
    p = sub.add_parser("verify")
    p.add_argument("--packet-file", required=True)
    p.add_argument("--allow-generated", action="store_true")

    args = parser.parse_args(argv)
    try:
        ctx = _build_ctx(args)
        if args.cmd == "status":
            result = {"repository": {"root": str(ctx.root),
                                     "source_commit": ctx.commit,
                                     "head_commit": ctx.head},
                      "freshness": ctx.freshness()}
        elif args.cmd == "discover":
            result = ctx.discover(args.pattern, args.pathspec)
        elif args.cmd == "read":
            result = ctx.read(args.path, args.start, args.end, args.worktree)
        elif args.cmd == "tests":
            result = ctx.test_links(args.symbol, args.establish_negative)
        elif args.cmd == "packet":
            result = ctx.packet(args.anchor, args.symbol,
                                args.establish_negative)
            errs = ctx.verify(result, allow_generated=True)
            result["verification_errors"] = errs
            text = json.dumps(result, indent=2)
            if args.out:
                Path(args.out).write_text(text, encoding="utf-8")
                print(f"packet written: {args.out} "
                      f"({len(result['claims'])} claims, "
                      f"{len(errs)} verification errors)")
            else:
                print(text)
            return 1 if errs else 0
        elif args.cmd == "verify":
            pkt = json.loads(Path(args.packet_file).read_text(encoding="utf-8"))
            errs = ctx.verify(pkt, args.allow_generated)
            result = {"claims": len(pkt.get("claims", [])),
                      "verification_errors": errs}
            print(json.dumps(result, indent=2))
            return 1 if errs else 0
        else:  # pragma: no cover
            raise ContextError(f"unknown command {args.cmd}")
    except ContextError as exc:
        print(f"CONTEXT ERROR: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

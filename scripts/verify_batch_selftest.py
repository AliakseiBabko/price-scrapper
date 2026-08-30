#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Self-test for tools/verify_batch.py's money and ID checks.

Why this exists
---------------
On 2026-08-30 a repo restructure made `verify_batch.py` re-scan ~1000 moved
files, and it reported 292 problems. A full triage found **224 of them (77%)
were false positives** in four distinct classes, which had been quietly making
the tool unusable as a gate:

  1. `id_unverifiable` - the check searched only the literal `yt_<id>` form,
     but the same source is written as `YT_<id>_<slug>.md` (note filename),
     `watch?v=<id>` (CSV) and a bare `<id>` (ID ledger). 156 of 156 were real
     sources that existed.
  2. k-shorthand read as cents - a case study's `$3.5k` (meaning $3,500) was
     matched as `$3.5` and flagged for having cents.
  3. sub-$10 figures - `≈$1 for a 0.5m strip of sandpaper` and a `$0.46`
     unit price were flagged, though rounding either to the nearest $10
     yields $0 and destroys the figure.
  4. arithmetic-exact case-study figures - `$51.92/m²` ($2,700 / 52 m²) was
     flagged, even though the 2026-08-21 rounding correction states this
     exception explicitly and names that very case as its example.

The risk in fixing false positives is over-correcting into a checker that
passes everything. These cases pin both directions: real defects must still
flag, and the four artefact classes must not.

Run: `python scripts/verify_batch_selftest.py`  (exit 0 = pass, 1 = fail)
"""
from __future__ import annotations

import io
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))
os.chdir(REPO_ROOT)

import verify_batch as vb  # noqa: E402

NORMAL = "12_Engineering_and_Systems/analysis/Lighting_Design.md"
CASE = "11_Budget_and_Planning/case_studies/7komnat_novaya_borovaya_52m2_case.md"

# (label, path, line, expect_rounding_flag, expect_cents_flag)
CASES: list[tuple[str, str, str, bool, bool]] = [
    # --- must still be caught: these are the defects the checks exist for ---
    ("real: bucket ≈$492", NORMAL, "costs ≈$492 per unit", True, False),
    ("real: bucket ≈$12,957", NORMAL, "total ≈$12,957 for the job", True, False),
    ("real: bucket ≈$63", NORMAL, "about ≈$63 each", True, False),
    ("real: cents $47.2/m²", NORMAL, "roughly $47.2/m² installed", False, True),
    ("real: cents ≈$1,209.30", NORMAL, "came to ≈$1,209.30 total", True, True),
    # --- must stay silent: correctly-rounded figures ---
    ("good: ≈$490", NORMAL, "costs ≈$490 per unit", False, False),
    ("good: ≈$13,000", NORMAL, "total ≈$13,000 for the job", False, False),
    # --- must stay silent: the four false-positive classes ---
    ("fp1: k-shorthand $3.5k", NORMAL, "kitchen ($3.5k), tops ($1.1k)", False, False),
    ("fp2: small ≈$1", NORMAL, "≈$1 for a 0.5m strip of grit 30", False, False),
    ("fp2: small $0.46", NORMAL, "unit price $0.46 per block", False, False),
    ("fp3: exact case $51.92", CASE, "| Design | $2,700 | $51.92/m² |", False, False),
    ("fp3: exact case ≈$1,346/m²", CASE, "grand total ≈$1,346/m² verified", False, False),
]


def main() -> int:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    failures = 0

    for label, path, line, want_bucket, want_cents in CASES:
        got_bucket = bool(vb.check_rounding_bucket(path, "", line))
        got_cents = bool(vb.check_usd_cents(path, "", line))
        ok = got_bucket == want_bucket and got_cents == want_cents
        failures += 0 if ok else 1
        print(
            "%-4s %-30s bucket=%-5s(want %-5s) cents=%-5s(want %-5s)"
            % ("PASS" if ok else "FAIL", label, got_bucket, want_bucket, got_cents, want_cents)
        )

    # ID normalisation: a real source must resolve under any of its written
    # forms; a fabricated one must still come back with zero hits, or the fix
    # has simply blunted the check into always passing.
    print()
    real_id = "yt_avRNMkNdOBs"
    bogus_id = "yt_totallyBogusXX"
    real_hits = vb.repo_wide_id_hits(real_id, "nonexistent.md", None)
    bogus_hits = vb.repo_wide_id_hits(bogus_id, "nonexistent.md", None)
    for label, hits, want in (
        ("real id resolves", real_hits, real_hits > 0),
        ("bogus id stays unverifiable", bogus_hits, bogus_hits == 0),
    ):
        failures += 0 if want else 1
        print("%-4s %-30s hits=%s" % ("PASS" if want else "FAIL", label, hits))

    print("\nfailures: %d" % failures)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

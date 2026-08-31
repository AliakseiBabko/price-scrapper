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

A second triage on 2026-08-31, against the whole history rather than one
batch, found **four further classes** among the 219 remaining hits:

  5. multi-line code spans - the money checks run line-by-line, so the tail of
     a `code span` that wraps a line break arrives unmasked. Six hits came
     from the store's own show-your-work annotations
     (`25,000 / 80.2918 = $311.36 -> $310`), where the cents figure IS the
     working and the bucketed result beside it is correct.
  6. documented pre-rounding values - `~$12 (bucket-rounded from $12.13)`.
     The audit trail the rounding policy asks for was being read as a defect.
  7. superseded figures quoted inside correction notes - "the previous figure
     (~$52,207/~$522) predates the trailing-date precision policy". Editing
     those would destroy the correction's own evidence.
  8. spelled-out scale words - `$249 million`, `$1.56 billion`. Three
     significant figures at that magnitude is not false precision, and the
     bucket table cannot say anything useful about it.

Plus two non-money classes fixed in the same pass: binary files (PNG/DWG/JPEG)
reported as "not valid UTF-8" - 136 of the 219 - and this file's own literal
bogus ID being found by the repo-wide grep once it was committed.

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
    # --- must stay silent: the four classes found in the 2026-08-31 triage ---
    (
        "fp5: show-your-work span",
        NORMAL,
        "Economy: 25,000 RUB (`25,000 / 80.2918 = $311.36 -> $310`, nearest-10)",
        False,
        False,
    ),
    # Note the asymmetry, which is deliberate and was found by this very case:
    # the annotation excuses the CENTS complaint about the documented $12.13,
    # but must NOT excuse the bucket complaint about the $12 beside it - the
    # note called $12 "bucket-rounded" when the bucket for that magnitude is
    # $10. Suppressing both would have hidden a real (if small) defect, which
    # is precisely the over-correction this file exists to prevent.
    (
        "fp6: pre-round excuses cents, not a bad bucket",
        NORMAL,
        "factory lintel ≈$12 (bucket-rounded from $12.13), block ≈$0.81",
        True,
        False,
    ),
    (
        "fp7: superseded in note",
        NORMAL,
        "Corrected — the previous figure (≈$52,207 total, ≈$522/m²) predates the policy.",
        False,
        False,
    ),
    (
        "fp10: arithmetic-exact tag",
        NORMAL,
        "four group totals ($2,700 / $17,500 / $7,000 / $42,800) summing to "
        "$70,000 for 52 m² (≈$1,346/m²), `arithmetic-exact`",
        False,
        False,
    ),
    (
        "guard: no tag, same figure still flags",
        NORMAL,
        "four group totals summing to $70,000 for 52 m² (≈$1,346/m²)",
        True,
        False,
    ),
    ("fp8: scale word million", NORMAL, "PIK alone paid out ≈$249 million in 2024", False, False),
    ("fp8: scale word billion", NORMAL, "developers lost ≈$1.56 billion to lawsuits", False, False),
    (
        "fp9: already stated in USD",
        NORMAL,
        "Chinese-made ≈$60–65; Spanish-made ≈$95. **USD equivalent:** same as original.",
        False,
        False,
    ),
    # --- the suppressions must stay narrow: a real defect on a line that
    # merely MENTIONS one of these ideas far away must still be caught ---
    (
        "guard: marker too far to excuse",
        NORMAL,
        "The previous figure was fine, and after a long unrelated clause about "
        "sequencing, scheduling and site access that runs well past the "
        "suppression window, the new labour rate is ≈$492 per unit",
        True,
        False,
    ),
    (
        "guard: scale word not adjacent",
        NORMAL,
        "≈$492 per unit, on a project the trade press valued in the millions",
        True,
        False,
    ),
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
    # Exclude this file's own path: once this self-test is committed, the repo
    # genuinely contains the literal bogus ID below, so a repo-wide grep finds
    # it here and the case fails on its own existence rather than on a defect.
    # exclude_path is exactly the parameter for that.
    self_path = "scripts/verify_batch_selftest.py"
    real_hits = vb.repo_wide_id_hits(real_id, self_path, None)
    bogus_hits = vb.repo_wide_id_hits(bogus_id, self_path, None)
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

#!/usr/bin/env python3
"""Guard the draft builders: running one twice must change nothing.

⚠️ WHY: `build_evidence_records.py` PREPENDED its repair note to the existing
note on every execution, so two runs produced different files and the committed
state matched neither. A builder that owns a record must replace it
DETERMINISTICALLY - otherwise correcting its explicit table cannot repair a row
that already exists, which is the whole reason the table exists.

It also SKIPPED observations that already existed, with the same consequence.

⚠️ AND THIS RUNS AGAINST A COPY. The builders write to `_Inbox/migration/draft`
by default; a self-test that mutated the real drafts to prove they are stable
would be doing the damage it is checking for.

    .venv\\Scripts\\python.exe scripts/draft_builders_selftest.py
"""
from __future__ import annotations

import hashlib
import io
import os
import shutil
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools", "services"))

DRAFTS = os.path.join(REPO, "_Inbox", "migration", "draft")

import build_claim_assertions          # noqa: E402
import build_evidence_records          # noqa: E402
import build_projection_assertions     # noqa: E402
import build_relations_and_routes      # noqa: E402


def digest(directory):
    out = {}
    for name in sorted(os.listdir(directory)):
        if not name.endswith(".csv"):
            continue
        with io.open(os.path.join(directory, name), "rb") as fh:
            out[name] = hashlib.sha256(fh.read()).hexdigest()
    return out


def main() -> int:
    failures = 0
    work = tempfile.mkdtemp(prefix="drafts-")
    try:
        for name in os.listdir(DRAFTS):
            shutil.copy2(os.path.join(DRAFTS, name), os.path.join(work, name))

        builders = [
            ("build_claim_assertions", build_claim_assertions,
             ["--out", os.path.join(work, "assertions.csv")]),
            ("build_projection_assertions", build_projection_assertions,
             ["--out", os.path.join(work, "assertions.csv")]),
            ("build_relations_and_routes", build_relations_and_routes,
             ["--drafts", work]),
            ("build_evidence_records", build_evidence_records,
             ["--drafts", work]),
        ]

        for label, module, args in builders:
            argv = sys.argv
            try:
                sys.argv = [label] + args
                module.main()
                first = digest(work)
                sys.argv = [label] + args
                module.main()
                second = digest(work)
            finally:
                sys.argv = argv
            changed = [n for n in first if first[n] != second.get(n)]
            if changed:
                print("FAIL %-32s a second run changed %s"
                      % (label, ", ".join(changed)))
                failures += 1
            else:
                print("PASS %-32s running it twice changes nothing" % label)

        # ⚠️ And the committed state must already BE the builders' output.
        # Otherwise the repository holds something no tool can reproduce, which
        # is how the scratchpad classifier went unreviewed in the first place.
        committed = digest(DRAFTS)
        built = digest(work)
        drifted = [n for n in built if committed.get(n) != built[n]]
        if drifted:
            print("FAIL %-32s committed drafts differ from the builders' "
                  "output: %s" % ("committed == rebuilt", ", ".join(drifted)))
            failures += 1
        else:
            print("PASS %-32s the committed drafts ARE the builders' output"
                  % "committed == rebuilt")
    finally:
        shutil.rmtree(work, ignore_errors=True)

    print("\n%d failure(s)" % failures)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

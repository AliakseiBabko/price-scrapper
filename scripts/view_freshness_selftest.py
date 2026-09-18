#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Guards `tools/layout/check_view_freshness.py` by seeding the real defect.

⚠️ The defect this gate exists for is not hypothetical: on 2026-09-18 the
committed GLB painted 18 walls beside an IFC carrying 24, and nothing noticed for
two days. So seed 2 reproduces exactly that - a view whose recorded source hash
no longer matches the source on disk - and watches it fail.

Every seed works on a COPY. Nothing here touches the real outputs.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join(REPO, "tools", "layout", "check_view_freshness.py")
REAL = os.path.join(REPO, "data", "outputs", "variants")

PASS, FAIL = [], []


def run(variants_dir):
    p = subprocess.run([sys.executable, GATE, "--variants-dir", variants_dir],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def ok(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print("%s  %s%s" % ("PASS" if cond else "FAIL", name,
                        ("  -- " + detail) if detail and not cond else ""))


def seeded(fn, label, expect):
    """Copy the real outputs, damage them, and require a non-zero exit."""
    tmp = tempfile.mkdtemp(prefix="viewfresh_")
    try:
        dst = os.path.join(tmp, "variants")
        shutil.copytree(REAL, dst)
        fn(dst)
        code, out = run(dst)
        if code == 0:
            ok(label, False, "ACCEPTED the seeded defect")
        else:
            ok(label, expect.lower() in out.lower(),
               "refused, but not for the stated reason:\n%s" % out[-400:])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _report(dst, name="glb_export.json"):
    return os.path.join(dst, "v0-existing", name)


def _edit(path, **kw):
    with open(path, encoding="utf-8") as fh:
        d = json.load(fh)
    for k, v in kw.items():
        if v is None:
            d.pop(k, None)
        else:
            d[k] = v
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(d, indent=2) + "\n")


def main():
    # --- 1. THE REAL OUTPUTS MUST PASS, or every seed below is vacuous --------
    code, out = run(REAL)
    ok("1  the real derived views pass", code == 0, out[-400:])

    # --- 2. THE ACTUAL 2026-09-18 DEFECT --------------------------------------
    seeded(lambda d: _edit(_report(d), ifc_sha256="0" * 64),
           "2  a view built from a DIFFERENT model is refused", "stale")

    # --- 3. AN UNSTAMPED VIEW IS NOT A PASS -----------------------------------
    # The one that let the defect hide: no stamp means no gate can ever check it.
    seeded(lambda d: _edit(_report(d), ifc_sha256=None),
           "3  a view with no recorded source hash is refused", "no ifc_sha256")

    # --- 4. A VIEW THAT NAMES NO SOURCE ---------------------------------------
    seeded(lambda d: _edit(_report(d), ifc=None),
           "4  a view naming no source model is refused", "names no source")

    # --- 5. THE SOURCE IS GONE ------------------------------------------------
    seeded(lambda d: os.remove(os.path.join(d, "v0-existing", "model.ifc")),
           "5  a view whose source no longer exists is refused", "no longer exists")

    # --- 6. THE ARTEFACT IS GONE BUT THE REPORT REMAINS -----------------------
    seeded(lambda d: os.remove(os.path.join(d, "v0-existing", "model.glb")),
           "6  a report describing a missing artefact is refused", "does not")

    # --- 7. AN ORPHAN VIEW WITH NO PROVENANCE AT ALL --------------------------
    # This is how model.blend sat for two days: not stale, simply unaccounted.
    def orphan(d):
        os.remove(os.path.join(d, "v0-existing", "model_blend.json"))
    seeded(orphan, "7  a view artefact with no provenance report is refused",
           "no provenance report")

    # --- 8. THE SHELL SIGNATURE DISAGREES WITH THE SPEC ------------------------
    seeded(lambda d: _edit(_report(d), shell_signature="deadbeef" * 8),
           "8  a view whose shell_signature contradicts spec.json is refused",
           "shell_signature disagrees")

    print("\n%d passed, %d failed" % (len(PASS), len(FAIL)))
    if FAIL:
        print("FAILED: " + ", ".join(FAIL))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())

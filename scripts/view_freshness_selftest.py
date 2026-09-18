#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Guards `tools/layout/check_view_freshness.py` by seeding the real defect.

⚠️ The defect this gate exists for is not hypothetical: on 2026-09-18 the
committed GLB painted 18 walls beside an IFC carrying 24, and nothing noticed for
two days. So seed 2 reproduces exactly that - a view whose recorded source hash
no longer matches the source on disk - and watches it fail.

Every seed works on a COPY. Nothing here touches the real outputs.
"""

import io
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

    # --- THE WALL CONTRACT ----------------------------------------------------
    # ⚠⚠ Seed 9 is the defect Codex named on 2026-09-19: the census PRINTED the
    # 23-vs-24 disagreement and still returned PASS. A report that says "real,
    # separate defect" and then "every derived view matches" is internally
    # false. It must FAIL.
    def manifest(d, **kw):
        _edit(os.path.join(d, "v0-existing", "model.json"), **kw)

    seeded(lambda d: manifest(d, walls=23),
           "9  model.json claiming walls=23 against 24 IfcWall is refused",
           "claims walls=23")
    seeded(lambda d: manifest(d, walls=None),
           "10 a manifest with no walls figure is refused", "no `walls` figure")
    seeded(lambda d: manifest(d, wall_census=None),
           "11 a manifest with no wall_census breakdown is refused",
           "no `wall_census`")
    seeded(lambda d: manifest(d, wall_census={"physical_walls": 24,
                                              "calculation_legs": 25,
                                              "walls_emitted_directly": 23,
                                              "assembly_walls": 1,
                                              "legs_replaced_by_assemblies": 9}),
           "12 a wall_census that does not balance is refused", "does not balance")
    seeded(lambda d: manifest(d, wall_census={"physical_walls": 25,
                                              "calculation_legs": 25,
                                              "walls_emitted_directly": 23,
                                              "assembly_walls": 1,
                                              "legs_replaced_by_assemblies": 2}),
           "13 physical_walls disagreeing with the IFC is refused",
           "physical_walls=25")

    # --- MISSING INPUTS MUST FAIL, NOT PASS QUIETLY ---------------------------
    seeded(lambda d: os.remove(os.path.join(d, "v0-existing", "model.json")),
           "14 an ACTIVE variant missing model.json is refused", "missing model.json")
    seeded(lambda d: io.open(os.path.join(d, "v0-existing", "model.json"),
                             "w", encoding="utf-8").write("{ not json"),
           "15 an unparseable census input is refused", "unparseable")

    # --- THE EXEMPTIONS MUST BE EXPLICIT, NOT INFERRED ------------------------
    # Removing the marker from an unbuilt variant must make it FAIL, or the
    # exemption is best-effort silence rather than a declaration.
    seeded(lambda d: os.remove(os.path.join(d, "v2-model-native", "UNBUILT.json")),
           "16 an unbuilt variant with no UNBUILT marker is refused",
           "missing model.ifc")

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

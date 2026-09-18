#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Is every DERIVED VIEW built from the model that is on disk right now?

⚠️⚠️ WHY THIS EXISTS
On 2026-09-18 Codex and Antigravity independently found the same defect: the
committed GLB painted **18** walls while the IFC beside it carried **24**,
exported a day and a half earlier, and `tools/blender/walk_viewer.html` loaded it
with **nothing checking**. The picture looked complete and showed a building that
no longer existed.

That is the "persuasive visualization becoming a second, weaker model" risk in
its simplest form, and it is the same shape as two defects this project had
already fixed elsewhere: the retired schematic that `compare_variants.py` kept
reading, and the acceptance record that said an approval "lapses" while nothing
read the file. **A record of provenance that nobody verifies provides none of the
protection it describes.**

⚠️ SO THE CHECK RECOMPUTES THE HASH EVERY RUN. It never trusts a stored
comparison, and it fails loudly rather than warning - a warning on a view is
exactly what got ignored for two days.

⚠️⚠️ 24 IfcWall IS CORRECT, AND MUST NOT BE "REPAIRED" BACK TO 25.
The compiler resolves **25 wall records**, the spec carries 25, and the IFC holds
**24** `IfcWall`. That is not drift:

    25 compiler legs - 2 (R1a, R1b) + 1 (A_NW_CORNER) = 24 physical walls

`R1a` and `R1b` are two CALCULATION LEGS of one monolithic pour. The generator
skips both legs and emits a single physical `IfcWall` for the assembly, which is
why `C_R1a_R1b` gets no connection either - it is a construction joint inside one
casting, not a junction between two walls. Three different counts for one model
(25 / 24 / and a manifest that says 23) is exactly the kind of spread that
invites someone to "fix" the right number into a wrong one, so this gate prints
the arithmetic rather than leaving it to be rediscovered.

⚠️ `model.json` saying **23** IS a real defect, and a separate one: it counts the
walls it wrote individually and omits the merged assembly from its own total.

⚠️ IT IS NOT A GEOMETRY CHECK. It answers only "was this view built from these
bytes". Whether the IFC itself is correct is `check_dxf_closure.py`,
`check_variant_basis.py` and the IDS suite. A fresh view of a wrong model is
still a wrong model.
"""

import argparse
import hashlib
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VARIANTS = os.path.join(REPO, "data", "outputs", "variants")

# A derived view: the report that records its provenance, the artefact it
# describes, and the key naming the source it was built from.
VIEWS = (
    {"report": "glb_export.json", "artefact": "model.glb", "source_key": "ifc"},
    {"report": "view_blend.json", "artefact": "model_view_no_ceiling.blend",
     "source_key": "ifc"},
    {"report": "model_blend.json", "artefact": "model.blend", "source_key": "ifc"},
)

# ⚠ `blender_env.json` was in this table on the first run and reported "names no
# source model". It is an ENVIRONMENT PROBE - status, blender, bonsai, ifc_core -
# not a view record, so pairing it with model.blend was my error. Removing it
# exposed the real gap underneath: **model.blend is a derived view with NO
# provenance record at all**, which is worse than a stale one, because there is
# nothing for a gate to even disagree with. Hence the orphan sweep below.
VIEW_ARTEFACTS = (".glb", ".blend")
ARTEFACT_EXEMPT = ("model_view_no_ceiling.blend1",)


def orphan_views(vdir, problems):
    """Any view artefact that NO report accounts for.

    A stale view at least declares what it came from. An unaccounted one cannot
    be checked by anything, ever, and will be shown to someone eventually.
    """
    name = os.path.basename(vdir)
    claimed = set()
    for view in VIEWS:
        if os.path.exists(os.path.join(vdir, view["report"])):
            claimed.add(view["artefact"])
    for entry in sorted(os.listdir(vdir)):
        if entry in ARTEFACT_EXEMPT or entry.endswith(".blend1"):
            continue
        if not entry.endswith(VIEW_ARTEFACTS):
            continue
        if entry not in claimed:
            problems.append(
                "%s/%s: a derived view with NO provenance report. Nothing records "
                "which model it was built from, so no gate can ever check it."
                % (name, entry))


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def check_variant(vdir, problems, notes):
    name = os.path.basename(vdir)
    for view in VIEWS:
        rep_path = os.path.join(vdir, view["report"])
        art_path = os.path.join(vdir, view["artefact"])
        if not os.path.exists(rep_path):
            continue
        if not os.path.exists(art_path):
            problems.append("%s/%s: the report exists but %s does not"
                            % (name, view["report"], view["artefact"]))
            continue
        try:
            with open(rep_path, encoding="utf-8") as fh:
                rep = json.load(fh)
        except Exception as exc:                             # noqa: BLE001
            problems.append("%s/%s: unreadable (%s)" % (name, view["report"], exc))
            continue

        src = rep.get(view["source_key"])
        if not src:
            problems.append("%s/%s: names no source model" % (name, view["report"]))
            continue
        # ⚠⚠ RESOLVE AGAINST THE REPORT'S OWN DIRECTORY FIRST. Seed 5 caught this:
        # the gate resolved a relative source against REPO, so when run on a COPY
        # of the outputs it happily verified the ORIGINAL model.ifc and passed a
        # tree whose source had been deleted. A check that reads a file other
        # than the one beside the artefact is not checking that artefact. The IFC
        # a view is built from sits next to it, so that is where to look.
        # ⚠ AND NO REPO-RELATIVE FALLBACK. The first fix still fell back to
        # REPO when the file was not beside the report, and seed 5 caught that
        # too: with the copy's model.ifc deleted, the fallback found the REAL one
        # and passed. A fallback that can silently read a different file is not a
        # resolution rule, it is a way to never fail. A variant's IFC always
        # lives in the variant directory, so that is the only place to look.
        src_path = src if os.path.isabs(src) else os.path.join(
            vdir, os.path.basename(src))
        if not os.path.exists(src_path):
            problems.append("%s/%s: source %s no longer exists"
                            % (name, view["report"], src))
            continue

        recorded = rep.get("ifc_sha256")
        if not recorded:
            # ⚠ An UNSTAMPED view is not a pass. It is a view that cannot be
            # checked, which is what allowed the 18-vs-24 GLB to sit unnoticed.
            problems.append(
                "%s/%s: NO ifc_sha256 recorded, so this view cannot be verified "
                "against its source at all. Re-export it." % (name, view["report"]))
            continue

        actual = sha256(src_path)
        if actual != recorded:
            problems.append(
                "%s/%s: STALE. Built from IFC %s..., but %s is now %s.... "
                "Re-export before this view is shown to anyone."
                % (name, view["report"], recorded[:12],
                   os.path.basename(src_path), actual[:12]))
            continue

        # The shell signature is a second, independent statement about the same
        # model. When both the spec and the view carry one they must agree.
        spec_path = os.path.join(vdir, "spec.json")
        if rep.get("shell_signature") and os.path.exists(spec_path):
            try:
                with open(spec_path, encoding="utf-8") as fh:
                    spec_sig = json.load(fh).get("shell_signature")
            except Exception:                                # noqa: BLE001
                spec_sig = None
            if spec_sig and spec_sig != rep["shell_signature"]:
                problems.append(
                    "%s/%s: shell_signature disagrees with spec.json (%s... vs %s...)"
                    % (name, view["report"], str(rep["shell_signature"])[:12],
                       str(spec_sig)[:12]))
                continue
        notes.append("%s/%s fresh against %s" % (name, view["report"], os.path.basename(src_path)))


def wall_census(vdir):
    """The 25 / 24 / 23 spread, printed so nobody has to rediscover it.

    Read-only and best-effort: a missing file or a parse failure is silence, not
    a problem. This gate is about provenance, not geometry.
    """
    out = {}
    spec = os.path.join(vdir, "spec.json")
    if os.path.exists(spec):
        try:
            with open(spec, encoding="utf-8") as fh:
                out["spec_wall_records"] = len(json.load(fh).get("walls", []))
        except Exception:                                    # noqa: BLE001
            pass
    man = os.path.join(vdir, "model.json")
    if os.path.exists(man):
        try:
            with open(man, encoding="utf-8") as fh:
                out["manifest_claims"] = json.load(fh).get("walls")
        except Exception:                                    # noqa: BLE001
            pass
    ifc = os.path.join(vdir, "model.ifc")
    if os.path.exists(ifc):
        n = 0
        try:
            with open(ifc, encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    if "=IFCWALL(" in line.upper():
                        n += 1
            out["ifc_IfcWall"] = n
        except Exception:                                    # noqa: BLE001
            pass
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--variants-dir", default=VARIANTS)
    args = ap.parse_args()

    problems, notes = [], []
    if not os.path.isdir(args.variants_dir):
        print("no variants directory at %s" % args.variants_dir)
        return 0
    for entry in sorted(os.listdir(args.variants_dir)):
        vdir = os.path.join(args.variants_dir, entry)
        if os.path.isdir(vdir):
            check_variant(vdir, problems, notes)
            orphan_views(vdir, problems)

    for entry in sorted(os.listdir(args.variants_dir)):
        vdir = os.path.join(args.variants_dir, entry)
        if not os.path.isdir(vdir):
            continue
        c = wall_census(vdir)
        if c:
            print("  walls %s: spec %s records, IFC %s IfcWall, manifest claims %s"
                  % (entry, c.get("spec_wall_records", "?"), c.get("ifc_IfcWall", "?"),
                     c.get("manifest_claims", "?")))
            if (c.get("spec_wall_records") == 25 and c.get("ifc_IfcWall") == 24):
                print("        ^ CORRECT: 25 legs - 2 (R1a, R1b) + 1 (A_NW_CORNER "
                      "assembly) = 24 physical walls. Do NOT 'fix' 24 back to 25.")
            if c.get("manifest_claims") == 23 and c.get("ifc_IfcWall") == 24:
                print("        ^ but model.json says 23: it omits the merged "
                      "assembly from its own count. Real, and a separate defect.")

    for n in notes:
        print("  ok    %s" % n)
    for p in problems:
        print("  FAIL  %s" % p)
    if problems:
        print("\nFAIL - %d derived view(s) do not match the model on disk." % len(problems))
        return 1
    print("\nPASS - every derived view was built from the model currently on disk.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

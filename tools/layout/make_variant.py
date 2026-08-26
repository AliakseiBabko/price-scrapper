#!/usr/bin/env python3
"""One command from a layout variant to everything you can look at.

Describe a change in words, write it as a variant patch, run this. It applies
the patch, checks it against the constraints that may never move, builds the
model, and produces every representation: A3 sheets, a DXF for TrueView, a
Blender scene, the comparison sheet, and a refreshed gallery.

    python tools/layout/make_variant.py data/variants/v3-my-idea.json

Steps can be skipped when iterating (--no-blend is the slow one).

Two Python environments are involved and neither has everything:
  .venv-ifc314  ifcopenshell, ezdxf, numpy   - model, DXF, Blender
  .venv         pymupdf, cairosvg            - PDF rendering, gallery
so this script calls each tool with the interpreter that can run it.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
IFC_PY = REPO / ".venv-ifc314" / "Scripts" / "python.exe"
DOC_PY = REPO / ".venv" / "Scripts" / "python.exe"
BLENDER = REPO / "tools" / "blender" / "bin" / "blender-5.2.0-windows-x64" / "blender.exe"
PROFILE = REPO / "tools" / "blender" / "profile3"
BONSAI_SITE = PROFILE / "extensions" / ".local" / "lib" / "python3.13" / "site-packages"
OUTPUTS = REPO / "data" / "outputs" / "variants"
SCHEDULES = REPO / "data" / "canonical" / "room_schedules.json"


def run(label: str, argv: list[str], cwd: Path | None = None, optional: bool = False) -> dict:
    started = time.time()
    proc = subprocess.run([str(a) for a in argv], cwd=str(cwd or REPO),
                          capture_output=True, text=True, encoding="utf-8", errors="replace")
    ok = proc.returncode == 0
    result = {"step": label, "ok": ok, "seconds": round(time.time() - started, 1)}
    if not ok:
        result["error"] = (proc.stderr or proc.stdout or "")[-600:]
        print("  %-22s FAILED%s" % (label, "" if optional else "  <-- stopping"))
        print("    " + result["error"].strip().replace("\n", "\n    ")[:600])
    else:
        print("  %-22s ok   %5.1fs" % (label, result["seconds"]))
    return result


def check_constraints(variant: dict) -> list[str]:
    """Refuse to move what is common property.

    The вентблоки and the plumbing стояки belong to the building, not the flat.
    A variant that quietly assumes one of them moves would produce a drawing a
    contractor cannot build, so it is caught here rather than on site.
    """
    if not SCHEDULES.exists():
        return []
    constraints = json.loads(SCHEDULES.read_text(encoding="utf-8"))["developer_plan"].get("constraints", [])
    immovable_zones = {c.get("zone", "").lower() for c in constraints if not c.get("movable", True)}
    words = " ".join(z for z in immovable_zones).replace("/", " ").split()
    problems = []
    for op in variant.get("operations", []):
        blob = json.dumps(op, ensure_ascii=False).lower()
        if op.get("op") in {"wall.remove", "wall.reposition", "zone.merge", "zone.split"}:
            hit = [w for w in words if len(w) > 4 and w in blob]
            if hit:
                problems.append(
                    "%s touches %s, which holds immovable services (вентблок / стояки). "
                    "Confirm the block itself is untouched, or state in the variant why it does "
                    "not apply." % (op.get("op"), ", ".join(sorted(set(hit)))))
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("variant", help="path to a variant json, or a variant id")
    ap.add_argument("--no-blend", action="store_true", help="skip the Blender scene (slowest step)")
    ap.add_argument("--no-gallery", action="store_true")
    ap.add_argument("--force", action="store_true", help="build even if a constraint check fails")
    a = ap.parse_args()

    path = Path(a.variant)
    if not path.exists():
        path = REPO / "data" / "variants" / (a.variant + ".json")
    if not path.exists():
        raise SystemExit("no such variant: %s" % a.variant)
    variant = json.loads(path.read_text(encoding="utf-8"))
    vid = variant["variant_id"]
    out = OUTPUTS / vid

    print("variant %s - %s" % (vid, variant.get("name", "")))
    problems = check_constraints(variant)
    for p in problems:
        print("  CONSTRAINT  %s" % p)
    if problems and not a.force:
        print("\nStopped. Re-run with --force once you have confirmed the services are untouched.")
        return 2

    steps = [run("model + sheets", [IFC_PY, REPO / "tools" / "layout" / "build_variant.py", path])]
    if steps[-1]["ok"]:
        steps.append(run("audit geometry",
                         [IFC_PY, REPO / "tools" / "ifc" / "audit_model_quality.py",
                          "--spec", out / "spec.json", "--strict"], optional=True))
        steps.append(run("dxf for TrueView",
                         [IFC_PY, REPO / "tools" / "drawings" / "export_variant_dxf.py", vid]))
        if not a.no_blend and BLENDER.exists():
            steps.append(run("blender scene",
                             [IFC_PY, REPO / "tools" / "blender" / "verify_environment.py",
                              "--blender", BLENDER, "--profile", PROFILE,
                              "--bonsai-site", BONSAI_SITE,
                              "--ifc", out / "model.ifc",
                              "--blend-output", out / "model.blend",
                              "--output", out / "blender_env.json"], optional=True))
        steps.append(run("comparison sheet",
                         [DOC_PY, REPO / "tools" / "layout" / "compare_variants.py"], optional=True))
        if not a.no_gallery:
            steps.append(run("gallery",
                             [DOC_PY, REPO / "tools" / "drawings" / "build_gallery.py"], optional=True))

    artifacts = {
        "spec": out / "spec.json",
        "model (IFC)": out / "model.ifc",
        "A3 sheet (PDF)": out / "sheets" / "apartment_architectural_plan_a3.pdf",
        "DXF for TrueView": out / ("%s_plan.dxf" % vid),
        "Blender scene": out / "model.blend",
        "comparison": OUTPUTS / "comparison" / "variant_comparison_a3.pdf",
        "gallery": REPO / "data" / "outputs" / "gallery" / "index.html",
    }
    print("\nartifacts:")
    for label, p in artifacts.items():
        print("  %-18s %s%s" % (label, p.relative_to(REPO), "" if p.exists() else "   (not built)"))

    failed = [s for s in steps if not s["ok"]]
    print("\n%d/%d steps ok" % (len(steps) - len(failed), len(steps)))
    return 1 if any(s["step"] in {"model + sheets", "dxf for TrueView"} for s in failed) else 0


if __name__ == "__main__":
    raise SystemExit(main())

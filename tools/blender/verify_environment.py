"""Probe Blender/Bonsai availability without modifying user files or IFC data."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--blender", default="blender")
    parser.add_argument("--bonsai-site", type=Path)
    parser.add_argument("--profile", type=Path)
    parser.add_argument("--ifc", type=Path)
    parser.add_argument("--blend-output", type=Path)
    args = parser.parse_args()
    executable = shutil.which(args.blender) or (args.blender if Path(args.blender).is_file() else None)
    result = {"status": "blocked", "blender": {"requested": args.blender, "found": bool(executable)}, "bonsai": {"status": "not_checked_without_blender"}, "ifc_core": {"status": "verified_separately", "runtime": "Python 3.14 / IfcOpenShell 0.8.5"}, "decision": "Install and pin a Blender/Bonsai pair before production authoring."}
    if executable:
        probe = subprocess.run([executable, "--background", "--python-expr", "import bpy; print(bpy.app.version_string)"], capture_output=True, text=True, check=False)
        result["blender"].update({"version_probe_exit": probe.returncode, "stdout": probe.stdout[-500:], "stderr": probe.stderr[-500:]})
        result["status"] = "probe_passed" if probe.returncode == 0 else "probe_failed"
        if args.bonsai_site:
            expression = (
                f"import sys; sys.path.insert(0,r'{args.bonsai_site.resolve()}'); "
                "import bpy; r=bpy.ops.preferences.addon_enable(module='bonsai'); "
                "print('BONSAI_ENABLE',r); print('BIM_OPERATOR_COUNT',len([x for x in dir(bpy.ops.bim) if not x.startswith('_')]))"
            )
            if args.ifc and args.blend_output:
                expression += f"; r=bpy.ops.bim.load_project(filepath=r'{args.ifc.resolve()}'); print('IFC_LOAD',r); r=bpy.ops.wm.save_as_mainfile(filepath=r'{args.blend_output.resolve()}'); print('BLEND_SAVE',r)"
            env = os.environ.copy()
            if args.profile:
                profile = args.profile.resolve()
                env["BLENDER_USER_CONFIG"] = str(profile / "config")
                env["BLENDER_USER_EXTENSIONS"] = str(profile / "extensions")
            bonsai_probe = subprocess.run([executable, "--background", "--python-expr", expression], capture_output=True, text=True, check=False, env=env)
            result["bonsai"] = {"status": "probe_passed" if bonsai_probe.returncode == 0 else "probe_failed", "exit_code": bonsai_probe.returncode, "stdout": bonsai_probe.stdout[-2000:], "stderr": bonsai_probe.stderr[-2000:]}
            if bonsai_probe.returncode == 0:
                result["decision"] = "Blender/Bonsai pair verified for PoC use; production authoring still requires IFC and drawing review gates."
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    # ⚠⚠ THIS SCRIPT SAVES A model.blend, AND ITS OWN REPORT IS AN ENVIRONMENT
    # PROBE, NOT A VIEW RECORD. So the .blend it wrote carried NO provenance at
    # all - nothing said which IFC it came from, and no gate could ever check it.
    # That is worse than a stale view, which at least declares its source. The
    # environment report stays what it is; a separate provenance record goes
    # beside the artefact for tools/layout/check_view_freshness.py to read.
    if args.ifc and args.blend_output and args.blend_output.exists():
        import hashlib
        h = hashlib.sha256()
        with open(args.ifc, "rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                h.update(chunk)
        prov = {
            "ifc": str(args.ifc),
            "ifc_sha256": h.hexdigest(),
            "blend": str(args.blend_output),
            "written_by": "tools/blender/verify_environment.py",
            "note": ("provenance only. The environment probe lives in the file "
                     "named by --output and is deliberately NOT this."),
        }
        (args.blend_output.parent / "model_blend.json").write_text(
            json.dumps(prov, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

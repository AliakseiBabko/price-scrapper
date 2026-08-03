"""Build all current-apartment planned outputs in the correct order."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


DEFAULT_OUTPUT_DIR = Path("data/outputs/current_apartment")
DEFAULT_BLENDER = Path("tools/blender/bin/blender-5.2.0-windows-x64/blender.exe")


def run_command(command: list[str]) -> None:
    print(json.dumps({"running": command}, indent=2))
    completed = subprocess.run(command, check=False)
    if completed.returncode != 0:
        raise SystemExit(f"Command failed with exit code {completed.returncode}: {' '.join(command)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--blender", type=Path, default=DEFAULT_BLENDER)
    parser.add_argument("--skip-blender", action="store_true")
    args = parser.parse_args()

    output_dir = args.output_dir
    ifc_path = output_dir / "current_apartment_seed.ifc"
    manifest_path = output_dir / "current_apartment_seed.json"
    validation_path = output_dir / "current_apartment_validation.json"
    sheet_dir = output_dir / "sheets"
    blend_path = output_dir / "current_apartment_seed_services.blend"
    render_dir = output_dir / "renders"

    run_command(
        [
            sys.executable,
            "tools/ifc/current_apartment_layout.py",
            "--output",
            str(ifc_path),
            "--manifest",
            str(manifest_path),
        ]
    )
    run_command(
        [
            sys.executable,
            "tools/ifc/validate_current_apartment_seed.py",
            "--ifc",
            str(ifc_path),
            "--manifest",
            str(manifest_path),
            "--output",
            str(validation_path),
        ]
    )
    run_command(
        [
            sys.executable,
            "tools/drawings/apartment_sheet_from_ifc.py",
            "--ifc",
            str(ifc_path),
            "--manifest",
            str(manifest_path),
            "--output-dir",
            str(sheet_dir),
            "--sheet-set",
        ]
    )

    if not args.skip_blender:
        if not args.blender.is_file():
            raise SystemExit(f"Blender executable not found: {args.blender}")
        run_command(
            [
                str(args.blender),
                "--background",
                "--python",
                "tools/blender/build_apartment_demo.py",
                "--",
                "--ifc",
                str(ifc_path),
                "--manifest",
                str(manifest_path),
                "--output-blend",
                str(blend_path),
                "--render-dir",
                str(render_dir),
            ]
        )

    print(
        json.dumps(
            {
                "status": "built",
                "ifc": str(ifc_path),
                "manifest": str(manifest_path),
                "validation": str(validation_path),
                "sheets": str(sheet_dir),
                "blend": None if args.skip_blender else str(blend_path),
                "renders": None if args.skip_blender else str(render_dir),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Create a repeatable, non-destructive intake report for DWG/DXF sources."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

DWG_VERSIONS = {b"AC1021": "AutoCAD 2007", b"AC1024": "AutoCAD 2010", b"AC1027": "AutoCAD 2013", b"AC1032": "AutoCAD 2018"}
DXF_UNITS = {0: "unitless", 1: "inches", 2: "feet", 4: "millimetres", 5: "centimetres", 6: "metres"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def inspect_dxf(path: Path) -> dict:
    try:
        import ezdxf  # type: ignore
    except ImportError:
        return {"status": "not_run", "reason": "ezdxf is not installed"}
    try:
        doc = ezdxf.readfile(path)
        code = int(doc.header.get("$INSUNITS", 0) or 0)
        return {
            "status": "ok", "version": doc.dxfversion,
            "header_insunits": code, "header_units_label": DXF_UNITS.get(code, "unknown"),
            "measurement_mode": doc.header.get("$MEASUREMENT"),
            "entity_count": len(doc.modelspace()),
            "dimension_entity_count": len(doc.modelspace().query("DIMENSION")),
            "dimension_samples_mm": [round(entity.get_measurement(), 3) for entity in list(doc.modelspace().query("DIMENSION"))[:20] if not entity.dxf.text],
            "layers": sorted(layer.dxf.name for layer in doc.layers),
        }
    except Exception as exc:
        return {"status": "failed", "reason": str(exc)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--dxf", type=Path)
    parser.add_argument("--expected-units", choices=["mm", "cm", "m", "in", "ft"])
    parser.add_argument("--control-dimensions", type=Path)
    parser.add_argument("--convert", action="store_true", help="Convert one DWG to DXF using the installed ODA converter")
    parser.add_argument("--converter", type=Path, default=Path("C:/Users/User/AppData/Local/Programs/ODA/ODAFileConverter 27.1.0/ODAFileConverter.exe"))
    args = parser.parse_args()
    if not args.source.is_file():
        raise SystemExit(f"Source not found: {args.source}")
    suffix = args.source.suffix.lower()
    header = args.source.read_bytes()[:6]
    report = {
        "source": str(args.source), "source_hash_sha256": sha256(args.source),
        "source_size_bytes": args.source.stat().st_size, "source_type": suffix.lstrip("."),
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "underlay_policy": "reference-only; original retained in inbox",
        "conversion": {"status": "not_run", "converter": None},
        "unit_verification": {"status": "pending", "expected_units": args.expected_units, "evidence": []},
        "control_dimensions": {"status": "pending", "checks": []},
        "canonical_model": {"status": "not_generated", "reason": "source geometry is not approved yet"},
    }
    if suffix == ".dwg":
        report["dwg_header"] = {"signature": header.decode("ascii", errors="replace"), "release": DWG_VERSIONS.get(header, "unknown")}
        report["conversion"]["reason"] = "No DWG-to-DXF converter detected; rerun with --dxf after dedicated conversion."
        if args.convert:
            if not args.converter.is_file():
                raise SystemExit(f"ODA converter not found: {args.converter}")
            with tempfile.TemporaryDirectory(prefix="price-scrapper-oda-") as staging:
                source_dir, target_dir = Path(staging) / "source", Path(staging) / "dxf"
                source_dir.mkdir()
                target_dir.mkdir()
                staged_source = source_dir / args.source.name
                shutil.copy2(args.source, staged_source)
                command = [str(args.converter), str(source_dir), str(target_dir), "ACAD2018", "DXF", "0", "1"]
                completed = subprocess.run(command, capture_output=True, text=True, check=False, timeout=180)
                generated = target_dir / f"{args.source.stem}.dxf"
                if completed.returncode != 0 or not generated.is_file():
                    raise SystemExit(f"ODA conversion failed: exit={completed.returncode}; {completed.stderr[-500:]}")
                converted_path = args.report.parent / "dxf" / generated.name
                converted_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(generated, converted_path)
                args.dxf = converted_path
                report["conversion"] = {"status": "completed", "converter": str(args.converter), "dxf": str(converted_path), "dxf_hash_sha256": sha256(converted_path)}
    elif suffix == ".dxf":
        report["dxf_inspection"] = inspect_dxf(args.source)
        report["conversion"] = {"status": "not_required", "converter": "source is already DXF"}
    else:
        raise SystemExit("Only DWG and DXF sources are supported")
    if args.dxf:
        if not args.dxf.is_file():
            raise SystemExit(f"DXF not found: {args.dxf}")
        if report["conversion"].get("status") != "completed":
            report["conversion"] = {"status": "provided", "converter": "external/dedicated", "dxf": str(args.dxf), "dxf_hash_sha256": sha256(args.dxf)}
        report["dxf_inspection"] = inspect_dxf(args.dxf)
        if report["dxf_inspection"].get("status") == "ok":
            report["unit_verification"] = {"status": "header_observed_manual_confirmation_required", "expected_units": args.expected_units, "observed_units": report["dxf_inspection"].get("header_units_label"), "evidence": ["DXF $INSUNITS header; verify against a known apartment dimension before scaling"]}
    if args.control_dimensions:
        report["control_dimensions"] = {"status": "recorded_manual_measurement_required", "checks": json.loads(args.control_dimensions.read_text(encoding="utf-8"))}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote intake report: {args.report}")
    print("Source retained; no archive or geometry transformation performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

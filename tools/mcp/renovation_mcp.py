"""Safe line-oriented agent boundary for validated renovation operations.

This is intentionally a local JSON-lines adapter, not an unrestricted shell
or arbitrary Python executor. Each operation has fixed arguments and paths.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PYTHON = ROOT / ".venv-ifc314" / "Scripts" / "python.exe"


def run_operation(request: dict) -> dict:
    operation = request.get("operation")
    allowed = {"validate_canonical", "generate_ifc", "validate_design"}
    if operation not in allowed:
        return {"ok": False, "error": f"Operation not allowed: {operation}", "allowed": sorted(allowed)}
    commands = {
        "validate_canonical": ["tools/ifc/validate_canonical.py", "--schema", "schemas/renovation-model.schema.json", "--input", request.get("input", "data/canonical/apartment_poc.json")],
        "generate_ifc": ["tools/ifc/poc_renovation.py", "--input", request.get("input", "data/canonical/apartment_poc.json"), "--output-dir", request.get("output_dir", "data/outputs/ifc-poc")],
        "validate_design": ["tools/design/validate_design.py", "--input", request.get("input", "data/canonical/apartment_design.json"), "--output", request.get("output", "data/outputs/design_validation.json")],
    }
    args = [str(PYTHON), *commands[operation]]
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, check=False)
    return {"ok": result.returncode == 0, "operation": operation, "exit_code": result.returncode, "stdout": result.stdout[-4000:], "stderr": result.stderr[-4000:]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", type=Path)
    args = parser.parse_args()
    requests = [json.loads(args.request.read_text(encoding="utf-8"))] if args.request else [json.loads(line) for line in sys.stdin if line.strip()]
    for request in requests:
        print(json.dumps(run_operation(request), ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

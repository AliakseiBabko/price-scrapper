"""Register external/AI assets without allowing them into QTO automatically."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--asset", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-url")
    parser.add_argument("--license", default="unknown")
    parser.add_argument("--declared-width-m", type=float)
    parser.add_argument("--declared-depth-m", type=float)
    parser.add_argument("--declared-height-m", type=float)
    args = parser.parse_args()
    if not args.asset.is_file():
        raise SystemExit(f"Asset not found: {args.asset}")
    digest = hashlib.sha256(args.asset.read_bytes()).hexdigest()
    result = {"asset": str(args.asset), "sha256": digest, "source_url": args.source_url, "license": args.license, "declared_dimensions_m": {"width": args.declared_width_m, "depth": args.declared_depth_m, "height": args.declared_height_m}, "scale_status": "pending_manual_verification", "qto_eligible": False, "metadata_status": "visual_asset_metadata_separate_from_ifc"}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Registered asset without QTO eligibility: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

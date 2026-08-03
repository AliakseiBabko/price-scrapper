"""Validate design JSON and report conceptual MEP clashes and lighting estimates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    model = json.loads(args.input.read_text(encoding="utf-8"))
    errors, warnings = [], []
    rooms = {room["room_id"]: room for room in model.get("rooms", [])}
    for item in model.get("furniture", []):
        room = rooms.get(item.get("room_id"))
        if not room:
            errors.append(f"Furniture {item.get('item_id')} references unknown room")
            continue
        if item["x_m"] + item["width_m"] > room["length_m"] or item["y_m"] + item["depth_m"] > room["width_m"]:
            errors.append(f"Furniture {item.get('item_id')} exceeds room boundary")
        if not item.get("verified_dimensions", False):
            warnings.append(f"Furniture {item.get('item_id')} is not dimension verified")
    mep_items = [item for discipline in model.get("mep", {}).values() for item in discipline]
    for item in mep_items:
        room = rooms.get(item.get("room_id"))
        if not room:
            errors.append(f"MEP {item.get('id')} references unknown room")
            continue
        if not (0 <= item.get("x_m", -1) <= room["length_m"] and 0 <= item.get("y_m", -1) <= room["width_m"]):
            errors.append(f"MEP {item.get('id')} is outside room boundary")
    for i, left in enumerate(mep_items):
        for right in mep_items[i + 1:]:
            if left.get("room_id") == right.get("room_id") and abs(left.get("x_m", 0) - right.get("x_m", 0)) < 0.1 and abs(left.get("y_m", 0) - right.get("y_m", 0)) < 0.1:
                warnings.append(f"Conceptual MEP clash: {left.get('id')} / {right.get('id')}")
    lighting = []
    for scenario in model.get("lighting_scenarios", []):
        room = rooms.get(scenario.get("room_id"))
        area = room["length_m"] * room["width_m"] if room else 0
        estimated_lux = scenario.get("fixture_count", 0) * scenario.get("fixture_lumens", 0) * scenario.get("dimming", 1) * 0.6 / area if area else 0
        lighting.append({"scenario_id": scenario.get("scenario_id"), "estimated_average_lux": round(estimated_lux, 1), "target_lux": scenario.get("target_lux"), "status": "visual_estimate_not_lux_validated"})
    result = {"status": "valid" if not errors else "invalid", "errors": errors, "warnings": warnings, "lighting_estimates": lighting, "engineering_boundary": "MEP and lux results are conceptual; licensed design and specialist simulation remain required."}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

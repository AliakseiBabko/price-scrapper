#!/usr/bin/env python3
"""Apply a layout variant to the base apartment spec and draw it.

A variant is a patch, not a copy: a list of typed operations in the same
vocabulary the layout-case dataset uses for what architects do to a plan
(`wall.remove`, `zone.merge`, `opening.create`, …). Keeping variants as
patches means the base geometry has one definition, the diff between two
options is readable, and a variant can cite the rule or case that suggested it.

Output per variant: the derived spec, an IFC, and A3 sheets.

Usage:
  python tools/layout/build_variant.py data/variants/v1-kitchen-living.json
  python tools/layout/build_variant.py --all
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
VARIANTS = REPO / "data" / "variants"
OUTPUTS = REPO / "data" / "outputs" / "variants"
IFC_PYTHON = REPO / ".venv-ifc314" / "Scripts" / "python.exe"


def find_room(spec, name):
    for r in spec["rooms"]:
        if r["name"] == name:
            return r
    raise SystemExit("no room named %r" % name)


def rect_union(a, b):
    x0 = min(a["x_m"], b["x_m"])
    y0 = min(a["y_m"], b["y_m"])
    x1 = max(a["x_m"] + a["width_m"], b["x_m"] + b["width_m"])
    y1 = max(a["y_m"] + a["depth_m"], b["y_m"] + b["depth_m"])
    return x0, y0, x1 - x0, y1 - y0


def apply_op(spec: dict, op: dict, log: list[str]) -> None:
    kind = op["op"]

    if kind == "wall.remove":
        names = op["walls"]
        found = [w for w in spec["walls"] if w["name"] in names]
        if len(found) != len(names):
            missing = set(names) - {w["name"] for w in found}
            raise SystemExit("wall.remove: no such wall(s): %s" % ", ".join(sorted(missing)))
        for w in found:
            # Kept in the model, flagged: the demolition sheet has to draw it.
            w["phase"] = "demolished"
        # openings and fills hosted by a demolished wall go with it
        for o in spec["openings"]:
            if o["host_wall"] in names:
                o["phase"] = "demolished"
        log.append("demolished %d wall(s): %s" % (len(found), ", ".join(names)))

    elif kind == "wall.add":
        w = dict(op["wall"])
        w.setdefault("phase", "new")
        w.setdefault("kind", "partition")
        w.setdefault("thickness_m", spec.get("default_wall_thickness_m", 0.15))
        spec["walls"].append(w)
        log.append("new wall %r" % w["name"])

    elif kind == "wall.thicken":
        w = next((x for x in spec["walls"] if x["name"] == op["wall"]), None)
        if w is None:
            raise SystemExit("wall.thicken: no such wall %r" % op["wall"])
        w["thickness_m"] = op["to_m"]
        w["phase"] = "modified"
        log.append("thickened %r to %d mm" % (w["name"], round(op["to_m"] * 1000)))

    elif kind == "opening.create":
        o = dict(op["opening"])
        o.setdefault("phase", "new")
        o.setdefault("bottom_m", 0.0)
        o.setdefault("height_m", 2.07)
        spec["openings"].append(o)
        log.append("new %s opening %r" % (o.get("kind", "door"), o["name"]))

    elif kind == "opening.remove":
        before = len(spec["openings"])
        spec["openings"] = [o for o in spec["openings"] if o["name"] not in op["openings"]]
        spec["fills"] = [f for f in spec["fills"] if f["name"] not in op.get("fills", [])]
        log.append("removed %d opening(s)" % (before - len(spec["openings"])))

    elif kind == "zone.merge":
        a, b = find_room(spec, op["rooms"][0]), find_room(spec, op["rooms"][1])
        x, y, w, d = rect_union(a, b)
        merged = {
            "name": op["into"], "x_m": round(x, 2), "y_m": round(y, 2),
            "width_m": round(w, 2), "depth_m": round(d, 2),
            "area_m2": round(a["area_m2"] + b["area_m2"], 2),
            "role": op.get("role", a.get("role", "other")),
            "source": "merged from %s + %s" % (a["name"], b["name"]),
        }
        spec["rooms"] = [r for r in spec["rooms"] if r["name"] not in op["rooms"]] + [merged]
        for wall_name, rooms in list((spec.get("space_boundaries") or {}).items()):
            spec["space_boundaries"][wall_name] = [op["into"] if r in op["rooms"] else r for r in rooms]
        for old in op["rooms"]:
            positions = (spec.get("electrical_plan") or {}).pop(old, None)
            if positions:
                spec["electrical_plan"].setdefault(op["into"], []).extend(positions)
            for p in spec.get("plumbing_plan") or []:
                if p["room"] == old:
                    p["room"] = op["into"]
        log.append("merged %s + %s -> %s (%.2f m2)"
                   % (a["name"], b["name"], merged["name"], merged["area_m2"]))

    elif kind == "room.resize":
        r = find_room(spec, op["room"])
        for key in ("x_m", "y_m", "width_m", "depth_m", "area_m2", "role"):
            if key in op:
                r[key] = op[key]
        log.append("resized %r to %.2f m2" % (r["name"], r["area_m2"]))

    elif kind == "furniture.place":
        spec.setdefault("furniture", []).append(dict(op["item"]))
        log.append("placed %r in %s" % (op["item"]["name"], op["item"].get("room", "?")))

    elif kind == "finish.set":
        spec.setdefault("finishes", {})[op["room"]] = op["finish"]
        log.append("finishes set for %s" % op["room"])

    elif kind == "circuit.assign":
        spec.setdefault("circuits", {}).update(op["circuits"])
        log.append("assigned %d lighting circuit(s)" % len(op["circuits"]))

    else:
        raise SystemExit("unknown op %r - extend apply_op or fix the variant" % kind)


def build_one(variant_path: Path, render: bool) -> dict:
    variant = json.loads(variant_path.read_text(encoding="utf-8"))
    base_path = REPO / variant["base_spec"]
    spec = json.loads(base_path.read_text(encoding="utf-8"))

    spec["spec_id"] = variant["variant_id"]
    spec["name"] = variant["name"]
    spec["derived_from"] = variant["base_spec"]
    spec["status"] = variant.get("status", "draft")

    log: list[str] = []
    for op in variant.get("operations", []):
        apply_op(spec, op, log)

    out = OUTPUTS / variant["variant_id"]
    out.mkdir(parents=True, exist_ok=True)
    spec_out = out / "spec.json"
    spec_out.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    result = {"variant_id": variant["variant_id"], "spec": str(spec_out.relative_to(REPO)),
              "operations_applied": log}

    proc = subprocess.run(
        [str(IFC_PYTHON), "model_from_spec.py", "--spec", str(spec_out),
         "--output", str(out / "model.ifc"), "--manifest", str(out / "model.json")],
        cwd=str(REPO / "tools" / "ifc"), capture_output=True, text=True, encoding="utf-8")
    if proc.returncode != 0:
        raise SystemExit("model build failed for %s:\n%s" % (variant["variant_id"], proc.stderr[-2000:]))
    result["model"] = json.loads(proc.stdout)

    if render:
        proc = subprocess.run(
            [str(IFC_PYTHON), str(REPO / "tools" / "drawings" / "apartment_sheet_from_ifc.py"),
             "--ifc", str(out / "model.ifc"), "--manifest", str(out / "model.json"),
             "--output-dir", str(out / "sheets"), "--sheet-kind", "architectural"],
            capture_output=True, text=True, encoding="utf-8")
        if proc.returncode != 0:
            result["sheet_error"] = proc.stderr[-800:]
        else:
            result["sheets"] = sorted(p.name for p in (out / "sheets").glob("*.pdf"))
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("variant", nargs="?", help="path to a variant json; omit with --all")
    ap.add_argument("--all", action="store_true", help="build every variant in data/variants/")
    ap.add_argument("--no-render", action="store_true", help="model only, skip the sheets")
    a = ap.parse_args()

    paths = sorted(VARIANTS.glob("*.json")) if a.all else [Path(a.variant)]
    if not paths:
        raise SystemExit("nothing to build")
    results = [build_one(p, render=not a.no_render) for p in paths]
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

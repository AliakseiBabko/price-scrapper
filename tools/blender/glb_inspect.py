"""Read a .glb without Blender and report what is actually inside it.

A GLB is a 12-byte header followed by chunks; the first chunk is the glTF JSON.
Parsing it directly means the check does not trust the exporter's own report -
the same reason this repo's DXF gates re-derive geometry from the source PDF
rather than from the file under test.

Used two ways:
  - as the verdict half of `glb_material_probe.py` (with --expect <probe.json>)
  - standalone, to describe any exported model (`--glb model.glb`)
"""

from __future__ import annotations

import argparse
import json
import struct
from pathlib import Path

GLB_MAGIC = 0x46546C67  # 'glTF'
CHUNK_JSON = 0x4E4F534A  # 'JSON'


def read_glb_json(path: Path) -> dict:
    data = path.read_bytes()
    if len(data) < 12:
        raise ValueError("%s is too short to be a GLB" % path)
    magic, version, total = struct.unpack_from("<III", data, 0)
    if magic != GLB_MAGIC:
        raise ValueError("%s is not a GLB (bad magic)" % path)
    if total != len(data):
        raise ValueError("%s declares %d bytes but is %d" % (path, total, len(data)))
    offset = 12
    while offset < len(data):
        length, kind = struct.unpack_from("<II", data, offset)
        offset += 8
        if kind == CHUNK_JSON:
            return json.loads(data[offset:offset + length].decode("utf-8"))
        offset += length + (-length % 4)
    raise ValueError("%s has no JSON chunk" % path)


def summarise(doc: dict) -> dict:
    mats = []
    for m in doc.get("materials", []):
        pbr = m.get("pbrMetallicRoughness", {}) or {}
        mats.append({
            "name": m.get("name"),
            "baseColorFactor": pbr.get("baseColorFactor"),
            "metallicFactor": pbr.get("metallicFactor"),
            "roughnessFactor": pbr.get("roughnessFactor"),
            "has_baseColorTexture": "baseColorTexture" in pbr,
        })
    return {
        "generator": (doc.get("asset") or {}).get("generator"),
        "gltf_version": (doc.get("asset") or {}).get("version"),
        "counts": {k: len(doc.get(k, [])) for k in
                   ("scenes", "nodes", "meshes", "materials", "textures", "images", "accessors")},
        "mesh_names": [m.get("name") for m in doc.get("meshes", [])],
        "node_names": [n.get("name") for n in doc.get("nodes", [])],
        "materials": mats,
    }


def close(a, b, tol=1e-3) -> bool:
    return a is not None and b is not None and abs(float(a) - float(b)) <= tol


def verdict(summary: dict, expect: dict) -> dict:
    by_name = {m["name"]: m for m in summary["materials"]}
    results, failures = [], []
    for case in expect["cases"]:
        name = case["material"]
        got = by_name.get(name)
        row = {"material": name, "kind": case["kind"], "present_in_glb": got is not None}
        if got is None:
            # For the negative control an absent material is one valid outcome.
            row["survived"] = False
        else:
            bcf = got["baseColorFactor"]
            want = case.get("expect_base_color_factor")
            if want is None:
                # Negative control: it "survived" only if a real colour came
                # through. glTF's default white (1,1,1,1) means the network was
                # dropped, which is the expected failure.
                row["baseColorFactor"] = bcf
                row["survived"] = bool(bcf) and not all(close(x, y) for x, y in zip(bcf, [1, 1, 1, 1]))
            else:
                row["baseColorFactor"] = bcf
                row["survived"] = bool(bcf) and all(close(x, y) for x, y in zip(bcf, want))
                if "expect_roughness" in case:
                    row["roughness_ok"] = close(got["roughnessFactor"], case["expect_roughness"])
                    row["roughnessFactor"] = got["roughnessFactor"]
                if "expect_metallic" in case:
                    row["metallic_ok"] = close(got["metallicFactor"], case["expect_metallic"])
                    row["metallicFactor"] = got["metallicFactor"]
        results.append(row)

    flat = [r for r in results if r["kind"].startswith("flat")]
    ctrl = [r for r in results if r["kind"].endswith("negative_control")]

    for r in flat:
        if not r["survived"]:
            failures.append("flat material %s did not survive" % r["material"])
        for k in ("roughness_ok", "metallic_ok"):
            if k in r and not r[k]:
                failures.append("%s: %s mismatch" % (r["material"], k))
    for r in ctrl:
        if r["survived"]:
            failures.append(
                "NEGATIVE CONTROL %s survived - the probe is not testing what it "
                "claims, so the flat result cannot be trusted either" % r["material"])

    return {
        "results": results,
        "flat_base_colour_survives": all(r["survived"] for r in flat) if flat else None,
        "procedural_dropped_as_expected": all(not r["survived"] for r in ctrl) if ctrl else None,
        "failures": failures,
        "pass": not failures,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--glb", type=Path, required=True)
    ap.add_argument("--expect", type=Path, help="probe JSON; enables the pass/fail verdict")
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()

    doc = read_glb_json(args.glb)
    report = {"glb": str(args.glb), "bytes": args.glb.stat().st_size, "summary": summarise(doc)}

    rc = 0
    if args.expect:
        report["verdict"] = verdict(report["summary"], json.loads(args.expect.read_text(encoding="utf-8")))
        rc = 0 if report["verdict"]["pass"] else 1

    text = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())

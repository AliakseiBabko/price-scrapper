import json, io, os, collections
os.chdir(r"c:\Users\User\Documents\price-scrapper")

poly = json.load(io.open("data/cad/room_polygons.json", encoding="utf-8"))

ROLE = {
    "Kids Room": "kids", "Living and Dining Room": "living", "Kitchen": "kitchen",
    "Bedroom small": "bedroom", "Balcony": "balcony", "Hallway": "hallway",
    "Bathroom": "bathroom", "Entrance": "entrance", "Laundry Room": "laundry", "WC": "wc",
}

rooms = []
for r in poly["rooms"]:
    rooms.append({
        "name": r["name"],
        "role": ROLE.get(r["name"], "other"),
        # The AREA is Homestyler's own figure - exact. The BOX is recovered
        # geometry and only good enough to place the room and its label.
        "area_m2": r["label_area_m2"],
        "x_m": round(r["x_mm"] / 1000, 3),
        "y_m": round(r["y_mm"] / 1000, 3),
        "width_m": round(r["width_mm"] / 1000, 3),
        "depth_m": round(r["depth_mm"] / 1000, 3),
        "perimeter_m": r["perimeter_m"],
        "source": "area and perimeter from the DWG room label; extent grown from that label's seed",
        "extent_confidence": "good" if r["trustworthy"] else "approximate",
        "extent_delta_pct": r["delta_pct"],
    })

# the owner's layout: the CAD spec and the v1 variant both describe it
p = "data/canonical/current_apartment_cad.json"
spec = json.load(io.open(p, encoding="utf-8"), object_pairs_hook=collections.OrderedDict)
spec["rooms"] = rooms
spec["evidence"]["rooms_status"] = (
    "SOLVED for names, areas and perimeters: Homestyler writes them into the DWG on layer "
    "'P-Comment Text' as e.g. 'Kids Room S:15.28m² C:18.43m'. Those numbers are authoritative. "
    "Room OUTLINES are still approximate - each room is grown from its label's seed and checked "
    "against its own area, and the per-room error is carried in extent_delta_pct. Use the areas "
    "for quantities; use the boxes only to place things."
)
spec["room_probe"] = "superseded by the label-seeded growth; see data/cad/room_polygons.json"
io.open(p, "w", encoding="utf-8").write(json.dumps(spec, ensure_ascii=False, indent=2) + "\n")

v = "data/variants/v1-homestyler.json"
var = json.load(io.open(v, encoding="utf-8"), object_pairs_hook=collections.OrderedDict)
var["operations"] = [op for op in var["operations"] if op["op"] != "room.add"]
for r in rooms:
    var["operations"].append({"op": "room.add", "room": r})
var["room_schedule"] = [{"name": r["name"], "role": r["role"], "area_m2": r["area_m2"],
                         "perimeter_m": r["perimeter_m"]} for r in rooms]
io.open(v, "w", encoding="utf-8").write(json.dumps(var, ensure_ascii=False, indent=2) + "\n")

print("injected %d rooms; total %.2f m2" % (len(rooms), sum(r["area_m2"] for r in rooms)))
print("good extents: %d, approximate: %d"
      % (sum(1 for r in rooms if r["extent_confidence"] == "good"),
         sum(1 for r in rooms if r["extent_confidence"] != "good")))

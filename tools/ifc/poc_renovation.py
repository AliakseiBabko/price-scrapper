"""Deterministic IFC geometry PoC for the renovation project.

This is intentionally independent of Blender, Bonsai, MCP, and cloud assets.
It creates a small IFC4 model from canonical JSON, validates the relationships
needed by the fixture, and writes a transparent quantity report.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path

import ifcopenshell
import ifcopenshell.api
import ifcopenshell.geom
from ifcopenshell.guid import new as new_guid
from jsonschema import Draft202012Validator


def load_input(path: Path, schema_path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(schema).iter_errors(data),
        key=lambda error: list(error.path),
    )
    if errors:
        details = "; ".join(error.message for error in errors)
        raise ValueError(f"Canonical model schema validation failed: {details}")
    dimensions = data["room_dimensions"]
    required = ("length", "width", "height", "wall_thickness")
    missing = [key for key in required if key not in dimensions]
    if missing:
        raise ValueError(f"Missing room dimensions: {', '.join(missing)}")
    if data.get("units") != "m":
        raise ValueError("The PoC input must use metres explicitly.")
    return data


def add_owner_history(model: ifcopenshell.file):
    person = model.create_entity("IfcPerson", Identification="poc-user")
    organisation = model.create_entity(
        "IfcOrganization", Identification="price-scrapper", Name="price-scrapper"
    )
    user = model.create_entity(
        "IfcPersonAndOrganization", ThePerson=person, TheOrganization=organisation
    )
    application = model.create_entity(
        "IfcApplication",
        ApplicationDeveloper=organisation,
        Version="0.1.0",
        ApplicationFullName="price-scrapper IFC PoC",
        ApplicationIdentifier="PRICE-SCRAPPER-POC",
    )
    return model.create_entity(
        "IfcOwnerHistory",
        OwningUser=user,
        OwningApplication=application,
        ChangeAction="ADDED",
        LastModifiedDate=int(time.time()),
        LastModifyingUser=user,
        LastModifyingApplication=application,
        CreationDate=int(time.time()),
    )


def create_product(model, ifc_class: str, name: str, owner_history):
    product = ifcopenshell.api.run(
        "root.create_entity", model, ifc_class=ifc_class, name=name
    )
    if hasattr(product, "OwnerHistory") and product.OwnerHistory is None:
        product.OwnerHistory = owner_history
    return product


def placement(model, x: float, y: float, z: float, rotation_degrees: float):
    radians = math.radians(rotation_degrees)
    origin = model.create_entity("IfcCartesianPoint", Coordinates=(x, y, z))
    axis = model.create_entity(
        "IfcDirection", DirectionRatios=(0.0, 0.0, 1.0)
    )
    reference = model.create_entity(
        "IfcDirection", DirectionRatios=(math.cos(radians), math.sin(radians), 0.0)
    )
    relative = model.create_entity(
        "IfcAxis2Placement3D", Location=origin, Axis=axis, RefDirection=reference
    )
    return model.create_entity(
        "IfcLocalPlacement", PlacementRelTo=None, RelativePlacement=relative
    )


def extruded_representation(
    model,
    body_context,
    x_dimension: float,
    y_dimension: float,
    height: float,
):
    profile_origin = model.create_entity(
        "IfcCartesianPoint", Coordinates=(0.0, 0.0)
    )
    profile_position = model.create_entity(
        "IfcAxis2Placement2D", Location=profile_origin
    )
    profile = model.create_entity(
        "IfcRectangleProfileDef",
        ProfileType="AREA",
        ProfileName="Rectangular PoC profile",
        Position=profile_position,
        XDim=x_dimension,
        YDim=y_dimension,
    )
    solid_position = model.create_entity(
        "IfcAxis2Placement3D",
        Location=model.create_entity(
            "IfcCartesianPoint", Coordinates=(0.0, 0.0, 0.0)
        ),
    )
    solid = model.create_entity(
        "IfcExtrudedAreaSolid",
        SweptArea=profile,
        Position=solid_position,
        ExtrudedDirection=model.create_entity(
            "IfcDirection", DirectionRatios=(0.0, 0.0, 1.0)
        ),
        Depth=height,
    )
    return model.create_entity(
        "IfcProductDefinitionShape",
        Representations=[
            model.create_entity(
                "IfcShapeRepresentation",
                ContextOfItems=body_context,
                RepresentationIdentifier="Body",
                RepresentationType="SweptSolid",
                Items=[solid],
            )
        ],
    ), solid


def add_relationship(model, relation_class, owner_history, **attributes):
    return model.create_entity(
        relation_class,
        GlobalId=new_guid(),
        OwnerHistory=owner_history,
        **attributes,
    )


def build_model(data: dict, output_path: Path) -> dict:
    model = ifcopenshell.file(schema="IFC4")
    owner_history = add_owner_history(model)

    project = create_product(model, "IfcProject", data["project_name"], owner_history)
    ifcopenshell.api.run(
        "unit.assign_unit",
        model,
        length={"is_metric": True, "raw": "METERS"},
        area={"is_metric": True, "raw": "SQUARE_METERS"},
        volume={"is_metric": True, "raw": "CUBIC_METERS"},
    )
    model_context = ifcopenshell.api.run(
        "context.add_context", model, context_type="Model"
    )
    body_context = ifcopenshell.api.run(
        "context.add_context",
        model,
        context_type="Model",
        context_identifier="Body",
        target_view="MODEL_VIEW",
        parent=model_context,
    )
    project.RepresentationContexts = [model_context]

    site = create_product(model, "IfcSite", "PoC site", owner_history)
    building = create_product(model, "IfcBuilding", "PoC building", owner_history)
    storey = create_product(model, "IfcBuildingStorey", data["storey_name"], owner_history)
    ifcopenshell.api.run("aggregate.assign_object", model, products=[site], relating_object=project)
    ifcopenshell.api.run("aggregate.assign_object", model, products=[building], relating_object=site)
    ifcopenshell.api.run("aggregate.assign_object", model, products=[storey], relating_object=building)

    dims = data["room_dimensions"]
    length = float(dims["length"])
    width = float(dims["width"])
    height = float(dims["height"])
    thickness = float(dims["wall_thickness"])

    # Each local profile is x-by-y, then rotated into the room perimeter.
    wall_specs = [
        ("South Wall", length, thickness, 0.0, 0.0, 0.0),
        ("East Wall", width, thickness, length, 0.0, 90.0),
        ("North Wall", length, thickness, length, width, 180.0),
        ("West Wall", width, thickness, 0.0, width, 270.0),
    ]
    walls = []
    for name, x_dim, y_dim, x, y, rotation in wall_specs:
        wall = create_product(model, "IfcWall", name, owner_history)
        wall.Representation, _ = extruded_representation(
            model, body_context, x_dim, y_dim, height
        )
        wall.ObjectPlacement = placement(model, x, y, 0.0, rotation)
        ifcopenshell.api.run("spatial.assign_container", model, products=[wall], relating_structure=storey)
        walls.append(wall)

    slab = create_product(model, "IfcSlab", "Floor slab", owner_history)
    slab.Representation, _ = extruded_representation(
        model, body_context, length, width, 0.15
    )
    slab.ObjectPlacement = placement(model, 0.0, 0.0, -0.15, 0.0)
    ifcopenshell.api.run("spatial.assign_container", model, products=[slab], relating_structure=storey)

    # A space is deliberately included because IfcConvert's SVG floor-plan
    # mode uses IfcSpace as its default inclusion target.  This is a simple
    # geometric room proxy, not a claim that space boundaries are fully
    # authored yet.
    space = create_product(model, "IfcSpace", "Apartment room", owner_history)
    space.Representation, _ = extruded_representation(
        model,
        body_context,
        max(length - 2 * thickness, 0.01),
        max(width - 2 * thickness, 0.01),
        0.01,
    )
    space.ObjectPlacement = placement(model, thickness, thickness, 0.0, 0.0)
    # IfcSpace is a spatial element rather than a normal physical product;
    # it is aggregated under the storey rather than put in a
    # IfcRelContainedInSpatialStructure relation.
    ifcopenshell.api.run(
        "aggregate.assign_object", model, products=[space], relating_object=storey
    )

    door_data = data["door_opening"]
    target_wall = walls[int(door_data["wall_index"])]
    opening_width = float(door_data["width"])
    opening_height = float(door_data["height"])
    offset = float(door_data["offset_from_corner"])

    opening = create_product(model, "IfcOpeningElement", "Door opening", owner_history)
    opening.Representation, _ = extruded_representation(
        model, body_context, opening_width, thickness * 1.2, opening_height
    )
    opening.ObjectPlacement = placement(model, offset, -thickness * 0.1, 0.0, 0.0)
    add_relationship(
        model,
        "IfcRelVoidsElement",
        owner_history,
        RelatingBuildingElement=target_wall,
        RelatedOpeningElement=opening,
    )

    door = create_product(model, "IfcDoor", "Interior door", owner_history)
    door.Representation, _ = extruded_representation(
        model, body_context, opening_width, thickness * 0.4, opening_height
    )
    door.ObjectPlacement = placement(model, offset, thickness * 0.3, 0.0, 0.0)
    ifcopenshell.api.run("spatial.assign_container", model, products=[door], relating_structure=storey)
    add_relationship(
        model,
        "IfcRelFillsElement",
        owner_history,
        RelatingOpeningElement=opening,
        RelatedBuildingElement=door,
    )

    model.write(str(output_path))
    return {
        "ifc_path": str(output_path),
        "wall_count": len(walls),
        "opening_count": 1,
        "door_count": 1,
        "floor_area_m2": length * width,
        "gross_wall_volume_m3": 2 * (length + width) * thickness * height,
        "opening_volume_m3": thickness * 1.2 * opening_width * opening_height,
    }


def validate_model(ifc_path: Path, expected: dict) -> dict:
    model = ifcopenshell.open(str(ifc_path))
    walls = model.by_type("IfcWall")
    slabs = model.by_type("IfcSlab")
    openings = model.by_type("IfcOpeningElement")
    doors = model.by_type("IfcDoor")
    voids = model.by_type("IfcRelVoidsElement")
    fills = model.by_type("IfcRelFillsElement")

    checks = {
        "reopened_ifc": True,
        "four_walls": len(walls) == expected["wall_count"],
        "one_slab": len(slabs) == 1,
        "one_space": len(model.by_type("IfcSpace")) == 1,
        "one_opening": len(openings) == expected["opening_count"],
        "one_door": len(doors) == expected["door_count"],
        "void_relationship": len(voids) == 1 and voids[0].RelatedOpeningElement == openings[0],
        "fill_relationship": len(fills) == 1 and fills[0].RelatedBuildingElement == doors[0],
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise AssertionError(f"IFC validation failed: {', '.join(failed)}")
    return checks


def mesh_volume(vertices: list[float], faces: list[int]) -> float:
    """Return the absolute closed-mesh volume using signed triangle tetrahedra."""
    volume = 0.0
    for index in range(0, len(faces), 3):
        a = vertices[faces[index] * 3 : faces[index] * 3 + 3]
        b = vertices[faces[index + 1] * 3 : faces[index + 1] * 3 + 3]
        c = vertices[faces[index + 2] * 3 : faces[index + 2] * 3 + 3]
        volume += (
            a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0])
        ) / 6.0
    return abs(volume)


def geometry_qto(ifc_path: Path) -> dict:
    """Calculate fixture quantities from tessellated IFC geometry."""
    model = ifcopenshell.open(str(ifc_path))
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)

    def volume(product) -> float:
        shape = ifcopenshell.geom.create_shape(settings, product)
        geometry = shape.geometry
        return mesh_volume(list(geometry.verts), list(geometry.faces))

    wall_volumes = [volume(wall) for wall in model.by_type("IfcWall")]
    slab = model.by_type("IfcSlab")[0]
    opening = model.by_type("IfcOpeningElement")[0]
    return {
        "geometry_wall_volume_m3": sum(wall_volumes),
        "geometry_slab_volume_m3": volume(slab),
        "geometry_opening_volume_m3": volume(opening),
        "wall_volume_count": len(wall_volumes),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument(
        "--schema", type=Path, default=Path("schemas/renovation-model.schema.json")
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    data = load_input(args.input, args.schema)
    ifc_path = args.output_dir / "renovation_poc.ifc"
    qto_path = args.output_dir / "renovation_poc.qto.json"
    validation_path = args.output_dir / "renovation_poc.validation.json"

    summary = build_model(data, ifc_path)
    validation = validate_model(ifc_path, summary)
    geometry = geometry_qto(ifc_path)
    summary.update(geometry)
    effective_opening_volume = (
        float(data["room_dimensions"]["wall_thickness"])
        * float(data["door_opening"]["width"])
        * float(data["door_opening"]["height"])
    )
    summary["effective_opening_intersection_volume_m3"] = effective_opening_volume
    summary["geometry_net_wall_volume_m3"] = geometry["geometry_wall_volume_m3"]
    summary["expected_net_wall_volume_m3"] = (
        summary["gross_wall_volume_m3"] - effective_opening_volume
    )
    summary["qto_consistency"] = {
        "net_wall_volume_delta_m3": abs(
            summary["expected_net_wall_volume_m3"]
            - summary["geometry_net_wall_volume_m3"]
        ),
        "opening_representation_delta_m3": abs(
            summary["opening_volume_m3"] - geometry["geometry_opening_volume_m3"]
        ),
    }
    if any(value > 0.001 for value in summary["qto_consistency"].values()):
        raise AssertionError(f"QTO mismatch: {summary['qto_consistency']}")
    summary["net_wall_volume_m3"] = summary["expected_net_wall_volume_m3"]
    qto_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    validation_path.write_text(json.dumps(validation, indent=2), encoding="utf-8")
    print(json.dumps({"summary": summary, "validation": validation}, indent=2))


if __name__ == "__main__":
    main()

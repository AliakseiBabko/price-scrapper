#!/usr/bin/env python3
"""Validate the layout-case / layout-rule dataset and its cross-references.

Cases live in data/layout_cases/*.json, rules in data/layout_rules/rules.jsonl.
Beyond JSON Schema this checks the things a schema cannot: that every
`solves`/`sequence_after`/`zone_ids` id resolves, that every frame an
evidence block cites actually exists on disk, and that the case <-> rule
links point both ways.

Usage:
  python tools/layout/validate_layout_data.py [--strict-frames]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CASES = REPO / "data" / "layout_cases"
RULES = REPO / "data" / "layout_rules" / "rules.jsonl"
TEMPLATES = REPO / "data" / "deliverable_templates"
SCHEMAS = REPO / "schemas"


def load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def validate_schema(instance, schema, label, errors):
    try:
        import jsonschema
    except ImportError:
        return False
    v = jsonschema.Draft202012Validator(schema)
    for e in sorted(v.iter_errors(instance), key=lambda e: list(e.path)):
        errors.append("%s: %s at %s" % (label, e.message, "/".join(str(x) for x in e.path)))
    return True


def check_case(case: dict, path: Path, strict_frames: bool, errors: list[str]):
    cid = case.get("case_id", path.name)
    zone_ids = {z["id"] for z in case.get("zones", [])}
    problem_ids = {p["id"] for p in case.get("problems", [])}
    move_ids = {m["id"] for m in case.get("moves", [])}

    def check_zones(ids, where):
        for z in ids or []:
            if z not in zone_ids:
                errors.append("%s: %s references unknown zone %r" % (cid, where, z))

    for p in case.get("problems", []):
        check_zones(p.get("zone_ids"), "problem " + p["id"])
    for m in case.get("moves", []):
        check_zones(m.get("target_zone_ids"), "move " + m["id"])
        for s in m.get("solves", []):
            if s not in problem_ids:
                errors.append("%s: move %s solves unknown problem %r" % (cid, m["id"], s))
        for s in m.get("sequence_after", []):
            if s not in move_ids:
                errors.append("%s: move %s sequenced after unknown move %r" % (cid, m["id"], s))
    for t in case.get("tradeoffs", []):
        for m in t.get("move_ids", []):
            if m not in move_ids:
                errors.append("%s: tradeoff %s references unknown move %r" % (cid, t["id"], m))

    if case.get("case_kind") != "survey":
        # A survey states general observations, not per-apartment problems it then solves.
        unsolved = problem_ids - {s for m in case.get("moves", []) for s in m.get("solves", [])}
        for p in sorted(unsolved):
            errors.append("%s: problem %s is never addressed by a move (note it or drop it)" % (cid, p))

    for v in case.get("variants", []):
        for m in v.get("move_ids", []):
            if m not in move_ids:
                errors.append("%s: variant %s references unknown move %r" % (cid, v["id"], m))
    finals = [v for v in case.get("variants", []) if v.get("status") == "final"]
    if len(finals) > 1:
        errors.append("%s: %d variants marked final" % (cid, len(finals)))

    docs = {d["id"]: d for d in case.get("provenance", {}).get("companion_documents", [])}
    refs = [(v.get("document_ref"), "variant " + v["id"]) for v in case.get("variants", [])]
    refs += [(s.get("document_ref"), "sub_case " + s["id"]) for s in case.get("sub_cases", [])]
    refs += [(ev.get("document_ref"), where) for ev, where in walk_evidence(case)]
    for ref, where in refs:
        if not ref:
            continue
        doc = docs.get(ref.get("document_id"))
        if not doc:
            errors.append("%s: %s cites unknown document %r" % (cid, where, ref.get("document_id")))
        elif ref.get("page") and doc.get("page_count") and ref["page"] > doc["page_count"]:
            errors.append("%s: %s cites page %d of %s which has %d pages"
                          % (cid, where, ref["page"], doc["id"], doc["page_count"]))

    if case.get("case_kind") == "single_apartment" and "apartment" not in case:
        errors.append("%s: single_apartment case has no apartment block" % cid)
    if case.get("case_kind") == "survey" and not case.get("sub_cases"):
        errors.append("%s: survey case has no sub_cases" % cid)

    frames_dir = case.get("provenance", {}).get("frames_dir")
    if frames_dir:
        base = REPO / frames_dir
        for ev, where in walk_evidence(case):
            f = ev.get("frame")
            if f and not (base / f).exists():
                msg = "%s: %s cites missing frame %s" % (cid, where, f)
                errors.append(msg) if strict_frames else print("  warn: " + msg)


def walk_evidence(node, where="case"):
    """Yield every (evidence, location) pair anywhere in the case."""
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "evidence" and isinstance(v, dict):
                yield v, where
            else:
                label = node.get("id", where) if k in ("moves", "problems", "tradeoffs") else where
                yield from walk_evidence(v, node.get("id", label) if isinstance(node, dict) and "id" in node else label)
    elif isinstance(node, list):
        for item in node:
            yield from walk_evidence(item, where)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict-frames", action="store_true",
                    help="treat a missing frame file as an error (frames are gitignored)")
    a = ap.parse_args()

    errors: list[str] = []
    case_schema = load_json(SCHEMAS / "layout-case.schema.json")
    rule_schema = load_json(SCHEMAS / "layout-rule.schema.json")

    cases = {}
    for p in sorted(CASES.glob("*.json")):
        case = load_json(p)
        schema_ran = validate_schema(case, case_schema, p.name, errors)
        check_case(case, p, a.strict_frames, errors)
        cases[case["case_id"]] = case

    rules = {}
    if RULES.exists():
        for i, line in enumerate(RULES.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            rule = json.loads(line)
            validate_schema(rule, rule_schema, "%s:%d" % (RULES.name, i), errors)
            rules[rule["rule_id"]] = rule

    # cross-references both ways
    for rid, rule in rules.items():
        for cid in rule["supported_by"]:
            if cid not in cases:
                errors.append("rule %s supported_by unknown case %r" % (rid, cid))
            elif rid not in cases[cid].get("rules_derived", []):
                errors.append("rule %s claims case %s, but that case does not list it in rules_derived" % (rid, cid))
        for other in rule.get("conflicts_with", []):
            if other not in rules:
                errors.append("rule %s conflicts_with unknown rule %r" % (rid, other))
            elif rule.get("confidence") != "contested":
                errors.append("rule %s declares a conflict but is not marked contested" % rid)
    for cid, case in cases.items():
        for rid in case.get("rules_derived", []):
            if rid not in rules:
                errors.append("case %s derives unknown rule %r" % (cid, rid))

    templates = {}
    tpl_schema = load_json(SCHEMAS / "deliverable-template.schema.json")
    for p in sorted(TEMPLATES.glob("*.json")):
        tpl = load_json(p)
        validate_schema(tpl, tpl_schema, p.name, errors)
        templates[tpl["template_id"]] = tpl
        for cid in tpl.get("provenance", {}).get("case_ids", []):
            if cid not in cases:
                errors.append("template %s cites unknown case %r" % (tpl["template_id"], cid))
    for cid, case in cases.items():
        ref = case.get("deliverable_template_ref")
        if ref and ref not in templates:
            errors.append("case %s references unknown deliverable template %r" % (cid, ref))

    print("%d case(s), %d rule(s), %d deliverable template(s)" % (len(cases), len(rules), len(templates)))
    if not schema_ran:
        print("  note: jsonschema not installed - structural validation skipped")
    for e in errors:
        print("  ERROR " + e)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

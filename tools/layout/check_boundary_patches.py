#!/usr/bin/env python3
"""Gate the boundary-condition records: geometry, epistemics, and eligibility.

⚠️⚠️ THE THREE THINGS THIS SEPARATES ON PURPOSE
-----------------------------------------------
  COVERAGE is checked on PATCH GEOMETRY.      does every in-scope face have a
                                              complete, non-overlapping cover?
  EPISTEMIC STATUS is checked PER ASSERTION.  not per patch - one row-level
                                              status would launder the
                                              difference between an
                                              owner-stated adjacency and a
                                              merely candidate contact.
  ELIGIBILITY is decided by an AUTHORED TABLE. `insulation_decision_table.csv`,
                                              not a rule buried in code.

⚠⚠ AND WHAT "COVERED" MEANS: every face CLASSIFIED `envelope` has a
complete cover. Faces still classified `unknown` are covered by nothing and
block nothing, so a pass means *inventory complete, classification incomplete* -
never "every boundary in the flat is understood".

⚠️ THE IN-SCOPE INVENTORY IS A SEPARATE FILE WITH A SEPARATE ORIGIN. If the
patches decided what was in scope, "every in-scope face is covered" would be
circular - a face nobody thought about would never be in scope, and the check
would pass by construction. See `build_boundary_inventory.py`.

⚠️⚠️ `unknown` IS LEGAL AND IS NOT ELIGIBILITY. An unknown value satisfies
INVENTORY completeness - we are allowed not to know - but it never makes a face
generator-eligible, and a candidate or disputed value may reach REVIEW output
only. The previous generation rule was a geometric flood that read "absent from
our model" as "outside", and it was wrong twice; replacing it with an equally
implicit categorical rule would be the same mistake in new clothes.

    .venv-ifc314\\Scripts\\python.exe tools/layout/check_boundary_patches.py
"""
from __future__ import annotations

import argparse
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "tools"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.tabular import finite, read_csv  # noqa: E402

CANON = os.path.join(REPO, "data", "canonical")
PATCHES = os.path.join(CANON, "wall_boundary_patches.csv")
ASSERTIONS = os.path.join(CANON, "wall_boundary_assertions.csv")
INVENTORY = os.path.join(CANON, "boundary_face_inventory.csv")
DECISIONS = os.path.join(CANON, "insulation_decision_table.csv")

TOLERANCE_MM = 0.5

PHASES = ("existing", "demolished", "new")
STATES = ("active", "retired")

# ⚠️ ORTHOGONAL AXES, each with its own closed vocabulary. The first draft of
# this schema mixed them into ONE column - `outside` / `party_flat:2Б/2` /
# `common_corridor` / `shaft` - which is the one-column mistake the services
# data model had already rejected, reappearing in the geometry. They are not
# mutually exclusive: a neighbour's balcony is third-party AND unconditioned
# AND separated by air, and only the CONTACT fact suppresses an end cap.
PROPERTIES = {
    "adjacent_scope": ("ours", "common_property", "other_unit", "exterior",
                       "unknown"),
    "adjacent_scope_ref": None,            # free text - a unit designation
    "adjacent_space_kind": ("habitable", "wet_room", "corridor", "loggia",
                            "balcony", "shaft", "exterior_air", "unknown"),
    "conditioning": ("conditioned", "unconditioned", "exterior", "unknown"),
    "contact_kind": ("direct_space_boundary", "abutting_masonry",
                     "separated_by_joint", "open", "unknown"),
}

# Every patch must answer these. `adjacent_scope_ref` is deliberately NOT
# required: the scope can be known while the unit is not, which is precisely
# the difference a per-patch status would have hidden.
REQUIRED_PROPERTIES = ("adjacent_scope", "adjacent_space_kind",
                       "conditioning", "contact_kind")

VALUE_STATES = ("asserted", "derived", "candidate", "disputed", "unknown")

# ⚠⚠ THREE OUTCOMES, NOT TWO AND A NULL. `None` conflated a PROVEN `no`
# with "nobody knows yet" and with "no rule matches", and a generator reading
# them as one falsy value would turn uncertainty into silent omission - the
# omission looking exactly like a confident decision not to insulate.
REQUIRED = "required"
NOT_REQUIRED = "not_required"
UNRESOLVED = "unresolved"

# ⚠️ A value state that may drive GENERATION. Candidate and disputed may appear
# in review output and nowhere else; unknown drives nothing at all.
GENERATOR_STATES = ("asserted", "derived")

# ⚠️ A GEOMETRY BOUND CARRIES ITS OWN BASIS. M2's wall end is compiler-derived
# while its 570 mm transition is owner-stated, and describing the patch as
# having one geometry basis would misreport both.
BOUND_BASES = ("compiler_derived", "owner_stated", "drawing_printed",
               "drawing_scaled", "photo_observed", "assumed", "unknown")


def _rows(path, required):
    return read_csv(path, required=required)


def load_inventory(path=INVENTORY):
    return _rows(path, ["host_id", "face_ref", "length_mm", "in_scope"])


def load_patches(path=PATCHES):
    return _rows(path, ["patch_uuid", "host_id", "face_ref", "phase",
                        "along_from_mm", "along_from_basis", "along_to_mm",
                        "along_to_basis", "vertical", "state"])


def load_assertions(path=ASSERTIONS):
    return _rows(path, ["patch_uuid", "property", "value", "value_state",
                        "knowledge_basis"])


def load_decisions(path=DECISIONS):
    return _rows(path, ["rule_id", "adjacent_scope", "adjacent_space_kind",
                        "conditioning", "contact_kind", "insulation_required"])


def _uuid_ok(value):
    import uuid as _uuid
    try:
        _uuid.UUID(str(value))
    except (ValueError, AttributeError, TypeError):
        return False
    return True


def check(inventory=None, patches=None, assertions=None, decisions=None):
    inventory = load_inventory() if inventory is None else inventory
    patches = load_patches() if patches is None else patches
    assertions = load_assertions() if assertions is None else assertions
    decisions = load_decisions() if decisions is None else decisions
    problems = []

    # ⚠⚠ UNIQUENESS IS CHECKED ON THE SEQUENCE, BEFORE ANY dict() COLLAPSES
    # IT. Every keyed lookup in this file used to be built straight from the
    # rows, so a duplicate row silently overwrote its twin and the validator
    # reported nothing - a second `contact_kind` assertion turned an eligible
    # patch unresolved with zero problems. A collection that deduplicates
    # destroys the defect being checked, which the discipline doc already
    # names, and it happened here in three places at once.
    def _duplicates(label, rows, key):
        seen, dupes = set(), []
        for row in rows:
            value = tuple((row.get(k) or "").strip() for k in key)
            if value in seen:
                dupes.append(
                    "%s has a DUPLICATE row for %s. Whichever row is read last "
                    "would decide the answer, so file order would decide "
                    "construction" % (label, " / ".join(value)))
            seen.add(value)
        return dupes

    problems.extend(_duplicates("the face inventory", inventory,
                                ("host_id", "face_ref")))
    problems.extend(_duplicates("the assertions", assertions,
                                ("patch_uuid", "property")))
    problems.extend(_duplicates("the decision table", decisions, ("rule_id",)))

    faces = dict(((r["host_id"], r["face_ref"]), r) for r in inventory)
    in_scope = set(k for k, r in faces.items()
                   if (r.get("in_scope") or "").strip() == "envelope")

    # ── identity ─────────────────────────────────────────────────────────────
    seen, retired = {}, set()
    for row in patches:
        pid = (row.get("patch_uuid") or "").strip()
        if not _uuid_ok(pid):
            problems.append(
                "patch %r does not carry a UUID. Identity must be minted, "
                "never derived from a host id, a face name or a coordinate - "
                "a patch that moves would otherwise become a different thing"
                % pid)
            continue
        if pid in seen:
            problems.append("patch %s appears twice" % pid)
        seen[pid] = row
        state = (row.get("state") or "").strip()
        if state not in STATES:
            problems.append("patch %s has state %r, not one of %s"
                            % (pid, state, ", ".join(STATES)))
        if state == "retired":
            retired.add(pid)
            # ⚠️ SPLITTING RETIRES AND SUCCEEDS. Moving the old identity onto
            # one child would make the survivor silently inherit a history that
            # is no longer about it.
            successors = [s.strip() for s in
                          (row.get("successors") or "").split(";") if s.strip()]
            if len(successors) < 2:
                problems.append(
                    "patch %s is retired with %d successor(s). A retired patch "
                    "names the patches that replaced it, and a split has at "
                    "least two - the old identity must not land on one child"
                    % (pid, len(successors)))
        if (row.get("phase") or "").strip() not in PHASES:
            problems.append("patch %s has phase %r, not one of %s"
                            % (pid, row.get("phase"), ", ".join(PHASES)))

    for pid in retired:
        for successor in (seen[pid].get("successors") or "").split(";"):
            successor = successor.strip()
            if successor and successor not in seen:
                problems.append("patch %s names successor %s, which does not "
                                "exist" % (pid, successor))

    # ── geometry, and each bound's own basis ─────────────────────────────────
    by_face = {}
    for pid, row in sorted(seen.items()):
        if pid in retired:
            continue
        key = (row["host_id"], row["face_ref"])
        if key not in faces:
            problems.append(
                "patch %s is on %s.%s, which the compiler does not resolve as "
                "a face" % (pid, key[0], key[1]))
            continue
        lo, hi = finite(row.get("along_from_mm")), finite(row.get("along_to_mm"))
        if lo is None or hi is None:
            problems.append(
                "patch %s has a non-finite bound (%r..%r). It parses and then "
                "makes every comparison against it false, so a malformed patch "
                "would read as covering everything and nothing"
                % (pid, row.get("along_from_mm"), row.get("along_to_mm")))
            continue
        if hi <= lo:
            problems.append("patch %s runs %.1f..%.1f, which is empty or "
                            "reversed" % (pid, lo, hi))
            continue
        for column in ("along_from_basis", "along_to_basis"):
            basis = (row.get(column) or "").strip()
            if basis not in BOUND_BASES:
                problems.append(
                    "patch %s %s is %r, not one of %s. EACH BOUND carries its "
                    "own provenance - one of M2's is the compiler's wall end "
                    "and the other is the owner's 570 mm"
                    % (pid, column, basis, ", ".join(BOUND_BASES)))
        vertical = (row.get("vertical") or "").strip()
        if vertical == "full_height":
            pass
        elif vertical == "interval":
            v0, v1 = finite(row.get("v_from_mm")), finite(row.get("v_to_mm"))
            if v0 is None or v1 is None or v1 <= v0:
                problems.append(
                    "patch %s declares a vertical interval but gives %r..%r - "
                    "adjacency can change with height, so the interval must be "
                    "real when it is claimed"
                    % (pid, row.get("v_from_mm"), row.get("v_to_mm")))
        else:
            problems.append(
                "patch %s has vertical %r. It must be `full_height` or "
                "`interval` - EXPLICITLY, because assuming full height is how "
                "a patch silently claims a wall it only partly describes"
                % (pid, vertical))
        length = finite(faces[key].get("length_mm"))
        if length is not None and hi > length + TOLERANCE_MM:
            problems.append("patch %s runs to %.1f on a face %.1f mm long"
                            % (pid, hi, length))
        by_face.setdefault((key, (row.get("phase") or "").strip()),
                           []).append((lo, hi, pid))

    # ── coverage: every in-scope face, exactly once, per phase ───────────────
    covered = set()
    for (key, phase), spans in sorted(by_face.items()):
        covered.add(key)
        spans.sort()
        length = finite(faces[key].get("length_mm")) or 0.0
        if spans[0][0] > TOLERANCE_MM:
            problems.append("%s.%s (%s) is uncovered from 0.0 to %.1f"
                            % (key[0], key[1], phase, spans[0][0]))
        for (lo0, hi0, a), (lo1, hi1, b) in zip(spans, spans[1:]):
            if lo1 > hi0 + TOLERANCE_MM:
                problems.append("%s.%s (%s) has a GAP %.1f..%.1f between "
                                "patches %s and %s"
                                % (key[0], key[1], phase, hi0, lo1, a, b))
            elif lo1 < hi0 - TOLERANCE_MM:
                problems.append("%s.%s (%s) has patches %s and %s OVERLAPPING "
                                "%.1f..%.1f"
                                % (key[0], key[1], phase, a, b, lo1, hi0))
        if length - spans[-1][1] > TOLERANCE_MM:
            problems.append("%s.%s (%s) is uncovered from %.1f to %.1f"
                            % (key[0], key[1], phase, spans[-1][1], length))

    for key in sorted(in_scope - covered):
        problems.append(
            "%s.%s is an ENVELOPE face in the inventory and no patch covers "
            "it. The inventory is authored separately for exactly this reason "
            "- a face the patches never mention must still be accounted for"
            % (key[0], key[1]))

    # ── epistemic status, PER ASSERTION ──────────────────────────────────────
    by_patch = {}
    for row in assertions:
        pid = (row.get("patch_uuid") or "").strip()
        prop = (row.get("property") or "").strip()
        if pid not in seen:
            problems.append("an assertion names patch %s, which does not exist"
                            % pid)
            continue
        if prop not in PROPERTIES:
            problems.append("assertion on %s has property %r, which is not one "
                            "of %s" % (pid, prop, ", ".join(sorted(PROPERTIES))))
            continue
        allowed = PROPERTIES[prop]
        value = (row.get("value") or "").strip()
        if allowed is not None and value not in allowed:
            problems.append("assertion %s.%s has value %r, not one of %s"
                            % (pid, prop, value, ", ".join(allowed)))
        state = (row.get("value_state") or "").strip()
        if state not in VALUE_STATES:
            problems.append("assertion %s.%s has value_state %r, not one of %s"
                            % (pid, prop, state, ", ".join(VALUE_STATES)))
        if not (row.get("knowledge_basis") or "").strip():
            problems.append(
                "assertion %s.%s has no knowledge_basis. Evidence and status "
                "belong to each asserted VALUE, not to its container"
                % (pid, prop))
        if state in ("asserted", "derived") and not (
                row.get("evidence") or "").strip() and not (
                row.get("raw_text") or "").strip():
            problems.append(
                "assertion %s.%s is %s with neither evidence nor raw text - a "
                "confident value nobody can trace is worse than `unknown`"
                % (pid, prop, state))
        if value == "unknown" and state not in ("unknown", "candidate"):
            problems.append(
                "assertion %s.%s has value `unknown` but state %r. Not knowing "
                "something is not an assertion about it" % (pid, prop, state))
        by_patch.setdefault(pid, {})[prop] = row

    for pid, row in sorted(seen.items()):
        if pid in retired:
            continue
        have = by_patch.get(pid, {})
        for prop in REQUIRED_PROPERTIES:
            if prop not in have:
                problems.append(
                    "patch %s (%s.%s) asserts nothing about %r. Every patch "
                    "answers all four axes, even if the answer is `unknown`"
                    % (pid, row["host_id"], row["face_ref"], prop))

    # ── eligibility, from the AUTHORED table ─────────────────────────────────
    if not decisions:
        problems.append(
            "the insulation decision table is EMPTY. Generation must be driven "
            "by an authored table over the assertions; an implicit categorical "
            "rule in code is the same mistake as the geometric flood it "
            "replaced")
    for rule in decisions:
        verdict = (rule.get("insulation_required") or "").strip()
        if verdict not in ("yes", "no"):
            problems.append("decision rule %r has insulation_required %r, "
                            "which must be yes or no"
                            % (rule.get("rule_id"), verdict))

    # ⚠⚠ OVERLAPPING RULES WITH DIFFERENT VERDICTS ARE REFUSED OUTRIGHT.
    # The first version matched the FIRST rule that fit, so inserting an
    # opposite rule above INS-EXT-OPEN flipped M2 from insulated to not, and
    # validation reported nothing. There is no precedence column and there
    # should not be one: CSV row order must never decide construction.
    def _overlap(a, b):
        for prop in REQUIRED_PROPERTIES:
            av, bv = (a.get(prop) or "").strip(), (b.get(prop) or "").strip()
            if av == "*" or bv == "*":
                continue
            if av != bv:
                return False
        return True

    for i, a in enumerate(decisions):
        for b in decisions[i + 1:]:
            if not _overlap(a, b):
                continue
            if (a.get("insulation_required") != b.get("insulation_required")):
                problems.append(
                    "decision rules %s and %s OVERLAP with opposite verdicts "
                    "(%s vs %s). A case they both match would be decided by "
                    "which row comes first - make them disjoint, never ordered"
                    % (a.get("rule_id"), b.get("rule_id"),
                       a.get("insulation_required"),
                       b.get("insulation_required")))
    return problems


def eligibility(patch_uuid, assertions=None, decisions=None):
    """(state, rule_id, why) for one patch - the ONE place eligibility resolves.

    ⚠⚠ STATE IS AN ENUM: `required`, `not_required`, `unresolved`. It used to
    be True/False/None, which made a PROVEN `no` and a merely unknown one the
    same falsy value to any caller that did not check identity. Issued
    generation must FAIL on `unresolved`; review output may show it. Turning
    "nobody has established this" into "no insulation here" is exactly how a
    missing band would look like a decision.

    ⚠⚠ A CANDIDATE OR DISPUTED VALUE NEVER REACHES A GENERATOR. It may be
    shown in review output, where a person reads it and can disagree. An
    `unknown` drives nothing at all. This is the guard that stops the schema
    quietly acquiring the authority the old flood heuristic had.
    """
    assertions = load_assertions() if assertions is None else assertions
    decisions = load_decisions() if decisions is None else decisions
    values, states = {}, {}
    for row in assertions:
        if (row.get("patch_uuid") or "").strip() != patch_uuid:
            continue
        prop = (row.get("property") or "").strip()
        # ⚠️ A DUPLICATE MUST NOT WIN BY BEING LAST. `check()` refuses
        # duplicates outright; this refuses to resolve past one, so a caller
        # that skipped validation cannot be handed a quietly overwritten value.
        if prop in values:
            return (UNRESOLVED, None,
                    "%s is asserted more than once - a duplicate row would "
                    "otherwise decide the answer by its position in the file"
                    % prop)
        values[prop] = (row.get("value") or "").strip()
        states[prop] = (row.get("value_state") or "").strip()

    for prop in REQUIRED_PROPERTIES:
        if prop not in values:
            return UNRESOLVED, None, "no assertion about %s" % prop
        if values[prop] == "unknown":
            return UNRESOLVED, None, "%s is unknown" % prop
        if states[prop] not in GENERATOR_STATES:
            return (UNRESOLVED, None,
                    "%s is %s, which may appear in review output only"
                    % (prop, states[prop]))

    matched = [rule for rule in decisions
               if all(rule.get(prop) in ("*", values[prop])
                      for prop in REQUIRED_PROPERTIES)]
    if not matched:
        return UNRESOLVED, None, "no decision rule matches %s" % values
    verdicts = set(r["insulation_required"] for r in matched)
    if len(verdicts) > 1:
        # ⚠⚠ NEVER RESOLVE A CONFLICT BY FILE ORDER. `check()` refuses an
        # overlapping pair with different verdicts, and this refuses to pick
        # one - CSV row order must not decide construction.
        return (UNRESOLVED, None,
                "rules %s disagree" % ", ".join(sorted(r["rule_id"] for r in matched)))
    rule = matched[0]
    return ((REQUIRED if rule["insulation_required"] == "yes" else NOT_REQUIRED),
            rule["rule_id"], rule.get("rationale", ""))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--show", action="store_true",
                    help="print each patch's eligibility verdict")
    a = ap.parse_args()

    problems = check()
    for problem in problems:
        print("FAIL %s" % problem)

    patches = load_patches()
    if a.show:
        for row in patches:
            verdict, rule, why = eligibility(row["patch_uuid"])
            print("  %-5s %-10s %8.1f..%-8.1f %-10s %s"
                  % (row["host_id"], row["face_ref"],
                     float(row["along_from_mm"]), float(row["along_to_mm"]),
                     {REQUIRED: "INSULATE", NOT_REQUIRED: "none",
                      UNRESOLVED: "UNRESOLVED"}[verdict],
                     rule or why))

    inventory = load_inventory()
    envelope = sum(1 for r in inventory if r.get("in_scope") == "envelope")
    print("%d patch(es), %d assertion(s), %d envelope face(s) of %d"
          % (len(patches), len(load_assertions()), envelope, len(inventory)))
    if problems:
        print("FAILED: %d problem(s)" % len(problems))
        return 1
    print("PASS - every face CLASSIFIED `envelope` is covered, and every value "
          "carries its own status")
    print("       !! inventory complete, CLASSIFICATION INCOMPLETE: %d face(s) "
          "are still `unknown` and block nothing"
          % sum(1 for r in inventory if r.get("in_scope") == "unknown"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

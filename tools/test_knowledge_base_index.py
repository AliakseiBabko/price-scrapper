#!/usr/bin/env python3
"""Focused parser fixture for the generated numeric-claims projection."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("knowledge_index", ROOT / "tools" / "build_knowledge_base_index.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class NumericClaimsFixtureTests(unittest.TestCase):
    def test_fixture_covers_numeric_shapes(self) -> None:
        text = (ROOT / "tests" / "fixtures" / "numeric_claims_fixture.md").read_text(encoding="utf-8")
        matches = list(MODULE.NUMERIC.finditer(text)) + list(MODULE.BARE_CURRENCY.finditer(text))
        units = {match.group("unit") for match in matches}
        self.assertIn("RUB/m²", units)
        self.assertIn("%", units)
        self.assertIn("mm", units)
        self.assertIn("days", units)
        self.assertTrue(any("200–450" in match.group("value") for match in matches))
        self.assertNotIn("1350", {match.group("value") for match in matches})

    def test_region_confidence_contract(self) -> None:
        self.assertEqual(MODULE.region_confidence("Test region, level 1"), "exact")
        self.assertEqual(MODULE.region_confidence("Test region, level 2"), "inferred")
        self.assertEqual(MODULE.region_confidence("unresolved"), "missing")


if __name__ == "__main__":
    unittest.main()

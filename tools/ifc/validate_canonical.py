"""Validate a canonical renovation JSON document against its JSON Schema."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema", type=Path, required=True)
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()

    schema = json.loads(args.schema.read_text(encoding="utf-8"))
    document = json.loads(args.input.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(document), key=lambda error: list(error.path))

    if errors:
        for error in errors:
            path = ".".join(str(part) for part in error.path) or "$"
            print(f"INVALID {path}: {error.message}")
        raise SystemExit(1)

    print(f"VALID canonical model: {args.input}")


if __name__ == "__main__":
    main()

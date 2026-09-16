#!/usr/bin/env python3
"""DEPRECATED SHIM. The generator is `model_from_resolved.py`.

Renamed 2026-09-16: it no longer reads the DXF. Walls, body polygons, openings,
shafts, frame members and лоджия bays all come from `resolve_v0_geometry`, the
same compiler the DXF serialiser consumes, and the build is verified to succeed
with no DXF present at all.

The old name said the opposite of what the module does, which is exactly the
kind of thing that lets a stale assumption survive. This shim exists so an
existing command keeps working; it will be removed.
"""
from model_from_resolved import *  # noqa: F401,F403
from model_from_resolved import main

if __name__ == "__main__":
    raise SystemExit(main())

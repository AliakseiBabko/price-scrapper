# -*- coding: utf-8 -*-
"""Make stdout safe for the names this project actually uses.

Why this exists
---------------
Half the elements in this vault are named in Russian - лоджия, вентблок,
прихожая - and every layout tool prints them. On a default Windows console
(cp1252/cp1251) `print` raises UnicodeEncodeError, so the tool dies at the
moment it reports.

That is not a cosmetic problem, because of WHERE it lands:

  * `check_dxf_closure.py` crashed inside the SUCCESS branch of its
    review-drawing check, and a bare `except Exception` there recorded the
    crash under the kind `stale_review_drawing`. The gate exited 1 with a
    specific, named, entirely false finding, two lines after printing that the
    drawing was byte-identical. Run with PYTHONIOENCODING=utf-8 it passed.
  * `structural_assembly_selftest.py` died on a BOM in the same way.

So a gate's verdict depended on which terminal ran it, and the failure mode was
a plausible-looking wrong answer rather than an obvious crash. Reconfiguring
here removes the dependency. `errors='replace'` means a console that genuinely
cannot show a glyph prints a placeholder instead of taking the tool down.

Call `utf8_console()` as the first statement of `main()`.
"""
from __future__ import print_function

import sys


def utf8_console(streams=None):
    """Re-encode stdout/stderr as UTF-8, never raising if that is impossible."""
    for stream in (streams or (sys.stdout, sys.stderr)):
        try:
            stream.reconfigure(encoding='utf-8', errors='replace')
        except (AttributeError, ValueError):
            pass          # Python 2, or a stream that is not reconfigurable

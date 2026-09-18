#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Guards the retirement of `build_variant.py` and `make_variant.py`.

⚠️⚠️ THE SEED THAT MATTERS IS NOT "DOES IT EXIT NON-ZERO".
It is whether a refused invocation leaves the outputs **untouched**. A retired
builder that still creates its output directory, truncates a file, or bumps an
mtime is still a builder, and the damage would be invisible in an exit code. So
every refusal here is checked against a full sha256 + mtime + size census of
`data/outputs/` taken immediately before it.

⚠️ mtime is checked as well as content, because a rewrite with identical bytes is
still a write - it would mean the tombstone is executing code it must not, and
the next change to that code would do real damage silently.
"""

import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUTS = os.path.join(REPO, "data", "outputs")
BUILD = os.path.join(REPO, "tools", "layout", "build_variant.py")
MAKE = os.path.join(REPO, "tools", "layout", "make_variant.py")
VARIANTS = os.path.join(REPO, "data", "variants")

PASS, FAIL = [], []


def ok(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print("%s  %s%s" % ("PASS" if cond else "FAIL", name,
                        ("  -- " + detail) if detail and not cond else ""))


def census(root):
    """Every file under root: size and mtime_ns. Cheap, and enough to catch a write."""
    out = {}
    for base, dirs, files in os.walk(root):
        dirs.sort()
        for f in sorted(files):
            p = os.path.join(base, f)
            try:
                st = os.stat(p)
            except OSError:
                continue
            out[os.path.relpath(p, root)] = (st.st_size, st.st_mtime_ns)
    return out


def diff(before, after):
    problems = []
    for k in sorted(set(before) | set(after)):
        b, a = before.get(k), after.get(k)
        if b is None:
            problems.append("CREATED %s" % k)
        elif a is None:
            problems.append("DELETED %s" % k)
        elif b != a:
            problems.append("MODIFIED %s (size %s->%s, mtime changed %s)"
                            % (k, b[0], a[0], b[1] != a[1]))
    return problems


def refuses(label, argv, expect="RETIRED"):
    """Must exit non-zero, say why, and change nothing under data/outputs."""
    before = census(OUTPUTS)
    p = subprocess.run([sys.executable] + argv, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", cwd=REPO)
    after = census(OUTPUTS)
    blob = (p.stdout or "") + (p.stderr or "")

    if p.returncode == 0:
        ok(label, False, "exited 0 - it must refuse")
        return
    if expect.lower() not in blob.lower():
        ok(label, False, "refused without saying %r:\n%s" % (expect, blob[:300]))
        return
    touched = diff(before, after)
    if touched:
        ok(label, False, "REFUSED BUT TOUCHED THE OUTPUTS:\n  " + "\n  ".join(touched[:8]))
        return
    ok(label, True)


def main():
    if not os.path.isdir(OUTPUTS):
        print("no data/outputs to census - cannot run")
        return 1

    # --- the exact invocation that built the sketch on 2026-09-18 -------------
    refuses("1  the 2026-09-18 reproduction is refused",
            [BUILD, os.path.join(VARIANTS, "v1-homestyler.json"), "--no-render"])

    # --- --all must not be a way round it ------------------------------------
    refuses("2  --all is refused", [BUILD, "--all"])

    # --- no arguments at all --------------------------------------------------
    refuses("3  a bare invocation is refused", [BUILD])

    # --- a NONEXISTENT variant must still refuse, not report "no such file" ---
    # If it got as far as resolving a path, the refusal is not early enough.
    refuses("4  refusal precedes any path resolution",
            [BUILD, os.path.join(VARIANTS, "definitely-not-a-variant.json")])

    # --- the wrapper the docs advertise --------------------------------------
    refuses("5  make_variant.py propagates the refusal", [MAKE, "v1-homestyler"])
    refuses("6  make_variant.py refuses an unknown variant too",
            [MAKE, "definitely-not-a-variant"])

    # --- the tombstone must NAME v1 as never buildable ------------------------
    p = subprocess.run([sys.executable, BUILD], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", cwd=REPO)
    blob = (p.stdout or "") + (p.stderr or "")
    ok("7  the refusal names v1-homestyler as reference_only",
       "reference_only" in blob and "v1-homestyler" in blob)
    ok("8  the refusal points at the replacement architecture",
       "ResolvedGeometry" in blob, blob[:200])

    # --- the quarantine must exist and be self-describing ---------------------
    q = os.path.join(OUTPUTS, "_QUARANTINE", "v1-homestyler-retired-20260919")
    ok("9  the v1 outputs are quarantined, not loose in variants/",
       os.path.isdir(q)
       and not os.path.isdir(os.path.join(OUTPUTS, "variants", "v1-homestyler")))
    ok("10 the quarantine carries a README and a hash manifest",
       os.path.exists(os.path.join(q, "README.md"))
       and os.path.exists(os.path.join(q, "QUARANTINE_MANIFEST.json")))

    print("\n%d passed, %d failed" % (len(PASS), len(FAIL)))
    if FAIL:
        print("FAILED: " + ", ".join(FAIL))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())

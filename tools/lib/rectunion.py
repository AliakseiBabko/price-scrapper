# -*- coding: utf-8 -*-
"""Union of axis-aligned rectangles, as closed loops - EXACTLY, no quantisation.

Why this exists
---------------
Owner, 2026-09-15, on the лоджия return: *"one surface means literally one
surface — currently you model M6b as a wall extruding from the surface."* The
photo `_Survey/IMG_20260913_134256_with_wall_segments.jpg` catches the building
mid-insulation and settles it: the mineral wool boards **turn from M6b's face
onto MB's without a break**, and the render closes over them. The finished skin
is ONE surface wrapping the corner; the wall boundary underneath is invisible.

The model was drawing that skin as one rectangle per wall, so a take-off
iterating surfaces saw four where the builder sees one, and every corner carried
a seam that exists in our data and not in the building.

The method
----------
Build the grid from the rectangles' OWN coordinates - every distinct x and every
distinct y become grid lines - so a cell is either wholly inside a rectangle or
wholly outside it and there is no sampling error at any scale. Mark covered
cells, take every cell edge whose two sides disagree, and chain those edges into
loops.

!! Emitting the union outline is not cosmetic. A closed loop around the whole
run is what lets a downstream consumer treat it as one surface; a pile of
rectangles cannot be distinguished from a pile of separate surfaces.
"""
from __future__ import print_function


def _grid(rects):
    xs = sorted(set([r[0] for r in rects] + [r[2] for r in rects]))
    ys = sorted(set([r[1] for r in rects] + [r[3] for r in rects]))
    return xs, ys


def union_loops(rects, eps=1e-6):
    """Closed loops bounding the union of `rects` [(x0,y0,x1,y1), ...]."""
    if not rects:
        return []
    xs, ys = _grid(rects)
    nx, ny = len(xs) - 1, len(ys) - 1
    cov = [[False] * nx for _ in range(ny)]
    for j in range(ny):
        cy = (ys[j] + ys[j + 1]) / 2.0
        for i in range(nx):
            cx = (xs[i] + xs[i + 1]) / 2.0
            for x0, y0, x1, y1 in rects:
                if x0 - eps < cx < x1 + eps and y0 - eps < cy < y1 + eps:
                    cov[j][i] = True
                    break

    def inside(i, j):
        return 0 <= i < nx and 0 <= j < ny and cov[j][i]

    # Directed boundary edges, oriented so the covered cell is on the LEFT.
    edges = {}
    for j in range(ny):
        for i in range(nx):
            if not cov[j][i]:
                continue
            x0, x1, y0, y1 = xs[i], xs[i + 1], ys[j], ys[j + 1]
            if not inside(i, j - 1):
                edges.setdefault((x0, y0), []).append((x1, y0))
            if not inside(i + 1, j):
                edges.setdefault((x1, y0), []).append((x1, y1))
            if not inside(i, j + 1):
                edges.setdefault((x1, y1), []).append((x0, y1))
            if not inside(i - 1, j):
                edges.setdefault((x0, y1), []).append((x0, y0))

    loops = []
    while edges:
        start = next(iter(edges))
        loop, cur = [start], start
        while True:
            nxts = edges.get(cur)
            if not nxts:
                break
            nxt = nxts.pop()
            if not nxts:
                del edges[cur]
            if nxt == start:
                break
            loop.append(nxt)
            cur = nxt
        if len(loop) >= 4:
            loops.append(_simplify(loop))
    return loops


def _simplify(loop):
    """Drop points that sit mid-run on a straight axis-aligned stretch."""
    out = []
    n = len(loop)
    for k in range(n):
        a, b, c = loop[k - 1], loop[k], loop[(k + 1) % n]
        if (a[0] == b[0] == c[0]) or (a[1] == b[1] == c[1]):
            continue
        out.append(b)
    return out or loop


def groups(rects, eps=1e-6):
    """Split rectangles into connected components - touching counts as joined."""
    n = len(rects)
    seen, out = [False] * n, []
    for s in range(n):
        if seen[s]:
            continue
        comp, stack = [], [s]
        seen[s] = True
        while stack:
            k = stack.pop()
            comp.append(k)
            for m in range(n):
                if seen[m]:
                    continue
                a, b = rects[k], rects[m]
                if (min(a[2], b[2]) - max(a[0], b[0]) >= -eps
                        and min(a[3], b[3]) - max(a[1], b[1]) >= -eps):
                    seen[m] = True
                    stack.append(m)
        out.append(comp)
    return out


def clip_halfplane(loop, ax, ay, nx, ny, eps=1e-6):
    """Sutherland-Hodgman: keep the part of `loop` on the +normal side.

    Owner, 2026-09-15, on the лоджия: *"the angle between glazing and M6b is a
    sharp angle... this angle should be really sharp, not like a rectangle like
    you draw. And for M2 is the same."*

    The лоджия's glazed face is DIAGONAL - that is the whole reason the plan
    draws it as a splay - so the walls and the insulation that run into it meet
    it at an acute angle, not a square end. Everything here is built from
    axis-aligned rectangles, which overshoot a diagonal by a small triangle:
    55 mm at M2's south-west corner and the same at M6b's, each about 200 mm
    wide. Squaring that off draws a stub sticking through the glass.

    Cutting on the glazing's own outer plane mitres both in one operation, and
    it is the SAME plane for both, so the finished surface stays continuous
    across the corner rather than acquiring a step of its own.
    """
    if not loop:
        return []
    def side(p):
        return (p[0] - ax) * nx + (p[1] - ay) * ny
    out = []
    n = len(loop)
    for i in range(n):
        cur, nxt = loop[i], loop[(i + 1) % n]
        sc, sn = side(cur), side(nxt)
        if sc >= -eps:
            out.append(cur)
        if (sc > eps and sn < -eps) or (sc < -eps and sn > eps):
            t = sc / (sc - sn)
            out.append((round(cur[0] + t * (nxt[0] - cur[0]), 1),
                        round(cur[1] + t * (nxt[1] - cur[1]), 1)))
    return out


def _shoelace_area(pts):
    a = 0.0
    for i in range(len(pts)):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % len(pts)]
        a += x0 * y1 - x1 * y0
    return abs(a) / 2.0


#!/usr/bin/env python
"""Split an oversized wiki page into a guide/detail set, safely and verifiably.

Written 2026-09-02, after the same line-range-extraction pattern was hand-rolled
four times in one session (Kitchen_Furniture, Budgeting_Guide, General_Dos_and_Donts,
Soundproofing). It exists so that a split is a two-command operation with the
verification built in, rather than a bespoke script each time.

Why line ranges and not a parser: the vault convention in
`00_Master/wiki_page_format.md` requires that a split MOVE existing prose rather
than re-derive it, "so no fact gets lost or silently altered". Extracting whole
line ranges byte-for-byte guarantees that literally; the checks below prove it.

Usage
-----
  # 1. See the page's sections, their sizes, and a suggested grouping
  python tools/split_page.py analyse 11_Budget_and_Planning/Budgeting_Guide.md

  # 2. Write a spec (JSON) describing where each section goes, then apply it
  python tools/split_page.py apply --spec spec.json

  # 3. If `analyse` reports FRAGMENTED instead, MERGE rather than split
  python tools/split_page.py merge --spec merge_spec.json

Spec format
-----------
{
  "source": "path/to/Page.md",
  "keep_title": true,
  "targets": {
     "path/to/analysis/New_Page.md": {
        "title": "Page title",
        "intro": "Intro paragraph.",
        "sections": [3, 5, 6],          # 1-based indices from `analyse`
        "footer": "optional footer text"
     }
  },
  "remainder_pointer": "markdown appended to the source page"
}
Sections not named in any target stay on the source page, in their original order.

Merge spec format
-----------------
For the OPPOSITE failure, where a page has many small dated sections because
each processing batch appended its own heading. Splitting such a page makes it
strictly worse; the fix is to group the sections under thematic parents,
DEMOTING the original dated headings from ## to ### rather than deleting them,
so no attribution or date is lost.

{
  "source": "path/to/Page.md",
  "groups": [
     {"title": "Thematic parent", "intro": "optional", "sections": [3, 7, 9]}
  ],
  "last": [12]                       # sections pinned to the end (Change Log etc.)
}
Ungrouped sections keep their original order and are emitted before the groups.
The same content-line and citation-ID parity checks run afterwards.
"""

import argparse, io, json, os, re, sys, collections

# The vault is full of Cyrillic and emoji headings; a cp1252 console must not
# be able to crash an analysis run.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HEADING = re.compile(r"^(#{1,6})\s+\S")
NL = chr(10)


def read(path):
    return io.open(path, encoding="utf-8").read().split("\n")


def sections(lines):
    """Return [(index, level, title, start, end)] over top-level (##) sections.

    Line 1 (the H1 title) and any preamble before the first ## are section 0.
    """
    marks = []
    for i, l in enumerate(lines, 1):
        m = HEADING.match(l)
        if m and len(m.group(1)) == 2:
            marks.append((i, l))
    out = []
    if not marks:
        return [(0, 1, lines[0] if lines else "", 1, len(lines))]
    if marks[0][0] > 1:
        out.append((0, 1, "(preamble)", 1, marks[0][0] - 1))
    for n, (start, title) in enumerate(marks):
        end = marks[n + 1][0] - 1 if n + 1 < len(marks) else len(lines)
        out.append((len(out), 2, title.strip(), start, end))
    return out


def cmd_analyse(args):
    lines = read(args.page)
    secs = sections(lines)
    total = len(lines)
    print("%s — %d lines, %d top-level sections" % (args.page, total, len(secs) - 1))
    print()
    for idx, lvl, title, a, b in secs:
        size = b - a + 1
        bar = "#" * min(40, max(1, size // 6))
        print("%3d  %4d lines  %-40s %s" % (idx, size, bar, title[:100]))
    print()
    avg = total / max(1, len(secs) - 1)
    print("average %.0f lines per section" % avg)
    if avg < 12 and len(secs) - 1 > 12:
        print("SIGNAL: looks FRAGMENTED (many small dated sections) — prefer MERGING "
              "under thematic parents over splitting. See wiki_page_format.md.")
    else:
        print("SIGNAL: sections are substantial — a split on whole-section seams is "
              "appropriate if they carry independent decisions.")


def cmd_apply(args):
    spec = json.load(io.open(args.spec, encoding="utf-8"))
    src = spec["source"]
    lines = read(src)
    secs = sections(lines)
    by_idx = {s[0]: s for s in secs}

    claimed = {}
    for path, t in spec["targets"].items():
        for i in t["sections"]:
            if i not in by_idx:
                sys.exit("spec error: section %r not in %s" % (i, src))
            if i in claimed:
                sys.exit("spec error: section %d claimed by %s and %s" % (i, claimed[i], path))
            claimed[i] = path

    moved_lines = set()
    for i, path in claimed.items():
        _, _, _, a, b = by_idx[i]
        moved_lines.update(range(a, b + 1))

    written = {}
    for path, t in spec["targets"].items():
        blocks = []
        for i in sorted(t["sections"]):
            _, _, _, a, b = by_idx[i]
            blocks.append("\n".join(lines[a - 1:b]).strip("\n"))
        body = "\n\n".join(blocks)
        text = "# %s\n\n%s\n\n%s\n" % (t["title"], t["intro"].strip(), body)
        if t.get("footer"):
            text += "\n" + t["footer"].strip() + "\n"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        io.open(path, "w", encoding="utf-8", newline="").write(text)
        written[path] = text

    rest = [l for n, l in enumerate(lines, 1) if n not in moved_lines]
    newsrc = "\n".join(rest).rstrip("\n") + "\n"
    if spec.get("remainder_pointer"):
        newsrc += "\n" + spec["remainder_pointer"].strip() + "\n"
    io.open(src, "w", encoding="utf-8", newline="").write(newsrc)
    written[src] = newsrc

    # ---- verification -------------------------------------------------
    orig_content = [l for l in lines if l.strip()]
    have = collections.Counter()
    for text in written.values():
        for l in text.split("\n"):
            if l.strip():
                have[l] += 1
    missing = [l for l in orig_content if have[l] < 1]

    idpat = re.compile(r"(?:_Sources/)?((?:YT|yt)_[A-Za-z0-9_\-]+)")
    before = set(idpat.findall("\n".join(lines)))
    after = set()
    for text in written.values():
        after |= set(idpat.findall(text))
    lost = sorted(before - after)

    print("split: %s" % src)
    for p, t in sorted(written.items()):
        print("   %-70s %4d lines" % (p, t.count("\n")))
    print()
    print("content lines in original : %d" % len(orig_content))
    print("MISSING after split       : %d" % len(missing))
    print("citation ids before/after : %d / %d   lost: %d" % (len(before), len(after), len(lost)))
    if missing[:5]:
        io.open("split_page_missing.txt", "w", encoding="utf-8").write("\n".join(missing))
        print("   (missing lines written to split_page_missing.txt)")
    if lost:
        print("   LOST IDS: %s" % ", ".join(lost))
    ok = not missing and not lost
    print()
    print("RESULT: %s" % ("CLEAN" if ok else "PROBLEM — review before committing"))
    return 0 if ok else 1


def cmd_merge(args):
    spec = json.load(io.open(args.spec, encoding="utf-8"))
    src = spec["source"]
    lines = read(src)
    secs = sections(lines)
    by_idx = {s[0]: s for s in secs}

    def block(i):
        _, _, _, a, b = by_idx[i]
        return NL.join(lines[a - 1:b]).strip(NL)

    claimed = {}
    for g in spec["groups"]:
        for i in g["sections"]:
            if i not in by_idx:
                sys.exit("spec error: section %r not in %s" % (i, src))
            if i in claimed:
                sys.exit("spec error: section %d claimed twice" % i)
            claimed[i] = g["title"]

    last = spec.get("last", [])
    pinned = set(last)
    parts = [block(i) for i in sorted(by_idx) if i not in claimed and i not in pinned]

    demoted = 0
    for g in spec["groups"]:
        out = ["## " + g["title"]]
        if g.get("intro"):
            out.append(g["intro"].strip())
        for i in sorted(g["sections"]):
            b = block(i).split(NL)
            if b and b[0].startswith("## "):
                b[0] = "#" + b[0]          # ## -> ###, heading text kept verbatim
                demoted += 1
            out.append(NL.join(b).strip(NL))
        parts.append((NL + NL).join(out))

    parts.extend(block(i) for i in last)
    text = (NL + NL).join(x for x in parts if x.strip()).rstrip(NL) + NL
    io.open(src, "w", encoding="utf-8", newline="").write(text)

    # ---- verification -------------------------------------------------
    # A demoted heading is the ONLY change a merge may make to a line, so the
    # parity check normalises "### " back to "## " before comparing. Everything
    # else must survive byte for byte, exactly as in a split.
    def norm(l):
        return l[1:] if l.startswith("### ") else l

    orig = [l for l in lines if l.strip()]
    have = collections.Counter(norm(l) for l in text.split(NL) if l.strip())
    missing = [l for l in orig if have[norm(l)] < 1]

    idpat = re.compile(r"(?:_Sources/)?((?:YT|yt)_[A-Za-z0-9_\-]+)")
    before = set(idpat.findall(NL.join(lines)))
    after = set(idpat.findall(text))
    lost = sorted(before - after)

    print("merge: %s" % src)
    print("   %d lines -> %d lines, %d sections -> %d, %d headings demoted ## -> ###"
          % (len(lines), text.count(NL), len(secs) - 1,
             len(re.findall(r"^## ", text, re.M)), demoted))
    print()
    print("content lines in original : %d" % len(orig))
    print("MISSING after merge       : %d" % len(missing))
    print("citation ids before/after : %d / %d   lost: %d" % (len(before), len(after), len(lost)))
    if missing:
        io.open("split_page_missing.txt", "w", encoding="utf-8").write(NL.join(missing))
        print("   (missing lines written to split_page_missing.txt)")
    if lost:
        print("   LOST IDS: %s" % ", ".join(lost))
    ok = not missing and not lost
    print()
    print("RESULT: %s" % ("CLEAN" if ok else "PROBLEM — review before committing"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("analyse", help="show a page's section structure and sizes")
    a.add_argument("page")
    a.set_defaults(func=cmd_analyse)
    b = sub.add_parser("apply", help="perform a split described by a JSON spec")
    b.add_argument("--spec", required=True)
    b.set_defaults(func=cmd_apply)
    c = sub.add_parser("merge", help="group a FRAGMENTED page's sections under thematic parents")
    c.add_argument("--spec", required=True)
    c.set_defaults(func=cmd_merge)
    args = ap.parse_args()
    rc = args.func(args)
    sys.exit(rc or 0)


if __name__ == "__main__":
    main()

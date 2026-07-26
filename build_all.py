#!/usr/bin/env python3
"""
Build both CHEMx19A Exam III sheets from source.

    python3 build_all.py

Produces:
    chem_x19a_mt3_instruction_sheet.pdf   2 pages, 23 numbered question boxes
    chem_x19a_mt3_info_sheet.pdf          1 page, chapter reference

Pipeline: render LaTeX -> measure each box at true column width ->
solve the optimal column split -> emit page/column breaks -> render PDF.
"""
import os
import re
import subprocess
import sys

import markdown
import numpy as np
from pdf2image import convert_from_bytes, convert_from_path
from weasyprint import HTML

import extract
import repack

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

PAGE_H = 11 * 72 - 2 * 0.3 * 72          # usable column height, points
COL_W = (8.5 - 0.6 - 0.16) / 2           # usable column width, inches
CAP = PAGE_H * 0.95                      # leave a safety margin
MD_EXT = ["tables", "sane_lists", "md_in_html"]


def css():
    return open("build_pdf.py").read().split('CSS = """')[1].split('"""')[0]


def helpers():
    """Pull eq_style / inject_eq_sizes out of build_pdf.py without running it."""
    ns = {}
    exec(open("build_pdf.py").read().split("import sys")[0], ns)
    return ns["inject_eq_sizes"]


def set_font(pt):
    s = open("build_pdf.py").read()
    for pat, rep in [
        (r"\.page \{ font-size: [\d.]+pt", f".page {{ font-size: {pt}pt"),
        (r"\.page h2 \{ font-size: [\d.]+pt", f".page h2 {{ font-size: {pt*1.22:.2f}pt"),
        (r"\.page h4 \{ font-size: [\d.]+pt", f".page h4 {{ font-size: {pt*1.04:.2f}pt"),
        (r"\.page:first-child \{ font-size: [\d.]+pt", f".page:first-child {{ font-size: {pt}pt"),
        (r"\.page:first-child h2 \{ font-size: [\d.]+pt", f".page:first-child h2 {{ font-size: {pt*1.22:.2f}pt"),
        (r"\.page:first-child h4 \{ font-size: [\d.]+pt", f".page:first-child h4 {{ font-size: {pt*1.04:.2f}pt"),
    ]:
        s = re.sub(pat, rep, s)
    open("build_pdf.py", "w").write(s)


def _tick(msg):
    print(f"\r{msg}", end="", flush=True)


def measure(blocks):
    """Rendered height of each block at the real column width, in points."""
    inject = helpers()
    style = css()
    out = []
    for i, b in enumerate(blocks, 1):
        _tick(f"    measuring block {i}/{len(blocks)}   ")
        body = markdown.markdown(inject(b), extensions=MD_EXT)
        html = (
            f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{style}\n'
            f"@page{{size:{COL_W}in 60in !important;margin:0 !important}}</style></head>"
            f'<body><div class="page"><div class="cols"><div class="col">{body}'
            f"</div></div></div></body></html>"
        )
        img = convert_from_bytes(HTML(string=html, base_url=".").write_pdf(), dpi=72)[0]
        a = np.array(img.convert("L"))
        rows = np.where((a < 200).sum(axis=1) > 0)[0]
        out.append(int(rows.max() - rows.min() + 1) if len(rows) else 0)
    _tick(" " * 40)
    return out


def paginate(blocks, groups):
    """Emit markdown with break markers for the given column groups."""
    parts = []
    for i, (a, b) in enumerate(groups):
        if i == 0:
            sep = ""
        elif i % 2 == 0:
            sep = "\n\n<!--pagebreak-->\n\n"
        else:
            sep = "\n\n<!--colbreak-->\n\n"
        parts.append(sep + "\n".join(blocks[a:b]))
    return "".join(parts) + "\n"


def pages_of(pdf):
    return len(convert_from_path(pdf, dpi=50))


def build(src_md, out_pdf, ncols, want_pages, start_pt, min_pt, step=0.2):
    """Largest font (in `step` increments) that ACTUALLY renders in want_pages.

    Ink height scales close to linearly with font size, so rather than
    scanning every candidate we measure once at start_pt, estimate the size
    that should just hit the page cap, and verify it by rendering. Line-wrap
    reflow means that estimate can land a step off the true boundary, so we
    nudge in the needed direction until the rendered page count matches --
    typically 2-3 renders total instead of a full scan of the font ladder.
    """
    blocks = extract.top_blocks(open(src_md, encoding="utf-8").read())
    tmp = f".{os.path.basename(out_pdf)}.md"
    tried = []
    last_rendered = None

    def attempt(pt):
        nonlocal last_rendered
        last_rendered = pt
        set_font(pt)
        heights = measure(blocks)
        max_h, groups = repack.partition(heights, ncols)
        open(tmp, "w", encoding="utf-8").write(paginate(blocks, groups))
        _tick(f"    rendering PDF at {pt}pt ...")
        subprocess.run([sys.executable, "build_pdf.py", tmp, out_pdf], check=True,
                       stdout=subprocess.DEVNULL)
        got = pages_of(out_pdf)
        _tick(" " * 40)
        print(f"  {pt}pt -> {got} page(s)")
        tried.append(pt)
        return got, heights, groups, max_h

    pt = start_pt
    got, heights, groups, max_h = attempt(pt)

    if got != want_pages:
        est = round(round(pt * CAP / max_h / step) * step, 2)
        est = max(min(est, start_pt - step), min_pt)
        if est not in tried:
            pt = est
            got, heights, groups, max_h = attempt(pt)

    while got != want_pages and round(pt - step, 2) >= min_pt:
        pt = round(pt - step, 2)
        if pt in tried:
            break
        got, heights, groups, max_h = attempt(pt)

    # the estimate can undershoot -- climb back up while it still fits, so we
    # don't leave readable font size on the table
    while got == want_pages and round(pt + step, 2) <= start_pt:
        nxt = round(pt + step, 2)
        if nxt in tried:
            break
        got2, heights2, groups2, max_h2 = attempt(nxt)
        if got2 != want_pages:
            break
        pt, got, heights, groups, max_h = nxt, got2, heights2, groups2, max_h2

    # attempt() always overwrites out_pdf, even on a failed try -- if the last
    # render wasn't the accepted pt (e.g. the climb loop's final overshoot),
    # re-render so the file on disk actually matches what we report/return
    if last_rendered != pt and got == want_pages:
        got, heights, groups, max_h = attempt(pt)

    os.remove(tmp)
    if got != want_pages:
        raise SystemExit(f"{src_md}: nothing fits {want_pages} pages in "
                          f"[{min_pt}, {start_pt}]pt ({len(tried)} render(s) tried)")
    fill = ", ".join(f"{100*sum(heights[a:b])/PAGE_H:.0f}%" for a, b in groups)
    print(f"  {out_pdf}: {got} page(s) at {pt}pt   columns {fill}   "
          f"({len(tried)} render(s))")
    return pt


if __name__ == "__main__":
    print("1. rendering equations ...")
    subprocess.run([sys.executable, "render_eq_exam3.py"], check=True,
                   stdout=subprocess.DEVNULL)
    print(f"   {len(os.listdir('assets'))} images in assets/")

    print("2. building instruction sheet (must be 2 pages) ...")
    build("qsection.md", "chem_x19a_mt3_instruction_sheet.pdf",
          ncols=4, want_pages=2, start_pt=10.0, min_pt=7.6)

    print("3. building info sheet (must be 1 page) ...")
    build("info_sheet.md", "chem_x19a_mt3_info_sheet.pdf",
          ncols=2, want_pages=1, start_pt=9.4, min_pt=8.6)

    print("\ndone.")

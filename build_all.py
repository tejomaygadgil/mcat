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


def measure(blocks):
    """Rendered height of each block at the real column width, in points."""
    inject = helpers()
    style = css()
    out = []
    for b in blocks:
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
    return out


def paginate(blocks, ncols):
    """Emit markdown with break markers for an even ncols split."""
    _, groups = repack.partition(measure(blocks), ncols)
    parts = []
    for i, (a, b) in enumerate(groups):
        if i == 0:
            sep = ""
        elif i % 2 == 0:
            sep = "\n\n<!--pagebreak-->\n\n"
        else:
            sep = "\n\n<!--colbreak-->\n\n"
        parts.append(sep + "\n".join(blocks[a:b]))
    return "".join(parts) + "\n", groups


def pages_of(pdf):
    return len(convert_from_path(pdf, dpi=50))


def build(src_md, out_pdf, ncols, want_pages, font_candidates):
    """Largest font that ACTUALLY renders in want_pages -- verified, not predicted.

    The predicted column height is accurate to a percent or so, which is not
    enough to trust near the limit, so each candidate is rendered and counted.
    """
    blocks = extract.top_blocks(open(src_md, encoding="utf-8").read())
    tmp = f".{os.path.basename(out_pdf)}.md"
    for pt in font_candidates:
        set_font(pt)
        heights = measure(blocks)
        laid_out, groups = paginate(blocks, ncols)
        open(tmp, "w", encoding="utf-8").write(laid_out)
        subprocess.run([sys.executable, "build_pdf.py", tmp, out_pdf], check=True,
                       stdout=subprocess.DEVNULL)
        got = pages_of(out_pdf)
        if got == want_pages:
            os.remove(tmp)
            fill = ", ".join(f"{100*sum(heights[a:b])/PAGE_H:.0f}%" for a, b in groups)
            print(f"  {out_pdf}: {got} page(s) at {pt}pt   columns {fill}")
            return pt
    if os.path.exists(tmp):
        os.remove(tmp)
    raise SystemExit(f"{src_md}: nothing fits {want_pages} pages")


if __name__ == "__main__":
    print("1. rendering equations ...")
    subprocess.run([sys.executable, "render_eq_exam3.py"], check=True,
                   stdout=subprocess.DEVNULL)
    print(f"   {len(os.listdir('assets'))} images in assets/")

    print("2. building instruction sheet (must be 2 pages) ...")
    build("qsection.md", "chem_x19a_mt3_instruction_sheet.pdf",
          ncols=4, want_pages=2,
          font_candidates=[10.0, 9.8, 9.6, 9.4, 9.2, 9.0, 8.8, 8.6,
                           8.4, 8.2, 8.0, 7.8, 7.6])

    print("3. building info sheet (must be 1 page) ...")
    build("info_sheet.md", "chem_x19a_mt3_info_sheet.pdf",
          ncols=2, want_pages=1,
          font_candidates=[9.4, 9.2, 9.0, 8.8, 8.6])

    print("\ndone.")

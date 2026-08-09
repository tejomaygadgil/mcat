#!/usr/bin/env python3
"""Build the CHEMx19A Final Exam sheet.

    uv run python build.py      ->  final.pdf   (2 pages)

Renders the LaTeX and diagram images, measures every box at the true column
width, splits the boxes into four balanced columns, then renders the PDF at
the largest font size that still fits on two pages.
"""
import os
import subprocess
import sys

# WeasyPrint dlopens the GTK stack (pango/cairo/gdk-pixbuf), which on macOS
# lives under the Homebrew prefix. dyld only reads DYLD_FALLBACK_LIBRARY_PATH
# at process launch, so setting it means re-exec'ing ourselves once. On Linux
# those libraries are already on the loader path and this is skipped.
if sys.platform == "darwin" and "DYLD_FALLBACK_LIBRARY_PATH" not in os.environ:
    brew = subprocess.run(["brew", "--prefix"], capture_output=True, text=True)
    if brew.returncode == 0:
        os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = f"{brew.stdout.strip()}/lib"
        os.execv(sys.executable, [sys.executable, *sys.argv])

import re
import shutil

import markdown
import matplotlib
from PIL import Image
from weasyprint import HTML

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["mathtext.fontset"] = "cm"
os.chdir(os.path.dirname(os.path.abspath(__file__)))

SRC, OUT, ASSETS = "sheet.md", "final.pdf", "assets"
WANT_PAGES = 2
N_COLS = 4                               # 2 pages x 2 columns
PT_START, PT_MIN, PT_STEP = 8.8, 7.2, 0.2

PAGE_H = 11 * 72 - 2 * 0.3 * 72          # usable column height, points
COL_W = (8.5 - 0.6 - 0.16) / 2           # usable column width, inches
PX_TO_PT = 0.75                          # WeasyPrint lays out in CSS px
MD_EXT = ["tables", "sane_lists", "md_in_html"]


# ============================================================== figures ====

DPI = 400
FONTSIZE = 22

# Block equations -- these get a line of their own on the sheet.
EQ_BLOCK = {
    "e_dhsoln": r"\Delta H_{solution} = \Delta H_{hydration} - \Delta H_{lattice\ energy}",
    "e_conc":   r"M = \dfrac{mol\ solute}{L\ solution}\qquad m = \dfrac{mol\ solute}{kg\ solvent}",
    "e_wv":     r"\%\,w/v = \dfrac{g\ solute}{100\ mL\ soln}\ \Rightarrow\ g = \dfrac{\%\times mL}{100}",
    "e_henry":  r"C_{gas} = k_H\,P_{gas}\qquad k_H = C_{gas}/P_{gas}",
    "e_raoult": r"P_{soln} = \chi_{solvent}\,P^{\circ}_{solvent}\qquad \Delta P = \chi_{solute}\,P^{\circ}_{solvent}",
    "e_chi":    r"\chi_{solvent} = \dfrac{mol_{solvent}}{mol_{solvent} + i\cdot mol_{solute}}",
    "e_coll":   r"\Delta T_f = i\,K_f\,m\qquad \Delta T_b = i\,K_b\,m",
    "e_osm":    r"\pi = i\,M\,R\,T\ \Rightarrow\ M = \dfrac{\pi}{i\,R\,T}",
}


def _mathtext(name, latex, color, pad):
    fig = plt.figure()
    fig.text(0.5, 0.5, f"${latex}$", fontsize=FONTSIZE, color=color,
             ha="center", va="center")
    fig.savefig(os.path.join(ASSETS, f"{name}.png"), dpi=DPI, transparent=True,
                bbox_inches="tight", pad_inches=pad)
    plt.close(fig)


def _mo_panel(ax, x0, sigma_low):
    """One MO energy-ladder panel; returns {level: (x, y)} centers.

    sigma_low=True is the O2/F2/Ne2 ordering (sigma2p below pi2p),
    False the B2/C2/N2 ordering (s-p mixing pushes sigma2p above pi2p).
    """
    W = 1.5      # single-level width
    G = 0.35     # gap in the doubled pi levels
    ys = {"s2s": 0.6, "s2s*": 1.9}
    if sigma_low:
        ys.update({"s2p": 3.4, "pi2p": 4.6, "pi2p*": 6.1, "s2p*": 7.4})
    else:
        ys.update({"pi2p": 3.4, "s2p": 4.6, "pi2p*": 6.1, "s2p*": 7.4})
    lab = {"s2s": r"$\sigma_{2s}$", "s2s*": r"$\sigma^*_{2s}$",
           "s2p": r"$\sigma_{2p}$", "pi2p": r"$\pi_{2p}$",
           "pi2p*": r"$\pi^*_{2p}$", "s2p*": r"$\sigma^*_{2p}$"}
    pos = {}
    for lvl, y in ys.items():
        double = lvl.startswith("pi")
        if double:
            for k, dx in enumerate((-(W + G) / 2, (W + G) / 2)):
                ax.plot([x0 + dx - W / 2, x0 + dx + W / 2], [y, y],
                        color="#111111", lw=1.8)
            pos[lvl] = [(x0 - (W + G) / 2, y), (x0 + (W + G) / 2, y)]
            lx = x0 - (W + G) / 2 - W / 2 - 0.25
        else:
            ax.plot([x0 - W / 2, x0 + W / 2], [y, y], color="#111111", lw=1.8)
            pos[lvl] = [(x0, y)]
            lx = x0 - W / 2 - 0.25
        ax.text(lx, y, lab[lvl], ha="right", va="center", fontsize=17)
    return pos


def render_figures():
    """Rebuild assets/ from scratch: equations, then the three diagrams."""
    shutil.rmtree(ASSETS, ignore_errors=True)
    os.makedirs(ASSETS)
    for name, latex in EQ_BLOCK.items():
        _mathtext(name, latex, "#111111", 0.04)

    # Heat-of-solution derivation for (18) -- three stacked lines, one image.
    fig = plt.figure()
    fig.text(0.5, 0.5, "\n".join((
        r"$\Delta H_{solution} = \Delta H_{solute} + (\Delta H_{solvent} + \Delta H_{mix})$",
        r"$\Delta H_{solute} = -\Delta H_{lattice\ energy}$",
        r"$(\Delta H_{hydration} = \Delta H_{solvent} + \Delta H_{mix})$")),
        fontsize=FONTSIZE, color="#111111", ha="center", va="center",
        linespacing=1.5)
    fig.savefig(os.path.join(ASSETS, "e_dhderiv.png"), dpi=DPI,
                transparent=True, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)

    # MO diagrams for (25) -- the two period-2 fill orders, O2 filled in as
    # the worked example (2 unpaired pi* electrons -> paramagnetic).
    fig = plt.figure(figsize=(9.2, 4.1))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 13.4); ax.set_ylim(-0.1, 9.4); ax.axis("off")
    ax.text(2.9, 8.6, "B$_2$  C$_2$  N$_2$", ha="center", va="center",
            fontsize=18, fontweight="bold")
    ax.text(9.9, 8.6, "O$_2$ filled  (F$_2$, Ne$_2$, NO, OF$^-$, Cl$_2$...)",
            ha="center", va="center", fontsize=18, fontweight="bold")
    _mo_panel(ax, 2.9, sigma_low=False)
    pos = _mo_panel(ax, 9.9, sigma_low=True)
    fills = {"s2s": ["↑↓"], "s2s*": ["↑↓"], "s2p": ["↑↓"],
             "pi2p": ["↑↓", "↑↓"], "pi2p*": ["↑", "↑"]}
    for lvl, arrows in fills.items():
        for (x, y), a in zip(pos[lvl], arrows):
            ax.text(x, y + 0.08, a, ha="center", va="bottom", fontsize=15,
                    color="#7a1f2b")
    fig.savefig(os.path.join(ASSETS, "f_mo.png"), dpi=DPI, transparent=True,
                bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)

    # Phase diagram for (14) -- generic curves, water's back-leaning fusion
    # line dashed, CO2 note lives in the box text.
    fig = plt.figure(figsize=(9.2, 5.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 10.6); ax.set_ylim(0, 10); ax.axis("off")
    ax.annotate("", xy=(10.3, 0.8), xytext=(0.7, 0.8),
                arrowprops=dict(arrowstyle="-|>", color="#111111", lw=1.4))
    ax.annotate("", xy=(0.7, 9.8), xytext=(0.7, 0.8),
                arrowprops=dict(arrowstyle="-|>", color="#111111", lw=1.4))
    ax.text(10.15, 0.35, "T", ha="center", fontsize=18)
    ax.text(0.28, 9.5, "P", ha="center", fontsize=18)
    tp, cp = (4.6, 3.4), (8.6, 7.6)
    ax.plot([1.4, tp[0]], [1.1, tp[1]], color="#111111", lw=2)     # sublimation
    ax.plot([tp[0], cp[0]], [tp[1], cp[1]], color="#111111", lw=2)  # vaporization
    ax.plot([tp[0], 5.6], [tp[1], 9.6], color="#111111", lw=2)      # fusion
    ax.plot([tp[0], 3.6], [tp[1], 9.6], color="#7a1f2b", lw=2, ls="--")
    ax.text(3.35, 9.0, "H$_2$O", color="#7a1f2b", fontsize=16, ha="right")
    ax.text(5.75, 9.1, "most subst.", fontsize=16, ha="left")
    ax.plot(*tp, "o", ms=7, color="#111111")
    ax.plot(*cp, "o", ms=7, color="#111111")
    ax.text(tp[0] + 0.15, tp[1] - 0.55, "triple pt\n(3 phases)", fontsize=15,
            ha="left", va="top")
    ax.text(cp[0] + 0.25, cp[1] - 0.3, "critical pt", fontsize=15, ha="left")
    ax.text(2.4, 6.0, "SOLID", fontsize=18, fontweight="bold")
    ax.text(5.6, 5.6, "LIQUID", fontsize=18, fontweight="bold")
    ax.text(6.9, 1.7, "GAS", fontsize=18, fontweight="bold")
    ax.text(9.0, 9.2, "supercritical", fontsize=15, ha="center")
    fig.savefig(os.path.join(ASSETS, "f_phase.png"), dpi=DPI, transparent=True,
                bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)

    # Heating curve for (26) -- five segments, each labeled with its q.
    fig = plt.figure(figsize=(9.2, 4.6))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(-0.4, 11.6); ax.set_ylim(-1.6, 9.4); ax.axis("off")
    xs = [0.0, 1.6, 3.6, 5.6, 8.6, 10.2]
    ys = [0.6, 2.6, 2.6, 6.4, 6.4, 8.4]
    ax.plot(xs, ys, color="#111111", lw=2.2)
    ax.annotate("", xy=(11.4, -1.3), xytext=(0.0, -1.3),
                arrowprops=dict(arrowstyle="-|>", color="#111111", lw=1.2))
    ax.text(5.7, -1.0, "heat added  (reverse path: all q negative)",
            ha="center", fontsize=15)
    for x1, x2, y1, y2, txt, dy in (
            (0.0, 1.6, 0.6, 2.6, "q$_1$=m·C$_{ice}$·ΔT", 0.75),
            (1.6, 3.6, 2.6, 2.6, "q$_2$=n·ΔH$_{fus}$", 0.55),
            (3.6, 5.6, 2.6, 6.4, "q$_3$=m·C$_{liq}$·ΔT", 1.15),
            (5.6, 8.6, 6.4, 6.4, "q$_4$=n·ΔH$_{vap}$", 0.55),
            (8.6, 10.2, 6.4, 8.4, "q$_5$=m·C$_{gas}$·ΔT", 0.75)):
        ax.text((x1 + x2) / 2 + 0.35, (y1 + y2) / 2 - dy, txt, fontsize=15.5,
                ha="center", va="top")
    ax.text(0.4, 2.9, "mp", fontsize=14, ha="right", color="#7a1f2b")
    ax.text(4.7, 6.75, "bp", fontsize=14, ha="right", color="#7a1f2b")
    ax.text(0.8, 4.2, "solid", fontsize=15, ha="center")
    ax.text(4.0, 7.6, "liquid", fontsize=15, ha="center")
    ax.text(9.9, 5.4, "gas", fontsize=15, ha="center")
    fig.savefig(os.path.join(ASSETS, "f_heat.png"), dpi=DPI, transparent=True,
                bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)


# ========================================================= markdown -> PDF ==

EQ_RENDER_DPI = 400
EQ_SCALE = 0.378
EQ_VSQUASH = 0.9025
EQ_MAX_WIDTH_PT = 82

# Per-image width caps, in points. matplotlib sizes each PNG to its content,
# so without a cap a long equation would set its own scale on the page.
EQ_WIDTH_PT = {
    "e_dhsoln": 205, "e_dhderiv": 195, "e_conc": 175, "e_wv": 185, "e_henry": 170,
    "e_raoult": 215, "e_chi": 120, "e_coll": 150, "e_osm": 140,
    "f_mo": 184, "f_phase": 148, "f_heat": 175,
}

CSS = """
@page { size: Letter; margin: 0.3in; }
* { box-sizing: border-box; }
body { font-family: 'DejaVu Sans', sans-serif; font-size: 8.6pt;
       line-height: 1.12; color: #111; margin: 0; }
.cols { display: flex; gap: 0.16in; align-items: flex-start; }
.col  { flex: 1 1 0; min-width: 0; }
.page { break-after: page; line-height: 1.05; }
.page:last-child { break-after: auto; }
.page h4 { margin: 1.6pt 0 1.2pt; font-weight: 700; background: #111;
           color: #fff; padding: 0.5pt 4pt; border-radius: 2px;
           break-after: avoid; }
.page p { margin: 0.3pt 0; break-inside: avoid; }
.page ol, .page ul { padding-left: 9pt; margin: 0.3pt 0 0.7pt;
                     break-inside: avoid; }
.page li { margin: 0; padding: 0; }
.page ul + ol, .page ol + ul,
.page ul + ul, .page ol + ol { margin-top: 0; }
em { color: #444; }
table { width: 100%; border-collapse: collapse; margin: 1pt 0 2pt;
        font-size: 8pt; line-height: 1.05; break-inside: avoid; }
th, td { border: 0.6pt solid #999; padding: 0.5pt 2pt; text-align: left;
         vertical-align: middle; }
th { background: #eee; font-weight: 700; }
img.eq { display: block; max-width: 100%; margin: 0.5pt auto; }
img.eqi { display: inline-block; vertical-align: -0.15em; margin: 0 1pt; }
td:has(img.eq) { text-align: center; }
.problem { border: 0.5pt solid #999; border-radius: 2px;
           padding: 1pt 2.5pt 1pt; margin: 0 0 1pt;
           box-decoration-break: clone; -webkit-box-decoration-break: clone; }
.problem h4 { margin-top: 0; margin-left: -2.5pt; margin-right: -2.5pt; }
.nohdr thead { display: none; }
"""


def css(pt):
    """Base stylesheet plus the font sizes for this pass of the font search."""
    return (f"{CSS}.page {{ font-size: {pt}pt; }}\n"
            f".page h4 {{ font-size: {pt * 1.04:.2f}pt; }}\n"
            f".page table {{ font-size: {pt * 0.93:.2f}pt; }}\n")


def eq_style(png_path):
    """Fixed pt dimensions for one equation image, honouring its width cap."""
    with Image.open(png_path) as im:
        w_px, h_px = im.size
    h_pt = h_px * 72 / EQ_RENDER_DPI * EQ_SCALE
    w_pt = w_px * 72 / EQ_RENDER_DPI * EQ_SCALE
    name = os.path.splitext(os.path.basename(png_path))[0]
    max_w = EQ_WIDTH_PT.get(name, EQ_MAX_WIDTH_PT)
    if w_pt > max_w:
        h_pt *= max_w / w_pt
        w_pt = max_w
    return f"height:{h_pt * EQ_VSQUASH:.2f}pt;width:{w_pt:.2f}pt"


def inject_eq_sizes(text):
    return re.sub(
        r'<img src="(assets/[^"]+\.png)" class="(eqi?)">',
        lambda m: f'<img src="{m[1]}" class="{m[2]}" style="{eq_style(m[1])}">',
        text)


def to_html(md_text, pt):
    body = ""
    for page in re.split(r"\n?<!--\s*pagebreak\s*-->\n?", md_text):
        if not page.strip():
            continue
        divs = "".join(
            f'<div class="col">{markdown.markdown(c, extensions=MD_EXT)}</div>'
            for c in re.split(r"\n?<!--\s*colbreak\s*-->\n?", page) if c.strip())
        body += f'<div class="page"><div class="cols">{divs}</div></div>'
    return ('<!DOCTYPE html><html><head><meta charset="utf-8">'
            f"<style>{css(pt)}</style></head><body>{body}</body></html>")


def render_pdf(md_text, pt, out):
    """Write the sheet and report how many pages it came to."""
    doc = HTML(string=to_html(inject_eq_sizes(md_text), pt), base_url=".").render()
    doc.write_pdf(out)
    return len(doc.pages)


# =============================================================== layout ====

def _tick(msg):
    print(f"\r{msg}", end="", flush=True)


def top_blocks(text):
    """Split text into top-level <div>...</div> blocks, honouring nesting."""
    text = re.sub(r"\n?<!--\s*colbreak\s*-->\n?", "\n", text)   # drop stale breaks
    blocks, depth, start = [], 0, None
    for m in re.finditer(r"<div\b[^>]*>|</div>", text):
        if not m.group(0).startswith("</"):
            if depth == 0:
                start = m.start()
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                blocks.append(text[start:m.end()])
    return blocks


def measure(blocks, pt):
    """Laid-out height of each block at the real column width, in points.

    Each block is rendered alone into one absurdly tall column and closed with
    an anchor; WeasyPrint reports that anchor's y position, which is where the
    block's content ends.
    """
    heights = []
    for i, b in enumerate(blocks, 1):
        _tick(f"    measuring block {i}/{len(blocks)}   ")
        body = markdown.markdown(inject_eq_sizes(b), extensions=MD_EXT)
        html = (
            f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{css(pt)}\n'
            f"@page{{size:{COL_W}in 60in !important;margin:0 !important}}</style></head>"
            f'<body><div class="page"><div class="cols"><div class="col">{body}'
            f'<span id="end"></span></div></div></div></body></html>'
        )
        page = HTML(string=html, base_url=".").render().pages[0]
        heights.append(round(page.anchors["end"][1] * PX_TO_PT))
    _tick(" " * 40)
    return heights


def pack(heights):
    """Balanced split into N_COLS contiguous column groups.

    Unlike mt3's hand-pinned boundaries, the cut points are solved for: DP
    over (block index, columns left) minimising the tallest column. Returns
    (tallest column height, [(start, end), ...]).
    """
    n = len(heights)
    prefix = [0]
    for h in heights:
        prefix.append(prefix[-1] + h)

    from functools import lru_cache

    @lru_cache(maxsize=None)
    def best(i, k):
        """(max col height, first cut) packing blocks[i:] into k columns."""
        if k == 1:
            return prefix[n] - prefix[i], n
        res = (float("inf"), n)
        for j in range(i + 1, n - k + 2):
            head = prefix[j] - prefix[i]
            tail, _ = best(j, k - 1)
            cand = max(head, tail)
            if cand < res[0]:
                res = (cand, j)
        return res

    groups, i = [], 0
    for k in range(N_COLS, 0, -1):
        _, j = best(i, k)
        groups.append((i, j))
        i = j
    return best(0, N_COLS)[0], groups


def paginate(blocks, groups):
    """Emit markdown with break markers for the given column groups."""
    parts = []
    for i, (a, b) in enumerate(groups):
        sep = "" if i == 0 else ("\n\n<!--pagebreak-->\n\n" if i % 2 == 0
                                 else "\n\n<!--colbreak-->\n\n")
        parts.append(sep + "\n".join(blocks[a:b]))
    return "".join(parts) + "\n"


def fit(md_text):
    """Largest font (in PT_STEP increments) that ACTUALLY renders in WANT_PAGES.

    Ink height scales close to linearly with font size, so rather than scanning
    every candidate we measure once at PT_START, estimate the size that should
    just hit the page cap, and verify it by rendering. Line-wrap reflow means
    that estimate can land a step off the true boundary, so we nudge in the
    needed direction until the rendered page count matches -- typically 2-3
    renders total instead of a full scan of the font ladder.
    """
    CAP = PAGE_H * 0.95
    blocks = top_blocks(md_text)
    tried = []
    last_rendered = None

    def attempt(pt):
        nonlocal last_rendered
        last_rendered = pt
        heights = measure(blocks, pt)
        max_h, groups = pack(heights)
        _tick(f"    rendering PDF at {pt}pt ...")
        got = render_pdf(paginate(blocks, groups), pt, OUT)
        _tick(" " * 40)
        print(f"  {pt}pt -> {got} page(s)")
        tried.append(pt)
        return got, heights, groups, max_h

    pt = PT_START
    got, heights, groups, max_h = attempt(pt)

    if got != WANT_PAGES:
        est = round(round(pt * CAP / max_h / PT_STEP) * PT_STEP, 2)
        est = max(min(est, PT_START - PT_STEP), PT_MIN)
        if est not in tried:
            pt = est
            got, heights, groups, max_h = attempt(pt)

    while got != WANT_PAGES and round(pt - PT_STEP, 2) >= PT_MIN:
        pt = round(pt - PT_STEP, 2)
        if pt in tried:
            break
        got, heights, groups, max_h = attempt(pt)

    # the estimate can undershoot -- climb back up while it still fits, so we
    # don't leave readable font size on the table
    while got == WANT_PAGES and round(pt + PT_STEP, 2) <= PT_START:
        nxt = round(pt + PT_STEP, 2)
        if nxt in tried:
            break
        got2, heights2, groups2, max_h2 = attempt(nxt)
        if got2 != WANT_PAGES:
            break
        pt, got, heights, groups, max_h = nxt, got2, heights2, groups2, max_h2

    # attempt() always overwrites OUT, even on a failed try -- if the last
    # render wasn't the accepted pt (e.g. the climb loop's final overshoot),
    # re-render so the file on disk actually matches what we report
    if last_rendered != pt and got == WANT_PAGES:
        got, heights, groups, max_h = attempt(pt)

    if got != WANT_PAGES:
        raise SystemExit(f"{SRC}: nothing fits {WANT_PAGES} pages in "
                         f"[{PT_MIN}, {PT_START}]pt ({len(tried)} render(s) tried)")
    fill = ", ".join(f"{100 * sum(heights[a:b]) / PAGE_H:.0f}%" for a, b in groups)
    cuts = [b for _, b in groups[:-1]]
    print(f"  {OUT}: {got} page(s) at {pt}pt   columns {fill}   cuts {cuts}   "
          f"({len(tried)} render(s))")


if __name__ == "__main__":
    print("1. rendering figures ...")
    render_figures()
    print(f"   {len(os.listdir(ASSETS))} images in {ASSETS}/")

    print(f"2. building {OUT} (must be {WANT_PAGES} pages) ...")
    fit(open(SRC, encoding="utf-8").read())

    print("\ndone.")

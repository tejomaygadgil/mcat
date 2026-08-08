#!/usr/bin/env python3
"""Build the CHEMx19A Exam III sheet.

    uv run python build.py      ->  mt3.pdf   (2 pages, 20 numbered boxes)

Renders the LaTeX and diagram images, measures every box at the true column
width, splits the boxes into columns at PINS, then renders the PDF at the
largest font size that still fits on two pages.
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

import math
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

SRC, OUT, ASSETS = "sheet.md", "mt3.pdf", "assets"
WANT_PAGES = 2
PINS = [6, 13, 18]                       # column boundaries, in blocks
PT_START, PT_MIN, PT_STEP = 8.8, 7.6, 0.2

PAGE_H = 11 * 72 - 2 * 0.3 * 72          # usable column height, points
COL_W = (8.5 - 0.6 - 0.16) / 2           # usable column width, inches
CAP = PAGE_H * 0.95                      # leave a safety margin
PX_TO_PT = 0.75                          # WeasyPrint lays out in CSS px
MD_EXT = ["tables", "sane_lists", "md_in_html"]


# ============================================================== figures ====

DPI = 400
FONTSIZE = 22

# Block equations -- these get a line of their own on the sheet.
EQ_BLOCK = {
    "e3_photo":       r"KE = h\nu - \Phi = h(c/\lambda) - \Phi = \dfrac{1}{2}m_eu^2",
    "e3_photo_u":     r"u = \sqrt{(2hc/m_e)(1/\lambda - 1/\lambda_{thr})}",
    "e3_heisenberg":  r"\Delta x\cdot\Delta p \geq \dfrac{h}{4\pi} = \mathrm{5.2728e{-}35}\ \mathrm{J}{\cdot}\mathrm{s},\ \ \Delta p = m\Delta u",
    "e3_bondenthalpy": r"\Delta H_f = \Sigma BE(\mathrm{reactants}) - \Sigma BE(\mathrm{products})",
    "e3_dhfsum":      r"\Delta H_f = \Sigma\Delta H(\mathrm{broken}) + \Sigma\Delta H(\mathrm{formed})",
    "e3_dele":        r"E = h\nu = h(c/\lambda) = R(1/n_f^2-1/n_i^2)",
    "e3_bornhaber":   r"\Delta H\degree_f = \Delta H_{sub} + \Sigma IE + \dfrac{1}{2}BE + EA + U",
    "s5_ni_solve":    r"n_i = \sqrt{1/\left(1/n_f^2 - hc/(R\lambda)\right)}",
    "s5_nf_solve":    r"n_f = \sqrt{1/\left(1/n_i^2 + hc/(R\lambda)\right)}",
}

# Inline math -- variables and short expressions set into running text.
EQ_INLINE = {
    "m_lam": r"\lambda",         "m_nu":  r"\nu",
    "m_phi": r"\Phi",            "m_E":   r"E",
    "m_uv":  r"u",               "m_m":   r"m",
    "m_n":   r"n",               "m_Z":   r"Z",
    "m_ie":  r"IE",              "m_ie2": r"IE_2",
    "m_ea":  r"EA",              "m_en":  r"EN",
    "m_den": r"\Delta EN",       "m_Ul":  r"U",
    "m_dH":  r"\Delta H",        "m_sig": r"\Sigma",
    "q_l":   r"l",               "q_ml":  r"m_l",
    "q_ms":  r"m_s",             "q_msval": r"\pm 1/2",
    "q_n2":  r"n^2",             "q_2n2": r"2n^2",
    "v_c":   r"c",               "v_h":   r"h",
    "v_me":  r"m_e",             "v_zeff": r"Z_{eff}",
    "s_na":  r"N_A",             "s_dhf": r"\Delta H\degree_f",
    "s5_lamthr": r"\lambda_{thr}",  "s5_nuthr": r"\nu_{thr}",
    "s5_R":  r"R",               "s5_hc": r"hc",
    "s5_hR": r"h/R",             "s5_hcR": r"hc/R",
    "s20_2hcme": r"2hc/m_e",
    # compound expressions -- one image reads better than stitched letters
    "v_en":       r"\Delta EN = |EN_A - EN_B|",
    "v_u":        r"U \propto \dfrac{q_1 q_2}{r_1 + r_2}",
    "v_zeffdef":  r"Z_{eff} \approx Z - (\mathrm{core}\ e^-)",
    "v_fc":       r"FC = (\mathrm{valence}\ e^-) - [\mathrm{nonbonding}\ e^- + \#\,\mathrm{bonds}]",
    "x_phithr":   r"\Phi = h\nu_{thr} = h(c/\lambda_{thr})",
    "x_lamthr":   r"\lambda_{thr} = hc/\Phi",
    "x_keeq":     r"KE = h(c/\lambda) - \Phi",
    "x_ueq":      r"u = \sqrt{2\,KE/m_e}",
    "x_dpeq":     r"\Delta p = m\cdot\Delta u",
    "x_dxeq":     r"\Delta x \geq h/(4\pi\cdot\Delta p)",
}

# White variants, for the few symbols that sit on a black `####` header bar.
EQ_WHITE = {
    "s_zeff_w": r"Z_{eff}",
    "w_hnu":    r"h\nu",
    "w_cln":    r"c = \lambda\nu",
    "w_ephot":  r"E = h\nu = h\,(c/\lambda)",
    "w_deb":    r"\lambda = h/(m\cdot u)",
}


def _mathtext(name, latex, color, pad):
    fig = plt.figure()
    fig.text(0.5, 0.5, f"${latex}$", fontsize=FONTSIZE, color=color,
             ha="center", va="center")
    fig.savefig(os.path.join(ASSETS, f"{name}.png"), dpi=DPI, transparent=True,
                bbox_inches="tight", pad_inches=pad)
    plt.close(fig)


def render_figures():
    """Rebuild assets/ from scratch: equations, then the two diagrams."""
    shutil.rmtree(ASSETS, ignore_errors=True)
    os.makedirs(ASSETS)
    for name, latex in EQ_BLOCK.items():
        _mathtext(name, latex, "#111111", 0.04)
    for name, latex in EQ_INLINE.items():
        _mathtext(name, latex, "#111111", 0.02)
    for name, latex in EQ_WHITE.items():
        _mathtext(name, latex, "#ffffff", 0.02)

    # Born-Haber cycle diagram for (22) -- LiF example with per-step enthalpies.
    # Final font pt on the sheet = fontsize * 0.378 (EQ_SCALE), so 20 -> ~7.6pt.
    fig = plt.figure(figsize=(9.2, 4.9))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    BOX = dict(boxstyle="round,pad=0.35", fc="white", ec="#111111", lw=1.4)
    ARR = dict(arrowstyle="-|>", color="#7a1f2b", lw=2.0)
    ax.text(2.1, 8.9, r"$\mathrm{Li^+(g) + F^-(g)}$", ha="center", va="center",
            fontsize=20, bbox=BOX)
    ax.text(2.1, 5.0, r"$\mathrm{Li(g) + F(g)}$", ha="center", va="center",
            fontsize=20, bbox=BOX)
    ax.text(2.1, 1.1, r"$\mathrm{Li(s) + \frac{1}{2}F_2(g)}$", ha="center",
            va="center", fontsize=20, bbox=BOX)
    ax.text(8.7, 1.1, r"$\mathrm{LiF(s)}$", ha="center", va="center",
            fontsize=20, bbox=BOX)
    for x in (1.5, 2.7):
        ax.annotate("", xy=(x, 4.3), xytext=(x, 1.8), arrowprops=ARR)
        ax.annotate("", xy=(x, 8.2), xytext=(x, 5.7), arrowprops=ARR)
    ax.annotate("", xy=(8.7, 1.9), xytext=(3.8, 8.6), arrowprops=ARR)
    ax.annotate("", xy=(7.7, 1.1), xytext=(3.6, 1.1), arrowprops=ARR)
    ax.text(1.35, 3.05, "subl.\n+155.2", ha="right", va="center", fontsize=17)
    ax.text(2.85, 3.05, "diss.\n+75.3", ha="left", va="center", fontsize=17)
    ax.text(1.35, 6.95, "IE\n+520", ha="right", va="center", fontsize=17)
    ax.text(2.85, 6.95, "−EA\n−328", ha="left", va="center", fontsize=17)
    ax.text(6.9, 5.9, "−U\n−1017", ha="left", va="center", fontsize=17)
    ax.text(5.65, 0.45, r"$\Delta H\degree_f = -594.1$ kJ", ha="center",
            va="center", fontsize=17)
    out_path = os.path.join(ASSETS, "e3_bhcycle.png")
    fig.savefig(out_path, dpi=DPI, transparent=True,
                bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)

    # Lewis-structure gallery for page 2 -- correct completed structures for the
    # molecules asked in the practice exam, ch.9 slides, and ch.9 homework quiz.
    # Compact grid: captions sit directly under each structure.
    fig = plt.figure(figsize=(9.2, 19.1))
    W = 10.0
    H = W * 19.1 / 9.2
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    AFS, LFS = 16, 13
    R = 0.24     # bond clearance around atom label
    B = 0.72     # bond length

    def atom(x, y, s, fs=None):
        ax.text(x, y, s, ha="center", va="center", fontsize=fs or AFS,
                color="#111111")

    def bond(x1, y1, x2, y2, order=1):
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
        px, py = -uy, ux
        a1, b1 = x1 + ux * R, y1 + uy * R
        a2, b2 = x2 - ux * R, y2 - uy * R
        for o in {1: [0], 2: [-0.05, 0.05], 3: [-0.09, 0, 0.09]}[order]:
            ax.plot([a1 + px * o, a2 + px * o], [b1 + py * o, b2 + py * o],
                    color="#111111", lw=1.25, solid_capstyle="round")

    def lp(x, y, ang):
        a = math.radians(ang)
        cx, cy = x + math.cos(a) * R * 1.45, y + math.sin(a) * R * 1.45
        px, py = -math.sin(a), math.cos(a)
        for o in (-0.07, 0.07):
            ax.plot([cx + px * o], [cy + py * o], marker="o", ms=2.3,
                    color="#111111")

    def tlp(x, y, d):          # terminal single-bonded atom: 3 lone pairs
        for a in (d, d + 75, d - 75): lp(x, y, a)

    def dlp(x, y, d):          # terminal double-bonded atom: 2 lone pairs
        for a in (d + 50, d - 50): lp(x, y, a)

    def cap(x, y, s):
        ax.text(x, y, s, ha="center", va="center", fontsize=LFS,
                fontweight="bold", color="#111111")

    def brackets(xl, xr, yb, yt, q):
        for xs, sgn in ((xl, 1), (xr, -1)):
            ax.plot([xs + sgn * 0.09, xs, xs, xs + sgn * 0.09],
                    [yb, yb, yt, yt], color="#111111", lw=1.2)
        ax.text(xr + 0.1, yt, q, ha="left", va="center", fontsize=12,
                color="#111111")

    # --- row 1: CO2, CO, NH3, H2CO ---
    y = H - 0.85
    x = 1.1
    atom(x, y, "C"); atom(x - B, y, "O"); atom(x + B, y, "O")
    bond(x, y, x - B, y, 2); bond(x, y, x + B, y, 2)
    dlp(x - B, y, 180); dlp(x + B, y, 0)
    cap(x, y - 1.05, "CO$_2$")
    x = 3.5
    atom(x, y, "C"); atom(x + B, y, "O")
    bond(x, y, x + B, y, 3); lp(x, y, 180); lp(x + B, y, 0)
    cap(x + 0.36, y - 1.05, "CO")
    x = 5.9
    atom(x, y, "N"); atom(x - 0.8 * B, y, "H"); atom(x + 0.8 * B, y, "H")
    atom(x, y - 0.8 * B, "H")
    bond(x, y, x - 0.8 * B, y); bond(x, y, x + 0.8 * B, y)
    bond(x, y, x, y - 0.8 * B); lp(x, y, 90)
    cap(x, y - 1.05 - 0.25, "NH$_3$")
    x = 8.4
    atom(x, y, "C"); atom(x, y + 0.8 * B, "O")
    atom(x - 0.62 * B, y - 0.55 * B, "H"); atom(x + 0.62 * B, y - 0.55 * B, "H")
    bond(x, y, x, y + 0.8 * B, 2)
    bond(x, y, x - 0.62 * B, y - 0.55 * B); bond(x, y, x + 0.62 * B, y - 0.55 * B)
    dlp(x, y + 0.8 * B, 90)
    cap(x, y - 1.05, "H$_2$CO")

    # --- row 2: NF3, CH2Cl2, NH4+, ClO- ---
    y = H - 3.4
    x = 1.1
    atom(x, y, "N"); atom(x - B, y, "F"); atom(x + B, y, "F"); atom(x, y - 0.85 * B, "F")
    bond(x, y, x - B, y); bond(x, y, x + B, y); bond(x, y, x, y - 0.85 * B)
    lp(x, y, 90); tlp(x - B, y, 180); tlp(x + B, y, 0); tlp(x, y - 0.85 * B, 270)
    cap(x, y - 1.65, "NF$_3$")
    x = 3.5
    atom(x, y, "C"); atom(x, y + 0.8 * B, "H"); atom(x - 0.8 * B, y, "H")
    atom(x + B, y, "Cl"); atom(x, y - 0.85 * B, "Cl")
    bond(x, y, x, y + 0.8 * B); bond(x, y, x - 0.8 * B, y)
    bond(x, y, x + B, y); bond(x, y, x, y - 0.85 * B)
    tlp(x + B, y, 0); tlp(x, y - 0.85 * B, 270)
    cap(x, y - 1.65, "CH$_2$Cl$_2$")
    x = 5.95
    atom(x, y, "N"); atom(x, y + 0.75 * B, "H"); atom(x, y - 0.75 * B, "H")
    atom(x - 0.75 * B, y, "H"); atom(x + 0.75 * B, y, "H")
    bond(x, y, x, y + 0.75 * B); bond(x, y, x, y - 0.75 * B)
    bond(x, y, x - 0.75 * B, y); bond(x, y, x + 0.75 * B, y)
    brackets(x - 1.0, x + 1.0, y - 0.85, y + 0.85, "+")
    cap(x, y - 1.65, "NH$_4$$^+$")
    x = 8.35
    atom(x, y, "Cl"); atom(x + B, y, "O")
    bond(x, y, x + B, y)
    lp(x, y, 90); lp(x, y, 180); lp(x, y, 270)
    lp(x + B, y, 90); lp(x + B, y, 0); lp(x + B, y, 270)
    brackets(x - 0.62, x + B + 0.62, y - 0.55, y + 0.55, "−")
    cap(x + 0.36, y - 1.65, "ClO$^-$")

    # --- row 3: NO2- resonance pair, CO3 2- ---
    y = H - 6.5
    for k, (o1, o2) in enumerate(((2, 1), (1, 2))):
        x = 1.0 + k * 2.8
        ox1, oy1 = x - 0.75 * B, y - 0.55 * B
        ox2, oy2 = x + 0.75 * B, y - 0.55 * B
        atom(x, y, "N"); atom(ox1, oy1, "O"); atom(ox2, oy2, "O")
        bond(x, y, ox1, oy1, o1); bond(x, y, ox2, oy2, o2)
        lp(x, y, 90)
        (dlp if o1 == 2 else tlp)(ox1, oy1, 215)
        (dlp if o2 == 2 else tlp)(ox2, oy2, 325)
        brackets(x - 1.15, x + 1.15, y - 1.0, y + 0.45, "−")
    ax.text(2.4, y - 0.25, "↔", ha="center", va="center", fontsize=17,
            color="#111111")
    cap(2.4, y - 1.55, "NO$_2$$^-$ (2 equivalent forms)")
    x = 7.3
    atom(x, y, "C"); atom(x, y + 0.85 * B, "O")
    ox1, oy1 = x - 0.85 * B, y - 0.55 * B
    ox2, oy2 = x + 0.85 * B, y - 0.55 * B
    atom(ox1, oy1, "O"); atom(ox2, oy2, "O")
    bond(x, y, x, y + 0.85 * B, 2); bond(x, y, ox1, oy1); bond(x, y, ox2, oy2)
    dlp(x, y + 0.85 * B, 90); tlp(ox1, oy1, 215); tlp(ox2, oy2, 325)
    brackets(x - 1.35, x + 1.35, y - 1.0, y + 0.95, "2−")
    cap(x, y - 1.55, "CO$_3$$^{2-}$ (×3 forms)")

    # --- row 4: HNO3 (with formal charges), BeCl2, KCl, epoxide ---
    y = H - 9.4
    x = 1.35
    atom(x, y, "N"); atom(x, y + 0.85 * B, "O")
    atom(x - B, y, "O"); atom(x + B, y, "O"); atom(x + 1.75 * B, y, "H")
    bond(x, y, x, y + 0.85 * B, 2); bond(x, y, x - B, y); bond(x, y, x + B, y)
    bond(x + B, y, x + 1.75 * B, y)
    dlp(x, y + 0.85 * B, 90); tlp(x - B, y, 180)
    lp(x + B, y, 90); lp(x + B, y, 270)
    atom(x + 0.28, y + 0.32, "+", fs=10)
    atom(x - B - 0.12, y + 0.4, "−", fs=10)
    cap(x + 0.3, y - 1.25, "HNO$_3$ (FC on N, O)")
    x = 4.9
    atom(x, y, "Be"); atom(x - B, y, "Cl"); atom(x + B, y, "Cl")
    bond(x, y, x - B, y); bond(x, y, x + B, y)
    tlp(x - B, y, 180); tlp(x + B, y, 0)
    cap(x, y - 1.25, "BeCl$_2$ (4 e-)")
    x = 7.35
    atom(x - 1.1, y, "K$^+$"); atom(x, y, "Cl")
    lp(x, y, 0); lp(x, y, 90); lp(x, y, 180); lp(x, y, 270)
    brackets(x - 0.58, x + 0.58, y - 0.5, y + 0.5, "−")
    cap(x - 0.5, y - 1.25, "KCl (ionic)")
    x = 9.15
    atom(x, y + 0.45, "O")
    atom(x - 0.42, y - 0.3, "C"); atom(x + 0.42, y - 0.3, "C")
    bond(x, y + 0.45, x - 0.42, y - 0.3); bond(x, y + 0.45, x + 0.42, y - 0.3)
    bond(x - 0.42, y - 0.3, x + 0.42, y - 0.3)
    lp(x, y + 0.45, 130); lp(x, y + 0.45, 50)
    cap(x, y - 1.25, "Epoxide")

    # --- row 5: BF3, PCl5, SF6 ---
    y = H - 12.1
    x = 1.3
    atom(x, y, "B"); atom(x, y + B, "F")
    ox1, oy1 = x - 0.85 * B, y - 0.55 * B
    ox2, oy2 = x + 0.85 * B, y - 0.55 * B
    atom(ox1, oy1, "F"); atom(ox2, oy2, "F")
    bond(x, y, x, y + B); bond(x, y, ox1, oy1); bond(x, y, ox2, oy2)
    tlp(x, y + B, 90); tlp(ox1, oy1, 215); tlp(ox2, oy2, 325)
    cap(x, y - 1.7, "BF$_3$ (6 e-)")
    x = 4.9
    atom(x, y, "P")
    for adeg in (90, 162, 234, 306, 18):
        a = math.radians(adeg)
        fx, fy = x + math.cos(a) * B, y + math.sin(a) * B
        atom(fx, fy, "Cl", fs=14); bond(x, y, fx, fy); tlp(fx, fy, adeg)
    cap(x, y - 1.7, "PCl$_5$ (10 e-)")
    x = 8.3
    atom(x, y, "S")
    for adeg in (0, 60, 120, 180, 240, 300):
        a = math.radians(adeg)
        fx, fy = x + math.cos(a) * B, y + math.sin(a) * B
        atom(fx, fy, "F", fs=14); bond(x, y, fx, fy); tlp(fx, fy, adeg)
    cap(x, y - 1.7, "SF$_6$ (12 e-)")

    # --- row 6: CH3CHO, CH3CH2COOH, azide ---
    y = H - 15.2
    x = 1.1
    atom(x, y, "C"); atom(x - 0.72, y, "H")
    atom(x, y + 0.58, "H"); atom(x, y - 0.58, "H")
    bond(x, y, x - 0.72, y); bond(x, y, x, y + 0.58); bond(x, y, x, y - 0.58)
    atom(x + B, y, "C"); bond(x, y, x + B, y)
    atom(x + B, y + 0.62, "O"); bond(x + B, y, x + B, y + 0.62, 2)
    dlp(x + B, y + 0.62, 90)
    atom(x + 1.7 * B, y - 0.4, "H"); bond(x + B, y, x + 1.7 * B, y - 0.4)
    cap(x + 0.4, y - 1.3, "CH$_3$CHO (aldehyde)")
    x = 4.5
    for i in range(3):
        cx = x + i * B
        atom(cx, y, "C")
        if i: bond(cx - B, y, cx, y)
    atom(x - 0.72, y, "H"); bond(x, y, x - 0.72, y)
    for cx in (x, x + B):
        atom(cx, y + 0.58, "H"); bond(cx, y, cx, y + 0.58)
        atom(cx, y - 0.58, "H"); bond(cx, y, cx, y - 0.58)
    atom(x + 2 * B, y + 0.62, "O"); bond(x + 2 * B, y, x + 2 * B, y + 0.62, 2)
    dlp(x + 2 * B, y + 0.62, 90)
    atom(x + 3 * B, y, "O"); bond(x + 2 * B, y, x + 3 * B, y)
    lp(x + 3 * B, y, 90); lp(x + 3 * B, y, 270)
    atom(x + 3.72 * B, y, "H"); bond(x + 3 * B, y, x + 3.72 * B, y)
    cap(x + 1.1, y - 1.3, "CH$_3$CH$_2$COOH (carboxylic acid)")
    x = 8.6
    atom(x - 1.1, y, "R"); atom(x - 0.38, y, "N"); atom(x + 0.34, y, "N")
    atom(x + 1.06, y, "N")
    bond(x - 1.1, y, x - 0.38, y); bond(x - 0.38, y, x + 0.34, y)
    bond(x + 0.34, y, x + 1.06, y, 3)
    lp(x - 0.38, y, 90); lp(x - 0.38, y, 270); lp(x + 1.06, y, 0)
    atom(x - 0.38, y + 0.5, "−", fs=10); atom(x + 0.34, y + 0.5, "+", fs=10)
    cap(x, y - 1.3, "Azide (R–N$_3$)")

    # --- row 7: one-line templates ---
    y = H - 17.3
    x = 0.55
    atom(x, y, "R"); atom(x + 0.72, y, "O"); atom(x + 1.44, y, "H")
    bond(x, y, x + 0.72, y); bond(x + 0.72, y, x + 1.44, y)
    lp(x + 0.72, y, 90); lp(x + 0.72, y, 270)
    cap(x + 0.72, y - 0.95, "Alcohol")
    x = 2.85
    atom(x, y, "R"); atom(x + 0.72, y, "O"); atom(x + 1.44, y, "R")
    bond(x, y, x + 0.72, y); bond(x + 0.72, y, x + 1.44, y)
    lp(x + 0.72, y, 90); lp(x + 0.72, y, 270)
    cap(x + 0.72, y - 0.95, "Ether")
    x = 5.1
    atom(x, y, "R"); atom(x + 0.72, y, "O"); atom(x + 1.44, y, "O")
    atom(x + 2.16, y, "R")
    bond(x, y, x + 0.72, y); bond(x + 0.72, y, x + 1.44, y)
    bond(x + 1.44, y, x + 2.16, y)
    for ox in (0.72, 1.44):
        lp(x + ox, y, 90); lp(x + ox, y, 270)
    cap(x + 1.08, y - 0.95, "Peroxide")
    x = 8.15
    atom(x, y, "R"); atom(x + 0.72, y, "N"); bond(x, y, x + 0.72, y)
    atom(x + 1.35, y + 0.42, "R"); bond(x + 0.72, y, x + 1.35, y + 0.42)
    atom(x + 1.35, y - 0.42, "R"); bond(x + 0.72, y, x + 1.35, y - 0.42)
    lp(x + 0.72, y, 90)
    cap(x + 0.72, y - 0.95, "Amine")

    # --- row 8: C=O templates ---
    y = H - 19.4
    def carbonyl(x, right):
        atom(x, y, "R"); atom(x + 0.72, y, "C")
        atom(x + 0.72, y + 0.62, "O")
        bond(x, y, x + 0.72, y); bond(x + 0.72, y, x + 0.72, y + 0.62, 2)
        dlp(x + 0.72, y + 0.62, 90)
        return x + 0.72
    c = carbonyl(0.6, None)
    atom(c + 0.62, y - 0.38, "H"); bond(c, y, c + 0.62, y - 0.38)
    cap(c, y - 1.15, "Aldehyde")
    c = carbonyl(2.75, None)
    atom(c + 0.72, y, "R"); bond(c, y, c + 0.72, y)
    cap(c + 0.2, y - 1.15, "Ketone")
    c = carbonyl(4.9, None)
    atom(c + 0.72, y, "O"); bond(c, y, c + 0.72, y)
    lp(c + 0.72, y, 90); lp(c + 0.72, y, 270)
    atom(c + 1.4, y, "H"); bond(c + 0.72, y, c + 1.4, y)
    cap(c + 0.5, y - 1.15, "Carboxylic acid")
    c = carbonyl(7.6, None)
    atom(c + 0.72, y, "N"); bond(c, y, c + 0.72, y)
    lp(c + 0.72, y, 90)
    atom(c + 1.35, y + 0.42, "R"); bond(c + 0.72, y, c + 1.35, y + 0.42)
    atom(c + 1.35, y - 0.42, "R"); bond(c + 0.72, y, c + 1.35, y - 0.42)
    cap(c + 0.55, y - 1.15, "Amide")

    out_path = os.path.join(ASSETS, "e3_lewis.png")
    fig.savefig(out_path, dpi=DPI, transparent=True,
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
    "e3_photo": 210, "e3_photo_u": 190, "e3_heisenberg": 175,
    "e3_bondenthalpy": 240, "e3_dhfsum": 240, "e3_dele": 220,
    "s5_ni_solve": 105, "s5_nf_solve": 105, "e3_bornhaber": 235, "v_c": 6,
    "v_h": 7, "v_me": 15, "v_zeff": 22, "v_en": 112, "v_u": 62,
    "v_zeffdef": 108, "v_fc": 205, "s_na": 17, "s_dhf": 26, "s_zeff_w": 21,
    "s5_lamthr": 30, "s5_nuthr": 28, "m_lam": 7, "m_nu": 7, "m_phi": 9,
    "m_E": 8, "m_uv": 6, "m_ie": 15, "m_ie2": 21, "m_ea": 19, "m_en": 19,
    "m_den": 33, "m_Ul": 9, "m_dH": 21, "m_sig": 10, "x_phithr": 128,
    "x_lamthr": 60, "x_keeq": 86, "x_ueq": 66, "q_l": 6, "q_ml": 17,
    "q_ms": 18, "q_msval": 20, "q_n2": 14, "q_2n2": 20, "m_Z": 9, "m_m": 10,
    "m_n": 8, "x_dpeq": 64, "x_dxeq": 86, "w_hnu": 18, "w_cln": 40,
    "w_ephot": 104, "w_deb": 76, "s5_R": 8, "s5_hc": 18, "s5_hR": 32,
    "s5_hcR": 48, "s20_2hcme": 48, "e3_bhcycle": 250, "e3_lewis": 262,
}

CSS = """
@page { size: Letter; margin: 0.3in; }
* { box-sizing: border-box; }
body { font-family: 'DejaVu Sans', sans-serif; font-size: 8.6pt;
       line-height: 1.12; color: #111; margin: 0; }
.cols { display: flex; gap: 0.16in; align-items: flex-start; }
.col  { flex: 1 1 0; min-width: 0; }
.page { break-after: page; line-height: 1.06; }
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
th, td { border: 0.6pt solid #999; padding: 0.6pt 2.5pt; text-align: left;
         vertical-align: middle; }
th { background: #eee; font-weight: 700; }
img.eq { display: block; max-width: 100%; margin: 0.5pt auto; }
img.eqi { display: inline-block; vertical-align: -0.15em; margin: 0 1pt; }
td:has(img.eq) { text-align: center; }
.problem { border: 0.5pt solid #999; border-radius: 2px;
           padding: 1pt 2.5pt 1.2pt; margin: 0 0 1.2pt;
           box-decoration-break: clone; -webkit-box-decoration-break: clone; }
.problem h4 { margin-top: 0; margin-left: -2.5pt; margin-right: -2.5pt; }
.nohdr thead { display: none; }
.lut table { font-size: 7.2pt; table-layout: fixed; }
.lut th, .lut td { padding: 0.8pt 1.5pt; text-align: center;
                   word-break: break-word; }
.lut th:nth-child(1), .lut td:nth-child(1) { text-align: left; }
.lut-w1 th:nth-child(1), .lut-w1 td:nth-child(1) { width: 42%; }
.emtable table { font-size: 6.8pt; }
.emtable th, .emtable td { padding: 0.5pt 1pt; text-align: center;
                           white-space: nowrap; }
.emtable th:nth-child(1), .emtable td:nth-child(1) { text-align: left; }
"""


def css(pt):
    """Base stylesheet plus the font sizes for this pass of the font search."""
    return (f"{CSS}.page {{ font-size: {pt}pt; }}\n"
            f".page h4 {{ font-size: {pt * 1.04:.2f}pt; }}\n")


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
    """Column groups from PINS, plus the tallest column's height in points."""
    cuts = [0] + PINS + [len(heights)]
    groups = [(cuts[i], cuts[i + 1]) for i in range(len(cuts) - 1)]
    return max(sum(heights[a:b]) for a, b in groups), groups


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
    print(f"  {OUT}: {got} page(s) at {pt}pt   columns {fill}   "
          f"({len(tried)} render(s))")


if __name__ == "__main__":
    print("1. rendering figures ...")
    render_figures()
    print(f"   {len(os.listdir(ASSETS))} images in {ASSETS}/")

    print(f"2. building {OUT} (must be {WANT_PAGES} pages) ...")
    fit(open(SRC, encoding="utf-8").read())

    print("\ndone.")

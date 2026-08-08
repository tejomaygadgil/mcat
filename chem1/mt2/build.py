#!/usr/bin/env python3
"""Build the CHEMx19A Exam II sheet.

    uv run python build.py      ->  mt2.pdf   (2 pages)

Unlike the Exam III sheet, breaks here are hand-placed: sheet.md carries its
own <!--colbreak--> and <!--pagebreak--> markers and the type sizes are fixed,
so there is no measuring pass and no font search.
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

SRC, OUT, ASSETS = "sheet.md", "mt2.pdf", "assets"
WANT_PAGES = 2
MD_EXT = ["tables", "sane_lists", "md_in_html"]


# ============================================================== figures ====

DPI = 400
FONTSIZE = 22

EQUATIONS = {
    "eq_combined":  r"\dfrac{P_1V_1}{T_1} = \dfrac{P_2V_2}{T_2}",
    "eq_ideal":     r"PV = nRT",
    "eq_rms":       r"u_{rms} = \sqrt{\dfrac{3RT}{\mathcal{M}} \cdot 1000}",
    "eq_density":   r"d = \dfrac{\mathcal{M}P}{RT} \leftrightarrow \mathcal{M} = \dfrac{dRT}{P}",
    "eq_enthalpy":  r"\Delta H = \Delta U + P\Delta V",
    "eq_econs":     r"\Delta_{uni} = \Delta_{sys} + \Delta_{sur} = 0",
    "eq_intU":      r"\Delta U = q + w = -\Delta_{sur}",
    "eq_heat":      r"q = mC\Delta T",
    "eq_work":      r"w = -P\Delta V",
    "eq_calor_coffee": r"q_{rxn} = -C_{cal}\Delta T",
    "eq_calor_bomb":   r"q_{rxn} = -(mC + C_b)\Delta T",
    "eq_hform":     r"\Delta H\degree_{rxn} = \Sigma\, n\Delta H\degree_{f,p} - \Sigma\, n\Delta H\degree_{f,r}",
    "eq_R_atm":     r"R = 0.08206\ \mathrm{L \cdot atm / (mol \cdot K)}",
    "eq_R_J":       r"R = 8.314\ \mathrm{J / (mol \cdot K)}",
    "eq_heat_note": r"C_{H_2O} = 4.184\ \mathrm{J / (g \cdot \degree C)}",
    "eq_work_note": r"101.3\ \mathrm{J} = 1\ \mathrm{L \times atm}",
    "eq_hform_note": r"\Delta H\degree_{rxn} = \mathrm{kJ/mol}",
    "s2_ke":        r"KE = \frac{1}{2}mv^2",
    "s2_urms":      r"u_{rms} = \sqrt{\dfrac{3RT}{\mathcal{M}} \cdot 1000},\ \ R = 8.314\,\frac{J}{mol\,K}",
    "s2_dalton":    r"P_{tot} = P_A + P_B + P_C",
    "s2_dilution":  r"V_1 M_1 = V_2 M_2\ \ (M = \mathrm{mol/L})",
    "s2_combined":  r"\dfrac{P_1 V_1}{T_1} = \dfrac{P_2 V_2}{T_2}\ \ (T\ \mathrm{in\ K})",
    "s2_ideal":     r"PV = nRT,\ \ R = 0.08206\,\frac{atm\,L}{mol\,K}",
    "s2_deltaE":    r"\Delta E = q + w",
    "s2_work":      r"w = -P\Delta V\ \ (101.3\,\mathrm{J} = 1\,\mathrm{L\,atm})",
    "s2_enthalpy":  r"\Delta H = \Delta U + P\Delta V",
    "s2_q":         r"q = mC\Delta T,\ \ C_{H_2O} = 4.184\,\frac{J}{g\,\degree C}",
    "s2_yield":     r"\%\,\mathrm{yield} = \dfrac{\mathrm{actual}}{\mathrm{theoretical}} \times 100",
    "s2_hess":      r"\Delta H_{rxn} = \Sigma\,\Delta H\,(\mathrm{steps})",
    "s2_hform":     r"\Delta H\degree_{rxn} = \Sigma n\Delta H\degree_{f,p} - \Sigma n\Delta H\degree_{f,r}",
    "s2_mv":        r"\%\,(w/v) = \dfrac{\mathrm{g\ solute}}{100\ \mathrm{mL}}",
    "s2_calor":     r"q_{rxn} = -(mC\Delta T + C_{cal}\Delta T),\ \ C_{H_2O} = 4.184\,\frac{J}{g\,\degree C}",
    "s2_stp":       r"\mathrm{STP:}\ 273\,K,\ 1\,atm,\ 22.4\,\frac{L}{mol}",
    "s2_gasmm":     r"\mathcal{M} = \dfrac{mRT}{PV},\ \ d = \dfrac{P\mathcal{M}}{RT}",
    "s2_wetgas":    r"P_{gas} = P_{total} - P_{H_2O}",
    "s2_pchain":    r"1\,atm = 760\,\mathrm{mmHg} = 760\,\mathrm{torr} = 14.7\,\mathrm{psi} = 101.3\,\mathrm{kPa}",
}


def render_figures():
    """Rebuild assets/ from scratch."""
    shutil.rmtree(ASSETS, ignore_errors=True)
    os.makedirs(ASSETS)
    for name, latex in EQUATIONS.items():
        fig = plt.figure()
        fig.text(0.5, 0.5, f"${latex}$", fontsize=FONTSIZE, color="#111111",
                 ha="center", va="center")
        fig.savefig(os.path.join(ASSETS, f"{name}.png"), dpi=DPI,
                    transparent=True, bbox_inches="tight", pad_inches=0.04)
        plt.close(fig)


# ========================================================= markdown -> PDF ==

EQ_RENDER_DPI = 400
EQ_SCALE = 0.378
EQ_VSQUASH = 0.95
EQ_MAX_WIDTH_PT = 82

# Per-image width caps, in points. matplotlib sizes each PNG to its content,
# so without a cap a long equation would set its own scale on the page.
EQ_WIDTH_PT = {
    "eq_hform": 128,
    "s2_dilution": 105, "s2_ideal": 110, "s2_q": 110, "s2_work": 115,
    "s2_urms": 140, "s2_stp": 108, "s2_pchain": 195, "s2_hform": 128,
    "s2_calor": 168, "s2_combined": 90, "s2_hess": 85, "s2_yield": 100,
}


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
        r'<img src="(assets/[^"]+\.png)" class="eq">',
        lambda m: f'<img src="{m[1]}" class="eq" style="{eq_style(m[1])}">',
        text)


CSS = """
@page { size: Letter; margin: 0.3in; }
* { box-sizing: border-box; }
body { font-family: 'DejaVu Sans', sans-serif; font-size: 8.6pt;
       line-height: 1.12; color: #111; margin: 0; }
.cols { display: flex; gap: 0.26in; align-items: flex-start; }
.col  { flex: 1 1 0; min-width: 0; }
.page { break-after: page; }
.page:last-child { break-after: auto; }
h2 { font-size: 10pt; font-weight: 700; margin: 0 0 2pt; }
h3 { font-size: 9.5pt; margin: 4pt 0 1.5pt; padding: 0.5pt 4pt;
     background: #111; color: #fff; border-radius: 2px; break-after: avoid; }
h4 { font-size: 8.8pt; margin: 2.5pt 0 1pt; padding-bottom: 0.5pt;
     border-bottom: 0.75pt solid #bbb; break-after: avoid; }
p  { margin: 0.8pt 0; break-inside: avoid; }
em { color: #444; }
table { width: 100%; border-collapse: collapse; margin: 1pt 0 2pt;
        font-size: 8pt; line-height: 1.05; break-inside: avoid; }
th, td { border: 0.6pt solid #999; padding: 0.6pt 2.5pt; text-align: left;
         vertical-align: middle; }
th { background: #eee; font-weight: 700; }
img.eq { display: block; max-width: 100%; margin: 1pt auto; }
td:has(img.eq) { text-align: center; }
td:nth-child(1), th:nth-child(1) { width: 24%; }
td:nth-child(2), th:nth-child(2) { width: 36%; }
ol, ul { margin: 1pt 0 2pt; padding-left: 14pt; break-inside: avoid; }
li { margin: 0; padding: 0; }
hr { border: none; border-top: 0.6pt dashed #ccc; margin: 3pt 0; }
.ch7 h2 { margin-bottom: 2pt; }
.ch7 h4 { font-size: 8pt; margin: 2pt 0 0.5pt; padding-bottom: 0.3pt; }
.ch7 em { font-size: 7.3pt; }
.ch7 table { font-size: 7.3pt; line-height: 0.98; margin: 0.5pt 0 2pt; }
.ch7 th, .ch7 td { padding: 0.3pt 2pt; }
.page:nth-child(2) { font-size: 6.75pt; line-height: 1.02; }
.page:nth-child(2) h2 { font-size: 8.2pt; margin: 0 0 1.5pt; }
.page:nth-child(2) h4 { font-size: 7pt; margin: 1.6pt 0 0.3pt; padding-bottom: 0.3pt;
                        border-bottom: 0.5pt solid #ccc; }
.page:nth-child(2) ol, .page:nth-child(2) ul { padding-left: 9pt; margin: 0.3pt 0 0.7pt; }
.page:nth-child(2) li { margin: 0; }
.page:nth-child(2) p { margin: 0.3pt 0; }
.page:nth-child(2) .cols { gap: 0.18in; }
.page:nth-child(2) ul + ol, .page:nth-child(2) ol + ul,
.page:nth-child(2) ul + ul, .page:nth-child(2) ol + ol { margin-top: 0; }
.page:nth-child(2) img.eq { margin: 0.5pt auto; }
"""


def to_html(md_text):
    body = ""
    for page in re.split(r"\n?<!--\s*pagebreak\s*-->\n?", md_text):
        if not page.strip():
            continue
        divs = "".join(
            f'<div class="col">{markdown.markdown(c, extensions=MD_EXT)}</div>'
            for c in re.split(r"\n?<!--\s*colbreak\s*-->\n?", page) if c.strip())
        body += f'<div class="page"><div class="cols">{divs}</div></div>'
    return ('<!DOCTYPE html><html><head><meta charset="utf-8">'
            f"<style>{CSS}</style></head><body>{body}</body></html>")


if __name__ == "__main__":
    print("1. rendering figures ...")
    render_figures()
    print(f"   {len(os.listdir(ASSETS))} images in {ASSETS}/")

    print(f"2. building {OUT} ...")
    md = inject_eq_sizes(open(SRC, encoding="utf-8").read())
    doc = HTML(string=to_html(md), base_url=".").render()
    doc.write_pdf(OUT)
    got = len(doc.pages)
    if got != WANT_PAGES:
        raise SystemExit(f"{OUT}: {got} page(s), expected {WANT_PAGES} -- "
                         f"adjust the breaks in {SRC}")
    print(f"   {OUT}: {got} page(s)")

    print("\ndone.")

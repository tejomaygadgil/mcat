#!/usr/bin/env python3
import re
import os
import markdown
from weasyprint import HTML
from PIL import Image

EQ_RENDER_DPI = 400
EQ_SCALE = 0.378
EQ_VSQUASH = 0.9025
EQ_MAX_WIDTH_PT = 82
EQ_WIDTH_OVERRIDES = {
    "eq_hform": 98,
    "s2_dilution": 105, "s2_ideal": 130, "s2_q": 110, "s2_work": 115,
    "s2_urms": 160, "s2_stp": 108, "s2_pchain": 195, "s2_hform": 128,
    "s2_calor": 168, "s2_combined": 100, "s2_hess": 85, "s2_yield": 120,
    "s2_molarity": 95, "s2_mv": 105, "s2_gasmm": 115,
    "e3_speed": 175, "e3_energy": 195, "e3_debroglie": 170,
    "e3_photo": 130, "e3_heisenberg": 175, "e3_formalcharge": 220,
    "e3_bondenthalpy": 240, "e3_mole": 110, "e3_me": 130, "e3_ke": 90,
    "e3_bohr": 150, "e3_dele": 200, "e3_zeff": 130, "e3_lattice": 78, "e3_den": 120,
    "e3_bornhaber": 235, "e3_cln": 60, "e3_ephoton": 92,
    "e3_debroglie2": 58, "e3_fc": 215,
    "v_c": 6, "v_h": 7, "v_me": 15, "v_na": 18, "v_zeff": 22,
    "v_en": 112, "v_u": 62, "v_zeffdef": 108, "v_debroglie": 52,
    "v_cln": 44, "v_eph": 78, "v_fc": 205,
    "s_na": 17, "s_zeff": 21, "s_ephot": 38, "s_dhrxn": 32,
    "s_lamthr": 52, "s_dhf": 26, "s_zeffeq": 92, "s_zeff_w": 21,
    "s5_de": 150, "s5_solven": 190, "s5_cascade": 170,
}

def eq_style(png_path):
    with Image.open(png_path) as im:
        w_px, h_px = im.size
    h_pt = h_px * 72 / EQ_RENDER_DPI * EQ_SCALE
    w_pt = w_px * 72 / EQ_RENDER_DPI * EQ_SCALE
    name = os.path.splitext(os.path.basename(png_path))[0]
    max_w = EQ_WIDTH_OVERRIDES.get(name, EQ_MAX_WIDTH_PT)
    if w_pt > max_w:
        ratio = max_w / w_pt
        h_pt *= ratio
        w_pt = max_w
    h_pt *= EQ_VSQUASH
    return f'height:{h_pt:.2f}pt;width:{w_pt:.2f}pt'


def inject_eq_sizes(text):
    def repl(m):
        src, cls = m.group(1), m.group(2)
        return f'<img src="{src}" class="{cls}" style="{eq_style(src)}">'
    return re.sub(r'<img src="(assets/[^"]+\.png)" class="(eqi?)">', repl, text)

import sys
SRC = sys.argv[1] if len(sys.argv)>1 else "chem_x19a_exam3_cheatsheet.md"
OUT = sys.argv[2] if len(sys.argv)>2 else "chem_x19a_exam3_cheatsheet.pdf"

md_text = open(SRC, encoding="utf-8").read()
md_text = inject_eq_sizes(md_text)

MD_EXTENSIONS = ["tables", "sane_lists", "md_in_html"]
COLBREAK = r"\n?<!--\s*colbreak\s*-->\n?"


def columns(md_chunk):
    pieces = [p for p in re.split(COLBREAK, md_chunk) if p.strip()]
    return [markdown.markdown(p, extensions=MD_EXTENSIONS) for p in pieces]


PAGEBREAK = r"\n?<!--\s*pagebreak\s*-->\n?"


def render_page(page_md):
    cols = "".join(f'<div class="col">{c}</div>' for c in columns(page_md))
    if page_md.count("<!--colbreak") == 0:
        cols += '<div class="col"></div>'
    return f'<div class="page"><div class="cols">{cols}</div></div>'


pages = [p for p in re.split(PAGEBREAK, md_text) if p.strip()]
body = "".join(render_page(p) for p in pages)

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
h4 { font-size: 8.8pt; margin: 2.5pt 0 1pt; font-weight: 700; break-after: avoid; }
p  { margin: 0.8pt 0; break-inside: avoid; }
em { color: #444; }
table { width: 100%; border-collapse: collapse; margin: 1pt 0 2pt;
        font-size: 8pt; line-height: 1.05; break-inside: avoid; }
th, td { border: 0.6pt solid #999; padding: 0.6pt 2.5pt; text-align: left;
         vertical-align: middle; }
th { background: #eee; font-weight: 700; }
img.eq { display: block; max-width: 100%; margin: 1pt auto; }
img.eqi { display: inline-block; vertical-align: -0.15em; margin: 0 1pt; }
td:has(img.eq) { text-align: center; }
.qftable table { table-layout: fixed; }
.qftable td:nth-child(1), .qftable th:nth-child(1) { width: 20%; }
.qftable td:nth-child(2), .qftable th:nth-child(2) { width: 40%; }
.qftable td:nth-child(3), .qftable th:nth-child(3) { width: 40%; }
ol, ul { margin: 1pt 0 2pt; padding-left: 14pt; break-inside: avoid; }
li { margin: 0; padding: 0; }
hr { border: none; margin: 3pt 0; }
.ch7 { border: 0.5pt solid #999; border-radius: 2px; padding: 2pt 5pt 4pt;
       margin: 0 0 4pt; box-decoration-break: clone; -webkit-box-decoration-break: clone; }
.ch7 h2 { margin-top: 0; margin-bottom: 2pt; }
.ch7 h4 { font-size: 8pt; margin: 2pt 0 0.5pt; padding-bottom: 0.3pt; }
.ch7 em { font-size: 7.3pt; }
.ch7 table { font-size: 7.3pt; line-height: 0.98; margin: 0.5pt 0 2pt; }
.ch7 th, .ch7 td { padding: 0.3pt 2pt; }
.page { font-size: 9.4pt; line-height: 1.06; }
.page h2 { font-size: 11.47pt; margin: 0 0 1.5pt; }
.page h4 { font-size: 9.78pt; margin: 1.6pt 0 1.2pt; font-weight: 700;
           background: #111; color: #fff; padding: 0.5pt 4pt;
           border-radius: 2px; break-after: avoid; }
.page:first-child { font-size: 9.4pt; }
.page:first-child h2 { font-size: 11.47pt; }
.page:first-child h3 { font-size: 9.4pt; }
.page:first-child h4 { font-size: 9.78pt; }
.page ol, .page ul { padding-left: 9pt; margin: 0.3pt 0 0.7pt; }
.page li { margin: 0; }
.page p { margin: 0.3pt 0; }
.page .cols { gap: 0.16in; }
.page ul + ol, .page ol + ul,
.page ul + ul, .page ol + ol { margin-top: 0; }
.page img.eq { margin: 0.5pt auto; }
.problem { border: 0.5pt solid #999; border-radius: 2px; padding: 1pt 2.5pt 1.2pt;
           margin: 0 0 1.2pt; box-decoration-break: clone; -webkit-box-decoration-break: clone; }
.problem h4 { margin-top: 0; margin-left: -2.5pt; margin-right: -2.5pt; }
.chbox { border: 0.5pt solid #999; border-radius: 2px; padding: 2pt 5pt 4pt;
         margin: 0 0 4pt; box-decoration-break: clone; -webkit-box-decoration-break: clone; }
.chbox h2 { margin-top: 0; }
.nohdr thead { display: none; }
.lut table { font-size: 7.2pt; }
.lut th, .lut td { padding: 0.8pt 1.5pt; text-align: center; white-space: nowrap; }
.lut th:nth-child(1), .lut td:nth-child(1) { text-align: left; }
.emtable table { font-size: 6.8pt; }
.emtable th, .emtable td { padding: 0.5pt 1pt; text-align: center; white-space: nowrap; }
.emtable th:nth-child(1), .emtable td:nth-child(1) { text-align: left; }
"""

html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>{CSS}</style></head>
<body>{body}</body></html>"""

HTML(string=html, base_url=".").write_pdf(OUT)
print("wrote", OUT)

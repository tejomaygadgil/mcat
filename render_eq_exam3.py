#!/usr/bin/env python3
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

plt.rcParams["mathtext.fontset"] = "cm"

OUT_DIR = "assets"
os.makedirs(OUT_DIR, exist_ok=True)

EQUATIONS = {
    "e3_speed":       r"c = \lambda\nu,\ \ c = 3.00\times10^{8}\,\mathrm{m/s}",
    "e3_energy":      r"E = h\nu = \dfrac{hc}{\lambda},\ \ h = 6.63\times10^{-34}\,\mathrm{J\cdot s}",
    "e3_debroglie":   r"\lambda = \dfrac{h}{mu}\ \ (m\ \mathrm{in\ kg},\ u\ \mathrm{in\ m/s})",
    "e3_photo":       r"KE = h\nu - \Phi = h(c/\lambda) - \Phi = \dfrac{1}{2}m_eu^2",
    "e3_photo_u":     r"u = \sqrt{(2hc/m_e)(1/\lambda - 1/\lambda_{thr})}",
    "e3_heisenberg":  r"\Delta x\cdot\Delta p \geq \dfrac{h}{4\pi} = \mathrm{5.2728e{-}35}\ \mathrm{J}{\cdot}\mathrm{s},\ \ \Delta p = m\Delta u",
    "e3_formalcharge":r"FC = (\#\,\mathrm{valence}\ e^-) - [\mathrm{nonbonding}\ e^- + \#\,\mathrm{bonds}]",
    "e3_bondenthalpy":r"\Delta H_f = \Sigma BE(\mathrm{reactants}) - \Sigma BE(\mathrm{products})",
    "e3_mole":        r"1\ \mathrm{mol} = 6.022\times10^{23}",
    "e3_me":          r"m_e = 9.11\times10^{-31}\,\mathrm{kg}",
    "e3_ke":          r"KE = \dfrac{1}{2}mu^2",
}

FONTSIZE = 22
DPI = 400

for name, latex in EQUATIONS.items():
    fig = plt.figure()
    fig.text(0.5, 0.5, f"${latex}$", fontsize=FONTSIZE, color="#111111",
              ha="center", va="center")
    out_path = os.path.join(OUT_DIR, f"{name}.png")
    fig.savefig(out_path, dpi=DPI, transparent=True,
                bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    print("wrote", out_path)

EXTRA = {
    "e3_dele":      r"E = h\nu = h(c/\lambda) = R(1/n_f^2-1/n_i^2)",
    "s5_ni_solve":  r"n_i = \sqrt{1/\left(1/n_f^2 - hc/(R\lambda)\right)}",
    "s5_nf_solve":  r"n_f = \sqrt{1/\left(1/n_i^2 + hc/(R\lambda)\right)}",
    "e3_zeff":      r"Z_{eff} \approx Z - (\mathrm{core}\ e^-)",
    "e3_lattice":   r"U \propto \dfrac{q_1 q_2}{r_1 + r_2}",
    "e3_den":       r"\Delta EN = |EN_A - EN_B|",
    "e3_bornhaber": r"\Delta H\degree_f = \Delta H_{sub} + \Sigma IE + \tfrac{1}{2}BE + EA + U",
    "e3_dhfsum":    r"\Delta H_f = \Sigma\Delta H(\mathrm{broken}) + \Sigma\Delta H(\mathrm{formed})",
    "e3_cln":       r"c = \lambda\nu",
    "e3_ephoton":   r"E = h\nu = \dfrac{hc}{\lambda}",
    "e3_debroglie2":r"\lambda = \dfrac{h}{mu}",
    "e3_fc":        r"FC = (\mathrm{valence}\ e^-) - [\mathrm{nonbonding}\ e^- + \#\,\mathrm{bonds}]",
}
for name, latex in EXTRA.items():
    latex = latex.replace(r"\tfrac", r"\dfrac")
    fig = plt.figure()
    fig.text(0.5, 0.5, f"${latex}$", fontsize=FONTSIZE, color="#111111",
             ha="center", va="center")
    out_path = os.path.join(OUT_DIR, f"{name}.png")
    fig.savefig(out_path, dpi=DPI, transparent=True,
                bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    print("wrote", out_path)

# inline variable symbols for page 1
INLINE = {
    "v_c":    r"c",
    "v_h":    r"h",
    "v_me":   r"m_e",
    "v_na":   r"N_A",
    "v_zeff": r"Z_{eff}",
    "v_en":   r"\Delta EN = |EN_A - EN_B|",
    "v_u":    r"U \propto \dfrac{q_1 q_2}{r_1 + r_2}",
    "v_zeffdef": r"Z_{eff} \approx Z - (\mathrm{core}\ e^-)",
    "v_debroglie": r"\lambda = h/(mu)",
    "v_cln":  r"c = \lambda\nu",
    "v_eph":  r"E = h\nu = hc/\lambda",
    "v_fc":   r"FC = (\mathrm{valence}\ e^-) - [\mathrm{nonbonding}\ e^- + \#\,\mathrm{bonds}]",
}
for name, latex in INLINE.items():
    fig = plt.figure()
    fig.text(0.5, 0.5, f"${latex}$", fontsize=FONTSIZE, color="#111111",
             ha="center", va="center")
    out_path = os.path.join(OUT_DIR, f"{name}.png")
    fig.savefig(out_path, dpi=DPI, transparent=True,
                bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    print("wrote", out_path)

# inline symbols for the instruction sheet
INLINE2 = {
    "s_na":     r"N_A",
    "s_zeff":   r"Z_{eff}",
    "s_dhrxn":  r"\Delta H_{rxn}",
    "s_dhf":    r"\Delta H\degree_f",
    "s_zeffeq": r"Z_{eff} \approx Z - \mathrm{core}\ e^-",
}
for name, latex in INLINE2.items():
    fig = plt.figure()
    fig.text(0.5, 0.5, f"${latex}$", fontsize=FONTSIZE, color="#111111",
             ha="center", va="center")
    out_path = os.path.join(OUT_DIR, f"{name}.png")
    fig.savefig(out_path, dpi=DPI, transparent=True,
                bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    print("wrote", out_path)

# document-wide inline math variables (all mathematical variables render as LaTeX)
MATHVARS = {
    "m_lam": r"\lambda",
    "m_nu":  r"\nu",
    "m_phi": r"\Phi",
    "m_E":   r"E",
    "m_uv":  r"u",
    "m_ke":  r"KE",
    "m_ie":  r"IE",
    "m_ie1": r"IE_1",
    "m_ie2": r"IE_2",
    "m_ea":  r"EA",
    "m_fc":  r"FC",
    "m_en":  r"EN",
    "m_den": r"\Delta EN",
    "m_Ul":  r"U",
    "m_dH":  r"\Delta H",
    "m_dp":  r"\Delta p",
    "m_dx":  r"\Delta x",
    "m_du":  r"\Delta u",
    "m_sfc": r"\Sigma FC",
    "m_sig": r"\Sigma",
    # compound expressions -- single image reads better than stitched letters
    "x_phithr":  r"\Phi = h\nu_{thr} = h(c/\lambda_{thr})",
    "x_lamthr":  r"\lambda_{thr} = hc/\Phi",
    "x_keeq":    r"KE = h(c/\lambda) - \Phi",
    "x_ueq":     r"u = \sqrt{2\,KE/m_e}",
    "x_dpeq":    r"\Delta p = m\cdot\Delta u",
    "x_dxeq":    r"\Delta x \geq h/(4\pi\cdot\Delta p)",
    "x_hmu":     r"h/(m\cdot u)",
    "m_m":       r"m",
    "m_n":       r"n",
    "m_Z":       r"Z",
    "q_npl":     r"n+l",
    "m_ns":      r"ns",
    "m_np":      r"np",
    "m_n1d":     r"(n\!-\!1)d",
    "q_l":       r"l",
    "q_ml":      r"m_l",
    "q_ms":      r"m_s",
    "q_nrange":  r"1, 2, 3, \ldots",
    "q_lrange":  r"0, 1, \ldots, n\!-\!1",
    "q_mlrange": r"-l, \ldots, 0, \ldots, +l",
    "q_msval":   r"\pm 1/2",
    "q_2l1":     r"2l\!+\!1",
    "q_n2":      r"n^2",
    "q_2n2":     r"2n^2",
    "q_lmax":    r"l \leq n\!-\!1",
}
for name, latex in MATHVARS.items():
    fig = plt.figure()
    fig.text(0.5, 0.5, f"${latex}$", fontsize=FONTSIZE, color="#111111",
             ha="center", va="center")
    out_path = os.path.join(OUT_DIR, f"{name}.png")
    fig.savefig(out_path, dpi=DPI, transparent=True,
                bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    print("wrote", out_path)

# white-text variant, only for symbols placed on a black header background
# (e.g. "#### (11) Z_eff & Core Electrons") -- reuses the same LaTeX source
WHITE_ON_DARK = {
    "s_zeff_w": INLINE2["s_zeff"],
    "w_cln":    r"c = \lambda\nu",
    "w_ephot":  r"E = h\nu = h\,(c/\lambda)",
    "w_deb":    r"\lambda = h/(m\cdot u)",
    "w_hnu":    r"h\nu",
}
for name, latex in WHITE_ON_DARK.items():
    fig = plt.figure()
    fig.text(0.5, 0.5, f"${latex}$", fontsize=FONTSIZE, color="#ffffff",
             ha="center", va="center")
    out_path = os.path.join(OUT_DIR, f"{name}.png")
    fig.savefig(out_path, dpi=DPI, transparent=True,
                bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    print("wrote", out_path)

# small inline formulas for the Bohr level-formula have/want/use table
BOHR_TABLE = {
    "s5_ninit":   r"n_{initial}",
    "s5_lamthr":  r"\lambda_{thr}",
    "s5_nuthr":   r"\nu_{thr}",
    "s5_R":       r"R",
    "s5_hc":      r"hc",
    "s5_hR":      r"h/R",
    "s5_hcR":     r"hc/R",
    "s20_2hcme":  r"2hc/m_e",
}
for name, latex in BOHR_TABLE.items():
    fig = plt.figure()
    fig.text(0.5, 0.5, f"${latex}$", fontsize=FONTSIZE, color="#111111",
             ha="center", va="center")
    out_path = os.path.join(OUT_DIR, f"{name}.png")
    fig.savefig(out_path, dpi=DPI, transparent=True,
                bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    print("wrote", out_path)

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
out_path = os.path.join(OUT_DIR, "e3_bhcycle.png")
fig.savefig(out_path, dpi=DPI, transparent=True,
            bbox_inches="tight", pad_inches=0.04)
plt.close(fig)
print("wrote", out_path)

# Lewis-structure gallery for page 2 -- correct completed structures for the
# molecules asked in the practice exam, ch.9 slides, and ch.9 homework quiz.
import math
fig = plt.figure(figsize=(9.2, 23.5))
W = 10.0
H = W * 23.5 / 9.2
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
AFS, LFS = 17, 15    # atom / caption font (final pt ~= fontsize * 0.378)
R = 0.26             # bond clearance around atom label
B = 0.85             # bond length

def atom(x, y, s, fs=None):
    ax.text(x, y, s, ha="center", va="center", fontsize=fs or AFS,
            color="#111111")

def bond(x1, y1, x2, y2, order=1):
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
    px, py = -uy, ux
    a1, b1 = x1 + ux * R, y1 + uy * R
    a2, b2 = x2 - ux * R, y2 - uy * R
    for o in {1: [0], 2: [-0.055, 0.055], 3: [-0.1, 0, 0.1]}[order]:
        ax.plot([a1 + px * o, a2 + px * o], [b1 + py * o, b2 + py * o],
                color="#111111", lw=1.3, solid_capstyle="round")

def lp(x, y, ang):
    a = math.radians(ang)
    cx, cy = x + math.cos(a) * R * 1.35, y + math.sin(a) * R * 1.35
    px, py = -math.sin(a), math.cos(a)
    for o in (-0.075, 0.075):
        ax.plot([cx + px * o], [cy + py * o], marker="o", ms=2.6,
                color="#111111")

def tlp(x, y, d):          # terminal atom w/ single bond: 3 lone pairs
    for a in (d, d + 75, d - 75): lp(x, y, a)

def dlp(x, y, d):          # terminal atom w/ double bond: 2 lone pairs
    for a in (d + 50, d - 50): lp(x, y, a)

def cap(x, y, s):
    ax.text(x, y, s, ha="center", va="center", fontsize=LFS,
            fontweight="bold", color="#111111")

def brackets(xl, xr, yb, yt, q):
    for xs, sgn in ((xl, 1), (xr, -1)):
        ax.plot([xs + sgn * 0.1, xs, xs, xs + sgn * 0.1],
                [yb, yb, yt, yt], color="#111111", lw=1.3)
    ax.text(xr + 0.12, yt + 0.05, q, ha="left", va="center",
            fontsize=LFS, color="#111111")

# --- row 1: CO2, CO, NH3, H2CO ---
y = H - 1.0
x = 1.1
atom(x, y, "C"); atom(x - B, y, "O"); atom(x + B, y, "O")
bond(x, y, x - B, y, 2); bond(x, y, x + B, y, 2)
dlp(x - B, y, 180); dlp(x + B, y, 0)
cap(x, y - 1.15, "CO$_2$")
x = 3.6
atom(x, y, "C"); atom(x + B, y, "O")
bond(x, y, x + B, y, 3); lp(x, y, 180); lp(x + B, y, 0)
cap(x + 0.4, y - 1.15, "CO")
x = 6.0
atom(x, y, "N"); atom(x - B, y, "H"); atom(x + B, y, "H"); atom(x, y - B, "H")
bond(x, y, x - B, y); bond(x, y, x + B, y); bond(x, y, x, y - B)
lp(x, y, 90)
cap(x, y - 1.6, "NH$_3$")
x = 8.5
atom(x, y, "C"); atom(x, y + 0.8 * B, "O")
atom(x - 0.7 * B, y - 0.6 * B, "H"); atom(x + 0.7 * B, y - 0.6 * B, "H")
bond(x, y, x, y + 0.8 * B, 2)
bond(x, y, x - 0.7 * B, y - 0.6 * B); bond(x, y, x + 0.7 * B, y - 0.6 * B)
dlp(x, y + 0.8 * B, 90)
cap(x, y - 1.35, "H$_2$CO")

# --- row 2: NF3, CH2Cl2, NH4+, ClO- ---
y = H - 3.9
x = 1.1
atom(x, y, "N"); atom(x - B, y, "F"); atom(x + B, y, "F"); atom(x, y - B, "F")
bond(x, y, x - B, y); bond(x, y, x + B, y); bond(x, y, x, y - B)
lp(x, y, 90); tlp(x - B, y, 180); tlp(x + B, y, 0); tlp(x, y - B, 270)
cap(x, y - 1.9, "NF$_3$")
x = 3.6
atom(x, y, "C"); atom(x, y + B, "H"); atom(x - B, y, "H")
atom(x + B, y, "Cl"); atom(x, y - B, "Cl")
bond(x, y, x, y + B); bond(x, y, x - B, y)
bond(x, y, x + B, y); bond(x, y, x, y - B)
tlp(x + B, y, 0); tlp(x, y - B, 270)
cap(x, y - 1.9, "CH$_2$Cl$_2$")
x = 6.3
atom(x, y, "N"); atom(x, y + 0.8 * B, "H"); atom(x, y - 0.8 * B, "H")
atom(x - 0.8 * B, y, "H"); atom(x + 0.8 * B, y, "H")
bond(x, y, x, y + 0.8 * B); bond(x, y, x, y - 0.8 * B)
bond(x, y, x - 0.8 * B, y); bond(x, y, x + 0.8 * B, y)
brackets(x - 1.15, x + 1.15, y - 1.0, y + 1.0, "+")
cap(x, y - 1.9, "NH$_4$$^+$")
x = 8.6
atom(x, y, "Cl"); atom(x + B, y, "O")
bond(x, y, x + B, y)
lp(x, y, 90); lp(x, y, 180); lp(x, y, 270)
lp(x + B, y, 90); lp(x + B, y, 0); lp(x + B, y, 270)
brackets(x - 0.6, x + B + 0.6, y - 0.55, y + 0.55, "−")
cap(x + 0.4, y - 1.9, "ClO$^-$")

# --- row 3: NO2- resonance pair, CO3 2- ---
y = H - 7.2
for k, (o1, o2) in enumerate(((2, 1), (1, 2))):
    x = 1.3 + k * 2.95
    ox1, oy1 = x - 0.75 * B, y - 0.62 * B
    ox2, oy2 = x + 0.75 * B, y - 0.62 * B
    atom(x, y, "N"); atom(ox1, oy1, "O"); atom(ox2, oy2, "O")
    bond(x, y, ox1, oy1, o1); bond(x, y, ox2, oy2, o2)
    lp(x, y, 90)
    (dlp if o1 == 2 else tlp)(ox1, oy1, 220)
    (dlp if o2 == 2 else tlp)(ox2, oy2, 320)
    brackets(x - 1.35, x + 1.35, y - 1.15, y + 0.5, "−")
ax.text(2.78, y - 0.3, "↔", ha="center", va="center", fontsize=19,
        color="#111111")
cap(2.8, y - 1.85, "NO$_2$$^-$ (2 equivalent forms)")
x = 7.3
atom(x, y, "C"); atom(x, y + 0.85 * B, "O")
ox1, oy1 = x - 0.8 * B, y - 0.6 * B
ox2, oy2 = x + 0.8 * B, y - 0.6 * B
atom(ox1, oy1, "O"); atom(ox2, oy2, "O")
bond(x, y, x, y + 0.85 * B, 2); bond(x, y, ox1, oy1); bond(x, y, ox2, oy2)
dlp(x, y + 0.85 * B, 90); tlp(ox1, oy1, 215); tlp(ox2, oy2, 325)
brackets(x - 1.65, x + 1.65, y - 1.2, y + 1.1, "2−")
cap(x, y - 1.85, "CO$_3$$^{2-}$ (×3 forms)")

# --- row 4: HNO3, BeCl2, KCl ---
y = H - 10.4
x = 1.4
atom(x, y, "N"); atom(x, y + 0.85 * B, "O")
atom(x - B, y, "O"); atom(x + B, y, "O"); atom(x + 1.8 * B, y, "H")
bond(x, y, x, y + 0.85 * B, 2); bond(x, y, x - B, y); bond(x, y, x + B, y)
bond(x + B, y, x + 1.8 * B, y)
dlp(x, y + 0.85 * B, 90); tlp(x - B, y, 180)
lp(x + B, y, 90); lp(x + B, y, 270)
cap(x + 0.3, y - 1.35, "HNO$_3$")
x = 5.0
atom(x, y, "Be"); atom(x - B, y, "Cl"); atom(x + B, y, "Cl")
bond(x, y, x - B, y); bond(x, y, x + B, y)
tlp(x - B, y, 180); tlp(x + B, y, 0)
cap(x, y - 1.35, "BeCl$_2$ (4 e- on Be)")
x = 8.6
atom(x - 1.5 * B, y, "K$^+$"); atom(x, y, "Cl")
lp(x, y, 0); lp(x, y, 90); lp(x, y, 180); lp(x, y, 270)
brackets(x - 0.62, x + 0.62, y - 0.55, y + 0.55, "−")
cap(x - 0.6, y - 1.35, "KCl (ionic)")

# --- row 5: BF3, PCl5, SF6 ---
y = H - 13.4
x = 1.4
atom(x, y, "B"); atom(x, y + B, "F")
ox1, oy1 = x - 0.85 * B, y - 0.6 * B
ox2, oy2 = x + 0.85 * B, y - 0.6 * B
atom(ox1, oy1, "F"); atom(ox2, oy2, "F")
bond(x, y, x, y + B); bond(x, y, ox1, oy1); bond(x, y, ox2, oy2)
tlp(x, y + B, 90); tlp(ox1, oy1, 215); tlp(ox2, oy2, 325)
cap(x, y - 1.9, "BF$_3$ (6 e- on B)")
x = 5.0
atom(x, y, "P")
for adeg in (90, 162, 234, 306, 18):
    a = math.radians(adeg)
    fx, fy = x + math.cos(a) * B, y + math.sin(a) * B
    atom(fx, fy, "Cl", fs=15); bond(x, y, fx, fy); tlp(fx, fy, adeg)
cap(x, y - 1.9, "PCl$_5$ (10 e-)")
x = 8.5
atom(x, y, "S")
for adeg in (0, 60, 120, 180, 240, 300):
    a = math.radians(adeg)
    fx, fy = x + math.cos(a) * B, y + math.sin(a) * B
    atom(fx, fy, "F", fs=15); bond(x, y, fx, fy); tlp(fx, fy, adeg)
cap(x, y - 1.9, "SF$_6$ (12 e-)")

# --- row 6: CH3CHO, CH3CH2COOH ---
y = H - 16.6
x = 1.0
atom(x, y, "C"); atom(x, y + 0.8 * B, "H"); atom(x - 0.8 * B, y, "H")
atom(x, y - 0.8 * B, "H")
bond(x, y, x, y + 0.8 * B); bond(x, y, x - 0.8 * B, y)
bond(x, y, x, y - 0.8 * B)
atom(x + B, y, "C"); bond(x, y, x + B, y)
atom(x + B, y + 0.85 * B, "O"); bond(x + B, y, x + B, y + 0.85 * B, 2)
dlp(x + B, y + 0.85 * B, 90)
atom(x + 1.75 * B, y - 0.45 * B, "H"); bond(x + B, y, x + 1.75 * B, y - 0.45 * B)
cap(x + 0.5, y - 1.6, "CH$_3$CHO (aldehyde)")
x = 5.3
for i in range(3):
    cx = x + i * B
    atom(cx, y, "C")
    if i: bond(cx - B, y, cx, y)
atom(x, y + 0.8 * B, "H"); bond(x, y, x, y + 0.8 * B)
atom(x - 0.8 * B, y, "H"); bond(x, y, x - 0.8 * B, y)
atom(x, y - 0.8 * B, "H"); bond(x, y, x, y - 0.8 * B)
atom(x + B, y + 0.8 * B, "H"); bond(x + B, y, x + B, y + 0.8 * B)
atom(x + B, y - 0.8 * B, "H"); bond(x + B, y, x + B, y - 0.8 * B)
atom(x + 2 * B, y + 0.85 * B, "O"); bond(x + 2 * B, y, x + 2 * B, y + 0.85 * B, 2)
dlp(x + 2 * B, y + 0.85 * B, 90)
atom(x + 3 * B, y, "O"); bond(x + 2 * B, y, x + 3 * B, y)
lp(x + 3 * B, y, 90); lp(x + 3 * B, y, 270)
atom(x + 3.8 * B, y, "H"); bond(x + 3 * B, y, x + 3.8 * B, y)
cap(x + 1.3, y - 1.6, "CH$_3$CH$_2$COOH (carboxylic acid)")

# --- rows 8-9: functional-group templates (slides "Lewis Structures in
# Organic Chemistry - 2") ---
y = H - 19.2
x = 0.9
atom(x, y, "R"); atom(x + 0.8 * B, y, "O"); atom(x + 1.6 * B, y, "H")
bond(x, y, x + 0.8 * B, y); bond(x + 0.8 * B, y, x + 1.6 * B, y)
lp(x + 0.8 * B, y, 90); lp(x + 0.8 * B, y, 270)
cap(x + 0.65, y - 1.0, "Alcohol")
x = 3.1
atom(x, y, "R"); atom(x + 0.8 * B, y, "O"); atom(x + 1.6 * B, y, "R")
bond(x, y, x + 0.8 * B, y); bond(x + 0.8 * B, y, x + 1.6 * B, y)
lp(x + 0.8 * B, y, 90); lp(x + 0.8 * B, y, 270)
cap(x + 0.65, y - 1.0, "Ether")
x = 5.3
atom(x, y, "R"); atom(x + 0.8 * B, y, "O"); atom(x + 1.6 * B, y, "O")
atom(x + 2.4 * B, y, "R")
bond(x, y, x + 0.8 * B, y); bond(x + 0.8 * B, y, x + 1.6 * B, y)
bond(x + 1.6 * B, y, x + 2.4 * B, y)
for ox in (0.8, 1.6):
    lp(x + ox * B, y, 90); lp(x + ox * B, y, 270)
cap(x + 1.0, y - 1.0, "Peroxide")
x = 8.3
atom(x, y, "R"); atom(x + 0.8 * B, y, "N"); bond(x, y, x + 0.8 * B, y)
rx, ry = x + 1.5 * B, y + 0.55 * B
atom(rx, ry, "R"); bond(x + 0.8 * B, y, rx, ry)
rx2, ry2 = x + 1.5 * B, y - 0.55 * B
atom(rx2, ry2, "R"); bond(x + 0.8 * B, y, rx2, ry2)
lp(x + 0.8 * B, y, 90)
cap(x + 0.65, y - 1.0, "Amine")

y = H - 21.6
x = 0.8
atom(x, y, "R"); atom(x + B, y, "C"); atom(x + B, y + 0.85 * B, "O")
atom(x + 1.8 * B, y - 0.4 * B, "H")
bond(x, y, x + B, y); bond(x + B, y, x + B, y + 0.85 * B, 2)
bond(x + B, y, x + 1.8 * B, y - 0.4 * B)
dlp(x + B, y + 0.85 * B, 90)
cap(x + 0.85, y - 1.15, "Aldehyde")
x = 2.9
atom(x, y, "R"); atom(x + B, y, "C"); atom(x + B, y + 0.85 * B, "O")
atom(x + 2 * B, y, "R")
bond(x, y, x + B, y); bond(x + B, y, x + B, y + 0.85 * B, 2)
bond(x + B, y, x + 2 * B, y)
dlp(x + B, y + 0.85 * B, 90)
cap(x + 0.85, y - 1.15, "Ketone")
x = 5.0
atom(x, y, "R"); atom(x + B, y, "C"); atom(x + B, y + 0.85 * B, "O")
atom(x + 2 * B, y, "O"); atom(x + 2.8 * B, y, "H")
bond(x, y, x + B, y); bond(x + B, y, x + B, y + 0.85 * B, 2)
bond(x + B, y, x + 2 * B, y); bond(x + 2 * B, y, x + 2.8 * B, y)
dlp(x + B, y + 0.85 * B, 90)
lp(x + 2 * B, y, 90); lp(x + 2 * B, y, 270)
cap(x + 1.3, y - 1.15, "Carboxylic acid")
x = 7.9
atom(x, y, "R"); atom(x + B, y, "C"); atom(x + B, y + 0.85 * B, "O")
atom(x + 2 * B, y, "N")
bond(x, y, x + B, y); bond(x + B, y, x + B, y + 0.85 * B, 2)
bond(x + B, y, x + 2 * B, y)
dlp(x + B, y + 0.85 * B, 90)
rx, ry = x + 2.7 * B, y + 0.5 * B
atom(rx, ry, "R"); bond(x + 2 * B, y, rx, ry)
rx2, ry2 = x + 2.7 * B, y - 0.5 * B
atom(rx2, ry2, "R"); bond(x + 2 * B, y, rx2, ry2)
lp(x + 2 * B, y, 90)
cap(x + 1.5, y - 1.15, "Amide")

y = H - 24.0
x = 1.5
c1x, c1y = x - 0.55 * B, y - 0.4 * B
c2x, c2y = x + 0.55 * B, y - 0.4 * B
atom(x, y + 0.55 * B, "O"); atom(c1x, c1y, "C"); atom(c2x, c2y, "C")
bond(x, y + 0.55 * B, c1x, c1y); bond(x, y + 0.55 * B, c2x, c2y)
bond(c1x, c1y, c2x, c2y)
lp(x, y + 0.55 * B, 130); lp(x, y + 0.55 * B, 50)
cap(x, y - 1.35, "Epoxide")
x = 4.6
atom(x, y, "R"); atom(x + 0.85 * B, y, "N"); atom(x + 1.75 * B, y, "N")
atom(x + 2.75 * B, y, "N")
bond(x, y, x + 0.85 * B, y); bond(x + 0.85 * B, y, x + 1.75 * B, y)
bond(x + 1.75 * B, y, x + 2.75 * B, y, 3)
lp(x + 0.85 * B, y, 90); lp(x + 0.85 * B, y, 270); lp(x + 2.75 * B, y, 0)
atom(x + 0.85 * B, y + 0.75, "−", fs=13)
atom(x + 1.75 * B, y + 0.75, "+", fs=13)
cap(x + 1.2, y - 1.35, "Azide (R–N$_3$)")

out_path = os.path.join(OUT_DIR, "e3_lewis.png")
fig.savefig(out_path, dpi=DPI, transparent=True,
            bbox_inches="tight", pad_inches=0.04)
plt.close(fig)
print("wrote", out_path)

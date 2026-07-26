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
    "e3_photo_thresh":r"\Phi = h\nu_{threshold} = h(c/\lambda_{threshold})",
    "e3_photo_u":     r"u = \sqrt{(2hc/m_e)(1/\lambda - 1/\lambda_{threshold})}",
    "e3_heisenberg":  r"\Delta x\cdot\Delta p \geq \dfrac{h}{4\pi},\ \ \Delta p = m\Delta u",
    "e3_formalcharge":r"FC = (\#\,\mathrm{valence}\ e^-) - [\mathrm{nonbonding}\ e^- + \#\,\mathrm{bonds}]",
    "e3_bondenthalpy":r"\Delta H_{rxn} = \Sigma\Delta H(\mathrm{bonds\ broken}) - \Sigma\Delta H(\mathrm{bonds\ formed})",
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

# white-text variant, only for symbols placed on a black header background
# (e.g. "#### (11) Z_eff & Core Electrons") -- reuses the same LaTeX source
WHITE_ON_DARK = {
    "s_zeff_w": INLINE2["s_zeff"],
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
    "s5_R":       r"R",
    "s5_hc":      r"hc",
    "s5_hR":      r"h/R",
    "s5_hcR":     r"hc/R",
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

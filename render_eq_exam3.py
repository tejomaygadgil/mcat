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

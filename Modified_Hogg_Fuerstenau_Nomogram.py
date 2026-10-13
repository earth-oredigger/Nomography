"""
    Modified_Hogg_Fuerstenau_Nomogram.py

    Modified Hogg & Fuerstenau mill power model, Eq. (2) of the article:

        Pnet = 0.267 * D^3.5 * (L/D) * Nc * rho_ap * (Jc - Jc^2) * sin(alpha)

    Units: D in ft (also shown in m); rho_ap in t/m3; alpha in degrees; Pnet in kW.

    Type 3 nomogram (F1 + F2 + ... + F7 = 0) after taking log10:
        -log Nc + [-log 0.267 - 3.5 log D] - log(L/D) + log Pnet - log rho_ap - log sin(alpha) - log(Jc - Jc^2) = 0

    Changes with respect to Hogg11_corrected.py:
      * constant 0.267 (offset 0.5735 = -log10 0.267) instead of 0.238 (0.6234)
      * filling term (Jc - Jc^2) instead of (Jc - 1.065 Jc^2)
      * exact degree-to-radian conversion (np.radians) instead of 3.1415/180
      * equation and variable symbols in the titles

    General version with a generic example (PyNomo requires one isopleth). To draw
    the article examples, replace the active 'isopleth_values' line in block_1_params
    by one of the commented lines.
"""
import sys
import numpy as np
from pyx import *

sys.path.insert(0, "..")
from pynomo.nomographer import Nomographer
text.set(text.LatexEngine)

C0 = -np.log10(0.267)   # = 0.57349


Nc_params_4 = {
    'u_min': 0.65,
    'u_max': 0.80,
    'function': lambda u: -np.log10(u),
    'title': r'$N_c$',
    'tick_levels': 2,
    'tick_text_levels': 1,
    'tick_side': 'left',
}

D_params_ft = {
    "tag": "D",
    'u_min': 10.0,
    'u_max': 40.0,
    'function': lambda u: C0 - 3.5*np.log10(u),
    'title': r'$D$',
    'tick_levels': 2,
    'tick_text_levels': 1,
    'extra_params': [{
        'u_min': 10,
        'u_max': 26.0,
        'tick_levels': 3,
        'tick_text_levels': 0,
    }],
}

LD_params_3 = {
    'u_min': 0.5,
    'u_max': 2.0,
    'function': lambda u: -np.log10(u),
    'title': r'$L/D$',
    'tick_levels': 2,
    'tick_text_levels': 1,
}

Pnet_params_1 = {
    'u_min': 1000.0,
    'u_max': 30000.0,
    'function': lambda u: np.log10(u),
    'title': r'$P_{net}$',
    'tick_levels': 2,
    'tick_text_levels': 1,
    'tick_side': 'left',
    'text_format': r"$%5.0f$",       # avoids the 1e+04 notation
    'extra_params': [{
        'u_min': 1000,
        'u_max': 30000.0,
        'tick_levels': 3,
        'tick_text_levels': 0,
    }],
}

Pap_params_5 = {
    'u_min': 2.0,
    'u_max': 6.0,
    'function': lambda u: -np.log10(u),
    'title': r'$\rho_{ap}$',
    'tick_levels': 3,
    'tick_text_levels': 1,
}

Alpha_params_7 = {
    'u_min': 25.0,
    'u_max': 45.0,
    'function': lambda u: -np.log10(np.sin(np.radians(u))),
    'title': r'$\alpha$',
    'tick_levels': 2,
    'tick_text_levels': 1,
    'tick_side': 'right',
}

Jc_params_6 = {
    'u_min': 0.20,
    'u_max': 0.40,
    'function': lambda u: -np.log10(u - u**2),
    'title': r'$J_c$',
    'tick_levels': 2,
    'tick_text_levels': 1,
    'tick_side': 'right',
}


block_1_params = {
    'block_type': 'type_3',
    'width': 10.0,
    'height': 10.0,
    'f_params': [Nc_params_4, D_params_ft, LD_params_3, Pnet_params_1, Pap_params_5, Alpha_params_7, Jc_params_6],
    # order of values: [Nc, D (ft), L/D, Pnet (kW), rho_ap (t/m3), alpha (deg), Jc]; 'x' = unknown
    # generic example: Nc 0.75, D 20 ft, L/D 1.5, rho_ap 4.5 t/m3, alpha 35 deg, Jc 0.30 -> Pnet = 5825 kW
    'isopleth_values': [[0.75, 20, 1.5, 'x', 4.5, 35, 0.30]],
    # 'isopleth_values': [[0.75, 18, 1.2, 'x', 5.38, 26.2, 0.35]],   # Figure 5 example
    # 'isopleth_values': [[0.72, 'x', 1.4, 9000, 5.4, 27, 0.34]],    # Figure 11 example
}

D_params_m = {
    "tag": "D",
    'u_min': 10.0*0.3048,
    'u_max': 40.0*0.3048,
    'function': lambda u: C0 - 3.5*np.log10(u),
    "align_func": lambda u: u/0.3048,
    "title": "",
    "tick_levels": 0,
    "tick_text_levels": 0,
    "tick_side": "left",
    "title_y_shift": 0.50,
    "title_x_shift": 0.0,
    "extra_params": [
        {
            "u_min": 10.0*0.3048,
            "u_max": 40.0*0.3048,
            "tick_levels": 3,
            "tick_text_levels": 2,
            "grid_length_0": 0.35,
            "grid_length_1": 0.30,
            "grid_length_2": 0.20,
            "grid_length_3": 0.15,
            "grid_length_4": 0.10,
            "text_distance_0": 0.40,
            "text_distance_1": 0.35,
            "text_distance_2": 0.30,
            "text_distance_3": 0.30,
            "text_distance_4": 0.30,
        }
    ],
}

block_2_params = {
    "block_type": "type_8",
    "f_params": D_params_m,
    "width": 5.0,
    "height": 10.0,
    "isopleth_values": [["x"]],
}


main_params = {
    'filename': 'Modified_Hogg_Fuerstenau_Nomogram.pdf',
    'paper_height': 20.0,
    'paper_width': 20.0,
    'block_params': [block_1_params, block_2_params],
    'transformations': [('rotate', 0.01), ('scale paper',)],
    'title_str': r'$P_{net}=0.267\cdot D^{3.5}\cdot{{L}\over{D}}\cdot N_{c}\cdot\rho_{ap}\cdot\left(J_{c}-J_{c}^{2}\right)\cdot\sin\alpha$',
    'title_y': 0.0,
}
Nomographer(main_params)

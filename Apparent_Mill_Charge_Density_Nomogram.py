"""
    apparent mill charge density

    using nomogram of type 10

    r_ap = 4.65*J_bc + 0.6*r_m*(1-J_BC) + 0.4r_p

    where
    r_p = (r_m-1)*f_sv + 1  ;  f_sv = 0.5

"""

#    rearrange equation for type 10 nomogram form:
#    0 = -r_ap + J_bc*(4.65 - 0.6*r_m) + 0.6*r_m + r_p

#    0 = F1(u) + F2(v)*F3(w) + F4(w)
#    F1(u) = -r_ap
#    F2(v) = J_bc
#    F3(w) = 4.65 - 0.6*r_m
#    F4(w) = 0.6*r_m + 0.4*r_p


import sys
import pyx

sys.path.insert(0, "..")
from pynomo.nomographer import Nomographer

axis_r_ap = {
    'tag': 'r_ap',
    'u_min': 2,
    'u_max': 7.0,
    'function': lambda r_ap: -r_ap,
    'title': r'$\rho_{ap}$',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'tick_side':'right',
}

axis_J_bc = {
    'tag': 'J_bc',
    'u_min': 0,
    'u_max': 1.0,
    'function': lambda J_bc: J_bc,
    'title': r'$J_b \over J_c$',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'tick_side': 'left',
}

axis_r_m = {
    'u_min': 2.0,
    'u_max': 7.0,
    'function_3': lambda r_m: 4.65 - 0.6*r_m,
    'function_4': lambda r_m: 0.6*r_m + 0.4*((r_m-1)*0.50 + 1),  # f_sv=0.50
    'title': r'$\rho_m, f_{sv}=0.50$',
    'tick_levels': 4,
    'tick_text_levels': 3,
    'scale_type': 'linear smart',
    'title_draw_center': True,
    'title_distance_center': -1.5,
    'tick_side': 'left',
}

block_1_params = {
    'block_type': 'type_10',
    'width': 15.0,
    'height': 15.0,
    'f1_params': axis_r_ap,
    'f2_params': axis_J_bc,
    'f3_params': axis_r_m,
    'isopleth_values': [[5.382, 1.0, 'x']],
     'mirror_x': True,
}

main_params = {
    'filename': 'mill_06.pdf',
    'paper_height': 15.0,
    'paper_width': 15.0,
    'block_params': [block_1_params],
    'transformations': [('rotate', 0.01), ('scale paper',)],
    #'isopleth_params': [{'color': 'CornFlowerBlue'}],
    'title_str': r'$\rho_{ap} = 4.65{J_b \over J_c} + 0.6\rho_m(1-{J_b \over J_c}) + 0.4\rho_p$',
}
Nomographer(main_params)

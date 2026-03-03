#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import inspect
import os

sys.path.insert(0, "..")

from nomogen import Nomogen
from pynomo.nomographer import Nomographer

myfile = os.path.basename(inspect.stack()[0][1]).replace(".py", "")

########################################
# Función objetivo
########################################

def grlt_eq(P, rho_s):
    # Evita division por cero
    if P <= 0:
        return None
    return 1000 / ((1 / rho_s) + ((100 - P) / P))

########################################
# Rangos físicos
########################################

P_min = 20
P_max = 80

rho_s_min = 2.5
rho_s_max = 4.0

grlt_values = [
    grlt_eq(P_min, rho_s_min),
    grlt_eq(P_min, rho_s_max),
    grlt_eq(P_max, rho_s_min),
    grlt_eq(P_max, rho_s_max),
]

grlt_min = min(grlt_values)
grlt_max = max(grlt_values)

NN = 5

##############################################
# Estilo con rejilla
##############################################

common_axis_style = {
    'tick_levels': 5,
    'tick_text_levels': 5,
    'tick_length': 0.07,
    'tick_length_levels': [1.2, 1.0, 0.8, 0.6, 0.5],
    'tick_color_levels': [
        (0, 0, 0),
        (0.2, 0.2, 0.2),
        (0.4, 0.4, 0.4),
        (0.6, 0.6, 0.6),
        (0.75, 0.75, 0.75)
    ],
    'tick_text_size': 0.8,
}

left_axis = {
    'u_min': P_min,
    'u_max': P_max,
    'title': r'$\% \ solidos$',
    'scale_type': 'linear smart',
    **common_axis_style
}

right_axis = {
    'u_min': rho_s_min,
    'u_max': rho_s_max,
    'title': r'$\rho_s$',
    'scale_type': 'linear smart',
    **common_axis_style
}

middle_axis = {
    'u_min': grlt_min,
    'u_max': grlt_max,
    'title': r'$gr/lt$',
    'scale_type': 'log smart',
    **common_axis_style
}

##############################################
# Bloque
##############################################

block_params0 = {
    'block_type': 'type_9',
    'f1_params': left_axis,
    'f2_params': middle_axis,
    'f3_params': right_axis,
    'transform_ini': False,
    'isopleth_values': [[72, 'x', 2.7]]
}

main_params = {
    'filename': myfile,
    'paper_height': 18,
    'paper_width': 12,
    'title_x': 6,
    'title_y': 1.5,
    'title_box_width': 10,
    'title_str': r'$gr/lt = 1000 / (1/\rho_s + (100-P)/P)$',
    'block_params': [block_params0],
    'transformations': [('scale paper',)],
    'npoints': NN
}

print("calculating the nomogram ...")
Nomogen(grlt_eq, main_params)

main_params['filename'] += '.pdf'
print("printing", main_params['filename'], "...")
Nomographer(main_params)

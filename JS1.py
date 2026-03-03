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

def rho_f_eq(f_lu, rho_l):
    return 100 / ((f_lu / rho_l) + (100 - f_lu))

########################################
# Rangos físicos
########################################

f_lu_min = 20
f_lu_max = 80

rho_l_min = 2.5
rho_l_max = 4.0

rho_f_values = [
    rho_f_eq(f_lu_min, rho_l_min),
    rho_f_eq(f_lu_min, rho_l_max),
    rho_f_eq(f_lu_max, rho_l_min),
    rho_f_eq(f_lu_max, rho_l_max),
]

rho_f_min = min(rho_f_values)
rho_f_max = max(rho_f_values)

NN = 5

##############################################
# Estilo con rejilla y colores
##############################################

common_axis_style = {
    'tick_levels': 5,
    'tick_text_levels': 5,

    # longitud base grande → ayuda a crear rejilla visual
    'tick_length': 0.07,

    # longitudes por nivel (rejilla visual)
    'tick_length_levels': [1.2, 1.0, 0.8, 0.6, 0.5],

    # colores por nivel (principal → secundario)
    'tick_color_levels': [
        (0, 0, 0),        # negro → principales
        (0.2, 0.2, 0.2),  # gris oscuro
        (0.4, 0.4, 0.4),  # gris medio
        (0.6, 0.6, 0.6),  # gris claro
        (0.75, 0.75, 0.75)
    ],

    'tick_text_size': 0.8,
}

left_axis = {
    'u_min': f_lu_min,
    'u_max': f_lu_max,
    'title': r'$f_{lu}$',
    'scale_type': 'linear smart',
    **common_axis_style
}

right_axis = {
    'u_min': rho_l_min,
    'u_max': rho_l_max,
    'title': r'$\rho_l$',
    'scale_type': 'log smart',
    **common_axis_style
}

middle_axis = {
    'u_min': rho_f_min,
    'u_max': rho_f_max,
    'title': r'$\rho_f$',
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
    'title_str': r'$\rho_f = 1 / (f_{lu}/\rho_l + 1 - f_{lu})$',
    'block_params': [block_params0],
    'transformations': [('scale paper',)],
    'npoints': NN
}

print("calculating the nomogram ...")
Nomogen(rho_f_eq, main_params)

main_params['filename'] += '.pdf'
print("printing", main_params['filename'], "...")
Nomographer(main_params)
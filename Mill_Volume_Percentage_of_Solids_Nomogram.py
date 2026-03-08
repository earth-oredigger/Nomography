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
# Target function
########################################

def fsv_eq(f_sw, rho_m):
    return 100 * (f_sw / rho_m) / ((f_sw / rho_m) + (100.0 - f_sw))

########################################
# Physical ranges
########################################

f_sw_min = 20.0
f_sw_max = 80.0

rho_m_min = 2.5
rho_m_max = 4.0

fsv_values = [
    fsv_eq(f_sw_min, rho_m_min),
    fsv_eq(f_sw_min, rho_m_max),
    fsv_eq(f_sw_max, rho_m_min),
    fsv_eq(f_sw_max, rho_m_max),
]

fsv_min = min(fsv_values)
fsv_max = max(fsv_values)

NN = 5

##############################################
# Axis style
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

##############################################
# Axes
##############################################

left_axis = {
    'u_min': f_sw_min,
    'u_max': f_sw_max,
    'title': r'$f_{sw}\ (\%)$',
    'scale_type': 'linear smart',
    **common_axis_style
}

right_axis = {
    'u_min': rho_m_min,
    'u_max': rho_m_max,
    'title': r'$\rho_m$',
    'scale_type': 'log smart',
    **common_axis_style
}

middle_axis = {
    'u_min': fsv_min,
    'u_max': fsv_max,
    'title': r'$f_{sv}\ (\%)$',
    'scale_type': 'linear smart',
    **common_axis_style
}

##############################################
# Nomogram block
##############################################

block_params0 = {
    'block_type': 'type_9',
    'f1_params': left_axis,
    'f2_params': middle_axis,
    'f3_params': right_axis,
    'transform_ini': False,
    'isopleth_values': [[72.0, 'x', 2.7]]
}

##############################################
# Main parameters
##############################################

main_params = {
    'filename': myfile,
    'paper_height': 18,
    'paper_width': 12,
    'title_x': 6,
    'title_y': 1.5,
    'title_box_width': 10,

    # ✔ title compatible with basic TeX
    'title_str': r'$f_{sv} = 100 (f_{sw}/\rho_m) / (f_{sw}/\rho_m + (100 - f_{sw}))$',

    'block_params': [block_params0],
    'transformations': [('scale paper',)],
    'npoints': NN
}

print("calculating the nomogram ...")
Nomogen(fsv_eq, main_params)

main_params['filename'] += '.pdf'
print("printing", main_params['filename'], "...")
Nomographer(main_params)
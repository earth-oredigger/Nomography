"""
    Circulating_Load_Nomogram.py
"""
import sys

sys.path.insert(0, "..")
from pynomo.nomographer import Nomographer

F2_F3_params_1 = {
    'u_min': 20,  # for alignment
    'u_max': 50,  # for alignment
    'f_grid': lambda u, v: 1/u,
    'g_grid': lambda u, v: -1.0,
    'h_grid': lambda u, v: -1/v,
    'u_start': 10,
    'u_stop': 50,
    'v_start': 66,
    'v_stop': 85,
    'u_values': [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 35, 40, 45, 50],
    'v_values': [66, 70, 75, 80, 85],
    'u_texts':['10', '11', '12', '13', '14', '15', '16', '', '18', '', '20', '', '', '', '', '25', '', '', '', '', '30', 'S2 = 35', '40', '', '50'],
    'v_texts':['66', '70', 'S3 = 75', '80', '85'],
    'grid': True,
    'text_prefix_u': r'$S_2$=',
    'text_prefix_v': r'$S_3$=',
}

CL_params_2 = {
    'u_min': 0.1,
    'u_max': 10.0,
    'f': lambda u: u,
    'g': lambda u: 0,
    'h': lambda u: 1.0,
    'title': r'$CL$',
    'scale_type': 'linear',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'grid': False
}


F1_params_3 = {
    'u_min': 10.0,
    'u_max': 65.0,
    'f': lambda u: -1/u,
    'g': lambda u: 1,
    'h': lambda u: 1/u,
    'title': r'$S1$',
    'scale_type': 'linear',
    'tick_levels': 3,
    'tick_text_levels': 2,
    'title_draw_center':True,
    'title_distance_center': -2.0,
    'title_opposite_tick':False,
    'grid': False}


block_params = {
    'block_type': 'type_9',
    'f1_params': F2_F3_params_1,
    'f2_params': CL_params_2,
    'f3_params': F1_params_3,
    'transform_ini': False,
    'isopleth_values': [[ [35, 75], 'x', 60]]
}

main_params = {
    'filename': 'Circulating_Load_Nomogram.pdf',
    'paper_height': 10.0,
    'paper_width': 20.0,
    'block_params': [block_params],
    'transformations': [('rotate', 0.01), ('scale paper',)],
    'title_str': r'$CL={{({{{100}\over{S_{2}}}-{{100}\over{S_{1}}}})}\over{({{{100}\over{S_{1}}}-{{100}\over{S_{3}}}})}}$',
    'debug': False,
    'title_y':-2.0,
    'title_x':1.0,
    'title_box_width':7,
    'make_grid':False,
}
Nomographer(main_params)

"""
    Law_of_Bond_Nomogram.py
"""
import sys

sys.path.insert(0, "..")
# sys.path[:0] = [".."]
from pynomo.nomographer import Nomographer

F80_params = {
    "u_min": 1000,
    "u_max": 120000,
    "function": lambda u: -(1 / (u**0.5)),
    "title": r"$F80$",
    "scale_type": "log",
    "tick_levels": 4,
    "tick_text_levels": 1,
    "tick_side": "left",
    "extra_params": [
        {
            "u_min": 1000,
            "u_max": 20000,
            "tick_levels": 5,
            "tick_text_levels": 1,
            "grid_length_0": 0.75,
            "grid_length_1": 0.60,
            "grid_length_2": 0.40,
            "grid_length_3": 0.25,
            "grid_length_4": 0.15,
            "text_distance_0": 1.0,
            "text_distance_1": 1.0,
            "text_distance_2": 0.80,
            "text_distance_3": 0.70,
            "text_distance_4": 0.70,
        }
    ],
}

P80_params = {
    "u_min": 50.0,
    "u_max": 500.0,
    "function": lambda u: (1 / (u**0.5)),
    "title": r"$P80$",
    "scale_type": "linear smart",
    "tick_levels": 4,
    "tick_text_levels": 1,
    "tick_side": "right",
    "extra_params": [
        {
            "u_min": 200,
            "u_max": 400,
            "tick_levels": 5,
            "tick_text_levels": 1,
            "grid_length_0": 0.75,
            "grid_length_1": 0.60,
            "grid_length_2": 0.40,
            "grid_length_3": 0.25,
            "grid_length_4": 0.15,
            "text_distance_0": 1.0,
            "text_distance_1": 1.0,
            "text_distance_2": 0.80,
            "text_distance_3": 0.70,
            "text_distance_4": 0.70,
        }
    ],
}

reference1_params = {
    "tag": "A",
    "u_min": 0.00001,
    "u_max": 0.1,
    "function": lambda u: -u,
    "reference": True,
    #'title': r'$A$',
    #'tick_levels': 2,
    #'tick_text_levels': 1,
    "scale_type": "linear smart",
}

block_1_params = {
    "block_type": "type_1",
    # "width": 10.0,
    # "height": 10.0,
    "f1_params": F80_params,
    "f2_params": P80_params,
    "f3_params": reference1_params,
    "isopleth_values": [[20000, "x", "x"]],
}


energy_per_st_params = {
    "tag": "E",
    "u_min": 5,
    "u_max": 20,
    "function": lambda u: u,
    "title": r"$E - kWh/st$",
    "title_draw_center": True,
    "title_distance_center": 1.5,
    # "title_x_shift": 0.90,
    #'title_y_shift':1.25,
    "tick_side": "left",
    "tick_levels": 3,
    "tick_text_levels": 1,
}

energy_per_st_index_params = {
    "tag": "Wi",
    "u_min": 8,
    "u_max": 25,
    "function": lambda u: 10 * u,
    "title": r"$Wi - kWh/st$",
    "title_draw_center": True,
    "title_distance_center": 1.5,
    # "title_x_shift": 0.25,
    # "title_y_shift": 1.25,
    "tick_side": "left",
    "tick_levels": 3,
    "tick_text_levels": 2,
    "scale_type": "linear smart",
}

reference2_params = {
    "tag": "A",
    "u_min": 0.00001,
    "u_max": 0.1,
    "function": lambda u: u,
    "reference": True,
    #'title': r'$u_3$',
    #'tick_levels': 3,
    #'tick_text_levels': 1,
    "scale_type": "linear smart",
}

block_2_params = {
    "block_type": "type_2",
    # "width": 10.0,
    # "height": 10.0,
    "f1_params": energy_per_st_params,
    "f2_params": energy_per_st_index_params,
    "f3_params": reference2_params,
    "mirror_x": True,
    "isopleth_values": [[6, 12.23, "x"]],
}

energy_per_mt_params = {
    "u_min": 5,
    "u_max": 20,
    "function": lambda u: u,
    # "title": r"$kWh/mt$",
    # "title_x_shift": 0.90,
    #'title_y_shift':1.25,
    "tick_side": "right",
    "scale_type": "manual data",
    "tick_levels": 3,
    "tick_text_levels": 1,
}

energy_per_mt_index_params = {
    "tag": "Wi",
    "u_min": 8 * 0.90718,
    "u_max": 25 * 0.90718,
    "function": lambda u: 10 * u / 0.90718,
    "title": r"$Wi - kWh/mt$",
    "title_x_shift": 0.25,
    "title_y_shift": 1.25,
    "title_draw_center": True,
    "title_distance_center": -1.75,
    "tick_side": "right",
    "tick_levels": 3,
    "tick_text_levels": 2,
    "scale_type": "linear smart",
}

reference3_params = {
    "tag": "A",
    "u_min": 0.00001,
    "u_max": 0.1,
    "function": lambda u: u,
    "reference": True,
    #'title': r'$u_3$',
    #'tick_levels': 3,
    #'tick_text_levels': 1,
    "scale_type": "linear smart",
}

block_3_params = {
    "block_type": "type_2",
    # "width": 10.0,
    # "height": 10.0,
    "f1_params": energy_per_mt_params,
    "f2_params": energy_per_mt_index_params,
    "f3_params": reference3_params,
    "mirror_x": True,
    "isopleth_values": [["x", "x", "x"]],
}


# # Indice = {
# #     "tag": "Wi",
# #     "u_min": 8 * 0.907,
# #     "u_max": 25 * 0.907,
# #     "function": lambda u: 10 * u,
# #     "align_func": lambda u: u / 0.907,
# #     "title": r"kWh/sht",
# #     "title_x_shift": -1.00,
# #     "title_y_shift": -0.25,
# #     "tick_side": "left",
# #     "tick_levels": 3,
# #     "tick_text_levels": 2,
# #     "scale_type": "linear smart",
# # }

# # block_3_params = {
# #     "block_type": "type_8",
# #     "f_params": Indice,
# #     # "isopleth_values": [["x"]],
# # }

E = {
    "tag": "E",
    "u_min": 5 * 0.907,
    "u_max": 20 * 0.907,
    "function": lambda u: u,
    "align_func": lambda u: u / 0.907,
    "title": r"E - kWh/mt",
    # "title_x_shift": -0.75,
    #'title_y_shift':0.25,
    "title_draw_center": True,
    "title_distance_center": -1.7,
    "tick_side": "right",
    "tick_levels": 3,
    "tick_text_levels": 1,
    #'scale_type':'linear smart',
}

block_4_params = {
    "block_type": "type_8",
    "f_params": E,
    "isopleth_values": [["x"]],
}


main_params = {
    "filename": "Law_of_Bond_Nomogram.pdf",
    "paper_height": 10.0,
    "paper_width": 15.0,
    "block_params": [
        block_1_params,
        block_2_params,
        block_3_params,
        block_4_params,
    ],
    "transformations": [("rotate", 0.01), ("scale paper",)],
    "title_str": r"$E=10\times Wi\times\left({{{1}\over{P80^{0.5}}}-{{1}\over{F80^{0.5}}}}\right)$",
    "debug": False,
}
Nomographer(main_params)

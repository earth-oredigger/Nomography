#!/usr/bin/env python3

# nomogen example
# The processing recovery equation

# pylint: disable=C

import sys
import math

import inspect
import os

sys.path.insert(0, "..")

from nomogen import Nomogen
from pynomo.nomographer import Nomographer

# get current file name
myfile = os.path.basename(inspect.stack()[0][1]).replace(".py", "")


########################################
#
#  this is the target function,
#  - the function that the nomogram implements
#  - add the limits of the variables below
#
#  format is m = m(l,r), where l, m & r are respectively the values
#                        for the left, middle & right hand axes
#
#
########################################


# simple example
# return value is the middle scale
# u & v are respectively the values on the left and right scales
def R(t, c):
    return 100*c*(1-t)/(c-t)


# range for the u scale (the left scale)
tmin = 0.05
tmax = 0.20

# range for the v scale (the right scale)
cmin = 5
cmax = 30

# range for the w scale (the middle scale)

Rvals = [R(tmin, cmin), R(tmin, cmax), R(tmax, cmin), R(tmax, cmax)]

Rmin = min(Rvals)
Rmax = max(Rvals)


###############################################################
#
# nr points (Chebyshev nodes) needed to define the scales
# a higher value may be necessary if the scales are very non-linear
# a lower value is faster and makes a smoother curve,
#     but could be less accurate
NN = 12


##############################################
#
# definitions for the axes for pyNomo
# dictionary with key:value pairs

left_axis = {
    'u_min': tmin,
    'u_max': tmax,
    'title': r'$ t \over f $',
    'title_x_shift': -0.3,
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
}

right_axis = {
    'u_min': cmin,
    'u_max': cmax,
    'title': r'$ c \over f $',
    'title_x_shift': 0.5,
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
}

middle_axis = {
    'u_min': Rmin,
    'u_max': Rmax,
    'title': r'$Rec \thinspace \%$',
    'title_x_shift': 1.9,
    'title_y_shift': -0.5,
    'scale_type': 'linear smart',
    'tick_levels': 3,
    'tick_text_levels': 2,
}

# assemble the above 3 axes into a block
block_params0 = {
    'block_type': 'type_9',
    'f1_params': left_axis,
    'f2_params': middle_axis,
    'f3_params': right_axis,

    # the isopleth connects the mid values of the outer axes
    # edit this for different values
    'isopleth_values': [[(left_axis['u_min'] + left_axis['u_max']) / 2, \
                         'x', \
                         (right_axis['u_min'] + right_axis['u_max']) / 2]],

    # log alignment errors
    # If this is missing or False then alignment error logs are disabled
    'LogAlignment': False,
}

# the nomogram parameters

main_params = {
    'filename': myfile,
    'paper_height': 10,  # units are cm
    'paper_width': 10,
    'title_x': 7.0,
    'title_y': 8.0,
    'title_box_width': 8.0,
    'title_str': r'$Rec \thinspace \% = {{100{c \over f}( 1 - {t \over f})} \over {{ {c \over f}} - { t \over f}}}$',
    'block_params': [block_params0],

    # set the colour of the ispleth/index line here
    'isopleth_params': [ {'color': 'Red'}, ],

    'transformations': [('scale paper',)],

    'npoints': NN,

    # instead of forcing the ends of the axes to the corners of the unit square,
    # nomogen can shape the nomogram to minimise parallax errors
    # uncomment the following line to select this option
    #'muShape': 1,

    # text to appear at the foot of the nomogram
    # note that latex rules apply
    # a default string will appear if this is omitted
    # make this an empty string to have no footer text
    #'footer_string': ' concentartion project footer string'
}

print("calculating the nomogram ...")
Nomogen(R, main_params)  # generate nomogram for the target function

main_params['filename'] += '.pdf'
print("printing ", main_params['filename'], " ...")
Nomographer(main_params)

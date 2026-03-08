"""
    Modified_Hogg_Fuerstenau_Nomogram.py

"""
import sys
import numpy as np
from pyx import *

sys.path.insert(0, "..")
from pynomo.nomographer import Nomographer
text.set(text.LatexEngine)


Nc_params_4 = {
    'u_min': 0.65,
    'u_max': 0.80,
    'function': lambda u: -np.log10(u),
    'title': r'$Nc$',
    'tick_levels': 2,
    'tick_text_levels': 1,
    'tick_side': 'left',
}

D_params_2 = {
    'u_min': 10.0,
    'u_max': 40.0,
    'function': lambda u: 0.6234-3.5*np.log10(u),
    'title': r'$D$',
    'tick_levels': 2,
    'tick_text_levels': 1,
    	
     'extra_params':[{
    		'u_min':10,
    			'u_max':26.0,
    				'tick_levels':3,
    					'tick_text_levels':0,
    		
    	}	
    	],
   
}

LD_params_3 = {
    'u_min': 1.0,
    'u_max': 1.8,
    'function': lambda u: -np.log10(u),
    'title': r'$L/D$',
    'tick_levels': 2,
    'tick_text_levels': 1,
}

Pnet_params_1 = {
    'u_min': 1000.0,
    'u_max': 30000.0,
    'function': lambda u: np.log10(u),
    'title': r'$Pnet$',
    'tick_levels': 2,
    'tick_text_levels': 1,
    'tick_side': 'left',
   
    'extra_params':[{
    		'u_min':1000,
    			'u_max':12000.0,
    				'tick_levels':3,
    					'tick_text_levels':0,
    		
    	}	
    	],
   
}


Pap_params_5 = {
    'u_min': 2.0,
    'u_max': 5.5,
    'function': lambda u: -np.log10(u),
    'title': r'$P_ap$',
    'tick_levels': 3,
    'tick_text_levels': 1,
}

Alpha_params_7 = {
    'u_min': 25.0,
    'u_max': 35.0,
    'function': lambda u: -np.log10(np.sin(u*3.1415/180)),
    'title': r'$Alpha$',
    'tick_levels': 2,
    'tick_text_levels': 1,
    'tick_side': 'right',
}

Jc_params_6 = {
    'u_min': 0.30,
    'u_max': 0.44,
    'function': lambda u: -np.log10(u-1.065*u**2),
    'title': r'$Jc$',
    'tick_levels': 2,
    'tick_text_levels': 1,
    'tick_side': 'right',
}


block_1_params = {
    'block_type': 'type_3',
    'width': 10.0,
    'height': 10.0,
    'f_params': [Nc_params_4, D_params_2, LD_params_3, Pnet_params_1, Pap_params_5, Alpha_params_7, Jc_params_6 ],
    'isopleth_values': [[0.75, 18, 1.2, 'x', 3, 30, 0.35]],
}

main_params = {
    'filename': 'Modified_Hogg_Fuerstenau_Nomogram.pdf',
    'paper_height': 20.0,
    'paper_width': 20.0,
    'block_params': [block_1_params],
    'transformations': [('rotate', 0.01), ('scale paper',)],
    'title_str': r'$P_{net}=0.267\cdot D^{3.5}\cdot{{L}\over{D}}\cdot N_{c}\cdot\rho_{ap}\cdot\left({J_{c}-J_{c}^{2}}\right)\cdot\sin\alpha$',
    'title_y': 0.0,
}
Nomographer(main_params)

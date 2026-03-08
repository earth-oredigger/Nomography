"""
    Azzaroni_Nomogram.py
"""
import sys
import numpy as np
from pyx import *

sys.path.insert(0, "..")
from pynomo.nomographer import Nomographer
text.set(text.LatexEngine)



F80_params_1 = {
    'u_min': 1000.0,
    'u_max': 10000.0,
    'function': lambda u:-np.log10(6.06)-0.263*np.log10(u),
    'title': r'$F80$',
    'tick_levels': 3,
    'tick_text_levels': 1,
    'tick_side': 'left',
     
}

dB_params_2 = {
    'u_min': 25,
    'u_max': 100.0,
    'function': lambda u: np.log10(u),
    'title': r'$d_B$',
    'tick_levels': 3,
    'tick_text_levels': 1,
 
}


Rho_params_3 = {
    'u_min': 2.0,
    'u_max': 4.0,
    'function': lambda u: -0.4*np.log10(u),
    'title': r'$Rho_m$',
    'tick_levels': 0,
    'tick_text_levels': 0,
    'extra_params':[{
    		'u_min':2.0,
    			'u_max':4.0,
    				'tick_levels':1,
    					'tick_text_levels':1,
    						'grid_length_0':0.30,
    							'grid_length_1':0.20,
    								'grid_length_2':0.10,
    									'grid_length_3':0.10,
    											'text_distance_0':0.35,
    													'text_distance_1':0.30,
    														'text_distance_2':0.30,
    															'text_distance_3':0.30,
    															'text_distance_4':0.30,
    	}
    	],
    	
}
Wi_params_4 = {
    'u_min': 8,
    'u_max': 25,
    'function': lambda u: -0.4*np.log10(u),
    'title': r'$W_i$',
    'tick_levels': 0,
    'tick_text_levels': 0,
      'extra_params':[{
    		'u_min':8.0,
    			'u_max':25,
    				'tick_levels':2,
    					'tick_text_levels':1,
    						'grid_length_0':0.30,
    							'grid_length_1':0.20,
    								'grid_length_2':0.10,
    									'grid_length_3':0.10,
    											'text_distance_0':0.35,
    													'text_distance_1':0.30,
    														'text_distance_2':0.30,
    															'text_distance_3':0.30,
    															'text_distance_4':0.30,
    	}
    	],
    	
    
       
}

N_params_5 = {
    'u_min': 11.0,
    'u_max': 17.0,
    'function': lambda u:0.25*np.log10(u),
    'title': r'$N$',
    'tick_levels': 0,
    'tick_text_levels': 0,
     'tick_side': 'right',
     'extra_params':[{
    		'u_min':11.0,
    			'u_max':17.0,
    				'tick_levels':2,
    					'tick_text_levels':1,
    						'grid_length_0':0.30,
    							'grid_length_1':0.15,
    								'grid_length_2':0.10,
    									'grid_length_3':0.10,
    											'text_distance_0':0.35,
    													'text_distance_1':0.30,
    														'text_distance_2':0.30,
    															'text_distance_3':0.30,
    															'text_distance_4':0.30,
    	}
    	],
    	
    
     
     }


D_params_6_feet = {
    'tag':'D',
    'u_min': 10.0,
    'u_max': 30.0,
    'function': lambda u: 0.25*np.log10(u),
    'title': r'$D$',
    'tick_levels': 0,
    'tick_text_levels': 0,
    'tick_side': 'right',
    'extra_params':[{
    		'u_min':10.0,
    			'u_max':30.0,
    				'tick_levels':2,
    					'tick_text_levels':1,
    						'grid_length_0':0.30,
    							'grid_length_1':0.15,
    								'grid_length_2':0.10,
    									'grid_length_3':0.10,
    											'text_distance_0':0.35,
    													'text_distance_1':0.30,
    														'text_distance_2':0.30,
    															'text_distance_3':0.30,
    															'text_distance_4':0.30,
    	}
    	],
    	
    
     
}


block_1_params = {
    'block_type': 'type_3',
    'width': 10.0,
    'height': 10.0,
    'f_params': [F80_params_1, dB_params_2, Rho_params_3,
                 Wi_params_4, N_params_5, D_params_6_feet],
    'isopleth_values': [[2000, 'x', 3, 17, 15, 15, 20 ]],
}

D_params_1_mm = {
    'tag':'D',
    'u_min': 10.0*0.3048,
    'u_max': 30.0*0.3048,
    'function': lambda u: 0.25*np.log10(u),
    'align_func':lambda u:u/0.3048,
    'title': r'$D \enspace (mm)$',
    'tick_levels': 0,
    'tick_text_levels': 0,
    'tick_side':'left',
    #'title_y_shift':0.50,
    #'title_x_shift':0.0,
    'title_draw_center':True,
    'title_distance_center': -1.0,
    'title_opposite_tick':False,
    #'scale_type': 'linear smart',
    'extra_params':[{
    		'u_min':10.0*0.3048,
    			'u_max':30.0*0.3048,
    				'tick_levels':3,
    					'tick_text_levels':1,
    						'grid_length_0':0.30,
    							'grid_length_1':0.20,
    								'grid_length_2':0.10,
    									'grid_length_3':0.10,
    											'text_distance_0':0.35,
    													'text_distance_1':0.30,
    														'text_distance_2':0.30,
    															'text_distance_3':0.30,
    																'text_distance_4':0.30,
    		
    	}	
    	],
}

block_2_params={
				'block_type':'type_8',
				'f_params':D_params_1_mm,
				'isopleth_values': [['x']],
}


main_params = {
    'filename': 'Azzaroni_Nomogram.pdf',
    'paper_height': 20.0,
    'paper_width': 25.0,
    'block_params': [block_1_params, block_2_params],
    'transformations': [('rotate', 0.01), ('scale paper',)],
    'extra_texts': [
        {
            'x': 1.0,
            'y': 1.0,
            'text': r'$d_{B}^{*}=6.06\cdot F_{80}^{0.263}\cdot{{{\left({\rho_{m}\cdot W_{i}}\right)}^{0.4}}\over{{\left({N\cdot D}\right)}^{0.25}}}$',
            'width': 10,
        }
    ],
}
Nomographer(main_params)

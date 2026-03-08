"""
    Mill_Speed_Nomogram.py

"""
import sys

sys.path.insert(0, "..")
from pynomo.nomographer import Nomographer

Nc_params_1 = {
    'u_min': 0.1,
    'u_max': 1.0,
    'function': lambda u: u,
    'title': r'$Nc$',
    'tick_levels': 0,
    'tick_text_levels': 0,
    'tick_side': 'right',
    'extra_params':[{
    		'u_min':0.1,
    			'u_max':1.0,
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

N_params_2 = {
    'u_min': 10,
    'u_max': 20,
    'function': lambda u: u,
    'title': r'$N$',
    'tick_levels': 0,
    'tick_text_levels': 0,
    'scale_type': 'linear smart',
    'tick_side': 'left',
    'extra_params':[{
    		'u_min':10,
    			'u_max':20,
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

D_ft_params_3 = {
    'tag':'D',
    'u_min': 10,
    'u_max': 30,
    'function': lambda u: (u**0.5)/76.6,
    'title': r'$D$',
    'tick_levels': 0,
    'tick_text_levels': 0,
    'tick_side': 'left',
    'extra_params':[{
    		'u_min':10,
    			'u_max':30,
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

block_1_params = {
    'block_type': 'type_2',
    'width': 10.0,
    'height': 10.0,
    'f1_params': Nc_params_1,
    'f2_params': N_params_2,
    'f3_params': D_ft_params_3,
    'isopleth_values': [['x', 15, 20]],
    'mirror_x': True,
}

D_m_params_1 = {
    'tag':'D',
    'u_min': 10*0.3048,
    'u_max': 30*0.3048,
    'function': lambda u: (u**0.5)/76.6,
     'align_func':lambda u:u/0.3048,
    'title': r'$$',
    'tick_levels': 0,
    'tick_text_levels': 0,
    'tick_side': 'right',
    'extra_params':[{
    		'u_min':10*0.3048,
    			'u_max':30*0.3048,
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
				'f_params':D_m_params_1,
				'isopleth_values': [['x']],
}


main_params = {
    'filename': 'Mill_Speed_Nomogram.pdf',
    'paper_height': 10.0,
    'paper_width': 10.0,
    'block_params': [block_1_params, block_2_params],
    'transformations': [('rotate', 0.01), ('scale paper',)],
    'title_str': r'$N_{c}={{N\cdot\sqrt{D}}\over{76.6}}$'
}
Nomographer(main_params)

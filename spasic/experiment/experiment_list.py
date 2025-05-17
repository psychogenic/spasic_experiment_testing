'''
@author: Pat Deegan
@copyright: Copyright (C) 2025 Pat Deegan, https://psychogenic.com
'''

import spasic.experiment.tt_um_test.loader
import spasic.experiment.tt_um_fstolzcode.loader
import spasic.experiment.tt_um_oscillating_bones.loader
import spasic.experiment.tt_um_qubitbytes_alive.loader
import spasic.experiment.wokwi_universal_gates_049.loader

ExperimentsAvailable = {
    
        # 1 sample experiment
        1: spasic.experiment.tt_um_test.loader.run_experiment,
        
        # 2 sample experiment
        2: spasic.experiment.tt_um_fstolzcode.loader.run_experiment,

        # oscillating bones
        3: spasic.experiment.tt_um_oscillating_bones.loader.run_experiment, 
        
        # calvin!  
        4: spasic.experiment.tt_um_qubitbytes_alive.loader.run_experiment,    

        # universal gates
        7: spasic.experiment.wokwi_universal_gates_049.loader.run_experiment,
    }


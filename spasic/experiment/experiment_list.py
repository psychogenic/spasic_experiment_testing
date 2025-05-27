'''
@author: Pat Deegan
@copyright: Copyright (C) 2025 Pat Deegan, https://psychogenic.com
'''

import spasic.experiment.tt_um_test.loader
import spasic.experiment.tt_um_fstolzcode.loader
import spasic.experiment.tt_um_oscillating_bones.loader
import spasic.experiment.tt_um_qubitbytes_alive.loader
import spasic.experiment.tt_um_andrewtron3000.loader
import spasic.experiment.wokwi_universal_gates_049.loader
import spasic.experiment.tt_um_ttrpg_SEU.loader

ExperimentsAvailable = {
    
        # 1 sample experiment
        1: spasic.experiment.tt_um_test.loader.run_experiment,
        
        # 2 TinyZuse FPU
        2: spasic.experiment.tt_um_fstolzcode.loader.run_experiment,

        # oscillating bones
        3: spasic.experiment.tt_um_oscillating_bones.loader.run_experiment, 
        
        # calvin!  
        4: spasic.experiment.tt_um_qubitbytes_alive.loader.run_experiment,    
  
        # Rule 30 Engine!
        5: spasic.experiment.tt_um_andrewtron3000.loader.run_experiment,
  
        # SEU detector in ttrpgdice
        6: spasic.experiment.tt_um_ttrpg_SEU.loader.run_experiment,
  
        # universal gates
        7: spasic.experiment.wokwi_universal_gates_049.loader.run_experiment,
  
        # 9 TinyQV
        9: spasic.experiment.tt_um_MichaelBell_tinyQV.loader.run_experiment,
  
        # lisa  
        10: spasic.experiment.tt_um_lisa.loader.run_experiment

}


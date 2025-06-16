'''
@author: Pat Deegan
@copyright: Copyright (C) 2025 Pat Deegan, https://psychogenic.com
'''

import spasic.experiment.tt_um_test.loader
import spasic.experiment.tt_um_fstolzcode.loader
import spasic.experiment.tt_um_oscillating_bones.loader
import spasic.experiment.tt_um_qubitbytes_alive.loader
import spasic.experiment.tt_um_urish_spell.loader
import spasic.experiment.tt_um_msg_in_a_bottle.loader
import spasic.experiment.tt_um_ttrpg_dice.loader
import spasic.experiment.tt_um_andrewtron3000.loader
import spasic.experiment.wokwi_universal_gates_049.loader
import spasic.experiment.tt_um_ttrpg_SEU.loader
import spasic.experiment.tt_um_MichaelBell_tinyQV.loader
import spasic.experiment.tt_um_lisa.loader
import spasic.experiment.tt_um_cejmu.loader
import spasic.experiment.rp2_temperature.loader
import spasic.experiment.tt_um_CKPope_top.loader

ExperimentsAvailable = {
    
        # 1 sample experiment
        1: spasic.experiment.tt_um_test.loader.run_experiment,
        
        # 2 TinyZuse FPU
        2: spasic.experiment.tt_um_fstolzcode.loader.run_experiment,

        # oscillating bones
        3: spasic.experiment.tt_um_oscillating_bones.loader.run_experiment, 
        
        # calvin!  
        4: spasic.experiment.tt_um_qubitbytes_alive.loader.run_experiment,

        # SPELL
        5: spasic.experiment.tt_um_urish_spell.loader.run_experiment,
  
        # SEU detector in ttrpgdice
        6: spasic.experiment.tt_um_ttrpg_SEU.loader.run_experiment,
  
        # universal gates
        7: spasic.experiment.wokwi_universal_gates_049.loader.run_experiment,
  
        # Rule 30 Engine!
        8: spasic.experiment.tt_um_andrewtron3000.loader.run_experiment,
  
        # 9 TinyQV
        9: spasic.experiment.tt_um_MichaelBell_tinyQV.loader.run_experiment,
  
        # lisa  
        10: spasic.experiment.tt_um_lisa.loader.run_experiment,
  
        # Dice roller
        11: spasic.experiment.tt_um_ttrpg_dice.loader.run_experiment,
  
        # Pinecone
        12: spasic.experiment.tt_um_msg_in_a_bottle.loader.run_experiment,
        
        # TinyRV1 from the University of Wuerzburg
        13: spasic.experiment.tt_um_cejmu.loader.run_experiment,
        
        # RP2 temperature measurement
        14: spasic.experiment.rp2_temperature.loader.run_experiment,
        
        # X/Y motion controller
        15: spasic.experiment.tt_um_CKPope_top.loader.run_experiment,
}

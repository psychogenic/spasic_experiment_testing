'''
Created on May 8, 2025

@author: Matt Venn
@copyright: Copyright (C) 2025 Matt Venn
'''

from spasic.experiment.experiment_result import ExpResult
from spasic.experiment.experiment_parameters import ExperimentParameters

def run_experiment(params:ExperimentParameters, response:ExpResult):
    
    # always wrap everything in a try block
    try:
        # import HERE, inside the function, 
        # such that loading all the experiment runners doesn't 
        # eat a ton of memory by pre-importing everything
        import spasic.experiment.tt_um_oscillating_bones.counter
        
        # run that experiment
        spasic.experiment.tt_um_oscillating_bones.counter.test_counter(params, response, num_iterations=16)
        
    except Exception as e:
        # an exception occurred... 
        # let the server know about it
        response.exception = e 
    else:
        # we get here, all went well
        # mark the experiment as completed
        response.completed = True
    return

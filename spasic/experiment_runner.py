'''
Created on Apr 30, 2025

@author: Pat Deegan
@copyright: Copyright (C) 2025 Pat Deegan, https://psychogenic.com
'''
import time
import _thread
from ttboard.demoboard import DemoBoard
from spasic.experiment.experiment_result import ExpResult
from spasic.experiment.experiment_parameters import ExperimentParameters
from spasic.experiment.experiment_list import ExperimentsAvailable

_thread.stack_size(5120)

class ExperimentRunner:
    '''
        ExperimentRunner: allows you to launch experiments and get their status as they go
        
        Example
        runner = ExperimentRunner()
        if not runner.launch(1):
            raise Exception("Ugh couldn't do it")
        
        while runner.experiment_running:
            time.sleep(1)
            print(f"After {runner.experiment_duration}s, results are now: {runner.experiment_result}")
            
        if runner.experiment_completed:
            print(f"Experiment completed after {runner.experiment_duration}s")
        else:
            print(f"Not running but not completed either... exception is: {runner.experiment_exception}")
            
            
    
    '''
    
    def __init__(self):
        self._result = ExpResult()
        self._params = ExperimentParameters(DemoBoard.get())
        
    def status(self):
        if self.experiment_running:
            print(f'Experiment {self.experiment_id} running ({self.experiment_duration}s)')
            print(f'\tCurrent results: {self.experiment_results_as_str}')
            return 
        
        if self.experiment_id == 0:
            print("No experiment yet run")
            return 
        
        if self.experiment_completed:
            print(f'Experiment {self.experiment_id} completed after {self.experiment_duration}s')
            print(f'  Final results: {self.experiment_results_as_str}')
            return
        
        if self.experiment_exception is not None:
            print(f'Experiment {self.experiment_id} had exception after {self.experiment_exception}')
            print(f'  Final results: {self.experiment_results_as_str}')
            return 
        
        print(f'Experiment {self.experiment_id} is marked neither as completed nor as having exception??')
        print(f'  Final results: {self.experiment_results_as_str}')
        
            
            
            
            
    
    @property 
    def experiment_id(self):
        return self._result.expid
    @property 
    def experiment_running(self):
        '''
            Experiment is still running?
        '''
        return self._result.running
    
    @property 
    def experiment_result(self):
        '''
            Current value of results reported by experiment
        '''
        if self._result.result is not None and len(self._result.result) > 10:
            return self._result.result[:10]
        
        return self._result.result
    
    @property 
    def experiment_results_as_str(self):
        return ' '.join(map(lambda x: hex(x), self._result.result))
    
    @property 
    def experiment_completed(self):
        return self._result.completed
    
    @property 
    def experiment_exception(self):
        '''
            Any exception reported by experiment
        '''
        return self._result.exception
    
    @property 
    def experiment_duration(self):
        '''
            Run time in seconds of experiment
        '''
        return self._result.run_duration
    
    def get_loader(self, experiment_id:int):
        
        if not isinstance(experiment_id, int):
            raise RuntimeError('Must pass experiment id as INTEGER') 

        if experiment_id not in ExperimentsAvailable:
            print(f"I'm not aware of experiment {experiment_id}.  Add it to ExperimentsAvailable")
            return False 
        
        runner = ExperimentsAvailable[experiment_id]
        return runner
    
    def monitor_until_completed(self, sleep_interval:float=0.25):
        
        if not self.experiment_id:
            print("No experiment run!")
            return 
        if self.experiment_completed:
            print("Already done!")
            self.status()
            
        
        print(f"Monitoring experiment {self.experiment_id}...")
        self.status()
        bts = bytearray()
        while not self.experiment_completed:
            if self.experiment_result != bts:
                print()
                self.status()
                bts = bytearray(self.experiment_result)
        
        print()
        print()
        print("Experiment run completed!  Final status:")
        self.status()
                
            
            
        
    
    def trigger_loader_in_mainthread(self, experiment_id:int, experiment_parameters:bytearray=None):
        '''
            A utility method for debugging
        
        '''
        runner = self.get_loader(experiment_id)
        
        if not runner:
            print(f"Could not fetch runner for exp {experiment_id}")
            return False
        
        if experiment_parameters is None:
            experiment_parameters = bytearray(10)
        
        self._result.expid = experiment_id
        self._result.start()
        self._params.start(experiment_parameters)
        
        runner(self._params, self._result)

        
        
    def launch(self, experiment_id:int, experiment_parameters:bytearray=None):
        '''
            launch experiment
            @param experiment_id: integer ID of experiment to run
            @param exp_params: optional bytearray of parameters to pass in (up to 10 bytes)
            @return: True on launch success
        
        '''
        if experiment_parameters is None:
            experiment_parameters = bytearray(10)

        parm_len = len(experiment_parameters) 
        if parm_len> 10:
            experiment_parameters = experiment_parameters[:10]
        elif parm_len < 10:
            experiment_parameters += bytearray(10 - parm_len)

        if self._result.running:
            print(f"Can't launch!  Experiment {self._result.expid} is currently running")
            return False 
        
        runner = self.get_loader(experiment_id)
        if not runner:
            print(f"Could not fetch runner for exp {experiment_id}")
            return False
        
        self._result.expid = experiment_id
        self._result.start()
        self._params.start(experiment_parameters)

        
        print(f"Launching experiment {experiment_id}")
        try:
            _thread.start_new_thread(runner, (self._params, self._result,))
        except:
            print("Could not launch experiment -- something still going on in there?")
            return False
        
        return True
    
    def abort(self):
        if not self._result.running:
            print("Nothing seems to be running at the moment")
            return False 
        
        print("Requesting experiment terminate...")
        self._params.terminate()
        time.sleep(2)
        if self.experiment_running:
            print("However, still seems to be running after 2 seconds...")
        else:
            print("Experiment has terminated")

def runExperiment1(runner:ExperimentRunner=None):
    print("runExperiment1")
    if runner is None:
        runner = ExperimentRunner()
    if not runner.launch(1):
        raise Exception("Ugh couldn't do it")
    
    while runner.experiment_running:
        time.sleep(1)
        runner.status()
        
    if runner.experiment_completed:
        print(f"Experiment completed after {runner.experiment_duration}s")
    else:
        print(f"Not running but not completed either... exception is: {runner.experiment_exception}")
    

if __name__ == '__main__':
    runner = ExperimentRunner()
    runExperiment1(runner)
    
# spASIC Experiment Testing

&copy; 2025 Pat Deegan, [https://psychogenic.com](https://psychogenic.com)

A system to allow you to develop and test your spASIC experiments on TT demoboards.

With this framework, you can easily design your experiment to run (in SPACE!) on the experiment module.

There are a few relatively simple steps to integrate your test in a manner that will work within the spasics SDK.  

## Quickstart Guide

More details below, but the short version is

   1. Fork this repository
	
   2. In your clone, create a package under spasic.experiment using `spasic.experiment.tt_um_test` as a guide
	
   3. Run your tests using the ExperimentRunner and ensure all is well
   
   4. Make a pull-request to merge your experiment prior to launch
   

## Running experiments

To get this working, you should have a [TT06 demoboard](https://github.com/tinytapeout/tt-demo-pcb)--TT06 because that's the chip we're launching, though you could do dev on other demoboards too.

Using your preferred method to get files onto the micropython filesystem, copy over the [spasic](spasic) module to the root directory.

With that installed, you should be able to access the REPL and do:

```
from spasic.experiment_runner import ExperimentRunner
runner = ExperimentRunner()

runner.launch(1)
```

The `ExperimentRunner` instance acts like the module on board the satellite in that it can:

  * start up experiment functions, providing the right type of objects as arguments 
  
  * optionally pass parameters to the experiments
  
  * get results reported by experiments as they are running and once they've completed
  
  * request experiments terminate prior to completion (allowing for "infinite loop" functions that we can leave running for a long time and still terminate eventually)
  
### Runner methods

In addition to allowing you to start-up experiments, the runner lets you see the state of things as the tests are running and when they are done.

The following methods and attributes are supported

   * `launch(EXP_ID, [ARGUMENT_BYTES])`: start the test, optionally passing (up to) 10 bytes of arbitrary data to configure the run
   
   * `status()`: utility method to print out a summary of current status
   
   * `experiment_id`: id of experiment (currently running or last) experiment
   
   * `experiment_running`: boolean indicating whether experiment is still running
   
   * `experiment_result`: a bytearray of data returned by experiment.  This can (and should likely) be updated by the test as it is running, as we can fetch intermediate results prior to run being completed
   
   * `experiment_completed`: a boolean indicating the experiment was completed normally.  Prior to returning from a test function, either this value should be True or an exception be set in results (more on this below)
   
   * `experiment_exception`: an instance of Exception, encountered during the run
   
   * `experiment_duration`: current or final run time of experiment, in seconds
   
   * `abort()`: a request will be sent to the experiment to complete now. You must respect this request in your test.
   
In addition, there are a few utility attributes/methods that make things easier:
   
   * `experiment_results_as_str`: gives you a representation of the bytes, like "0x3 0x0 0x7 0x0 0x0 0xff 0xff 0xff"
   
   * `status()`: prints out a summary of the experiment state (completed, runtime, result)
   
   * `monitor_until_completed()`: reports any changes to the results (by calling `status()`) during a run, and exits when the experiment stops running
   
 
   
### Sample Interaction
   
Here's a sample of launching an experiment and monitoring its status as it runs

```
    runner = ExperimentRunner()
    # launch experiment 1
    if not runner.launch(1):
        raise Exception("Ugh couldn't do it")
    
    runner.monitor_until_completed()
    
    # ok, we're done
    if runner.experiment_completed:
        print(f"Experiment completed after {runner.experiment_duration}s")
    else:
        print(f"Not running but not completed either... exception is: {runner.experiment_exception}")
```

This might output something like:


```
Launching experiment 1
Experiment 1 running (2s)
        Current results: 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0

Experiment 1 running (2s)
        Current results: 0x1 0x0 0x0 0x0 0x0 0x0 0x0 0x0
        
Experiment 1 running (9s)
        Current results: 0x3 0x0 0x2 0x0 0x0 0xff 0xff 0xff

Experiment 1 running (21s)
        Current results: 0x3 0x0 0x6 0x0 0x0 0xff 0xff 0xff

Experiment 1 completed after 23s
  Final results: 0x3 0x0 0x7 0x0 0x0 0xff 0xff 0xff

Experiment done!  Final status:
Experiment 2 completed after 23s
  Final results: 0x3 0x0 0x7 0x0 0x0 0xff 0xff 0xff

Experiment completed after 23s
```


## Writing Your Tests

Tests are written in python and have access to an instance of the [TT SDK's](https://github.com/TinyTapeout/tt-micropython-firmware) [DemoBoard](https://github.com/TinyTapeout/tt-micropython-firmware/blob/main/src/ttboard/demoboard.py), so you can select the design, twiddle its inputs, look at its outputs, etc.

The sample we were running above, "experiment 1", is located in [spasic.experiment.tt_um_test](spasic/experiment/tt_um_test), and is a good starting point for your own test.

   1. Create a package under `spasic.experiment` to hold your files.

So that's a directory under there, including at least an `__init__.py` file.  In theory, its name can be any valid python package name, but it's recommended you name it according to the design you're testing, e.g. `tt_um_factory_test`.

   2. Create a module which contains your experiment/test code.
   
In the sample, that's [counter.py](spasic/experiment/tt_um_test/counter.py).  You can name that whatever you like and do pretty much anything in there.  The main thing is that your experiment will have access to, and really *must* use, two objects: an `ExperimentParameters` to config and control it and an `ExpResult` instance to return your data through.


### Test module

Your test module can be anything but it has a couple of jobs to fulfill.  The most basic way to implement this is to have a function, say:

```
def my_superduper_test(params:ExperimentParameters, response:ExpResult):
	pass
```

so I'll use that as an example.

In that function, in addition to whatever you will be testing, you have two jobs:

   1. keep an eye on `params.keep_running`: if that's no longer True, you should return soon
   
   2. set `response.result` according to whatever you want to say back to the world at any point
   

**keep_running**

For the first of these, it's pretty simple: wherever you have a tight loop or will be spending some time, have a look at `keep_running` and return if it says you should not ... keep running.

```
def my_superduper_test(params:ExperimentParameters, response:ExpResult):
    for i in range(1000):
        if not params.keep_running:
            return
        time.sleep(0.05)
```


**result**

The result is a bytearray of up to 10 bytes in which you can stuff whatever data is relevant to you.  The format of this array is arbitrary, the idea being that you know how you stuffed it, and you'll be able to interpret it when it gets back to Earth.

```
def my_superduper_test(params:ExperimentParameters, response:ExpResult):
    # create a container of the right size for my result
    response.result = bytearray(4) # all 0 by default
    for count in range(1000):
        if not params.keep_running:
            return
        # update my result as I go along
        response.result[0:4] = count.to_bytes(4, 'little')
        time.sleep(0.05)
```

This example is trivial, but you get the idea.  Note that I didn't have to use `result[0:4]` here, but this is the way to do it if you had other bytes for other data that you didn't want to lose.



**TT functionality**

So far, the example had nothing to do with TT designs.  You'll want to get access to that `DemoBoard` object and setup your project, twiddle bits.  The instance is available in the `tt` attribute of that `ExperimentParameters` object.  Get it from there.

```
import time
from spasic.experiment.experiment_result import ExpResult
from spasic.experiment.experiment_parameters import ExperimentParameters


def my_superduper_test(params:ExperimentParameters, response:ExpResult):
    # create a container of the right size for my result
    response.result = bytearray(8) # all 0 by default
    
    # get the TT DemoBoard object from params passed in
    tt = params.tt 
    
    # Use the TT object to load your design, e.g. 
    tt.shuttle.tt_um_factory_test.enable()
    
    # We want to clock it manually, stop any auto-clocking:
    tt.clock_project_stop()
    
    # ... do things, keep an eye on keep_running and 
    # put interesting things in result bytes.
```

### Loader module

With the test module done, we need a way to bring it into the system.

For reasons (mainly memory conservation and the fact that we can not do dynamic imports in micropython), we have to use a loader function that hides the heavy imports from view until we actually need them.

So, in that same package, create another module that will contain the loader function.

In the sample, that's [loader.py](spasic/experiment/tt_um_test/loader.py).

This module requires (and should have) only one function, with this signature:

```
def some_name(params:ExperimentParameters, response:ExpResult):
	pass
```

This function has 3 jobs:

   1. import the test module we created in the section above
   
   2. actually run the test
   
   3. report completion or exceptions
   

So the complete function would look like this, in our example case


```

# import only these guys:
from spasic.experiment.experiment_result import ExpResult
from spasic.experiment.experiment_parameters import ExperimentParameters

def some_loader_name(params:ExperimentParameters, response:ExpResult):
    # try/except block
    try:
        # do the import INSIDE the function
        import spasic.experiment.tt_um_my_module.test_code
        # run the test
        spasic.experiment.tt_um_my_module.test_code.my_superduper_test(params, response)
    except Exception as e:
        # got an exception, report that
        response.exception = e
    else:
        # no exception, complete ok, report that
        response.completed = True
        
```


### Make the experiment available

All right, pretty much done here.

The final thing is to inform the system that this experiment exists to make it available.

Edit [experiment_list.py](spasic/experiment/experiment_list.py) and 

   1. add the import of your loader

```
import spasic.experiment.tt_um_my_module.loader

```

   2. add the loading function to the dictionary, giving it a unique integer key (less that 256)
   
```
import spasic.experiment.tt_um_test.loader
import spasic.experiment.tt_um_my_module.loader

ExperimentsAvailable = {
        # 1 sample experiment
        1: spasic.experiment.tt_um_test.loader.run_experiment,
        # ...
        
        # 22 my example test experiment
        22: spasic.experiment.tt_um_my_module.loader.some_loader_name,
    }
```

Now, since I gave it ID 22, I can launch it as we did above but with

```
runner.launch(22)

```

From here on in, you probably only need to tweak your test module, all the boiler plate should just work as is.  


When you're happy, make that PR!


    
### Passing arguments to experiments

The `launch()` method has an additional parameter: you can send some bytes into your loader function to set just how the experiment will run.  If you want to play with this, those bytes are in the `ExperimentParameters` object's `argument_bytes` attribute.

See the [factory test loader](https://github.com/psychogenic/spasics/blob/main/python/spasic/experiment/tt_um_factory_test/loader.py) for an example of how I'm doing that.



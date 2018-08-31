# BrainVision Parallel Port Latency Testing

This Python module is for testing the Brain Products "Trigger Box"

--> https://www.pressrelease.brainproducts.com/triggerbox2/

In particular, we want to check the latency of using a simple parallel port trigger
versus using triggers sent via the Trigger Box.

To check this, we will use a button box that can send triggers upon detecting a
button press (i.e., not passing the computer at all = almost no latency) as the
"ground truth". We will then detect the button presses on the button box with our
computer and immediately send a trigger either via

1. the classical parallel port or
2. the Trigger Box

Then we will calculate the difference between the "ground truth" trigger sent by
the button box and the trigger sent by either method 1. or 2. --- Finally, we will
compare the difference scores based on method 1. and 2.

If these scores are similar, we can safely use the Trigger Box from now on, and will
no longer have to take care to always buy legacy equipment that ships with a parallel port.

# Installation

First, see: http://psychopy.org/installation.html

and install an environment using conda:

```
conda create -n psypy3 python=3.5
conda activate psypy3
conda install numpy scipy matplotlib pandas pyopengl pillow lxml openpyxl xlrd configobj pyyaml gevent greenlet msgpack-python psutil pytables requests[security] cffi seaborn wxpython cython pyzmq pyserial
conda install -c conda-forge pyglet pysoundfile python-bidi moviepy pyosf
pip install zmq json-tricks pyparallel sounddevice pygame pysoundcard psychopy_ext psychopy
```

Finally, run `pip install -e .` from the project root.

# Tests

Run `pytest --verbose` from the project root.

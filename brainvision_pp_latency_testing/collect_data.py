"""Procedure to run and collect latency data.

# INSTRUCTIONS PARALLEL PORT
# http://stefanappelhoff.com/blog/2017/11/23/Triggers-with-Psychopy-on-BrainVision-Recorder
import time
from ctypes import windll

# Opening up the driver (first call is always slower)
assert windll.inpoutx64.IsInpOutDriverOpen()

windll.inpoutx64.Out32(0x378, 1)
time.sleep(0.5)
windll.inpoutx64.Out32(0x378, 0)


# INSTRUCTIONS TRIGGER BOX
# https://www.brainproducts.com/downloads.php?kid=40
import serial

# Open the Windows device manager,
# search for the "TriggerBox VirtualSerial Port (COM6)"
# in "Ports /COM & LPT)" and enter the COM port number in the constructor.
port = serial.Serial("COM6")

# Set the port to an initial state
port.write([0x00])

# Set Bit 0, Pin 2 of the Output(to Amp) connector
port.write([0x01])

# Reset Bit 0, Pin 2 of the Output(to Amp) connector
port.write([0x00])

# Reset the port to its default state
port.write([0xFF])

# Close the serial port
port.close()

"""
import os
import serial
from warnings import warn
if os.name == 'nt':
    send_triggers = True
    from ctypes import windll  # noqa F401
else:
    send_triggers = False
    warn('Not sending any triggers. Need Windows platform for that.')
from psychopy import visual, event, core  # noqa E402


# If we send triggers, warm up the driver
if send_triggers:
    assert windll.inpoutx64.IsInpOutDriverOpen()

# Make a psychopy window for the flow
# Using pyglet instead of pygame leads to an error with gammaRamp
# For proper timing, set fullscr to True
win = visual.Window(winType='pygame', fullscr=False)

# Determine minimum time that trigger has to be sent depending on EEG sampling
# frequency. Be generous ...
fs = 5000  # sampling frequency in Hz
trig_wait = (1 / fs) * 2

# Parallel port address
pp_adr = 0x378
marker_val = 1

# Serial port address
port = serial.Serial('COM1')
port.write([0])

# Assert we are running on the correct frame rate
fps = 120
print('Using fps: {}'.format(int(round(win.getActualFrameRate()))))
assert int(round(win.getActualFrameRate())) == fps

# Start the flow
run_loop = True
while run_loop:
    for frame in range(fps):
        keys = event.getKeys()

        # corresponds to button box key value
        if 'd' in keys:
            if send_triggers:

                # NOTE: Comment out one of the following
                # Using parallel port
                windll.inpoutx64.Out32(pp_adr, marker_val)
                core.wait(trig_wait)
                windll.inpoutx64.Out32(pp_adr, 0)

                # Using Brain Products TriggerBox
                # port.write(1)
                # core.wait(trig_wait)
                # port.write(0)

                print('TRIGGER')
            else:
                print('DUMMY TRIGGER')

        # We stop the procedure whenever we want
        elif 'escape' in keys:
            run_loop = False
            break

        # Flip the window to inquire new key presses that were done meanwhile
        win.flip()


# Clean up
print('\nBye.')
port.write([255])
port.close()
core.wait(1)
win.close()

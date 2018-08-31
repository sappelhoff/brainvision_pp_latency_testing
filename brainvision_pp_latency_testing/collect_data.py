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

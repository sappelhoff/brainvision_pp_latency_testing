"""Procedure to run and collect latency data."""
import time
from ctypes import windll

"""
# Method using a parallel port, see:
# http://stefanappelhoff.com/blog/2017/11/23/Triggers-with-Psychopy-on-BrainVision-Recorder
windll.inpoutx64.Out32(0x378, 1)
time.sleep(0.5)
windll.inpoutx64.Out32(0x378, 0)
"""

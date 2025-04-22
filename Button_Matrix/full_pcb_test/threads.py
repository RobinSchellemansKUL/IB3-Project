import RPi.GPIO as GPIO
import time
import pygame
import threading

from input_output import polling_bpm
from sequencer import play_sequencer

import variables

def thread_volume():
    if variables.thread_volume is None or not variables.thread_volume.is_alive():
        variables.thread_volume = threading.Thread(target=polling_bpm, daemon=True) #daemon close thread when variables program closes
        variables.thread_volume.start()

def thread_bpm():
    if variables.thread_bpm is None or not variables.thread_bpm.is_alive():
        variables.thread_bpm = threading.Thread(target=polling_bpm, daemon=True)
        variables.thread_bpm.start()

def thread_sequencer():
    if variables.thread_sequencer is None or not variables.thread_sequencer.is_alive():
        variables.thread_sequencer = threading.Thread(target=play_sequencer, daemon=True)
        variables.thread_sequencer.start()

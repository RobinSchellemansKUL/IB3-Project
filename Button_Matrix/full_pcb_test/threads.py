import RPi.GPIO as GPIO
import time
import pygame
import threading

from input_output import polling_bpm
from sequencer import play_sequencer

import main

def thread_volume():
    global thread_volume
    if thread_volume is None or not thread_volume.is_alive():
        rotary_thread = threading.Thread(target=9999999, daemon=True) #daemon close thread when main program closes
        rotary_thread.start()

def thread_bpm():
    if main.thread_bpm is None or not main.thread_bpm.is_alive():
        main.thread_bpm = threading.Thread(target=polling_bpm, daemon=True)
        main.thread_bpm.start()

def thread_sequencer():
    if main.thread_sequencer is None or not main.thread_sequencer.is_alive():
        main.thread_sequencer = threading.Thread(target=play_sequencer, daemon=True)
        main.thread_sequencer.start()

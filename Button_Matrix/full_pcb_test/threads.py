import RPi.GPIO as GPIO
import time
import pygame
import threading

import main
import input_output
import sequencer

def thread_volume():
    global thread_volume
    if thread_volume is None or not thread_volume.is_alive():
        rotary_thread = threading.Thread(target=9999999, daemon=True) #daemon close thread when main program closes
        rotary_thread.start()

def thread_bpm():
    if main.thread_bpm is None or not main.thread_bpm.is_alive():
        main.thread_bpm = threading.Thread(target=input_output.polling_bpm, daemon=True)
        main.thread_bpm.start()

def thread_button_matrix():
    global thread_button_matrix
    if thread_button_matrix is None or not thread_button_matrix.is_alive():
        rotary_thread = threading.Thread(target=input_output.polling_matrix, daemon=True)
        rotary_thread.start()

def thread_sequencer():
    if main.thread_sequencer is None or not main.thread_sequencer.is_alive():
        main.thread_sequencer = threading.Thread(target=sequencer.play_sequencer, daemon=True)
        thread_sequencer.start()

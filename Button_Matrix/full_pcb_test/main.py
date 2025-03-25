import RPi.GPIO as GPIO
import time
import pygame
import threading

import setup
import input_output

# Thread variables
play_thread = None
rotary_thread = None

thread_volume = None
thread_bpm = None
thread_button_matrix = None

sounds = []
sequence_1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
sequence_2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
sequence_3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
sequence_4 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

bpm = 120

modes = "default"
layers = 1

def main():
    # Setup
    global sounds
    sounds = setup.initiate()





main()
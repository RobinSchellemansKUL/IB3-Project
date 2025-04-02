import RPi.GPIO as GPIO
import time
import pygame

# Thread variables
thread_volume = None
thread_bpm = None
thread_button_matrix = None
thread_sequencer = None

# Sound sequences
# Sorted per layer.
# --> in every step, every sequence that is active
#sounds = []
last_selected_sound = 1
sequence_1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
sequence_2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
sequence_3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
sequence_4 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

bpm = 120

# Modes: default, write, layer
modes = "default"
# 0 not playing, 1 playing
playing = 0

# Four layers
# - layers --> in what layer we currently are (writing)
# - layers_active --> active layers are 1
layers = 1
layer_active = [0, 0, 0, 0]


# def main():
#     # Setup
#     global sounds
#     sounds = setup.initiate()
#
# main()
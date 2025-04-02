import time
import pygame

import main

sounds = []
def write_sounds(loaded_sounds):
    global sounds
    sounds = loaded_sounds

def play_sequencer():
    """function that plays sound according to BPM speed."""
    print("Sounds will be played")
    while main.playing:
        for i in range(0,15):
            for j in range(0,3):
                if main.layer_active[j] != 0:
                    if main.layer_active[j].sequence[i] != 0:
                        main.layer_active[j].sequence[i].play()
            time.sleep(60 / main.bpm)




import RPi.GPIO as GPIO
import pygame

import threads
import input_output
import sequencer

def initiate():
    # Initating mixer
    pygame.mixer.init(buffer=8192) # Increase buffer to avoid underrun errors

    # Loading sounds
    kick = pygame.mixer.Sound("/home/pi/sounds/kick1.wav")
    snare = pygame.mixer.Sound("/home/pi/sounds/snare1.wav")
    clap = pygame.mixer.Sound("/home/pi/sounds/clap1.wav")
    ride = pygame.mixer.Sound("/home/pi/sounds/ride1.wav")
    jazz = pygame.mixer.Sound("/home/pi/sounds/Jazz_Ride.wav")
    hihat = pygame.mixer.Sound("/home/pi/sounds/hihat1.wav")
    # More sounds...

    sounds = [kick, snare, clap, ride, jazz, hihat]

    # Startup sound
    jazz.play()
    print("Loaded all sounds")

    # Josse is brave, en zet de warnings af
    GPIO.setwarnings(False)
    # BCM numbering
    GPIO.setmode(GPIO.BCM)

    # Set Row pins as output
    GPIO.setup(7, GPIO.IN)
    GPIO.setup(8, GPIO.IN)
    GPIO.setup(12, GPIO.IN)
    GPIO.setup(15, GPIO.IN)
    GPIO.setup(16, GPIO.IN)

    # Set column pins as input and Pulled up high by default
    GPIO.setup(5, GPIO.OUT)
    GPIO.setup(6, GPIO.OUT)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)

    # Set CLK and DT for bpm
    GPIO.setup(11, GPIO.IN)
    GPIO.setup(10, GPIO.IN)

    # Set CLK and DT for volume
    GPIO.setup(26, GPIO.OUT)
    GPIO.setup(9, GPIO.OUT)

    print("GPIO pins activated")

    # Start threads
    threads.thread_volume()
    threads.thread_bpm()
    threads.thread_button_matrix()

    print("Threads activated")

    print("Setup done")
    return sounds

def main():
    sounds = initiate()
    input_output.write_sounds(sounds)
    sequencer.write_sounds(sounds)

main()
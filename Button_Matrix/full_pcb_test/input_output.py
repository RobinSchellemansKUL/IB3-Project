import RPi.GPIO as GPIO
import time
import pygame
import threading

######################
# Rotary decoder BPM #
######################

def polling_bpm():
    global bpm
    CLK = 11
    DT = 10

    prev_clk_state = GPIO.input(CLK)

    while True:
        clk_state = GPIO.input(CLK)
        dt_state = GPIO.input(DT)

        if clk_state != prev_clk_state:  # detect change
            if dt_state != clk_state:
                bpm += 5  # Turn clockwise increases BPM
            else:
                bpm -= 5  # turn counterclockwise lower BPM

            bpm = max(30, min(bpm, 300))  # Limiteer BPM tussen 30 en 300
            print(f"BPM: {bpm}")

        prev_clk_state = clk_state  # keep track of current clk state
        time.sleep(0.001)  #adjust delay to test out 0.01 (10ms) gives to much delay and wrong values

#################
# Button Matrix #
#################

def polling_matrix():
    while True:
        readRow(5)
        readRow(6)
        readRow(17)
        readRow(13)

def readRow(column):
    global modes

    row_1 = 7
    row_2 = 8
    row_3 = 12
    row_4 = 15
    row_5 = 16

    GPIO.output(column, GPIO.HIGH)

    if GPIO.input(row_1) == GPIO.HIGH and column == 5:
        print("Switch 1")
        button_action(1)

    if GPIO.input(row_1) == GPIO.HIGH and column == 6:
        print("Switch 2")
        button_action(2)

    if GPIO.input(row_1) == GPIO.HIGH and column == 17:
        print("Switch 3")
        button_action(3)

    if GPIO.input(row_1) == GPIO.HIGH and column == 13:
        print("Switch 4")
        button_action(4)

    if GPIO.input(row_2) == GPIO.HIGH and column == 5:
        print("Switch 5")
        button_action(5)

    if GPIO.input(row_2) == GPIO.HIGH and column == 6:
        print("Switch 6")
        button_action(6)

    if GPIO.input(row_2) == GPIO.HIGH and column == 17:
        print("Switch 7")
        button_action(7)

    if GPIO.input(row_2) == GPIO.HIGH and column == 13:
        print("Switch 8")
        button_action(8)

    if GPIO.input(row_3) == GPIO.HIGH and column == 5:
        print("Switch 9")
        button_action(9)

    if GPIO.input(row_3) == GPIO.HIGH and column == 6:
        print("Switch 10")
        button_action(10)

    if GPIO.input(row_3) == GPIO.HIGH and column == 17:
        print("Switch 11")
        button_action(11)

    if GPIO.input(row_3) == GPIO.HIGH and column == 13:
        print("Switch 12")
        button_action(12)

    if GPIO.input(row_4) == GPIO.HIGH and column == 5:
        print("Switch 13")
        button_action(13)

    if GPIO.input(row_4) == GPIO.HIGH and column == 6:
        print("Switch 14")
        button_action(14)

    if GPIO.input(row_4) == GPIO.HIGH and column == 17:
        print("Switch 15")
        button_action(15)

    if GPIO.input(row_4) == GPIO.HIGH and column == 13:
        print("Switch 16")
        button_action(16)

    if GPIO.input(row_5) == GPIO.HIGH and column == 5:
        print("Switch 17")
        # play => start sequencer

    if GPIO.input(row_5) == GPIO.HIGH and column == 6:
        print("Switch 18")
        # write
        if modes == "write":
            modes = "default"
        else:
            modes = "write"

    if GPIO.input(row_5) == GPIO.HIGH and column == 17:
        print("Switch 19")
        # layer
        if modes == "layer":
            modes = "default"
        else:
            modes = "layer"

    if GPIO.input(row_5) == GPIO.HIGH and column == 13:
        print("Switch 20")
        # no action

def button_action(switch):
    global modes
    global layers
    global sounds
    match modes:
        case "write":
            match layers:
                case 1:
                    sequence_1[i] = last_selected_sound
                case 2:
                    sequence_2[i] = last_selected_sound
                case 3:
                    sequence_3[i] = last_selected_sound
                case 4:
                    sequence_4[i] = last_selected_sound
        case "layer":
            if switch > 0 and switch <= 4:
                layers = switch
        case _:
            sounds[switch].play()

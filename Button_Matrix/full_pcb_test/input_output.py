import RPi.GPIO as GPIO
import time
import pygame
import threading


from variables import modes, layers, layer_active, sequence_1, sequence_2, sequence_3, sequence_4
import variables

sounds = []
def write_sounds(loaded_sounds):
    global sounds
    sounds = loaded_sounds

######################
# Rotary decoder BPM #
######################

def polling_bpm():
    CLK = 11
    DT = 10

    prev_clk_state = GPIO.input(CLK)

    while True:
        clk_state = GPIO.input(CLK)
        dt_state = GPIO.input(DT)

        if clk_state != prev_clk_state:  # detect change
            if dt_state != clk_state:
                main.bpm += 5  # Turn clockwise increases BPM
            else:
                main.bpm -= 5  # turn counterclockwise lower BPM

            main.bpm = max(30, min(main.bpm, 300))  # Limiteer BPM tussen 30 en 300
            print(f"BPM: {main.bpm}")

        prev_clk_state = clk_state  # keep track of current clk state
        time.sleep(0.001)  #adjust delay to test out 0.01 (10ms) gives to much delay and wrong values

#################
# Button Matrix #
#################

def readRow(row):
    waiting = 0.2
    row_1 = 7
    row_2 = 8
    row_3 = 12
    row_4 = 15
    row_5 = 16

    GPIO.output(row, GPIO.HIGH)

    if GPIO.input(row_1) == GPIO.HIGH and row == 5:
        print("Switch 1")
        button_action(1)
        time.sleep(waiting)

    elif GPIO.input(row_1) == GPIO.HIGH and row == 6:
        print("Switch 2")
        button_action(2)

    elif GPIO.input(row_1) == GPIO.HIGH and row == 17:
        print("Switch 3")
        button_action(3)

    elif GPIO.input(row_1) == GPIO.HIGH and row == 13:
        print("Switch 4")
        button_action(4)

    elif GPIO.input(row_2) == GPIO.HIGH and row == 5:
        print("Switch 5")
        button_action(5)

    elif GPIO.input(row_2) == GPIO.HIGH and row == 6:
        print("Switch 6")
        button_action(6)

    elif GPIO.input(row_2) == GPIO.HIGH and row == 17:
        print("Switch 7")
        button_action(7)

    elif GPIO.input(row_2) == GPIO.HIGH and row == 13:
        print("Switch 8")
        button_action(8)

    elif GPIO.input(row_3) == GPIO.HIGH and row == 5:
        print("Switch 9")
        button_action(9)

    elif GPIO.input(row_3) == GPIO.HIGH and row == 6:
        print("Switch 10")
        button_action(10)

    elif GPIO.input(row_3) == GPIO.HIGH and row == 17:
        print("Switch 11")
        button_action(11)

    elif GPIO.input(row_3) == GPIO.HIGH and row == 13:
        print("Switch 12")
        button_action(12)

    elif GPIO.input(row_4) == GPIO.HIGH and row == 5:
        print("Switch 13")
        button_action(13)
        time.sleep(waiting)

    elif GPIO.input(row_4) == GPIO.HIGH and row == 6:
        print("Switch 14")
        button_action(14)
        time.sleep(waiting)

    elif GPIO.input(row_4) == GPIO.HIGH and row == 17:
        print("Switch 15")
        button_action(15)
        time.sleep(waiting)

    elif GPIO.input(row_4) == GPIO.HIGH and row == 13:
        print("Switch 16")
        button_action(16)
        time.sleep(waiting)

    elif GPIO.input(row_5) == GPIO.HIGH and row == 5:
        print("Switch 17")
        if main.playing == 0:
            main.playing = 1
        else:
            main.playing = 0
        time.sleep(waiting)

    elif GPIO.input(row_5) == GPIO.HIGH and row == 6:
        print("Switch 18")
        # write
        if main.modes == "write":
            main.modes = "default"
        else:
            main.modes = "write"
        time.sleep(waiting)

    elif GPIO.input(row_5) == GPIO.HIGH and row == 17:
        print("Switch 19")
        # layer
        if main.modes == "layer":
            main.modes = "default"
        else:
            main.modes = "layer"
        time.sleep(waiting)

    elif GPIO.input(row_5) == GPIO.HIGH and row == 13:
        print("Switch 20")
        # no action
        time.sleep(waiting)

    GPIO.output(row, GPIO.LOW)

def button_action(switch):
    global sounds
    match modes:
        case "write":
            match layers:
                case 1:
                    sequence_1[switch] = main.last_selected_sound
                case 2:
                    sequence_2[switch] = main.last_selected_sound
                case 3:
                    sequence_3[switch] = main.last_selected_sound
                case 4:
                    sequence_4[switch] = main.last_selected_sound
        case "layer":
            if 0 < switch <= 4:
                main.layers = switch
                if layer_active[switch] == 0:
                    match switch:
                        case 1:
                            layer_active[switch] = sequence_1
                        case 2:
                            layer_active[switch] = sequence_2
                        case 3:
                            layer_active[switch] = sequence_3
                        case 4:
                            layer_active[switch] = sequence_4
                else:
                    layer_active[switch] = 0
        case _:
            print(switch)
            #print(sounds)
            #sounds[switch-1].play()
            #main.last_selected_sound = switch

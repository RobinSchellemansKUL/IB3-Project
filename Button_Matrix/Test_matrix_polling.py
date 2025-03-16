import RPi.GPIO as GPIO
import time
import pygame
import threading

# Initating mixer
pygame.mixer.init(buffer=8192) #increase buffer to avoid underrun errors

#loading sounds
kick = pygame.mixer.Sound("/home/pi/sounds/kick1.wav")
snare = pygame.mixer.Sound("/home/pi/sounds/snare1.wav")
clap = pygame.mixer.Sound("/home/pi/sounds/clap1.wav")
ride = pygame.mixer.Sound("/home/pi/sounds/ride1.wav")
jazz = pygame.mixer.Sound("/home/pi/sounds/Jazz_Ride.wav")
hihat = pygame.mixer.Sound("/home/pi/sounds/hihat1.wav")

# Startup sound
jazz.play()

#################
#setup variables#
#################
# Set the Row Pins
ROW_1 = 7
ROW_2 = 8

# Set the Column Pins
COL_1 = 5
COL_2 = 6

GPIO.setwarnings(False)
# BCM numbering
GPIO.setmode(GPIO.BCM)

# Set Row pins as output
GPIO.setup(ROW_1, GPIO.OUT)
GPIO.setup(ROW_2, GPIO.OUT)

# Set column pins as input and Pulled up high by default
GPIO.setup(COL_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(COL_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#thread variables
play_thread = None
rotary_thread = None

#flags & main program variables
playing = False
sounds_list = []
modes = ["default","add_sound_to_list","play_mode"]
current_mode_i = 0
bpm = 120 #random start value

#####################
#end setup variables#
#####################

#after setup show current mode in terminal.
print(f"we are in {modes[current_mode_i]}")

#################################
#functions for drummachine logic#
#################################
def change_mode():
    global current_mode_i, playing
    current_mode_i = (current_mode_i + 1) % len(modes) #% makes sure when end of list is reached that you go back to beginning
    print(f"Change mode to: {modes[current_mode_i]}")

    if modes[current_mode_i] == "play_mode":
        playing = True
        start_thread_play_sounds(play_sounds)
    else:
        playing = False

def start_thread_play_sounds(target):
    global play_thread
    if play_thread is None or not play_thread.is_alive():
        play_thread = threading.Thread(target=target, daemon=True) #daemon sluit thread af wanneer hoofd programma sluit
        play_thread.start()

def play_sounds():
    """function that plays sound according to BPM speed."""
    print("sounds will be played")
    global playing
    while playing:
        if sounds_list:  # only play when there are sounds in the list
            for sound in sounds_list:
                sound.play()
                time.sleep(60 / bpm)  # Timing based on BPM
        else:
            print("No sounds in list")
            time.sleep(1)

###############################
##start reading buttons logic##
###############################
# function to read each row and each column
def readRow(line):
    GPIO.output(line, GPIO.LOW)
    if GPIO.input(COL_1) == GPIO.LOW and line == ROW_1:
        match modes[current_mode_i]:
            case "default": #default behavior just plays a sound
                #Button columnm 1 and row 1 is pressed
                kick.play()
                print(f"rij 1 kolom 1 is ingedrukt gpio {line}")
                time.sleep(0.2)
            case "add_sound_to_list":
                print(f"we are in{modes[current_mode_i]}")
                kick.play()
                sounds_list.append(kick)
                print("kick sound successfully added to list")
                time.sleep(0.2)

    if GPIO.input(COL_1) == GPIO.LOW and line == ROW_2:
        match modes[current_mode_i]:
            case "default":
                clap.play()
                print(f"rij 2 kolom 1 is ingedrukt gpio {line}")
                time.sleep(0.2)
            case "add_sound_to_list":
                print(f"we are in{modes[current_mode_i]}")
                clap.play()
                sounds_list.append(clap)
                print("clap sound successfully added to list")
                time.sleep(0.2)

    if GPIO.input(COL_2) == GPIO.LOW and line == ROW_1:
        match modes[current_mode_i]:
            case "default":
                ride.play()
                print(f"rij 1 kolom 2 is ingedrukt gpio {line}")
                time.sleep(0.2)
            case "add_sound_to_list":
                print(f"we are in{modes[current_mode_i]}")
                ride.play()
                sounds_list.append(ride)
                print("clap sound successfully added to list")
                time.sleep(0.2)

    if GPIO.input(COL_2) == GPIO.LOW and line == ROW_2:
        print(f"rij 2 kolom 2 is ingedrukt gpio {line}")
        change_mode()
        time.sleep(0.2)
    GPIO.output(line, GPIO.HIGH)



##############################
##rotary encoder 1 BPM speed##
##############################

# Pins setup
CLK = 11  #
DT = 10   #

GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)


#interupt method doesnt work (failed to add edge detection error) already installed rpi-lgpio and ran with sudo
'''
def rotary_callback(channel):
    print("rotary encoder callback works")
    global bpm
    clk_state = GPIO.input(CLK)
    dt_state = GPIO.input(DT)

    if dt_state != clk_state:
        bpm += 1  # turn clockwise increases BPM
    else:
        bpm -= 1  # turn counterclockwise lowers BPM

    bpm = max(30, min(bpm, 400))  # limit BPM between 30 and between(current_bmp and 300)
    print(f"BPM: {bpm}")
'''

##add and interrupt listener before the endless loop for the rotary encoder
#GPIO.add_event_detect(CLK, GPIO.FALLING, callback=rotary_callback, bouncetime=50)

########################################################
#Rotary encoder with polling method (use another thread)
########################################################

def polling_method_rotary_encoder():
    global bpm
    prev_clk_state = GPIO.input(CLK)

    while True:
        clk_state = GPIO.input(CLK)
        dt_state = GPIO.input(DT)

        if clk_state != prev_clk_state:  # detect change
            if dt_state != clk_state:
                bpm += 1  # Turn clockwise increases BPM
            else:
                bpm -= 1  # turn counterclockwise lower BPM

            bpm = max(30, min(bpm, 300))  # Limiteer BPM tussen 30 en 300
            print(f"BPM: {bpm}")

        prev_clk_state = clk_state  # keep track of current clk state
        time.sleep(0.001)  #adjust delay to test out 0.01 (10ms) gives to much delay and wrong values

def start_thread_rotary():
    global rotary_thread
    if rotary_thread is None or not rotary_thread.is_alive():
        rotary_thread = threading.Thread(target=polling_method_rotary_encoder, daemon=True) #daemon close thread when main program closes
        rotary_thread.start()

####################################
#endless loop to check button matrix#
####################################

# Endless loop for checking rows
def main():
    start_thread_rotary()
    try:
        while True:
            readRow(ROW_1) #gpio7
            readRow(ROW_2) #gpio8
            #time.sleep(0.2) putting sleep time on every button individually causes less delay
    except KeyboardInterrupt:
        print("\nProgramma gestopt")
        GPIO.cleanup() #set pins back to input pins

main()







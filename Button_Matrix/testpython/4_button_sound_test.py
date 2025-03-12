import RPi.GPIO as GPIO
import time
import pygame

# Initating mixer
pygame.mixer.init()
kick = pygame.mixer.Sound("/home/pi/sounds/kick1.wav")
snare = pygame.mixer.Sound("/home/pi/sounds/snare1.wav")
clap = pygame.mixer.Sound("/home/pi/sounds/clap1.wav")
ride = pygame.mixer.Sound("/home/pi/sounds/ride1.wav")
jazz = pygame.mixer.Sound("/home/pi/sounds/Jazz_Ride.wav")
hihat = pygame.mixer.Sound("/home/pi/sounds/hihat1.wav")
# Startup test
jazz.play()

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

# function to read each row and each column
def readRow(line):
    GPIO.output(line, GPIO.LOW)
    if(GPIO.input(COL_1) == GPIO.LOW):
        kick.play()
        print(f"rij gpio {line} kolom 1 is ingedrukt")
    if(GPIO.input(COL_2) == GPIO.LOW):
        clap.play()
        print(f"rij gpio {line} kolom 2 is ingedrukt")
    GPIO.output(line, GPIO.HIGH)

# Endless loop by checking each row
try:
    while True:
        readRow(ROW_1) #gpio7
        readRow(ROW_2) #gpio8
        time.sleep(0.15) # adjust this per your own setup
except KeyboardInterrupt:
    print("\nProgramma gestopt")
    GPIO.cleanup() #set pins back to input pins
import RPi.GPIO as GPIO
import time

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
        print(f"rij gpio {line} kolom 1 is ingedrukt")
    if(GPIO.input(COL_2) == GPIO.LOW):
        print(f"rij gpio {line} kolom 2 is ingedrukt")
    GPIO.output(line, GPIO.HIGH)

# Endless loop by checking each row
try:
    while True:
        readRow(ROW_1) #gpio7
        readRow(ROW_2) #gpio8
        time.sleep(0.05) # adjust this per your own setup
except KeyboardInterrupt:
    print("\nProgramma gestopt")
    GPIO.cleanup() #set pins back to input pins
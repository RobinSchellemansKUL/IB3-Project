import RPi.GPIO as GPIO
import time
import pygame

# Init Pygame mixer
pygame.mixer.init(buffer=8192)  # increase buffer to avoid underrun errors
kick = pygame.mixer.Sound("/home/pi/sounds/kick1.wav")
snare = pygame.mixer.Sound("/home/pi/sounds/snare1.wav")
clap = pygame.mixer.Sound("/home/pi/sounds/clap1.wav")
ride = pygame.mixer.Sound("/home/pi/sounds/ride1.wav")
jazz = pygame.mixer.Sound("/home/pi/sounds/Jazz_Ride.wav")
hihat = pygame.mixer.Sound("/home/pi/sounds/hihat1.wav")

# Startup test
jazz.play()

# GPIO setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Define rows (outputs)
ROW_1 = 7
ROW_2 = 8

# Define columns (inputs with pull-ups)
COL_1 = 5
COL_2 = 6

GPIO.setup(ROW_1, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(ROW_2, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(COL_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(COL_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Store the state of previous columns to detect changes
prev_state = {COL_1: GPIO.HIGH, COL_2: GPIO.HIGH}

# Flag for when an interrupt occurs
interrupt_flag = False

# Matrix scanning function
def check_matrix():
    for row in [ROW_1, ROW_2]:
        GPIO.output(row, GPIO.LOW)  # Activate this row by setting it LOW

        # Check column states for each row
        if GPIO.input(COL_1) == GPIO.LOW and prev_state[COL_1] == GPIO.HIGH:
            kick.play()
            print("Rij 1 Kolom 1: Kick!")
            prev_state[COL_1] = GPIO.LOW  # Update state
        elif GPIO.input(COL_1) == GPIO.HIGH and prev_state[COL_1] == GPIO.LOW:
            prev_state[COL_1] = GPIO.HIGH  # Update state to released

        if GPIO.input(COL_2) == GPIO.LOW and prev_state[COL_2] == GPIO.HIGH:
            ride.play()
            print("Rij 1 Kolom 2: Ride!")
            prev_state[COL_2] = GPIO.LOW  # Update state
        elif GPIO.input(COL_2) == GPIO.HIGH and prev_state[COL_2] == GPIO.LOW:
            prev_state[COL_2] = GPIO.HIGH  # Update state to released

        GPIO.output(row, GPIO.HIGH)  # Deactivate this row by setting it HIGH

# Interrupt callback function
def column_interrupt_callback(channel):
    global interrupt_flag
    interrupt_flag = True  # Set the flag when interrupt occurs

# Set up event detection for columns (Interrupt)
GPIO.add_event_detect(COL_1, GPIO.FALLING, callback=column_interrupt_callback, bouncetime=200)
GPIO.add_event_detect(COL_2, GPIO.FALLING, callback=column_interrupt_callback, bouncetime=200)

# Main program that continuously checks the matrix
try:
    print("Wachten op input... (CTRL+C om te stoppen)")
    while True:
        if interrupt_flag:
            check_matrix()  # Scan the matrix to identify which button was pressed
            interrupt_flag = False  # Reset flag after scanning
        time.sleep(0.01)  # Small delay to reduce CPU usage
except KeyboardInterrupt:
    print("\nProgramma gestopt")
    GPIO.cleanup()

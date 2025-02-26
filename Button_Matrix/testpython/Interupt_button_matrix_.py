import RPi.GPIO as GPIO
from pad4pi import rpi_gpio
import time

KEYPAD = [
    [1, 2],
    [4, 5]
]

ROW_PINS = [7, 8] # BCM numbering
COL_PINS = [5, 6] # BCM numbering

def print_key(key):
    print(f"Received key from interrupt:: {key}")

try:
    factory = rpi_gpio.KeypadFactory()
    keypad = factory.create_keypad(keypad=KEYPAD,row_pins=ROW_PINS, col_pins=COL_PINS) # makes assumptions about keypad layout and GPIO pin numbers

    keypad.registerKeyPressHandler(print_key)

    print("Press buttons on your keypad. Ctrl+C to exit.")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Goodbye")
finally:
    keypad.cleanup()
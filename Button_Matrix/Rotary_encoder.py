import RPi.GPIO as GPIO
import time

# Pins setup
CLK = 11
DT = 10
bpm = 120
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

##manual test just reading the pins
"""
try:
    while True:
        clk_state = GPIO.input(CLK)
        dt_state = GPIO.input(DT)
        print(f"CLK: {clk_state}, DT: {dt_state}")
        time.sleep(0.1)  # kleine vertraging om te voorkomen dat de console te snel volloopt
except KeyboardInterrupt:
    GPIO.cleanup()
"""


last_clk_state = GPIO.input(CLK)

while True:
    clk_state = GPIO.input(CLK)
    dt_state = GPIO.input(DT)

    if clk_state != last_clk_state:  # Detect change
        if dt_state != clk_state: #if DT pin is not equal to clk
            bpm += 1
        else:
            bpm -= 1

        bpm = max(30, min(bpm, 300))
        print(f"CLK: {clk_state}, DT: {dt_state}")  # Debugging
        print(f"BPM: {bpm}")
    last_clk_state = clk_state
    time.sleep(0.01)  # 10ms delay om CPU-belasting te beperken

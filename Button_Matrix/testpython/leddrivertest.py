import RPi.GPIO as GPIO
import time

CLK_PIN = 14
LATCH_PIN = 27
BLANK_PIN = 22
SI_PIN = 24
delay = 1/10
# Josse is brave, en zet de warnings af
GPIO.setwarnings(False)
# BCM numbering
GPIO.setmode(GPIO.BCM)

# Set CLK, SIN, LAT and blank for led driver
GPIO.setup(CLK_PIN, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(LATCH_PIN, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)



try:
    print("start")
    GPIO.output(22, GPIO.LOW)
    GPIO.output(24, GPIO.HIGH)
    GPIO.output(LATCH_PIN, GPIO.LOW) #LATCH
    GPIO.output(22, GPIO.LOW)
    for i in range(0,8):
        GPIO.output(CLK_PIN, GPIO.HIGH)
        time.sleep(1/30000000)
        GPIO.output(CLK_PIN, GPIO.LOW)
        time.sleep(1/30000000)
    GPIO.output(24, GPIO.LOW)
    for i in range(0,8):
        GPIO.output(CLK_PIN, GPIO.HIGH)
        time.sleep(1/30000000)
        GPIO.output(CLK_PIN, GPIO.LOW)
        time.sleep(1/30000000)
    GPIO.output(CLK_PIN, GPIO.LOW)
    GPIO.output(LATCH_PIN, GPIO.HIGH)
    time.sleep(1/30000000)
    GPIO.output(LATCH_PIN, GPIO.LOW)
    print("klaar!")
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.output(24, GPIO.LOW)
    GPIO.output(27, GPIO.LOW)
    GPIO.output(CLK_PIN, GPIO.LOW)
    print("\n program closed.")
    GPIO.cleanup()




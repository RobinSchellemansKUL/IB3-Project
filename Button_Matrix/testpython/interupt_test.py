import RPi.GPIO as GPIO
import time

##test script om te kijken of interupts werken met de button matrix

def event_callback(pin):
    value = GPIO.input(pin)
    print(f"pin :: {pin}, value is {value}")

if __name__ == '__main__':
    button_pin = 6
    row_pin = 8

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(row_pin, GPIO.OUT)
    GPIO.setup(button_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

    GPIO.output(row_pin, GPIO.HIGH)

    # GPIO.RISING, GPIO.FALLING, or GPIO.BOTH
    GPIO.add_event_detect(button_pin, GPIO.BOTH,
                          callback=event_callback,
                          bouncetime=50)

    try:
        time.sleep(1000000) # let program run for a while
    except KeyboardInterrupt:
        GPIO.cleanup()
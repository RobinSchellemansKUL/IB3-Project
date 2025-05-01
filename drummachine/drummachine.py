import RPi.GPIO as GPIO
import pygame

class DrumMachine:
    _instance = None
    _sounds = None

    _input_output = None
    _playing = None
    _channel_groups = None
    _next_channel_index = []

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # Initating mixer
        pygame.mixer.pre_init(buffer=2**10) # Increase buffer to avoid underrun errors 2**10= 1024
        pygame.init()
        # Loading sounds
        kick = pygame.mixer.Sound("/home/pi/sounds/kick1.wav")
        snare = pygame.mixer.Sound("/home/pi/sounds/snare1.wav")
        clap = pygame.mixer.Sound("/home/pi/sounds/clap1.wav")
        ride = pygame.mixer.Sound("/home/pi/sounds/ride1.wav")
        jazz = pygame.mixer.Sound("/home/pi/sounds/Jazz_Ride.wav")
        hihat = pygame.mixer.Sound("/home/pi/sounds/hihat1.wav")
        # More sounds...

        self._sounds = [kick, snare, clap, ride, jazz, hihat]

        pygame.mixer.set_num_channels(len(self._sounds) * 3)

        # for every sound make a channel group (3 channels per sound)
        self._channel_groups = [
            [pygame.mixer.Channel(i * 3 + j) for j in range(3)] for i in range(len(self._sounds)) #channel_groups is an array that contains 3 channels for every sound (i).
        ]

        #create an array full of 0 to keep track of the available channel for each sound (in the beginning available channel is channel 0)
        for i in range(len(self._sounds)):
            self._next_channel_index.append(0)
        print("Loaded all sounds")

        # Josse is brave, en zet de warnings af
        GPIO.setwarnings(False)
        # BCM numbering
        GPIO.setmode(GPIO.BCM)

        # Set Row pins as output
        GPIO.setup(7, GPIO.IN)
        GPIO.setup(8, GPIO.IN)
        GPIO.setup(12, GPIO.IN)
        GPIO.setup(15, GPIO.IN)
        GPIO.setup(16, GPIO.IN)

        # Set column pins as input and Pulled up high by default
        GPIO.setup(5, GPIO.OUT)
        GPIO.setup(6, GPIO.OUT)
        GPIO.setup(17, GPIO.OUT)
        GPIO.setup(13, GPIO.OUT)

        # Set CLK and DT for volume
        GPIO.setup(11, GPIO.IN)
        GPIO.setup(10, GPIO.IN)

        # Set CLK and DT for BPM
        GPIO.setup(26, GPIO.IN)
        GPIO.setup(9, GPIO.IN)

        print("GPIO pins activated")

        # Setting up variables
        self._playing = 0

        print("Variables initialized")

        # Start threads
        # threads.thread_volume()
        # threads.thread_bpm()
        # print("Threads activated")
        # print("Setup done")

        # Startup sound
        jazz.play()

    def run_drummachine(self):
        try:
            while True:
                self._input_output.readRow(5)
                self._input_output.readRow(6)
                self._input_output.readRow(17)
                self._input_output.readRow(13)
        except KeyboardInterrupt:
            #stop threads
            self._input_output.stop_thread_bpm()
            print("\n program closed.")
            GPIO.cleanup()

    #Getters and setters
    @property
    def sounds(self):
        return self._sounds

    @property
    def playing(self):
        return self._playing

    @playing.setter
    def playing(self, value):
        self._playing = value

    @property
    def input_output(self):
        return self._input_output

    @input_output.setter
    def input_output(self, value):
        self._input_output = value

    @property
    def channel_groups(self):
        return self._channel_groups
    @channel_groups.setter
    def channel_groups(self, value):
        self._channel_groups = value

    @property
    def next_channel_index(self):
        return self._next_channel_index
    @next_channel_index.setter
    def next_channel_index(self, value):
        self._next_channel_index = value
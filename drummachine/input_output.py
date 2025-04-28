import RPi.GPIO as GPIO
import time
import pygame
import threading


class Input_Output:
    _instance = None
    _drummachine = None
    _sequencer = None

    _last_selected_sound = None

    _layer = None
    _mode = None

    thread_volume = None
    thread_bpm = None
    thread_button_matrix = None

    def __new__(cls, drummachine, sequencer):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, drummachine, sequencer):
        self._drummachine = drummachine
        self._sequencer = sequencer

        self._layer = 1
        self._mode = "default"

        self.start_thread_bpm()

    def readRow(self, row):
        waiting = 0.2
        row_1 = 7
        row_2 = 8
        row_3 = 12
        row_4 = 15
        row_5 = 16

        GPIO.output(row, GPIO.HIGH)

        if GPIO.input(row_1) == GPIO.HIGH and row == 5:
            print("Switch 1")
            self.button_action(1)
            time.sleep(waiting)

        elif GPIO.input(row_1) == GPIO.HIGH and row == 6:
            print("Switch 2")
            self.button_action(2)
            time.sleep(waiting)

        elif GPIO.input(row_1) == GPIO.HIGH and row == 17:
            print("Switch 3")
            self.button_action(3)
            time.sleep(waiting)

        elif GPIO.input(row_1) == GPIO.HIGH and row == 13:
            print("Switch 4")
            self.button_action(4)
            time.sleep(waiting)

        elif GPIO.input(row_2) == GPIO.HIGH and row == 5:
            print("Switch 5")
            self.button_action(5)
            time.sleep(waiting)

        elif GPIO.input(row_2) == GPIO.HIGH and row == 6:
            print("Switch 6")
            self.button_action(6)
            time.sleep(waiting)

        elif GPIO.input(row_2) == GPIO.HIGH and row == 17:
            print("Switch 7")
            self.button_action(7)
            time.sleep(waiting)

        elif GPIO.input(row_2) == GPIO.HIGH and row == 13:
            print("Switch 8")
            self.button_action(8)
            time.sleep(waiting)

        elif GPIO.input(row_3) == GPIO.HIGH and row == 5:
            print("Switch 9")
            self.button_action(9)
            time.sleep(waiting)

        elif GPIO.input(row_3) == GPIO.HIGH and row == 6:
            print("Switch 10")
            self.button_action(10)
            time.sleep(waiting)

        elif GPIO.input(row_3) == GPIO.HIGH and row == 17:
            print("Switch 11")
            self.button_action(11)
            time.sleep(waiting)

        elif GPIO.input(row_3) == GPIO.HIGH and row == 13:
            print("Switch 12")
            self.button_action(12)
            time.sleep(waiting)

        elif GPIO.input(row_4) == GPIO.HIGH and row == 5:
            print("Switch 13")
            self.button_action(13)
            time.sleep(waiting)

        elif GPIO.input(row_4) == GPIO.HIGH and row == 6:
            print("Switch 14")
            self.button_action(14)
            time.sleep(waiting)

        elif GPIO.input(row_4) == GPIO.HIGH and row == 17:
            print("Switch 15")
            self.button_action(15)
            time.sleep(waiting)

        elif GPIO.input(row_4) == GPIO.HIGH and row == 13:
            print("Switch 16")
            self.button_action(16)
            time.sleep(waiting)

        elif GPIO.input(row_5) == GPIO.HIGH and row == 5:
            print("Switch 17")
            if self._drummachine.playing == 0:
                self._drummachine.playing = 1
            else:
                self._drummachine.playing = 0
            print("debug")
            print(self._drummachine.playing)
            self._sequencer.start_thread_sequencer()
            time.sleep(waiting)

        elif GPIO.input(row_5) == GPIO.HIGH and row == 6:
            print("Switch 18")
            # write
            if self._mode == "write":
                self._mode = "default"
            else:
                self._mode = "write"
            time.sleep(waiting)

        elif GPIO.input(row_5) == GPIO.HIGH and row == 17:
            print("Switch 19")
            # layer
            if self._mode == "layer":
                self._mode = "default"
            else:
                self._mode = "layer"
            time.sleep(waiting)

        elif GPIO.input(row_5) == GPIO.HIGH and row == 13:
            print("Switch 20")
            # no action
            time.sleep(waiting)

        GPIO.output(row, GPIO.LOW)

    def button_action(self, switch):
        global sounds
        match self._mode:
            case "write":
                match self._layer:
                    case 1:
                        self._sequencer.sequence_1[switch] = self._last_selected_sound
                    case 2:
                        self._sequencer.sequence_2[switch] = self._last_selected_sound
                    case 3:
                        self._sequencer.sequence_3[switch] = self._last_selected_sound
                    case 4:
                        self._sequencer.sequence_4[switch] = self._last_selected_sound
            case "layer":
                if 0 < switch <= 4:
                    self._layer = switch
                    if self._drummachine.layers_active[switch] == 0:
                        match switch:
                            case 1:
                                self._sequencer.layers_active[switch] = self._drummachine.sequence_1
                            case 2:
                                self._sequencer.layers_active[switch] = self._drummachine.sequence_2
                            case 3:
                                self._sequencer.layers_active[switch] = self._drummachine.sequence_3
                            case 4:
                                self._sequencer.layers_active[switch] = self._drummachine.sequence_4
                    else:
                        self._sequencer.layers_active[switch] = 0
            case _:
                self._drummachine.sounds[switch-1].play()
                self._last_selected_sound = switch


    def start_thread_bpm(self):
        if self.thread_bpm is None or not self.thread_bpm.is_alive():
            self.thread_bpm = threading.Thread(target=self.polling_bpm, daemon=True) #daemon close thread when self program closes
            self.thread_bpm.start()

    def polling_bpm(self):
        CLK = 11
        DT = 10

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        prev_clk_state = GPIO.input(CLK)

        while True:
            clk_state = GPIO.input(CLK)
            dt_state = GPIO.input(DT)

            if clk_state != prev_clk_state:  # detect change
                if dt_state != clk_state:
                    self._sequencer.bpm += 5  # Turn clockwise increases BPM
                else:
                    self._sequencer.bpm -= 5  # turn counterclockwise lower BPM

                self._sequencer.bpm = max(30, min(self._sequencer.bpm, 300))  # Limiteer BPM tussen 30 en 300
                print(f"BPM: {self._sequencer.bpm}")

            prev_clk_state = clk_state  # keep track of current clk state
            time.sleep(0.001)  #adjust delay to test out 0.01 (10ms) gives to much delay and wrong values

    #Getters and Setters
    @property
    def drummachine(self):
        return self._drummachine

    @drummachine.setter
    def drummachine(self, value):
        self._drummachine = value

    @property
    def sequencer(self):
        return self._sequencer

    @sequencer.setter
    def sequencer(self, value):
        self._sequencer = value

    @property
    def last_selected_sound(self):
        return self._last_selected_sound

    @last_selected_sound.setter
    def last_selected_sound(self, value):
        self._last_selected_sound = value

    @property
    def layer(self):
        return self._layer

    @layer.setter
    def layer(self, value):
        self._layer = value

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        self._mode = value
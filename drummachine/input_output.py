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

    _thread_polling_stopper = False

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
        self.start_thread_volume()

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
            print(self._drummachine.playing)
            self._sequencer.start_thread_sequencer()
            time.sleep(waiting)

        elif GPIO.input(row_5) == GPIO.HIGH and row == 6:
            print("Switch 18")
            # write
            if self._mode == "write":
                self._mode = "default"
                print("Activated default mode")
            else:
                self._mode = "write"
                print("Activated write mode")
                self.led_write()
            time.sleep(waiting)

        elif GPIO.input(row_5) == GPIO.HIGH and row == 17:
            print("Switch 19")
            # layer
            if self._mode == "layer":
                self._mode = "default"
                print("Activated default mode")
            else:
                self._mode = "layer"
                print("Activated layer mode")
            time.sleep(waiting)

        elif GPIO.input(row_5) == GPIO.HIGH and row == 13:
            print("Switch 20")
            # no action
            time.sleep(waiting)

        # if self._drummachine.playing == 0:
        match self._mode:
            case "write":
                GPIO.output(row, GPIO.LOW)
            case _:
                GPIO.output(row, GPIO.LOW)
                self.led_clear()
        # else:
        #     GPIO.output(row, GPIO.LOW)

    def button_action(self, switch):
        global sounds
        match self._mode:
            case "write":
                if self._sequencer.layers_active[self._layer-1] != 0:
                    if self._sequencer.layers_active[self._layer-1][switch-1] == self._last_selected_sound:
                        self._sequencer.layers_active[self._layer-1][switch-1] = 0
                    else:
                        self._sequencer.layers_active[self._layer-1][switch-1] = self._last_selected_sound
                        print(f"Wrote {self._last_selected_sound} in layer {self._layer}")
                    self.led_write()
            case "layer":
                if 0 < switch <= 4:
                    self._layer = switch
                    if self._sequencer.layers_active[switch-1] == 0:
                        match switch:
                            case 1:
                                self._sequencer.layers_active[switch-1] = self._sequencer.sequence_1
                                print("layer 1 active")
                            case 2:
                                self._sequencer.layers_active[switch-1] = self._sequencer.sequence_2
                                print("layer 2 active")
                            case 3:
                                self._sequencer.layers_active[switch-1] = self._sequencer.sequence_3
                                print("layer 3 active")
                            case 4:
                                self._sequencer.layers_active[switch-1] = self._sequencer.sequence_4
                                print("layer 4 active")
                    else:
                        self._sequencer.layers_active[switch-1] = 0
                        print(f"layer{switch} deactivated")
                    self.led_switch(switch)
            case _:
                self._drummachine.sounds[switch-1].set_volume(self._sequencer.volume)
                self._drummachine.sounds[switch-1].play()
                self.led_switch(switch)
                self._last_selected_sound = self._drummachine.sounds[switch-1]


    def start_thread_bpm(self):
        if self.thread_bpm is None or not self.thread_bpm.is_alive():
            self.thread_bpm = threading.Thread(target=self.polling_bpm, daemon=True) #daemon close thread when self program closes
            self.thread_bpm.start()

    def start_thread_volume(self):
        if self.thread_volume is None or not self.thread_volume.is_alive():
            self.thread_volume = threading.Thread(target=self.polling_volume, daemon=True) #daemon close thread when self program closes
            self.thread_volume.start()

    def stop_thread_polling(self):
        print("Killing threads")
        self._thread_polling_stopper = True


    def polling_bpm(self):
        CLK = 26 #26 11
        DT = 9  #9 10

        prev_clk_state = GPIO.input(CLK)

        while not self._thread_polling_stopper:
            clk_state = GPIO.input(CLK)
            dt_state = GPIO.input(DT)

            if clk_state != prev_clk_state:  # detect change
                if dt_state != clk_state:
                    self._sequencer.bpm -= 5  # Turn counterclockwise decreases BPM
                else:
                    self._sequencer.bpm += 5  # turn clockwise increase BPM

                self._sequencer.bpm = max(30, min(self._sequencer.bpm, 300))  # Limiteer BPM tussen 30 en 300
                print(f"BPM: {self._sequencer.bpm}")

            prev_clk_state = clk_state  # keep track of current clk state
            time.sleep(0.001)  #adjust delay to test out 0.01 (10ms) gives to much delay and wrong values

    def polling_volume(self):
        CLK = 11 #26 11
        DT = 10  #9 10

        prev_clk_state = GPIO.input(CLK)

        while not self._thread_polling_stopper:
            clk_state = GPIO.input(CLK)
            dt_state = GPIO.input(DT)

            if clk_state != prev_clk_state:  # detect change
                if dt_state != clk_state:
                    self._sequencer.volume -= 0.05  # Turn counterclockwise decreases volume
                else:
                    self._sequencer.volume += 0.05  # turn clockwise increases volume

                self._sequencer.volume = round(max(0, min(self._sequencer.volume, 1)), 2)  # Limiteer BPM tussen 0 en 1
                print(f"Volume: {self._sequencer.volume}")

            prev_clk_state = clk_state  # keep track of current clk state
            time.sleep(0.001)  #adjust delay to test out 0.01 (10ms) gives to much delay and wrong values

    #helper function for binary code
    def led_write(self):
        number = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        if self._sequencer.layers_active[self._layer-1] != 0:
            for i in range(0, 16):
                if self._sequencer.layers_active[(self._layer-1)][i] == self.last_selected_sound:
                    number[i] = 1
            self.led_driver(number)
    def led_switch(self, switch):
        number = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        number[switch-1] = 1
        self.led_driver(number)

    def led_driver(self, number):
        CLK_PIN = 14
        LATCH_PIN = 27
        BLANK_PIN = 22
        SI_PIN = 24

        GPIO.output(BLANK_PIN, GPIO.LOW)
        GPIO.output(SI_PIN, GPIO.LOW)
        GPIO.output(LATCH_PIN, GPIO.LOW)
        GPIO.output(BLANK_PIN, GPIO.LOW)
        for i in range(15,-1, -1):
            if number[i] == 1:
                GPIO.output(SI_PIN, GPIO.HIGH)
            GPIO.output(CLK_PIN, GPIO.HIGH)
            time.sleep(1/30000000)
            GPIO.output(CLK_PIN, GPIO.LOW)
            time.sleep(1/30000000)
            GPIO.output(SI_PIN, GPIO.LOW)
        GPIO.output(LATCH_PIN, GPIO.HIGH)
        time.sleep(1/30000000)
        GPIO.output(LATCH_PIN, GPIO.LOW)

    def led_clear(self):
        CLK_PIN = 14
        LATCH_PIN = 27
        BLANK_PIN = 22
        SI_PIN = 24

        GPIO.output(BLANK_PIN, GPIO.LOW)
        GPIO.output(SI_PIN, GPIO.LOW)
        GPIO.output(LATCH_PIN, GPIO.LOW)
        GPIO.output(BLANK_PIN, GPIO.LOW)
        for i in range(0, 16):
            GPIO.output(CLK_PIN, GPIO.HIGH)
            time.sleep(1/30000000)
            GPIO.output(CLK_PIN, GPIO.LOW)
            time.sleep(1/30000000)
        GPIO.output(LATCH_PIN, GPIO.HIGH)
        time.sleep(1/30000000)
        GPIO.output(LATCH_PIN, GPIO.LOW)


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

    @property
    def thread_bpm_stopper(self):
        return self._thread_bpm_stopper

    @thread_bpm_stopper.setter
    def thread_bpm_stopper(self, value):
        self._thread_bpm_stopper = value


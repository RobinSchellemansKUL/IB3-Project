import time
import pygame
import threading

class Sequencer:
    _instance = None
    _drummachine = None

    thread_sequencer = None

    _sequence_1 = None
    _sequence_2 = None
    _sequence_3 = None
    _sequence_4 = None
    _layers_active = None

    _bpm = None

    def __new__(cls, drummachine):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, drummachine):
        self._drummachine = drummachine

        self._bpm = 120

        self._sequence_1 = [self._drummachine.sounds[0],0,0,0,self._drummachine.sounds[1],0,0,0,self._drummachine.sounds[0],0,self._drummachine.sounds[5],0,self._drummachine.sounds[1],0,0,0]
        # self._sequence_1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self._sequence_2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self._sequence_3 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self._sequence_4 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self._layers_active = [self._sequence_1,0,0,0]

    def start_thread_sequencer(self):
        print("degub")
        if self.thread_sequencer is None or not self.thread_sequencer.is_alive():
            self.thread_sequencer = threading.Thread(target=self.play_sequencer, daemon=True)
            self.thread_sequencer.start()

    def play_sequencer(self):
        timestamp = time.time()
        i = 0

        while self._drummachine.playing:
            timestampcheck = time.time()
            if timestampcheck - timestamp > 0.1:
                timestamp = time.time()
                for j in range(0,3):
                    if self._layers_active[j] != 0:
                        if self._layers_active[j][i] != 0:
                            self._layers_active[j][i].play()
                i += 1
                i = i%16

    # Getters and Setters
    @property
    def drummachine(self):
        return self._drummachine

    @drummachine.setter
    def drummachine(self, drummachine):
        self._drummachine = drummachine

    @property
    def sequence_1(self):
        return self._sequence_1

    @sequence_1.setter
    def sequence_1(self, value):
        self._sequence_1 = value

    @property
    def sequence_2(self):
        return self._sequence_2

    @sequence_2.setter
    def sequence_2(self, value):
        self._sequence_2 = value

    @property
    def sequence_3(self):
        return self._sequence_3

    @sequence_3.setter
    def sequence_3(self, value):
        self._sequence_3 = value

    @property
    def sequence_4(self):
        return self._sequence_4

    @sequence_4.setter
    def sequence_4(self, value):
        self._sequence_4 = value

    @property
    def layers_active(self):
        return self._layers_active

    @layers_active.setter
    def layers_active(self, value):
        self._layers_active = (value)

    @property
    def bpm(self):
        return self._bpm

    @bpm.setter
    def bpm(self, value):
        self._bpm = value
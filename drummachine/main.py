from drummachine import DrumMachine
from input_output import Input_Output
from sequencer import Sequencer

drummachine = DrumMachine()
sequencer = Sequencer(drummachine)
input_output = Input_Output(drummachine, sequencer)

drummachine.input_output = input_output
sequencer.input_output = input_output

drummachine.run_drummachine()
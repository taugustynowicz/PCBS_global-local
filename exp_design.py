import expyriment as xpy
from expyriment.io import Keyboard
import random

# Import all the audio files
AAAAA = xpy.stimuli.Audio("AAAAA.wav")
BBBBB = xpy.stimuli.Audio("BBBBB.wav")
AAAAB = xpy.stimuli.Audio("AAAAB.wav")
BBBBA = xpy.stimuli.Audio("BBBBA.wav")

# Initialize Expyriment
xpy.control.initialize()

# Set the level of event logging
xpy.control.defaults.event_logging = 3

# Create a Keyboard object
kb = Keyboard()

# Create a screen to display stimuli
screen = xpy.stimuli.BlankScreen()

# Create a fixation cross
fixation_cross = xpy.stimuli.FixCross(size=(20, 20), line_width=4)

# Function to display the fixation cross
def display_fixation_cross():
    fixation_cross.present()

# Create the rule of stim presentation
series_type = ["freq"]*60 + ["inf"]*20
random.shuffle(series_type)

initial_series = ["freq"]*20

total_series = initial_series + series_type

# Create a clock for timing
clock = xpy.misc.Clock()

# Create a variable interval of 1350 to 1650 ms with 50-ms steps
interval = list(range(1350, 1651, 50))

# Function to play audio with silence
def play_with_silence(audio):
    audio.play()

    # Check for escape key press after each block
    keypress = kb.check(keys=[Keyboard.get_quit_key()])
    if keypress is not None:
        key, rt = keypress
        if key:
            xpy.control.end()
            exit()

    clock.wait(random.choice(interval)) 

# Define block types
block_types = ['a', 'b', 'c', 'd'] * 2
random.shuffle(block_types)

# Start the experiment
xpy.control.start(skip_ready_screen = True)

# Present the fixation cross before playing blocks
display_fixation_cross()

# Play blocks
for block_type in block_types:
    if block_type == 'a':
        for types in total_series:
            if types == "freq":
                play_with_silence(AAAAA)
            else:
                play_with_silence(AAAAB)
    elif block_type == 'b':
        for types in total_series:
            if types == "freq":
                play_with_silence(BBBBB)
            else:
                play_with_silence(BBBBA)
    elif block_type == 'c':
        for types in total_series:
            if types == "freq":
                play_with_silence(AAAAB)
            else:
                play_with_silence(AAAAA)
    elif block_type == 'd':
        for types in total_series:
            if types == "freq":
                play_with_silence(BBBBA)
            else:
                play_with_silence(BBBBB)

# End the experiment
xpy.control.end()
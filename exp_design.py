import expyriment
import random

# Import all the audio files
AAAAA = expyriment.stimuli.Audio("AAAAA.wav")
BBBBB = expyriment.stimuli.Audio("BBBBB.wav")
AAAAB = expyriment.stimuli.Audio("AAAAB.wav")
BBBBA = expyriment.stimuli.Audio("BBBBA.wav")

# Create the rule of stim presentation
series_type = ["freq"]*60 + ["inf"]*20
random.shuffle(series_type)

initial_series = ["freq"]*20

total_series = initial_series + series_type

# Create a clock for timing
clock = expyriment.misc.Clock()

# Create a variable interval of 1350 to 1650 ms with 50-ms steps
interval = list(range(1350, 1651, 50))

# Function to play audio with silence
def play_with_silence(audio):
    audio.play()
    clock.delay(random.choice(interval))

# Define block types
block_types = ['a', 'b', 'c', 'd'] * 2
random.shuffle(block_types)

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

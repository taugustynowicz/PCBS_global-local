import numpy as np
import matplotlib.pyplot as plt
import simpleaudio as sa
# import expyriment as xp


######################
### DEFINE STIMULI ###
######################

### SOUND A ###

# note frequencies
A1_freq = 350
A2_freq = 700
A3_freq = 1400

# get timesteps for each sample
SAMPLE_RATE = 44100
DURATION_sound = 0.05
t = np.linspace(start=0.0,
                stop=DURATION_sound,
                num=int(DURATION_sound * SAMPLE_RATE))

# generate sine wave notes
A1_note = np.sin(A1_freq * t * 2 * np.pi)
A2_note = np.sin(A2_freq * t * 2 * np.pi)
A3_note = np.sin(A3_freq * t * 2 * np.pi)

# mix audio together
n = len(t)
audio = np.zeros(n)
offset = 0
audio[0 + offset: n + offset] += A1_note
audio[0 + offset: n + offset] += A2_note
audio[0 + offset: n + offset] += A3_note

DURATION_break = 0.15
silence = np.zeros(int(DURATION_break * SAMPLE_RATE))

audio2 = np.hstack((audio, silence, audio, silence, audio))

plt.plot(audio2)
plt.show()


# normalize to 16-bit range
audio2 *= 32767 / np.max(np.abs(audio2))
# convert to 16-bit data
audio2 = audio2.astype(np.int16)

# start playback
play_obj = sa.play_buffer(audio2, 2, 2, SAMPLE_RATE)

# wait for playback to finish before exiting
play_obj.wait_done()





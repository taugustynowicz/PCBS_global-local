import numpy as np
import matplotlib.pyplot as plt
import simpleaudio as sa
import scipy.io.wavfile

######################
### DEFINE STIMULI ###
######################

### CREATE SOUNDS 'A' AND 'B' ###

# Note frequencies
freqs = [[350, 700, 1400], [500, 1000, 2000]]

# Sampling rate
sample_rate = 44100

# Duration of sound
duration_sound = 0.05 # 50 ms

# Time array
t = np.linspace(0, duration_sound, int(duration_sound * sample_rate)) # ??? 2 arg for linspace is exclusive 

# Generate sine wave notes
notes_A = [np.sin(freq * t * 2 * np.pi) for freq in freqs[0]]
notes_B = [np.sin(freq * t * 2 * np.pi) for freq in freqs[1]]

# Mix audio together
wave_A = np.sum(notes_A, axis = 0)
wave_B = np.sum(notes_B, axis = 0)

### Inspect the waves at this point

num_notes = len(notes_A)

fig, axs = plt.subplots(num_notes + 1, 1, figsize=(10, 5*(num_notes + 1)))

# Plot each note on a separate subplot
for ax, note in zip(axs, notes_A):
    ax.plot(note)

# Plot the mixed wave on the last subplot
axs[-1].plot(wave_A)
plt.show()

### Create the window

# Define the length of the rising, constant, and falling sections
def cosine_window(total_duration, rise_fall_duration = 0.007, sampling_rate = 44100):
    if total_duration - 2*rise_fall_duration < 0:
        raise ValueError("Rise and fall times are too long for the given length")
    
    n_sample_ramp = int(rise_fall_duration * sampling_rate)
    n_sample_flat = int(total_duration * sampling_rate) - 2 * n_sample_ramp
    
    ramp_up = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, n_sample_ramp, endpoint=False))
    ramp_down = 0.5 + 0.5 * np.cos(np.linspace(0, np.pi, n_sample_ramp, endpoint=False))
    
    return np.concatenate([
        ramp_up,
        np.ones(n_sample_flat),
        ramp_down
    ])  

# Create cosine window
window_cosine = cosine_window(duration_sound)

# Plot the cosine window
plt.plot(window_cosine)
plt.title('Cosine Window')
plt.show()

# Apply the window to the waves
windowed_wave_A = wave_A * window_cosine
windowed_wave_A = np.append(windowed_wave_A, 0)

windowed_wave_B = wave_B * window_cosine
windowed_wave_B = np.append(windowed_wave_B, 0)

# Define the desired amplitude
desired_amplitude = 32767

# Normalize windowed_wave_A
windowed_wave_A = windowed_wave_A / np.max(np.abs(windowed_wave_A)) * desired_amplitude

# Normalize windowed_wave_B
windowed_wave_B = windowed_wave_B / np.max(np.abs(windowed_wave_B)) * desired_amplitude

### Plot the smoothed wave

fig, axs = plt.subplots(2)

# Plot windowed_wave_A
axs[0].plot(windowed_wave_A)
axs[0].set_title('Windowed Wave A')

# Plot windowed_wave_B
axs[1].plot(windowed_wave_B)
axs[1].set_title('Windowed Wave B')

# Display the plots
plt.tight_layout()
plt.show()

### Create SOA

duration_soa = 0.15 # 150 ms
soa_wave = np.zeros(int(duration_soa * sample_rate))


### CREATE SERIES OF SOUNDS ###

# Sound 1 (AAAAA)
AAAAA = np.concatenate([windowed_wave_A, soa_wave, windowed_wave_A, soa_wave, \
                         windowed_wave_A, soa_wave, windowed_wave_A, soa_wave, \
                            windowed_wave_A], axis = 0)

# Sound 2 (BBBBB)
BBBBB = np.concatenate([windowed_wave_B, soa_wave, windowed_wave_B, soa_wave, \
                         windowed_wave_B, soa_wave, windowed_wave_B, soa_wave, \
                            windowed_wave_B], axis = 0)

# Sound 3 (AAAAB)
AAAAB = np.concatenate([windowed_wave_A, soa_wave, windowed_wave_A, soa_wave, \
                         windowed_wave_A, soa_wave, windowed_wave_A, soa_wave, \
                            windowed_wave_B], axis = 0)

# Sound 4 (BBBBA)
BBBBA = np.concatenate([windowed_wave_B, soa_wave, windowed_wave_B, soa_wave, \
                         windowed_wave_B, soa_wave, windowed_wave_B, soa_wave, \
                            windowed_wave_A], axis = 0)


# Convert the numpy array to 16-bit integers
audio_sound_1 = (BBBBA).astype(np.int16)

# Play the audio
play_obj = sa.play_buffer(audio_sound_1, 1, 2, sample_rate)

# Wait for playback to finish
play_obj.wait_done()

# Define func to save to .wav files
def write_array_as_sound(nparray, sample_rate, filename):
    scipy.io.wavfile.write(filename,
                           sample_rate,
                           nparray.T.astype(np.dtype('i2')))
    
# ### Save the sounds to .wav files

# # AAAAA
# write_array_as_sound(AAAAA, sample_rate, 'AAAAA.wav')

# # BBBBB
# write_array_as_sound(BBBBB, sample_rate, 'BBBBB.wav')

# # AAAAB
# write_array_as_sound(AAAAB, sample_rate, 'AAAAB.wav')

# # BBBBA
# write_array_as_sound(BBBBA, sample_rate, 'BBBBA.wav')



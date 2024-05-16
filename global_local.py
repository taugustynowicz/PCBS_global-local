import numpy as np
import matplotlib.pyplot as plt
import simpleaudio as sa

######################
### DEFINE STIMULI ###
######################

### CREATE SOUNDS 'A' AND 'B' ###

# Note frequencies
freqs = [[350, 700, 1400], [500, 1000, 2000]]
# Sampling rate
sample_rate = 44100
# Duration of sound
duration_sound = 0.05
# Time array
t = np.linspace(0, duration_sound, int(duration_sound * sample_rate)) # ??? 2 arg for linspace is exclusive 

# Generate sine wave notes
notes_A = [np.sin(freq * t * 2 * np.pi) for freq in freqs[0]]
notes_B = [np.sin(freq * t * 2 * np.pi) for freq in freqs[1]]

# Mix audio together
wave_A = np.sum(notes_A, axis = 0)
wave_B = np.sum(notes_B, axis = 0)

# # Calculate the number of subplots needed
# num_notes = len(notes)

# fig, axs = plt.subplots(num_notes + 1, 1, figsize=(10, 5*(num_notes + 1)))

# # Plot each note on a separate subplot
# for ax, note in zip(axs, notes):
#     ax.plot(note)

# # Plot the mixed wave on the last subplot
# axs[-1].plot(wave)
# plt.show()

# Define the length of the rising, constant, and falling sections
def trapezoidal_window(total_duration, rise_fall_duration = 0.007, sampling_rate = 44100):
    if total_duration - 2*rise_fall_duration < 0:
        raise ValueError("Rise and fall times are too long for the given length")
    
    n_sample_ramp = int(rise_fall_duration * sampling_rate)
    n_sample_flat = int(total_duration * sampling_rate) - 2 * n_sample_ramp
    return np.concatenate([
        np.linspace(0, 1, n_sample_ramp, endpoint=False),
        np.ones(n_sample_flat),
        np.linspace(1, 0, n_sample_ramp, endpoint=False)
    ])  

# Create trapezoidal window
window_trapezoidal = trapezoidal_window(duration_sound)

# # Plot the trapezoidal window
# plt.plot(window_trapezoidal)
# plt.title('Trapezoidal Window')
# plt.show()

windowed_wave_A = wave_A * window_trapezoidal

windowed_wave_A = np.append(windowed_wave_A, 0)
print(len(windowed_wave_A))

windowed_wave_B = wave_B * window_trapezoidal

windowed_wave_B = np.append(windowed_wave_B, 0)
print(len(windowed_wave_B))

# # Plot the smoothed wave
# fig, axs = plt.subplots(2)

# # Plot windowed_wave_A
# axs[0].plot(windowed_wave_A)
# axs[0].set_title('Windowed Wave A')

# # Plot windowed_wave_B
# axs[1].plot(windowed_wave_B)
# axs[1].set_title('Windowed Wave B')

# # Display the plots
# plt.tight_layout()
# plt.show()

# Convert the numpy array to 16-bit integers
audio_wave_A = (windowed_wave_A * 32767).astype(np.int16)

# Play the audio
play_obj = sa.play_buffer(audio_wave_A, 2, 2, sample_rate)

# Wait for playback to finish
play_obj.wait_done()

# Convert the numpy array to 16-bit integers
audio_wave_B = (windowed_wave_B * 32767).astype(np.int16)

# Play the audio
play_obj = sa.play_buffer(audio_wave_B, 2, 2, sample_rate)

# Wait for playback to finish
play_obj.wait_done()
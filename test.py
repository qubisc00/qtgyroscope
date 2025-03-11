import time
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('dark_background')

# Parameters (audio)
sr         = 44100  # Sample rate
n_ch       = 1      # Number of channels (1 for mono, adjust based on your microphone)
n_fft      = 4096   # FFT size
hop_length = int(n_fft / 4 * 3)  # Hop length
overlap    = n_fft - hop_length
n_plot_tf  = 80     # Number of time frames to plot
n_freqs    = n_fft // 2 + 1  # Number of frequency bins
f_max_idx  = 480    # Maximum frequency index to display
window     = np.hamming(n_fft)  # Hamming window
amp        = np.zeros((n_plot_tf, f_max_idx))  # Amplitude array

# Parameters (plot, video)
fps = 61
fig, ax = plt.subplots()
image = ax.imshow(amp.T, aspect="auto", origin='lower', extent=[0, n_plot_tf, 0, sr / 2])
ax.set_xlabel("Time frame")
ax.set_ylabel("Frequency (Hz)")
fig.colorbar(image)
vmax, vmin = 1.0, 0.0

# Global variable for amplitude
current_amp = np.zeros(f_max_idx)

# Function to process audio blocks
def audio_callback(indata, frames, time, status):
    global current_amp, vmax  # Declare as global
    if status:
        print(status)
    x = np.mean(indata, axis=1)  # Convert to mono
    current_amp = np.sqrt(np.abs(np.fft.rfft(window * x)))[0:f_max_idx]
    if vmax < np.max(current_amp):
        vmax = np.max(current_amp)

# Animation update function
def update(frame):
    global current_amp
    amp[:-1] = amp[1:]  # Shift the array
    amp[-1] = current_amp  # Add the latest data
    image.set_clim(vmin, vmax)
    image.set_data(amp.T[::-1])
    plt.title(f"fps: {fps:0.1f} Hz")

# Start audio stream
try:
    with sd.InputStream(channels=n_ch, samplerate=sr, blocksize=n_fft, callback=audio_callback):
        ani = FuncAnimation(fig, update, interval=1000 / fps)  # Update every frame
        plt.show()  # Show the plot
except KeyboardInterrupt:
    print("Stream stopped by user.")
except Exception as e:
    print(f"An error occurred: {e}")

plt.close()

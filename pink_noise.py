"""
pink_noise (ピンクノイズ 1/fゆらぎ)
参照元：
https://note.com/yyhhyy21/n/n72bbe5437bda からリファクタリング

"""

import numpy as np
import scipy.signal as sp
import wave
import sounddevice as sd
import matplotlib.pyplot as plt
import random

print(sd.query_devices())

# Constants
DURATION = 5.0  # Duration in seconds
FS = 44100  # Sampling frequency in Hz
AMPLITUDE = 10.0  # Amplitude
F0 = 440.0  # Fundamental frequency in Hz
NUM_HARMONICS = 40  # Number of harmonics

def generate_wave(t, amplitude, f0, num_harmonics):
    z = np.zeros(len(t))
    x = []
    pow_y = []

    for i in range(1, num_harmonics):
        j = random.randint(1, num_harmonics)
        contribution = (amplitude * (1 / (f0 * j)))**0.5 * np.cos(2 * np.pi * f0 * j * t)
        z += contribution
        pow_y.append((amplitude * (1 / (f0 * j)))**2)
        x.append(f0 * j)

    return z, x, pow_y

def play_and_save_wave(z, fs, filename):
    sd.play(z, fs)
    print("再生中")
    sd.wait()

    normalized_wave = (z / np.max(np.abs(z))) * np.iinfo(np.int16).max
    normalized_wave = normalized_wave.astype(np.int16)

    with wave.open(filename, "w") as wave_out:
        wave_out.setnchannels(1)
        wave_out.setsampwidth(2)  # 16bit = 2 bytes
        wave_out.setframerate(fs)
        wave_out.writeframes(normalized_wave)

def plot_waveform(t, z, filename):
    plt.figure(figsize=(8, 3))
    plt.plot(t, z)
    plt.xlim(0, 0.01)
    plt.savefig(filename)
    plt.show()

def plot_spectrum(x, pow_y, filename):
    plt.figure(figsize=(8, 3))
    plt.scatter(x, pow_y)
    plt.yscale('log')
    plt.xscale('log')
    plt.savefig(filename)
    plt.show()

def main():
    t = np.arange(0, FS * DURATION) / FS
    z, x, pow_y = generate_wave(t, AMPLITUDE, F0, NUM_HARMONICS)

    play_and_save_wave(z, FS, "sin_241003_008.wav")

    plot_waveform(t, z, "sin_241003_008.png")
    plot_spectrum(x, pow_y, "spectr_241003_008.png")

if __name__ == "__main__":
    main()
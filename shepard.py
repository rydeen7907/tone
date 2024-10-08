"""
shepard tone( 無限音階 )

参照元：
https://qiita.com/shionhonda/items/4fff494a0cd4d843b6df からリファクタリング

"""

import numpy as np
import argparse
from scipy.io import wavfile
import sounddevice as sd

print(sd.query_devices())

# 定数の定義
SAMPLE_RATE = 44100  # サンプルレート (samples per second)
DURATION_SECS = 10   # 音声の長さ (seconds)
TOTAL_SAMPLES = SAMPLE_RATE * DURATION_SECS  # 全体のサンプル数
LOUDNESS_MIN = 22    # 最小音量 (dB)
LOUDNESS_MAX = 56    # 最大音量 (dB)
COMPONENTS_MAX = 6  # コンポーネント数
FREQUENCY_MIN = 20   # 最小周波数 (Hz)

def shift(t, c):
    return c + t / TOTAL_SAMPLES

def theta(t, c):
    return 2 * np.pi / COMPONENTS_MAX * shift(t, c)

def loudness(t, c):
    return LOUDNESS_MIN + (LOUDNESS_MAX - LOUDNESS_MIN) * (1 - np.cos(theta(t, c))) / 2

def frequency(t, c):
    return FREQUENCY_MIN * 2 ** shift(t, c)

def amplitude(t, c):
    return 10 ** (loudness(t, c) / 20)

def generate_shepard_tone(down: bool = False) -> np.ndarray:
    t = np.linspace(0, TOTAL_SAMPLES - 1, TOTAL_SAMPLES)
    wave = np.zeros(TOTAL_SAMPLES)
    for c in range(COMPONENTS_MAX):
        wave += amplitude(t, c) * np.sin(2 * np.pi * np.cumsum(frequency(t, c)) / SAMPLE_RATE)

    wave = np.hstack((wave, wave))
    if down:
        wave = wave[::-1]

    # 波形を正規化
    return (wave / np.max(np.abs(wave))).astype(np.float32)

def main():
    parser = argparse.ArgumentParser(description='Shepard tone generator')
    parser.add_argument('--down', '-d', type=bool, default=False, help='Set True for descending tone')
    args = parser.parse_args()

    wave = generate_shepard_tone(args.down)
    
    # ファイル書き出し
    file_name = "shepard_down.wav" if args.down else "shepard_up.wav"
    wavfile.write(file_name, SAMPLE_RATE, wave)

    # 音声を再生
    sd.play(wave, SAMPLE_RATE)
    sd.wait()  # 再生終了まで待機

if __name__ == '__main__':
    main()
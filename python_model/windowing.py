
import numpy as np
import matplotlib.pyplot as plt

from adaptive_lut import build_lut, lookup_profile
from waveform_lfm import generate_lfm



def apply_window(signal, window_type):

    N = len(signal)

    if window_type.lower() == "hann":
        window = np.hanning(N)

    elif window_type.lower() == "hamming":
        window = np.hamming(N)

    elif window_type.lower() == "blackman":
        window = np.blackman(N)

    else:
        raise ValueError(
            "Unknown window. Use Hann, Hamming or Blackman."
        )

    windowed_signal = signal * window

    return windowed_signal, window



def calculate_fft(signal, sample_rate):

    N = len(signal)

    spectrum = np.fft.rfft(signal)

    frequency = np.fft.rfftfreq(
        N,
        1 / sample_rate
    )

    magnitude = np.abs(spectrum)

    magnitude = magnitude / np.max(magnitude)

    magnitude_db = 20 * np.log10(
        magnitude + 1e-12
    )

    return frequency, magnitude_db



if __name__ == "__main__":


    lut = build_lut()

    address = 0x55

    result = lookup_profile(address, lut)

    profile = result["profile"]


    sample_rate = 5_000_000


    t, signal, f_start, f_end = generate_lfm(
        fc=profile.fc,
        bandwidth=profile.bandwidth,
        pulse_duration=profile.pulse_duration,
        amplitude=profile.amplitude,
        sample_rate=sample_rate
    )


    hann_signal, hann_window = apply_window(
        signal,
        "hann"
    )

    hamming_signal, hamming_window = apply_window(
        signal,
        "hamming"
    )

    blackman_signal, blackman_window = apply_window(
        signal,
        "blackman"
    )


    print()
    print("==========================================")
    print("       AQUILA DIGITAL WINDOWING TEST")
    print("==========================================")

    print()
    print(f"LUT Address       : 0x{address:02X}")
    print(f"Center Frequency  : {profile.fc:.2f} Hz")
    print(f"Bandwidth         : {profile.bandwidth:.2f} Hz")
    print(f"Pulse Duration    : {profile.pulse_duration:.6f} s")
    print(f"Sample Rate       : {sample_rate} samples/s")

    print()
    print("Windows Applied")
    print("------------------------------------------")
    print("1. Hann")
    print("2. Hamming")
    print("3. Blackman")


    samples_to_show = min(500, len(signal))

    plt.figure(figsize=(10, 5))

    plt.plot(
        t[:samples_to_show] * 1000,
        signal[:samples_to_show],
        label="Original"
    )

    plt.plot(
        t[:samples_to_show] * 1000,
        hann_signal[:samples_to_show],
        label="Hann"
    )

    plt.plot(
        t[:samples_to_show] * 1000,
        hamming_signal[:samples_to_show],
        label="Hamming"
    )

    plt.plot(
        t[:samples_to_show] * 1000,
        blackman_signal[:samples_to_show],
        label="Blackman"
    )

    plt.title("AQUILA Digital Windowing")
    plt.xlabel("Time (ms)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()


    f_original, fft_original = calculate_fft(
        signal,
        sample_rate
    )

    f_hann, fft_hann = calculate_fft(
        hann_signal,
        sample_rate
    )

    f_hamming, fft_hamming = calculate_fft(
        hamming_signal,
        sample_rate
    )

    f_blackman, fft_blackman = calculate_fft(
        blackman_signal,
        sample_rate
    )


    plt.figure(figsize=(10, 5))

    plt.plot(
        f_original / 1000,
        fft_original,
        label="Original"
    )

    plt.plot(
        f_hann / 1000,
        fft_hann,
        label="Hann"
    )

    plt.plot(
        f_hamming / 1000,
        fft_hamming,
        label="Hamming"
    )

    plt.plot(
        f_blackman / 1000,
        fft_blackman,
        label="Blackman"
    )

    plt.xlim(
        max(0, f_start - profile.bandwidth) / 1000,
        (f_end + profile.bandwidth) / 1000
    )

    plt.ylim(-100, 5)

    plt.title("AQUILA Spectrum - Window Comparison")
    plt.xlabel("Frequency (kHz)")
    plt.ylabel("Magnitude (dB)")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()
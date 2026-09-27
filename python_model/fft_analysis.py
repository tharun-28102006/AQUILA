
import numpy as np
import matplotlib.pyplot as plt

from adaptive_lut import build_lut, lookup_profile
from waveform_lfm import generate_lfm
from windowing import apply_window



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



def find_peak_frequency(
    frequency,
    magnitude_db
):

    peak_index = np.argmax(
        magnitude_db
    )

    return frequency[peak_index]



def estimate_bandwidth(
    frequency,
    magnitude_db,
    threshold_db=-20
):

    valid = magnitude_db >= threshold_db

    if not np.any(valid):
        return 0.0, 0.0, 0.0

    frequencies = frequency[valid]

    f_low = frequencies[0]
    f_high = frequencies[-1]

    bandwidth = f_high - f_low

    return f_low, f_high, bandwidth



if __name__ == "__main__":


    lut = build_lut()

    address = 0x55

    result = lookup_profile(
        address,
        lut
    )

    profile = result["profile"]


    sample_rate = 5_000_000


    (
        time,
        signal,
        f_start,
        f_end
    ) = generate_lfm(
        fc=profile.fc,
        bandwidth=profile.bandwidth,
        pulse_duration=profile.pulse_duration,
        amplitude=profile.amplitude,
        sample_rate=sample_rate
    )


    windowed_signal, window = apply_window(
        signal,
        "hann"
    )


    frequency, magnitude_db = calculate_fft(
        windowed_signal,
        sample_rate
    )


    peak_frequency = find_peak_frequency(
        frequency,
        magnitude_db
    )

    measured_low, measured_high, measured_bw = (
        estimate_bandwidth(
            frequency,
            magnitude_db
        )
    )


    print()
    print("==========================================")
    print("       AQUILA FFT VERIFICATION")
    print("==========================================")

    print()
    print("EXPECTED PARAMETERS")
    print("------------------------------------------")

    print(
        f"Center Frequency : "
        f"{profile.fc:.2f} Hz"
    )

    print(
        f"Start Frequency  : "
        f"{f_start:.2f} Hz"
    )

    print(
        f"End Frequency    : "
        f"{f_end:.2f} Hz"
    )

    print(
        f"Bandwidth        : "
        f"{profile.bandwidth:.2f} Hz"
    )

    print(
        f"Pulse Duration   : "
        f"{profile.pulse_duration:.6f} s"
    )

    print(
        f"Amplitude        : "
        f"{profile.amplitude}"
    )

    print()
    print("MEASURED FROM FFT")
    print("------------------------------------------")

    print(
        f"Peak Frequency   : "
        f"{peak_frequency:.2f} Hz"
    )

    print(
        f"-20 dB Low       : "
        f"{measured_low:.2f} Hz"
    )

    print(
        f"-20 dB High      : "
        f"{measured_high:.2f} Hz"
    )

    print(
        f"-20 dB Bandwidth : "
        f"{measured_bw:.2f} Hz"
    )


    frequency_error = (
        peak_frequency - profile.fc
    )

    print()
    print("ERROR")
    print("------------------------------------------")

    print(
        f"Center Frequency Error : "
        f"{frequency_error:.2f} Hz"
    )


    plt.figure(
        figsize=(10, 5)
    )

    plt.plot(
        frequency / 1000,
        magnitude_db
    )

    plt.axvline(
        profile.fc / 1000,
        linestyle="--",
        label="Expected Fc"
    )

    plt.axhline(
        -20,
        linestyle="--",
        label="-20 dB"
    )

    plt.xlim(
        max(0, f_start - profile.bandwidth)
        / 1000,

        (f_end + profile.bandwidth)
        / 1000
    )

    plt.ylim(
        -100,
        5
    )

    plt.title(
        "AQUILA LFM Spectrum Verification"
    )

    plt.xlabel(
        "Frequency (kHz)"
    )

    plt.ylabel(
        "Magnitude (dB)"
    )

    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()
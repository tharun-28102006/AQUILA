import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

FS = 5_000_000

FILES = {
    "GEOMETRIC": "geometric_capture.csv",
    "LFM": "lfm_capture.csv",
    "PHASE_CODED": "phase_capture.csv",
}


def analyze_waveform(name, filename):

    path = Path(filename)

    if not path.exists():
        print(f"ERROR: {filename} not found")
        return

    df = pd.read_csv(path)

    samples = df["dac_sample"].to_numpy(dtype=float)

    n = len(samples)

    if n == 0:
        print(f"{name}: no samples")
        return

    time_us = np.arange(n) / FS * 1e6

    x = samples - np.mean(samples)


    peak = np.max(samples)
    minimum = np.min(samples)
    mean = np.mean(samples)
    vpp_code = peak - minimum

    print()
    print("=" * 60)
    print(name)
    print("=" * 60)
    print(f"Samples       : {n}")
    print(f"Duration      : {n / FS * 1e3:.3f} ms")
    print(f"Minimum       : {minimum:.2f}")
    print(f"Maximum       : {peak:.2f}")
    print(f"Mean          : {mean:.2f}")
    print(f"Peak-to-peak  : {vpp_code:.2f}")


    window = np.hanning(n)

    spectrum = np.fft.rfft(x * window)

    frequencies = np.fft.rfftfreq(n, 1 / FS)

    magnitude = np.abs(spectrum)

    if len(magnitude) > 1:

        peak_index = np.argmax(magnitude[1:]) + 1

        peak_frequency = frequencies[peak_index]

        print(f"FFT peak      : {peak_frequency / 1000:.2f} kHz")


    plt.figure(figsize=(10, 4))

    plt.plot(time_us, samples)

    plt.title(f"AQUILA {name} - DAC Output")

    plt.xlabel("Time (µs)")
    plt.ylabel("DAC Code")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        f"{name.lower()}_time.png",
        dpi=200
    )

    plt.show()


    plt.figure(figsize=(10, 4))

    plt.plot(
        frequencies / 1000,
        magnitude
    )

    plt.xlim(0, 500)

    plt.title(f"AQUILA {name} - FFT")

    plt.xlabel("Frequency (kHz)")
    plt.ylabel("Magnitude")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        f"{name.lower()}_fft.png",
        dpi=200
    )

    plt.show()



def generate_spectrogram(name, filename):

    path = Path(filename)

    if not path.exists():
        print(f"ERROR: {filename} not found")
        return

    df = pd.read_csv(path)

    samples = df["dac_sample"].to_numpy(dtype=float)

    x = samples - np.mean(samples)

    plt.figure(figsize=(10, 5))

    plt.specgram(
        x,
        NFFT=256,
        Fs=FS,
        noverlap=200
    )

    plt.ylim(100_000, 500_000)

    plt.title(
        f"AQUILA {name} - Frequency-Time Spectrogram"
    )

    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")

    plt.colorbar(
        label="Power/Frequency (dB)"
    )

    plt.tight_layout()

    plt.savefig(
        f"{name.lower()}_spectrogram.png",
        dpi=200
    )

    plt.show()



for name, filename in FILES.items():

    analyze_waveform(name, filename)



generate_spectrogram(
    "GEOMETRIC",
    "geometric_capture.csv"
)

generate_spectrogram(
    "LFM",
    "lfm_capture.csv"
)



print()
print("=" * 60)
print("AQUILA WAVEFORM ANALYSIS COMPLETE")
print("=" * 60)
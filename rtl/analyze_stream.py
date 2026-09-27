import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
import csv
import os

CSV_FILE = "aquila_stream_samples.csv"


samples = []
invalid = 0

with open(CSV_FILE, "r") as f:
    reader = csv.DictReader(f)

    for row in reader:
        try:
            samples.append(float(row["stream_sample"]))
        except (ValueError, TypeError):
            invalid += 1

samples = np.array(samples)


SAMPLE_RATE = 5_000_000
N = len(samples)

print()
print("=" * 60)
print(" AQUILA LFM STREAM ANALYSIS")
print("=" * 60)

print(f"CSV file        : {os.path.abspath(CSV_FILE)}")
print(f"Valid samples   : {N}")
print(f"Invalid entries : {invalid}")
print(f"Sample rate     : {SAMPLE_RATE/1e6:.2f} MSPS")
print(f"Duration        : {N/SAMPLE_RATE*1000:.3f} ms")
print(f"Minimum sample  : {samples.min():.0f}")
print(f"Maximum sample  : {samples.max():.0f}")
print(f"Mean sample     : {samples.mean():.2f}")


signal = samples - np.mean(samples)


fft = np.fft.rfft(signal)
freq = np.fft.rfftfreq(N, 1 / SAMPLE_RATE)

magnitude = np.abs(fft)

peak_index = np.argmax(magnitude)
peak_frequency = freq[peak_index]

print(f"FFT peak        : {peak_frequency/1000:.2f} kHz")


time = np.arange(N) / SAMPLE_RATE

plt.figure(figsize=(12, 5))

plt.plot(time * 1000, samples)

plt.xlabel("Time (ms)")
plt.ylabel("DAC Code")
plt.title("AQUILA LFM DAC Output")

plt.grid(True)
plt.tight_layout()

plt.savefig(
    "aquila_time_waveform.png",
    dpi=200
)

plt.close()


plt.figure(figsize=(12, 5))

mask = (
    (freq >= 50_000) &
    (freq <= 500_000)
)

plt.plot(
    freq[mask] / 1000,
    magnitude[mask]
)

plt.xlabel("Frequency (kHz)")
plt.ylabel("Magnitude")
plt.title("AQUILA DAC Output FFT")

plt.grid(True)
plt.tight_layout()

plt.savefig(
    "aquila_fft.png",
    dpi=200
)

plt.close()


f, t, Sxx = spectrogram(
    signal,
    fs=SAMPLE_RATE,
    nperseg=1024,
    noverlap=896,
    nfft=8192
)

frequency_mask = (
    (f >= 100_000) &
    (f <= 300_000)
)

f_band = f[frequency_mask]
S_band = Sxx[frequency_mask, :]


ridge_indices = np.argmax(S_band, axis=0)

ridge_frequency = f_band[ridge_indices]

power = np.max(S_band, axis=0)

valid = power > (np.max(power) * 0.05)

ridge_frequency_valid = ridge_frequency[valid]
time_valid = t[valid]


start_frequency = ridge_frequency_valid[0]
end_frequency = ridge_frequency_valid[-1]

minimum_frequency = ridge_frequency_valid.min()
maximum_frequency = ridge_frequency_valid.max()

print()
print("-" * 60)
print(" LFM FREQUENCY RIDGE")
print("-" * 60)

print(
    f"Measured start frequency : "
    f"{start_frequency/1000:.2f} kHz"
)

print(
    f"Measured end frequency   : "
    f"{end_frequency/1000:.2f} kHz"
)

print(
    f"Measured minimum         : "
    f"{minimum_frequency/1000:.2f} kHz"
)

print(
    f"Measured maximum         : "
    f"{maximum_frequency/1000:.2f} kHz"
)

print(
    f"Measured sweep           : "
    f"{(end_frequency-start_frequency)/1000:.2f} kHz"
)


plt.figure(figsize=(12, 6))

plt.pcolormesh(
    t * 1000,
    f_band / 1000,
    10 * np.log10(S_band + 1e-12),
    shading="auto"
)

plt.plot(
    time_valid * 1000,
    ridge_frequency_valid / 1000,
    linewidth=2
)

plt.xlabel("Time (ms)")
plt.ylabel("Frequency (kHz)")
plt.title("AQUILA LFM Spectrogram")

plt.colorbar(
    label="Power (dB)"
)

plt.ylim(100, 300)

plt.tight_layout()

plt.savefig(
    "aquila_spectrogram.png",
    dpi=200
)

plt.close()


print()
print("=" * 60)
print(" DIGITAL LFM VALIDATION")
print("=" * 60)

if N == 8000:
    print("PASS: 8000 samples captured")

if abs(N / SAMPLE_RATE - 0.004) < 1e-6:
    print("PASS: 4 ms waveform duration")

if (
    start_frequency > 140_000
    and end_frequency < 260_000
    and end_frequency > start_frequency
):
    print("PASS: LFM frequency sweep detected")
else:
    print("CHECK: LFM frequency sweep")

print()
print("Generated:")
print("  aquila_time_waveform.png")
print("  aquila_fft.png")
print("  aquila_spectrogram.png")

print("=" * 60)
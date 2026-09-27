import numpy as np
import pandas as pd
from scipy.signal import spectrogram


CSV_FILE = "rtl/aquila_lfm_1msps.csv"
FS = 5_000_000
FC_EXPECTED = 300_000
BW_EXPECTED = 80_000
TP_EXPECTED = 0.004     # 4 ms



data = pd.read_csv(CSV_FILE)

samples = data["dac_sample"].to_numpy(dtype=float)

print("==============================================")
print(" AQUILA LFM CAPTURE ANALYSIS")
print("==============================================")

print(f"Samples loaded     : {len(samples)}")
print(f"Sample rate        : {FS/1e6:.3f} MSPS")
print(f"Expected Fc        : {FC_EXPECTED/1e3:.1f} kHz")
print(f"Expected BW        : {BW_EXPECTED/1e3:.1f} kHz")
print(f"Expected duration  : {TP_EXPECTED*1000:.1f} ms")



signal = samples - 2048.0



nperseg = 256
noverlap = 192

frequencies, times, Sxx = spectrogram(
    signal,
    fs=FS,
    window="hann",
    nperseg=nperseg,
    noverlap=noverlap,
    mode="magnitude"
)



peak_indices = np.argmax(Sxx, axis=0)

peak_frequency = frequencies[peak_indices]



peak_magnitude = Sxx[peak_indices, np.arange(len(times))]

threshold = np.max(peak_magnitude) * 0.15

valid = peak_magnitude > threshold

valid_frequency = peak_frequency[valid]
valid_time = times[valid]



if len(valid_frequency) > 0:

    measured_start = valid_frequency[0]
    measured_end = valid_frequency[-1]

    measured_min = np.min(valid_frequency)
    measured_max = np.max(valid_frequency)

    measured_center = (measured_min + measured_max) / 2
    measured_bw = measured_max - measured_min

else:

    measured_start = 0
    measured_end = 0
    measured_center = 0
    measured_bw = 0



print("")
print("----------------------------------------------")
print(" MEASURED LFM RESULTS")
print("----------------------------------------------")

print(
    f"Measured start frequency : "
    f"{measured_start/1e3:.2f} kHz"
)

print(
    f"Measured end frequency   : "
    f"{measured_end/1e3:.2f} kHz"
)

print(
    f"Measured frequency range : "
    f"{measured_min/1e3:.2f} - "
    f"{measured_max/1e3:.2f} kHz"
)

print(
    f"Measured center          : "
    f"{measured_center/1e3:.2f} kHz"
)

print(
    f"Measured bandwidth       : "
    f"{measured_bw/1e3:.2f} kHz"
)



expected_start = FC_EXPECTED - BW_EXPECTED / 2
expected_end = FC_EXPECTED + BW_EXPECTED / 2

print("")
print("----------------------------------------------")
print(" EXPECTED LFM RESULTS")
print("----------------------------------------------")

print(
    f"Expected start frequency : "
    f"{expected_start/1e3:.2f} kHz"
)

print(
    f"Expected end frequency   : "
    f"{expected_end/1e3:.2f} kHz"
)

print(
    f"Expected center          : "
    f"{FC_EXPECTED/1e3:.2f} kHz"
)

print(
    f"Expected bandwidth       : "
    f"{BW_EXPECTED/1e3:.2f} kHz"
)



import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))

plt.pcolormesh(
    times * 1000,
    frequencies / 1000,
    20 * np.log10(Sxx + 1e-12),
    shading="auto"
)

plt.xlabel("Time (ms)")
plt.ylabel("Frequency (kHz)")
plt.title("AQUILA 5 MSPS LFM Spectrogram")

plt.ylim(100, 500)

plt.colorbar(label="Magnitude (dB)")

plt.tight_layout()

plt.savefig(
    "aquila_lfm_spectrogram.png",
    dpi=200
)

plt.show()



start_error = abs(measured_start - expected_start)
end_error = abs(measured_end - expected_end)

print("")
print("==============================================")

if (
    start_error < 10_000
    and end_error < 10_000
):
    print("PASS: LFM FREQUENCY SWEEP VERIFIED")
else:
    print("CHECK: LFM FREQUENCY SWEEP NEEDS REVIEW")

print("==============================================")

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


CSV_FILE = "aquila_lfm_samples.csv"

FS = 5_000_000

EXPECTED_FC = 300_000
EXPECTED_BW = 80_000
EXPECTED_TP = 0.004      # 4 ms

EXPECTED_START = EXPECTED_FC - EXPECTED_BW / 2
EXPECTED_END   = EXPECTED_FC + EXPECTED_BW / 2



data = np.loadtxt(
    CSV_FILE,
    delimiter=",",
    skiprows=1
)

sample_index = data[:, 0]
samples = data[:, 1]

N = len(samples)

time = np.arange(N) / FS



duration = N / FS

print()
print("==============================================")
print(" AQUILA LFM SIGNAL ANALYSIS")
print("==============================================")

print(f"Samples loaded       : {N}")
print(f"Sample rate          : {FS/1e6:.3f} MSPS")
print(f"Measured duration    : {duration*1000:.3f} ms")

print()
print("EXPECTED PARAMETERS")
print(f"Center frequency     : {EXPECTED_FC/1000:.1f} kHz")
print(f"Bandwidth            : {EXPECTED_BW/1000:.1f} kHz")
print(f"Start frequency      : {EXPECTED_START/1000:.1f} kHz")
print(f"End frequency        : {EXPECTED_END/1000:.1f} kHz")
print(f"Pulse duration       : {EXPECTED_TP*1000:.1f} ms")



signal_centered = samples - 2048



window = np.hanning(N)

fft_data = np.fft.rfft(signal_centered * window)

fft_mag = np.abs(fft_data)

freq = np.fft.rfftfreq(N, 1 / FS)



peak_index = np.argmax(fft_mag)

peak_frequency = freq[peak_index]

print()
print("FFT RESULT")
print(f"FFT peak frequency   : {peak_frequency/1000:.2f} kHz")



f, t, Sxx = signal.spectrogram(
    signal_centered,
    fs=FS,
    window="hann",
    nperseg=256,
    noverlap=192,
    mode="magnitude"
)



band_mask = (
    (f >= 100_000) &
    (f <= 500_000)
)

f_band = f[band_mask]
S_band = Sxx[band_mask, :]



ridge_indices = np.argmax(S_band, axis=0)

ridge_frequency = f_band[ridge_indices]


energy = np.max(S_band, axis=0)

threshold = np.max(energy) * 0.20

valid = energy > threshold

measured_start = ridge_frequency[valid][0]
measured_end = ridge_frequency[valid][-1]

measured_center = (
    measured_start + measured_end
) / 2

measured_bandwidth = (
    measured_end - measured_start
)



print()
print("SPECTROGRAM RESULT")

print(
    f"Measured start frequency : "
    f"{measured_start/1000:.2f} kHz"
)

print(
    f"Measured end frequency   : "
    f"{measured_end/1000:.2f} kHz"
)

print(
    f"Measured center          : "
    f"{measured_center/1000:.2f} kHz"
)

print(
    f"Measured bandwidth       : "
    f"{measured_bandwidth/1000:.2f} kHz"
)



center_error = abs(
    measured_center - EXPECTED_FC
)

bandwidth_error = abs(
    measured_bandwidth - EXPECTED_BW
)

duration_error = abs(
    duration - EXPECTED_TP
)


print()
print("ERROR")

print(
    f"Center-frequency error : "
    f"{center_error/1000:.2f} kHz"
)

print(
    f"Bandwidth error        : "
    f"{bandwidth_error/1000:.2f} kHz"
)

print(
    f"Duration error         : "
    f"{duration_error*1e6:.2f} us"
)



print()
print("VERIFICATION")

if N == int(FS * EXPECTED_TP):
    print("PASS: SAMPLE COUNT")

if abs(duration - EXPECTED_TP) < 1e-6:
    print("PASS: PULSE DURATION")

if abs(measured_center - EXPECTED_FC) < 10_000:
    print("PASS: CENTER FREQUENCY")
else:
    print("CHECK: CENTER FREQUENCY")

if abs(measured_bandwidth - EXPECTED_BW) < 15_000:
    print("PASS: BANDWIDTH")
else:
    print("CHECK: BANDWIDTH")



plt.figure()

plt.plot(
    time * 1000,
    samples
)

plt.xlabel("Time (ms)")
plt.ylabel("DAC Code")

plt.title(
    "AQUILA LFM Waveform - RTL Output"
)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "aquila_lfm_time_domain.png",
    dpi=200
)

plt.show()



plt.figure()

plt.plot(
    freq / 1000,
    fft_mag
)

plt.xlim(100, 300)

plt.xlabel("Frequency (kHz)")
plt.ylabel("Magnitude")

plt.title(
    "AQUILA LFM FFT"
)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "aquila_lfm_fft.png",
    dpi=200
)

plt.show()



plt.figure()

plt.pcolormesh(
    t * 1000,
    f_band / 1000,
    20 * np.log10(S_band + 1e-12),
    shading="auto"
)

plt.xlabel("Time (ms)")
plt.ylabel("Frequency (kHz)")

plt.title(
    "AQUILA LFM Spectrogram"
)

plt.ylim(100, 300)

plt.colorbar(
    label="Magnitude (dB)"
)

plt.tight_layout()

plt.savefig(
    "aquila_lfm_spectrogram.png",
    dpi=200
)

plt.show()


print()
print("==============================================")
print(" ANALYSIS COMPLETE")
print("==============================================")
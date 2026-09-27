import numpy as np
import csv

SAMPLE_RATE = 5_000_000


def read_csv(filename, column):
    data = []

    with open(filename, "r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            data.append(float(row[column]))

    return np.array(data)


waveform = read_csv(
    "aquila_waveform_samples.csv",
    "waveform_sample"
)

stream = read_csv(
    "aquila_stream_samples.csv",
    "stream_sample"
)

stream_12 = stream / 16.0

print()
print("=" * 60)
print(" AQUILA WAVEFORM ALIGNMENT TEST")
print("=" * 60)

print(f"Waveform samples : {len(waveform)}")
print(f"Stream samples   : {len(stream_12)}")



a = waveform - np.mean(waveform)
b = stream_12 - np.mean(stream_12)



correlation = np.correlate(a, b, mode="full")

delay = np.argmax(correlation) - (len(b) - 1)

print()
print(f"Detected sample delay : {delay}")



if delay > 0:

    aligned_waveform = waveform[delay:]
    aligned_stream = stream_12[:len(aligned_waveform)]

elif delay < 0:

    aligned_stream = stream_12[-delay:]
    aligned_waveform = waveform[:len(aligned_stream)]

else:

    aligned_waveform = waveform
    aligned_stream = stream_12


length = min(
    len(aligned_waveform),
    len(aligned_stream)
)

aligned_waveform = aligned_waveform[:length]
aligned_stream = aligned_stream[:length]



error = aligned_waveform - aligned_stream

max_error = np.max(np.abs(error))
mean_error = np.mean(np.abs(error))

print()
print("AFTER ALIGNMENT")
print("-" * 60)

print(f"Compared samples : {length}")
print(f"Maximum error    : {max_error:.2f}")
print(f"Mean error       : {mean_error:.2f}")



correlation_coefficient = np.corrcoef(
    aligned_waveform,
    aligned_stream
)[0, 1]

print(
    f"Correlation      : {correlation_coefficient:.6f}"
)



print()
print("=" * 60)

if correlation_coefficient > 0.95:

    print("PASS: STREAM PRESERVES FPGA WAVEFORM")

elif correlation_coefficient > 0.80:

    print("CHECK: STRONG WAVEFORM SIMILARITY")

else:

    print("CHECK: WAVEFORM ALIGNMENT / STREAM PATH")


print("=" * 60)
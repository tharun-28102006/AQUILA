
import numpy as np
import matplotlib.pyplot as plt

from adaptive_lut import build_lut, lookup_profile



def generate_lfm(
    fc,
    bandwidth,
    pulse_duration,
    amplitude,
    sample_rate
):
    """
    Generate a baseband-equivalent LFM chirp.

    fc              : Center frequency in Hz
    bandwidth       : Chirp bandwidth in Hz
    pulse_duration  : Pulse duration in seconds
    amplitude       : Normalized amplitude
    sample_rate     : Samples per second
    """

    num_samples = int(pulse_duration * sample_rate)

    t = np.arange(num_samples) / sample_rate

    f_start = fc - bandwidth / 2
    f_end = fc + bandwidth / 2

    chirp_rate = bandwidth / pulse_duration

    phase = (
        2 * np.pi *
        (
            f_start * t
            + 0.5 * chirp_rate * t**2
        )
    )

    signal = amplitude * np.sin(phase)

    return t, signal, f_start, f_end



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


    print()
    print("==========================================")
    print("        AQUILA LFM WAVEFORM TEST")
    print("==========================================")

    print()
    print("LUT ADDRESS")
    print("------------------------------------------")
    print(f"Address          : 0x{address:02X}")

    print()
    print("TRANSMISSION PROFILE")
    print("------------------------------------------")
    print(f"Center Frequency : {profile.fc:.2f} Hz")
    print(f"Bandwidth        : {profile.bandwidth:.2f} Hz")
    print(f"Pulse Duration   : {profile.pulse_duration:.6f} s")
    print(f"Amplitude        : {profile.amplitude}")
    print(f"Mode             : {profile.mode}")

    print()
    print("LFM PARAMETERS")
    print("------------------------------------------")
    print(f"Start Frequency  : {f_start:.2f} Hz")
    print(f"End Frequency    : {f_end:.2f} Hz")
    print(f"Chirp Rate       : {profile.bandwidth / profile.pulse_duration:.2f} Hz/s")
    print(f"Sample Rate      : {sample_rate} samples/s")
    print(f"Number Samples   : {len(signal)}")


    plt.figure(figsize=(10, 5))

    plt.plot(t * 1000, signal)

    plt.title("AQUILA LFM Chirp")
    plt.xlabel("Time (ms)")
    plt.ylabel("Amplitude")
    plt.grid(True)

    plt.tight_layout()
    plt.show()
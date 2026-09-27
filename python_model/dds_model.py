
import numpy as np
import matplotlib.pyplot as plt

from adaptive_lut import build_lut, lookup_profile



PHASE_BITS = 32

SAMPLE_CLOCK = 5_000_000



def calculate_phase_increment(
    frequency,
    sample_clock,
    phase_bits=PHASE_BITS
):

    phase_increment = round(
        frequency
        * (2 ** phase_bits)
        / sample_clock
    )

    return phase_increment



def generate_dds(
    frequency,
    duration,
    sample_clock,
    phase_bits=PHASE_BITS,
    amplitude=1.0
):

    num_samples = int(
        duration * sample_clock
    )

    phase_increment = calculate_phase_increment(
        frequency,
        sample_clock,
        phase_bits
    )

    phase_accumulator = np.zeros(
        num_samples,
        dtype=np.uint64
    )

    phase_mask = (1 << phase_bits) - 1


    phase = 0

    for i in range(num_samples):

        phase_accumulator[i] = phase

        phase = (
            phase + phase_increment
        ) & phase_mask


    phase_angle = (
        phase_accumulator
        / (2 ** phase_bits)
        * 2
        * np.pi
    )


    signal = amplitude * np.sin(
        phase_angle
    )

    return (
        phase_accumulator,
        signal,
        phase_increment
    )



if __name__ == "__main__":


    lut = build_lut()

    address = 0x55

    result = lookup_profile(
        address,
        lut
    )

    profile = result["profile"]


    frequency = profile.fc

    duration = profile.pulse_duration_us / 1_000_000

    sample_clock = SAMPLE_CLOCK


    (
        phase,
        signal,
        phase_increment
    ) = generate_dds(
        frequency=frequency,
        duration=duration,
        sample_clock=sample_clock,
        amplitude=profile.amplitude
    )


    print()
    print("==========================================")
    print("          AQUILA DDS MODEL")
    print("==========================================")

    print()
    print("DDS CONFIGURATION")
    print("------------------------------------------")

    print(f"Frequency       : {frequency:.2f} Hz")
    print(f"Sample Clock    : {sample_clock} Hz")
    print(f"Phase Bits      : {PHASE_BITS}")
    print(f"Phase Increment : {phase_increment}")


    actual_frequency = (
        phase_increment
        * sample_clock
        / (2 ** PHASE_BITS)
    )

    frequency_error = (
        actual_frequency - frequency
    )

    print(f"Actual Frequency: {actual_frequency:.6f} Hz")
    print(f"Frequency Error : {frequency_error:.6f} Hz")

    print()
    print("PHASE ACCUMULATOR")
    print("------------------------------------------")

    for i in range(10):

        print(
            f"Sample {i:02d} : "
            f"{phase[i]}"
        )


    time = np.arange(
        len(signal)
    ) / sample_clock


    samples_to_show = min(
        100,
        len(signal)
    )

    plt.figure(
        figsize=(10, 5)
    )

    plt.plot(
        time[:samples_to_show] * 1e6,
        signal[:samples_to_show]
    )

    plt.title(
        "AQUILA DDS Generated Waveform"
    )

    plt.xlabel(
        "Time (µs)"
    )

    plt.ylabel(
        "Amplitude"
    )

    plt.grid(True)

    plt.tight_layout()

    plt.show()
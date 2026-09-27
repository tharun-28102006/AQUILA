import numpy as np
from scipy import signal
from config import (
    DAC_BITS,
    DAC_FULL_SCALE_V,
    FILTER_CUTOFF_HZ,
    FILTER_C_FARADS,
    FILTER_R_OHMS,
    LOAD_OHMS,
    OPA2684_GAIN,
    OPA2835_GAIN,
    SAMPLE_RATE_HZ,
)


START_HZ = 260_000
END_HZ = 340_000
PULSE_DURATION_S = 0.004
INPUT_VPEAK = 1.0
FS = SAMPLE_RATE_HZ


def generate_input():
    sample_count = int(FS * PULSE_DURATION_S)
    time = np.arange(sample_count) / FS
    chirp_rate = (END_HZ - START_HZ) / PULSE_DURATION_S
    phase = 2.0 * np.pi * (START_HZ * time + 0.5 * chirp_rate * time ** 2)
    return time, INPUT_VPEAK * np.sin(phase)


def dac_model(signal_v):
    code = np.clip(
        np.round((signal_v / DAC_FULL_SCALE_V + 1.0) * ((1 << DAC_BITS) - 1) / 2.0),
        0,
        (1 << DAC_BITS) - 1,
    )
    return (code / ((1 << DAC_BITS) - 1) * 2.0 - 1.0) * DAC_FULL_SCALE_V


def filter_model(signal_v):
    numerator, denominator = signal.butter(4, FILTER_CUTOFF_HZ, fs=FS)
    return signal.lfilter(numerator, denominator, signal_v)


def response_hz(frequencies):
    numerator, denominator = signal.butter(4, FILTER_CUTOFF_HZ, fs=FS)
    _, response = signal.freqz(numerator, denominator, worN=2.0 * np.pi * np.asarray(frequencies) / FS)
    return response * OPA2835_GAIN * OPA2684_GAIN


def metrics(signal_v):
    vpp = float(np.max(signal_v) - np.min(signal_v))
    vrms = float(np.sqrt(np.mean(signal_v ** 2)))
    return {
        "vpp": vpp,
        "vrms": vrms,
        "ir_ms": vrms / LOAD_OHMS * 1000.0,
        "power_w": vrms ** 2 / LOAD_OHMS,
    }


def main():
    time, fpga_output = generate_input()
    dac_output = dac_model(fpga_output)
    filter_output = filter_model(dac_output)
    amplifier_output = filter_output * OPA2835_GAIN * OPA2684_GAIN
    test_frequencies = np.array([100_000, 200_000, 300_000, 400_000, 500_000, 700_000, 1_000_000])
    response = response_hz(test_frequencies)

    print("SIMULATION / BEHAVIORAL VALIDATION")
    print(f"Samples                 : {len(time)}")
    print(f"Sample rate             : {FS / 1e6:.2f} MSPS")
    print(f"Duration                : {PULSE_DURATION_S * 1e3:.3f} ms")
    print(f"Start frequency         : {START_HZ / 1e3:.1f} kHz")
    print(f"End frequency           : {END_HZ / 1e3:.1f} kHz")
    print(f"AD3541R full scale assumption: {DAC_FULL_SCALE_V:.3f} V peak")
    print(f"Filter RC concept       : {FILTER_R_OHMS:.0f} ohm, {FILTER_C_FARADS * 1e9:.1f} nF")
    print("\nSTAGE METRICS")
    for name, trace in (
        ("FPGA digital equivalent", fpga_output),
        ("AD3541R DAC output", dac_output),
        ("4th-order LPF output", filter_output),
        ("OPA2684 amplifier output", amplifier_output),
    ):
        result = metrics(trace)
        print(f"{name:28s}: Vpp={result['vpp']:.4f} V, RMS={result['vrms']:.4f} V")

    print("\n50 OHM LOAD ESTIMATE")
    load = metrics(amplifier_output)
    print(f"Vpp                     : {load['vpp']:.4f} V")
    print(f"Vrms                    : {load['vrms']:.4f} V")
    print(f"Irms                    : {load['ir_ms']:.3f} mA")
    print(f"Output power estimate   : {load['power_w']:.6f} W")

    print("\nANALOG FREQUENCY RESPONSE")
    for frequency, value in zip(test_frequencies, response):
        print(f"{frequency / 1e3:7.1f} kHz : {20.0 * np.log10(max(abs(value), 1e-12)):8.3f} dB")


if __name__ == "__main__":
    main()

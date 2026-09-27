import csv
from pathlib import Path

import numpy as np

from analog_validation import (
    END_HZ,
    FILTER_CUTOFF_HZ,
    FS,
    LOAD_OHMS,
    OPA2684_GAIN,
    OPA2835_GAIN,
    START_HZ,
    dac_model,
    filter_model,
    generate_input,
    metrics,
    response_hz,
)


OUTPUT_DIR = Path(__file__).resolve().parent


def main():
    time, fpga_output = generate_input()
    dac_output = dac_model(fpga_output)
    filter_output = filter_model(dac_output)
    opa2835_output = filter_output * OPA2835_GAIN
    amplifier_trace = opa2835_output * OPA2684_GAIN
    load_trace = amplifier_trace

    with (OUTPUT_DIR / "aquila_analog_results.csv").open("w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["time_s", "fpga_digital", "dac_output", "filter_output", "opa2835_output", "amplifier_output", "load_voltage"])
        writer.writerows(zip(time, fpga_output, dac_output, filter_output, opa2835_output, amplifier_trace, load_trace))

    frequencies = np.array([100_000, 200_000, 300_000, 400_000, 500_000, 700_000, 1_000_000])
    response = response_hz(frequencies)
    with (OUTPUT_DIR / "aquila_analog_frequency_response.csv").open("w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["frequency_hz", "gain_db"])
        writer.writerows(
            (frequency, 20.0 * np.log10(max(abs(value), 1e-12)))
            for frequency, value in zip(frequencies, response)
        )

    result = metrics(load_trace)
    print("SIMULATION / BEHAVIORAL VALIDATION")
    print(f"Samples                 : {len(time)}")
    print(f"Sample rate             : {FS / 1e6:.2f} MSPS")
    print(f"Duration                : {len(time) / FS * 1e3:.3f} ms")
    print(f"Start frequency         : {START_HZ / 1e3:.1f} kHz")
    print(f"End frequency           : {END_HZ / 1e3:.1f} kHz")
    print(f"Filter cutoff target    : {FILTER_CUTOFF_HZ / 1e3:.1f} kHz")
    print(f"50 ohm Vpp              : {result['vpp']:.4f} V")
    print(f"50 ohm Vrms             : {result['vrms']:.4f} V")
    print(f"50 ohm Irms             : {result['ir_ms']:.3f} mA")
    print(f"50 ohm power estimate   : {result['power_w']:.6f} W")
    print(f"Load                    : {LOAD_OHMS:.1f} ohm")
    print("Traces                   : aquila_analog_results.csv")
    print("Response                 : aquila_analog_frequency_response.csv")


if __name__ == "__main__":
    main()

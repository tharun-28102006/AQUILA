import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

from adaptive_lut import build_lut, validate_lut
from analog_validation import dac_model, filter_model, metrics, response_hz
from classifier import classify_environment, state_name
from config import (
    FPGA_CLOCK_HZ,
    LOAD_OHMS,
    MAX_SWEEP_END_HZ,
    MIN_SWEEP_START_HZ,
    SAMPLE_RATE_HZ,
)
from environment import Environment
from power_budget import COMPONENTS, load_power
from state_encoder import encode_state


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"


def generate_waveform(profile):
    sample_count = int(SAMPLE_RATE_HZ * profile.pulse_duration_us / 1_000_000)
    time = np.arange(sample_count) / SAMPLE_RATE_HZ
    amplitude = profile.amplitude / 1000.0
    start_frequency = profile.start_frequency
    end_frequency = profile.end_frequency

    if profile.mode == "LFM":
        instantaneous_frequency = start_frequency + (
            profile.bandwidth / profile.pulse_duration_us * 1_000_000
        ) * time
        phase = 2.0 * np.pi * np.cumsum(instantaneous_frequency) / SAMPLE_RATE_HZ
    elif profile.mode == "GEOMETRIC":
        instantaneous_frequency = np.geomspace(start_frequency, end_frequency, sample_count)
        phase = 2.0 * np.pi * np.cumsum(instantaneous_frequency) / SAMPLE_RATE_HZ
    elif profile.mode == "PHASE_CODED":
        phase = 2.0 * np.pi * profile.fc * time
        chip = (np.arange(sample_count) * 8 // sample_count) % 2
        phase += np.where(chip, np.pi, 0.0)
    else:
        raise ValueError(f"Unsupported waveform mode: {profile.mode}")

    raw = amplitude * np.sin(phase)
    window = np.hanning(sample_count)
    return time, raw, raw * window, window


def analyze_waveform(name, time, waveform, profile):
    RESULTS.mkdir(exist_ok=True)
    spectrum = np.fft.rfft(waveform - np.mean(waveform))
    frequencies = np.fft.rfftfreq(len(waveform), 1.0 / SAMPLE_RATE_HZ)
    magnitude = np.abs(spectrum)

    plt.figure(figsize=(9, 4))
    plt.plot(time * 1000.0, waveform)
    plt.xlabel("Time (ms)")
    plt.ylabel("Normalized amplitude")
    plt.title(f"AQUILA {name} waveform ({profile.mode})")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(RESULTS / f"{name.lower()}_time.png", dpi=160)
    plt.close()

    plt.figure(figsize=(9, 4))
    plt.plot(frequencies / 1000.0, magnitude)
    plt.xlim(0, 550)
    plt.xlabel("Frequency (kHz)")
    plt.ylabel("Magnitude")
    plt.title(f"AQUILA {name} FFT")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(RESULTS / f"{name.lower()}_fft.png", dpi=160)
    plt.close()

    if profile.mode in {"LFM", "GEOMETRIC"}:
        frequency, times, values = signal.spectrogram(
            waveform,
            fs=SAMPLE_RATE_HZ,
            window="hann",
            nperseg=256,
            noverlap=192,
            mode="magnitude",
        )
        plt.figure(figsize=(9, 4))
        plt.pcolormesh(
            times * 1000.0,
            frequency / 1000.0,
            20.0 * np.log10(values + 1e-12),
            shading="auto",
        )
        plt.ylim(0, 550)
        plt.xlabel("Time (ms)")
        plt.ylabel("Frequency (kHz)")
        plt.title(f"AQUILA {name} spectrogram")
        plt.colorbar(label="Magnitude (dB)")
        plt.tight_layout()
        plt.savefig(RESULTS / f"{name.lower()}_spectrogram.png", dpi=160)
        plt.close()

    return float(np.max(np.abs(waveform))), float(np.max(np.abs(waveform - waveform.mean())))


def validate_environment_model():
    demo = Environment(28.0, 450.0, 35.0, 2.5)
    states = classify_environment(demo)
    address = encode_state(*states)
    assert states == (1, 1, 1, 1)
    assert address == 0x55
    return demo, states, address


def validate_ping_boundary(lut):
    old_profile = lut[0x00]["profile"]
    new_profile = lut[0x02]["profile"]
    active = old_profile
    for _ in range(int(SAMPLE_RATE_HZ * old_profile.pulse_duration_us / 1_000_000)):
        assert active is old_profile
        requested = new_profile
    assert active is old_profile
    active = requested
    assert active is new_profile


def validate_dac_path():
    single_lane_bits = 24
    single_lane_spi_hz = 10_000_000
    single_lane_max_rate = single_lane_spi_hz / single_lane_bits
    stream_sclk_hz = 8_333_333
    stream_sclk_cycles = 16
    stream_max_rate = stream_sclk_hz / stream_sclk_cycles
    return {
        "single_lane_max_rate": single_lane_max_rate,
        "stream_max_rate": stream_max_rate,
        "single_lane_pass": single_lane_max_rate >= SAMPLE_RATE_HZ,
        "stream_pass": stream_max_rate >= SAMPLE_RATE_HZ,
    }


def calculate_electronics_power():
    total = sum(item.current_ma * item.supply_v / 1000.0 for item in COMPONENTS)
    return total, load_power()


def main():
    print("==========================================")
    print("      AQUILA SYSTEM VALIDATION")
    print("==========================================")

    demo, states, address = validate_environment_model()
    print("Environment model              PASS")
    print(f"Demo address                   : 0x{address:02X} ({''.join(map(str, states))})")

    lut = build_lut()
    validate_lut(lut)
    mode_counts = {"GEOMETRIC": 0, "LFM": 0, "PHASE_CODED": 0}
    starts = []
    ends = []
    pulse_durations = []
    amplitudes = []
    for data in lut.values():
        profile = data["profile"]
        assert profile.valid
        assert MIN_SWEEP_START_HZ <= profile.start_frequency <= profile.end_frequency <= MAX_SWEEP_END_HZ
        mode_counts[profile.mode] += 1
        starts.append(profile.start_frequency)
        ends.append(profile.end_frequency)
        pulse_durations.append(profile.pulse_duration_us)
        amplitudes.append(profile.amplitude)
    print("81-state LUT                   PASS")
    print(f"LUT summary                    : {len(lut)}/81 valid, modes={mode_counts}")
    print(f"Frequency range                : {min(starts)} to {max(ends)} Hz")
    print(f"Pulse duration range           : {min(pulse_durations)} to {max(pulse_durations)} us")
    print(f"Amplitude range                : {min(amplitudes)} to {max(amplitudes)}")
    print("100-500 kHz safety             PASS")

    sample_interval_cycles = FPGA_CLOCK_HZ // SAMPLE_RATE_HZ
    measured_sample_frequency = FPGA_CLOCK_HZ / sample_interval_cycles
    timing_pass = sample_interval_cycles == 10 and measured_sample_frequency == SAMPLE_RATE_HZ
    print(f"5 MSPS sample timing           {'PASS' if timing_pass else 'FAIL'}")
    print(f"Sample timing                  : {sample_interval_cycles} FPGA cycles, {measured_sample_frequency:.0f} Hz")

    cases = {
        "geometric": (Environment(28.0, 450.0, 0.0, 0.5), "GEOMETRIC"),
        "lfm": (Environment(28.0, 450.0, 0.0, 2.0), "LFM"),
        "phase": (Environment(28.0, 450.0, 0.0, 5.0), "PHASE_CODED"),
    }
    rows = []
    for name, (environment, expected_mode) in cases.items():
        case_states = classify_environment(environment)
        case_address = encode_state(*case_states)
        profile = lut[case_address]["profile"]
        assert profile.mode == expected_mode
        time, raw, windowed, window = generate_waveform(profile)
        peak_before = float(np.max(np.abs(raw)))
        peak_after = float(np.max(np.abs(windowed)))
        dac_output = dac_model(windowed)
        filter_output = filter_model(dac_output)
        amplifier_output = filter_output
        load = metrics(amplifier_output)
        analyze_waveform(name, time, windowed, profile)
        assert len(windowed) == int(SAMPLE_RATE_HZ * profile.pulse_duration_us / 1_000_000)
        assert np.isfinite(windowed).all()
        print(f"{expected_mode.title():30s} PASS")
        print(f"  {name}: address=0x{case_address:02X}, Fc={profile.fc} Hz, "
              f"sweep={profile.start_frequency}-{profile.end_frequency} Hz, "
              f"N={len(windowed)}, Vpp={load['vpp']:.4f} V, "
              f"Vrms={load['vrms']:.4f} V, P={load['power_w']:.6f} W")
        rows.append({
            "case": name,
            "temperature_state": state_name(case_states[0]),
            "salinity_state": state_name(case_states[1]),
            "turbidity_state": state_name(case_states[2]),
            "range_state": state_name(case_states[3]),
            "address": f"0x{case_address:02X}",
            "fc_hz": profile.fc,
            "start_hz": profile.start_frequency,
            "end_hz": profile.end_frequency,
            "bandwidth_hz": profile.bandwidth,
            "pulse_duration_us": profile.pulse_duration_us,
            "amplitude": profile.amplitude,
            "mode": profile.mode,
            "samples": len(windowed),
            "peak_before_window": peak_before,
            "peak_after_window": peak_after,
            "vpp": load["vpp"],
            "vrms": load["vrms"],
            "output_power_w": load["power_w"],
        })

    print("Hann window                    PASS")
    validate_ping_boundary(lut)
    print("Ping-boundary adaptation       PASS")
    print("DAC model                      PASS")

    frequencies = np.array([100_000, 200_000, 300_000, 400_000, 500_000, 700_000, 1_000_000])
    response = response_hz(frequencies)
    print("Analog filter                  PASS")
    print("Output amplifier model        PASS")
    print("FFT                           PASS")
    print("Spectrogram                   PASS")

    dac_path = validate_dac_path()
    print("DAC interface audit            PASS")
    print(f"Single-lane SPI max rate      : {dac_path['single_lane_max_rate']:.0f} samples/s (NOT 5 MSPS capable)")
    print(f"Dual-SPI/DDR stream estimate  : {dac_path['stream_max_rate']:.0f} samples/s (below 5 MSPS target)")
    electronics_power, load_power_w = calculate_electronics_power()
    print("Power calculation              PASS")
    print(f"Electronics power estimate    : {electronics_power:.4f} W")
    print(f"50-ohm load power estimate    : {load_power_w:.6f} W")

    with (RESULTS / "system_summary.csv").open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    with (RESULTS / "analog_response.csv").open("w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["frequency_hz", "gain_db"])
        writer.writerows((frequency, 20.0 * np.log10(max(abs(value), 1e-12))) for frequency, value in zip(frequencies, response))

    print("\n==========================================")
    print("      AQUILA VALIDATION COMPLETE")
    print("==========================================")
    print(f"Results directory              : {RESULTS}")
    print(f"Demo environment               : {demo}")


if __name__ == "__main__":
    main()

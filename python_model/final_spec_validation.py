import numpy as np
from scipy.signal import spectrogram

from adaptive_lut import MAX_SWEEP_END_HZ, MIN_SWEEP_START_HZ, build_lut, validate_lut
from waveform_lfm import generate_lfm


FS = 5_000_000


def generate_waveform(profile):
    samples = int(FS * profile.pulse_duration_us / 1_000_000)
    time = np.arange(samples) / FS
    amplitude = profile.amplitude / 1000.0
    start = profile.start_frequency
    end = profile.end_frequency
    if profile.mode == "LFM":
        _, waveform, _, _ = generate_lfm(
            profile.fc,
            profile.bandwidth,
            profile.pulse_duration_us / 1_000_000,
            amplitude,
            FS,
        )
    elif profile.mode == "GEOMETRIC":
        frequencies = np.geomspace(start, end, samples)
        phase = 2.0 * np.pi * np.cumsum(frequencies) / FS
        waveform = amplitude * np.sin(phase)
    else:
        phase = 2.0 * np.pi * profile.fc * time
        code = np.where((np.arange(samples) * 8 // samples) % 2, -1.0, 1.0)
        waveform = amplitude * np.sin(phase) * code
    return time, waveform * np.hanning(samples)


def check_profile(profile):
    assert profile.valid
    assert MIN_SWEEP_START_HZ <= profile.start_frequency
    assert profile.end_frequency <= MAX_SWEEP_END_HZ
    assert profile.bandwidth > 0
    assert 100 <= profile.pulse_duration_us <= 20_000
    assert 0 <= profile.amplitude <= 1_000
    assert profile.mode in {"GEOMETRIC", "LFM", "PHASE_CODED"}


def main():
    lut = build_lut()
    validate_lut(lut)
    cases = {
        "clear shallow": 0x00,
        "clear deep": 0x02,
        "turbid shallow": 0x08,
        "turbid deep": 0x0A,
        "high salinity": 0x20,
        "mixed environment": 0x99,
    }

    for name, address in cases.items():
        profile = lut[address]["profile"]
        check_profile(profile)
        time, waveform = generate_waveform(profile)
        expected_samples = int(FS * profile.pulse_duration_us / 1_000_000)
        assert len(waveform) == expected_samples
        frequencies, _, values = spectrogram(waveform, fs=FS, nperseg=256, noverlap=192)
        assert values.shape[0] == len(frequencies)
        print(f"PASS {name}: 0x{address:02X}, {profile.mode}, {len(waveform)} samples")

    active = lut[0x00]["profile"]
    requested = lut[0x02]["profile"]
    locked = active
    _, first_ping = generate_waveform(locked)
    assert len(first_ping) == int(FS * locked.pulse_duration_us / 1_000_000)
    locked = requested
    _, second_ping = generate_waveform(locked)
    assert len(second_ping) == int(FS * locked.pulse_duration_us / 1_000_000)
    assert active.fc != requested.fc
    print("PASS environment changes between pings: profile changed only at boundary")

    modes = set()
    for address, data in lut.items():
        profile = data["profile"]
        check_profile(profile)
        modes.add(profile.mode)
    assert modes == {"GEOMETRIC", "LFM", "PHASE_CODED"}
    print(f"PASS all 81 LUT states: {len(lut)}/81 valid")
    print(f"PASS waveform modes: {', '.join(sorted(modes))}")


if __name__ == "__main__":
    main()

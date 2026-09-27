from itertools import product
import csv
from config import (
    MAX_SWEEP_END_HZ,
    MIN_SWEEP_START_HZ,
)


MIN_USABLE_BW_HZ = 5_000
MAX_BW_HZ = 200_000
MIN_PULSE_DURATION_US = 100
MAX_PULSE_DURATION_US = 20_000
MAX_AMPLITUDE = 1_000

SAFE_FALLBACK = {
    "fc": 300_000,
    "bandwidth": 20_000,
    "pulse_duration_us": 4_000,
    "amplitude": 600,
    "mode": "GEOMETRIC",
}


class TransmissionProfile:
    def __init__(
        self,
        fc,
        bandwidth,
        pulse_duration_us,
        amplitude,
        mode,
        valid=True,
        fallback=False,
        reason="VALID",
    ):
        self.fc = fc
        self.bandwidth = bandwidth
        self.pulse_duration_us = pulse_duration_us
        self.amplitude = amplitude
        self.mode = mode
        self.valid = valid
        self.fallback = fallback
        self.reason = reason

    @property
    def start_frequency(self):
        return self.fc - self.bandwidth // 2

    @property
    def end_frequency(self):
        return self.fc + self.bandwidth // 2

    def __repr__(self):
        status = "VALID" if not self.fallback else f"FALLBACK ({self.reason})"
        return (
            f"Fc={self.fc} Hz, BW={self.bandwidth} Hz, "
            f"Tp={self.pulse_duration_us} us, A={self.amplitude}, "
            f"Mode={self.mode}, {status}"
        )


def get_range_profile(range_state):
    profiles = {
        0: (400_000, 80_000, 2_000, 600, "GEOMETRIC"),
        1: (300_000, 80_000, 4_000, 800, "LFM"),
        2: (180_000, 60_000, 8_000, 1_000, "PHASE_CODED"),
    }
    return profiles[range_state]


def generate_profile(temperature, salinity, turbidity, range_state):
    fc, bandwidth, pulse_duration, amplitude, mode = get_range_profile(range_state)

    if temperature == 0:
        fc *= 1.05
    elif temperature == 2:
        fc *= 0.95

    if salinity == 0:
        fc *= 1.02
    elif salinity == 2:
        fc *= 0.98

    if turbidity == 2:
        bandwidth *= 0.80

    fc = int(fc)
    bandwidth = int(bandwidth)
    start_frequency = fc - bandwidth // 2
    end_frequency = fc + bandwidth // 2

    reason = "VALID"
    if bandwidth < MIN_USABLE_BW_HZ:
        reason = "BW_TOO_SMALL"
    elif bandwidth > MAX_BW_HZ:
        reason = "BW_TOO_LARGE"
    elif start_frequency < MIN_SWEEP_START_HZ:
        reason = "FREQ_TOO_LOW"
    elif end_frequency > MAX_SWEEP_END_HZ:
        reason = "FREQ_TOO_HIGH"
    elif not MIN_PULSE_DURATION_US <= pulse_duration <= MAX_PULSE_DURATION_US:
        reason = "PULSE_DURATION_LIMIT"
    elif amplitude > MAX_AMPLITUDE:
        reason = "AMPLITUDE_LIMIT"
    elif mode not in {"GEOMETRIC", "LFM", "PHASE_CODED"}:
        reason = "INVALID_MODE"

    if reason != "VALID":
        return TransmissionProfile(
            SAFE_FALLBACK["fc"],
            SAFE_FALLBACK["bandwidth"],
            SAFE_FALLBACK["pulse_duration_us"],
            SAFE_FALLBACK["amplitude"],
            SAFE_FALLBACK["mode"],
            valid=False,
            fallback=True,
            reason=reason,
        )

    return TransmissionProfile(
        fc, bandwidth, pulse_duration, amplitude, mode, valid=True, fallback=False
    )


def build_lut():
    lut = {}
    state_number = 0
    for temperature, salinity, turbidity, range_state in product(range(3), repeat=4):
        address = (
            (temperature << 6)
            | (salinity << 4)
            | (turbidity << 2)
            | range_state
        )
        lut[address] = {
            "state_number": state_number,
            "temperature": temperature,
            "salinity": salinity,
            "turbidity": turbidity,
            "range": range_state,
            "profile": generate_profile(
                temperature, salinity, turbidity, range_state
            ),
        }
        state_number += 1
    return lut


def lookup_profile(address, lut):
    if address not in lut:
        raise ValueError(f"Invalid AQUILA LUT address: 0x{address:02X}")
    return lut[address]


def save_lut_csv(lut, filename="adaptive_lut_reference.csv"):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "address", "state_number", "temperature", "salinity", "turbidity",
            "range", "fc_hz", "bandwidth_hz", "pulse_duration_us", "amplitude",
            "mode", "valid", "fallback", "reason",
        ])
        for address, data in sorted(lut.items()):
            profile = data["profile"]
            writer.writerow([
                f"0x{address:02X}", data["state_number"], data["temperature"],
                data["salinity"], data["turbidity"], data["range"], profile.fc,
                profile.bandwidth, profile.pulse_duration_us, profile.amplitude,
                profile.mode, profile.valid, profile.fallback, profile.reason,
            ])


def validate_lut(lut):
    if len(lut) != 81:
        raise ValueError(f"Expected 81 LUT states, found {len(lut)}")
    invalid = []
    for address, data in lut.items():
        profile = data["profile"]
        if not profile.valid:
            invalid.append((address, profile.reason))
        if profile.start_frequency < MIN_SWEEP_START_HZ:
            invalid.append((address, "start_frequency"))
        if profile.end_frequency > MAX_SWEEP_END_HZ:
            invalid.append((address, "end_frequency"))
    if invalid:
        raise ValueError(f"Invalid LUT profiles: {invalid}")


if __name__ == "__main__":
    lut = build_lut()
    validate_lut(lut)
    save_lut_csv(lut)
    print(f"LUT states        : {len(lut)}")
    print("Valid profiles    : 81/81")
    print(f"Sweep start range : {MIN_SWEEP_START_HZ} Hz minimum")
    print(f"Sweep end range   : {MAX_SWEEP_END_HZ} Hz maximum")

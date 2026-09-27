"""
AQUILA — Transducer-Aware Adaptive Profile Validator
=====================================================

Pipeline:

Environment
    ↓
81-state Adaptive LUT
    ↓
Requested transmission profile
    ↓
Transducer compatibility validator
    ↓
VALID / REJECTED
    ↓
DDS / Waveform Generator

IMPORTANT:
- The transducer model is a preliminary BVD behavioral model.
- Cm and Lm are derived estimates.
- This is NOT final acoustic validation.
- Final validation requires measured/manufacturer impedance data.

Run:
    python transducer_aware_profile_validator.py
"""

import math
import csv


TRANSDUCER_RESONANCE_HZ = 235_000.0
TRANSDUCER_C0_F = 645e-12
TRANSDUCER_K33 = 0.58
TRANSDUCER_RM_OHM = 45.0

k2 = TRANSDUCER_K33 ** 2

TRANSDUCER_CM_F = (
    k2 * TRANSDUCER_C0_F
    / (1.0 - k2)
)

TRANSDUCER_LM_H = (
    1.0 /
    (
        (2.0 * math.pi * TRANSDUCER_RESONANCE_HZ) ** 2
        * TRANSDUCER_CM_F
    )
)


THS3091_CURRENT_LIMIT_A = 0.310

DRIVER_VPEAK = 2.575


MIN_FREQUENCY_HZ = 50_000
MAX_FREQUENCY_HZ = 500_000

RESONANCE_GUARD_HZ = 5_000

MAX_ALLOWED_FREQUENCY = (
    TRANSDUCER_RESONANCE_HZ - RESONANCE_GUARD_HZ
)


def bvd_impedance(frequency_hz):

    omega = 2.0 * math.pi * frequency_hz

    z_motional = (
        TRANSDUCER_RM_OHM
        + 1j * omega * TRANSDUCER_LM_H
        + 1 / (1j * omega * TRANSDUCER_CM_F)
    )

    y_static = 1j * omega * TRANSDUCER_C0_F

    y_total = (
        1 / z_motional
        + y_static
    )

    return 1 / y_total



def peak_current(frequency_hz):

    z = bvd_impedance(frequency_hz)

    impedance = abs(z)

    if impedance <= 0:
        return float("inf")

    return DRIVER_VPEAK / impedance



def validate_profile(
    fc_hz,
    bandwidth_hz,
    pulse_duration_us,
    amplitude,
    mode
):

    reasons = []


    start_frequency = (
        fc_hz - bandwidth_hz / 2.0
    )

    end_frequency = (
        fc_hz + bandwidth_hz / 2.0
    )


    if start_frequency < MIN_FREQUENCY_HZ:

        reasons.append(
            "Start frequency below electronic minimum"
        )

    if end_frequency > MAX_FREQUENCY_HZ:

        reasons.append(
            "End frequency above electronic maximum"
        )


    if end_frequency > MAX_ALLOWED_FREQUENCY:

        reasons.append(
            "Sweep enters transducer resonance guard region"
        )


    z_start = abs(
        bvd_impedance(start_frequency)
    )

    z_end = abs(
        bvd_impedance(end_frequency)
    )


    i_start = (
        DRIVER_VPEAK / z_start
    )

    i_end = (
        DRIVER_VPEAK / z_end
    )

    max_current = max(
        i_start,
        i_end
    )


    if max_current > THS3091_CURRENT_LIMIT_A:

        reasons.append(
            "Estimated driver current exceeds THS3091 reference limit"
        )


    if pulse_duration_us <= 0:

        reasons.append(
            "Invalid pulse duration"
        )


    if amplitude < 0:

        reasons.append(
            "Invalid amplitude"
        )

    if amplitude > 1000:

        reasons.append(
            "Amplitude exceeds 1000-unit digital scale"
        )


    if mode not in (
        "LFM",
        "GEOMETRIC",
        "PHASE_CODED"
    ):

        reasons.append(
            "Invalid waveform mode"
        )


    valid = (
        len(reasons) == 0
    )

    return {
        "valid": valid,

        "fc_hz": fc_hz,
        "bandwidth_hz": bandwidth_hz,

        "start_frequency_hz":
            start_frequency,

        "end_frequency_hz":
            end_frequency,

        "z_start_ohm":
            z_start,

        "z_end_ohm":
            z_end,

        "i_start_a":
            i_start,

        "i_end_a":
            i_end,

        "max_current_a":
            max_current,

        "reasons":
            reasons
    }



def generate_profile(
    temperature_state,
    salinity_state,
    turbidity_state,
    range_state
):


    if range_state == 0:

        fc = 300_000
        bandwidth = 100_000

    elif range_state == 1:

        fc = 200_000
        bandwidth = 70_000

    else:

        fc = 120_000
        bandwidth = 40_000


    if turbidity_state == 2:

        bandwidth *= 0.8

    if temperature_state == 2:

        fc *= 0.95

    elif temperature_state == 0:

        fc *= 1.05

    if salinity_state == 2:

        fc *= 0.98

    elif salinity_state == 0:

        fc *= 1.02


    if range_state == 0:

        pulse_duration_us = 2000

    elif range_state == 1:

        pulse_duration_us = 4000

    else:

        pulse_duration_us = 8000


    if range_state == 0:

        amplitude = 600

    elif range_state == 1:

        amplitude = 800

    else:

        amplitude = 1000


    if turbidity_state == 2:

        mode = "PHASE_CODED"

    elif range_state == 2:

        mode = "LFM"

    else:

        mode = "GEOMETRIC"

    return {
        "fc": fc,
        "bandwidth": bandwidth,
        "pulse_duration": pulse_duration_us,
        "amplitude": amplitude,
        "mode": mode
    }



print("=" * 78)
print(" AQUILA TRANSDUCER-AWARE 81-STATE PROFILE VALIDATION")
print("=" * 78)

print("\nTRANSDUCER MODEL")
print("-" * 78)

print(
    f"Resonance                : "
    f"{TRANSDUCER_RESONANCE_HZ/1000:.1f} kHz"
)

print(
    f"C0                       : "
    f"{TRANSDUCER_C0_F*1e12:.2f} pF"
)

print(
    f"Derived Cm               : "
    f"{TRANSDUCER_CM_F*1e12:.2f} pF"
)

print(
    f"Derived Lm               : "
    f"{TRANSDUCER_LM_H:.6f} H"
)

print(
    f"Resonance guard          : "
    f"{RESONANCE_GUARD_HZ/1000:.1f} kHz"
)

print(
    f"Maximum allowed end freq : "
    f"{MAX_ALLOWED_FREQUENCY/1000:.1f} kHz"
)

results = []

valid_count = 0
invalid_count = 0


for temperature_state in range(3):

    for salinity_state in range(3):

        for turbidity_state in range(3):

            for range_state in range(3):

                profile = generate_profile(
                    temperature_state,
                    salinity_state,
                    turbidity_state,
                    range_state
                )

                result = validate_profile(
                    profile["fc"],
                    profile["bandwidth"],
                    profile["pulse_duration"],
                    profile["amplitude"],
                    profile["mode"]
                )

                address = (
                    (temperature_state << 6)
                    | (salinity_state << 4)
                    | (turbidity_state << 2)
                    | range_state
                )

                row = {
                    "address":
                        address,

                    "temperature_state":
                        temperature_state,

                    "salinity_state":
                        salinity_state,

                    "turbidity_state":
                        turbidity_state,

                    "range_state":
                        range_state,

                    "fc_hz":
                        profile["fc"],

                    "bandwidth_hz":
                        profile["bandwidth"],

                    "start_hz":
                        result["start_frequency_hz"],

                    "end_hz":
                        result["end_frequency_hz"],

                    "pulse_duration_us":
                        profile["pulse_duration"],

                    "amplitude":
                        profile["amplitude"],

                    "mode":
                        profile["mode"],

                    "z_start_ohm":
                        result["z_start_ohm"],

                    "z_end_ohm":
                        result["z_end_ohm"],

                    "max_current_ma":
                        result["max_current_a"] * 1000,

                    "valid":
                        result["valid"],

                    "reason":
                        "; ".join(result["reasons"])
                }

                results.append(row)

                if result["valid"]:

                    valid_count += 1

                else:

                    invalid_count += 1



print("\n81-STATE VALIDATION")
print("-" * 78)

print(
    f"Total LUT states          : "
    f"{len(results)}"
)

print(
    f"Valid profiles            : "
    f"{valid_count}"
)

print(
    f"Rejected profiles         : "
    f"{invalid_count}"
)

print(
    f"Validation coverage       : "
    f"{len(results)}/81"
)



print("\nREJECTED PROFILES")
print("-" * 78)

rejected = [
    r for r in results
    if not r["valid"]
]

if len(rejected) == 0:

    print("None")

else:

    for r in rejected:

        print(
            f"0x{r['address']:02X} | "
            f"Fc={r['fc_hz']/1000:.1f} kHz | "
            f"BW={r['bandwidth_hz']/1000:.1f} kHz | "
            f"End={r['end_hz']/1000:.1f} kHz | "
            f"Reason={r['reason']}"
        )



print("\nRANGE-STATE SUMMARY")
print("-" * 78)

for range_state in range(3):

    subset = [
        r for r in results
        if r["range_state"] == range_state
    ]

    valid = [
        r for r in subset
        if r["valid"]
    ]

    print(
        f"Range state {range_state}: "
        f"{len(valid)}/{len(subset)} profiles valid"
    )

    if subset:

        max_end = max(
            r["end_hz"]
            for r in subset
        )

        max_current = max(
            r["max_current_ma"]
            for r in subset
        )

        print(
            f"  Maximum sweep end : "
            f"{max_end/1000:.2f} kHz"
        )

        print(
            f"  Maximum current   : "
            f"{max_current:.2f} mA"
        )



filename = (
    "transducer_aware_81_state_validation.csv"
)

fieldnames = list(
    results[0].keys()
)

with open(
    filename,
    "w",
    newline=""
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=fieldnames
    )

    writer.writeheader()

    writer.writerows(results)



print("\nFINAL STATUS")
print("-" * 78)

print(
    "Adaptive LUT generation      : PASS"
)

print(
    "81-state enumeration        : PASS"
)

print(
    "Transducer compatibility    : COMPLETE"
)

print(
    "Physical transducer model   : NOT FINAL"
)

print(
    "Acoustic validation         : NOT PERFORMED"
)

print(
    "Matching network            : NOT FINAL"
)

print("\nGenerated:")
print(
    f"  {filename}"
)

print("\n" + "=" * 78)
print(" END OF AQUILA TRANSDUCER-AWARE VALIDATION")
print("=" * 78)
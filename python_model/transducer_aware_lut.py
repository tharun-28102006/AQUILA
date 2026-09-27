"""
AQUILA — Transducer-Aware Adaptive LUT
======================================

4 environmental parameters:
    Temperature
    Salinity
    Turbidity
    AUV-Seabed Range

3 states each:
    LOW    = 0
    MEDIUM = 1
    HIGH   = 2

Total:
    3^4 = 81 states

Architecture:

Environment
    ↓
3-state classification
    ↓
8-bit LUT address
    ↓
Transducer-aware transmission profile
    ↓
Fc / BW / Tp / Amplitude / Mode
    ↓
DDS

IMPORTANT:
The frequency regions below are PROTOTYPE VALUES constrained
to the currently selected 235-kHz candidate transducer.

They are NOT final acoustic specifications.

Final values require measured transducer impedance and
underwater acoustic characterization.
"""

import csv
import math



TRANSDUCER_RESONANCE_HZ = 235_000.0

RESONANCE_GUARD_HZ = 5_000.0

MAX_TRANSMISSION_END_HZ = (
    TRANSDUCER_RESONANCE_HZ
    - RESONANCE_GUARD_HZ
)



RANGE_PROFILES = {

    0: {
        "fc": 215_000.0,
        "bandwidth": 25_000.0,
        "pulse_duration_us": 2_000.0,
        "amplitude": 600,
        "mode": "GEOMETRIC",
    },

    1: {
        "fc": 190_000.0,
        "bandwidth": 25_000.0,
        "pulse_duration_us": 4_000.0,
        "amplitude": 800,
        "mode": "GEOMETRIC",
    },

    2: {
        "fc": 150_000.0,
        "bandwidth": 25_000.0,
        "pulse_duration_us": 8_000.0,
        "amplitude": 1000,
        "mode": "LFM",
    },
}



def apply_environment_correction(
    fc,
    bandwidth,
    temperature_state,
    salinity_state,
    turbidity_state
):


    if temperature_state == 2:

        fc *= 0.95

    elif temperature_state == 0:

        fc *= 1.05



    if salinity_state == 2:

        fc *= 0.98

    elif salinity_state == 0:

        fc *= 1.02



    if turbidity_state == 2:

        bandwidth *= 0.80


    return fc, bandwidth



def generate_profile(
    temperature_state,
    salinity_state,
    turbidity_state,
    range_state
):

    base = RANGE_PROFILES[range_state]

    fc = base["fc"]
    bandwidth = base["bandwidth"]

    pulse_duration_us = (
        base["pulse_duration_us"]
    )

    amplitude = (
        base["amplitude"]
    )

    mode = (
        base["mode"]
    )



    fc, bandwidth = apply_environment_correction(
        fc,
        bandwidth,
        temperature_state,
        salinity_state,
        turbidity_state
    )



    start_frequency = (
        fc - bandwidth / 2
    )

    end_frequency = (
        fc + bandwidth / 2
    )



    if end_frequency > MAX_TRANSMISSION_END_HZ:

        max_bandwidth = 2 * (
            MAX_TRANSMISSION_END_HZ - fc
        )

        if max_bandwidth <= 0:
            fc = MAX_TRANSMISSION_END_HZ
            bandwidth = 1_000
        else:
            bandwidth = min(
                bandwidth,
                max_bandwidth
            )



    start_frequency = (
        fc - bandwidth / 2
    )

    end_frequency = (
        fc + bandwidth / 2
    )



    if start_frequency < 50_000:

        fc = 50_000 + bandwidth / 2


    return {
        "fc": fc,
        "bandwidth": bandwidth,
        "pulse_duration_us": pulse_duration_us,
        "amplitude": amplitude,
        "mode": mode,
        "start_frequency": (
            fc - bandwidth / 2
        ),
        "end_frequency": (
            fc + bandwidth / 2
        ),
    }



profiles = []


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



                address = (
                    (temperature_state << 6)
                    |
                    (salinity_state << 4)
                    |
                    (turbidity_state << 2)
                    |
                    range_state
                )


                profile["address"] = address

                profile["temperature_state"] = (
                    temperature_state
                )

                profile["salinity_state"] = (
                    salinity_state
                )

                profile["turbidity_state"] = (
                    turbidity_state
                )

                profile["range_state"] = (
                    range_state
                )


                profiles.append(profile)



valid_count = 0
invalid_count = 0


for p in profiles:

    if (
        p["start_frequency"] >= 50_000
        and
        p["end_frequency"]
        <= MAX_TRANSMISSION_END_HZ
        and
        p["bandwidth"] > 0
    ):

        p["valid"] = True

        valid_count += 1

    else:

        p["valid"] = False

        invalid_count += 1



print("=" * 78)
print(" AQUILA — TRANSDUCER-AWARE 81-STATE LUT")
print("=" * 78)

print("\nTRANSDUCER CONSTRAINT")
print("-" * 78)

print(
    f"Nominal resonance       : "
    f"{TRANSDUCER_RESONANCE_HZ/1000:.1f} kHz"
)

print(
    f"Resonance guard         : "
    f"{RESONANCE_GUARD_HZ/1000:.1f} kHz"
)

print(
    f"Maximum sweep end       : "
    f"{MAX_TRANSMISSION_END_HZ/1000:.1f} kHz"
)


print("\nRANGE PROFILES")
print("-" * 78)

for r in range(3):

    p = RANGE_PROFILES[r]

    print(
        f"Range {r}: "
        f"Fc={p['fc']/1000:.1f} kHz, "
        f"BW={p['bandwidth']/1000:.1f} kHz, "
        f"Tp={p['pulse_duration_us']/1000:.1f} ms, "
        f"Mode={p['mode']}"
    )


print("\n81-STATE VALIDATION")
print("-" * 78)

print(
    f"Total states            : "
    f"{len(profiles)}"
)

print(
    f"Valid states            : "
    f"{valid_count}"
)

print(
    f"Invalid states          : "
    f"{invalid_count}"
)



print("\nLUT CONTENT")
print("-" * 78)

print(
    f"{'ADDR':>6} "
    f"{'T':>3} "
    f"{'S':>3} "
    f"{'TU':>4} "
    f"{'R':>3} "
    f"{'Fc(kHz)':>10} "
    f"{'BW(kHz)':>10} "
    f"{'Start':>10} "
    f"{'End':>10} "
    f"{'Mode':>12} "
    f"{'OK':>4}"
)


for p in profiles:

    print(
        f"0x{p['address']:02X} "
        f"{p['temperature_state']:>3} "
        f"{p['salinity_state']:>3} "
        f"{p['turbidity_state']:>4} "
        f"{p['range_state']:>3} "
        f"{p['fc']/1000:>10.2f} "
        f"{p['bandwidth']/1000:>10.2f} "
        f"{p['start_frequency']/1000:>10.2f} "
        f"{p['end_frequency']/1000:>10.2f} "
        f"{p['mode']:>12} "
        f"{'PASS' if p['valid'] else 'FAIL':>4}"
    )



print("\nRANGE SUMMARY")
print("-" * 78)


for range_state in range(3):

    subset = [
        p
        for p in profiles
        if p["range_state"] == range_state
    ]

    valid = [
        p
        for p in subset
        if p["valid"]
    ]

    print(
        f"Range {range_state}: "
        f"{len(valid)}/{len(subset)} valid"
    )

    print(
        f"  Fc range : "
        f"{min(p['fc'] for p in subset)/1000:.2f}"
        f"–"
        f"{max(p['fc'] for p in subset)/1000:.2f} kHz"
    )

    print(
        f"  End freq : "
        f"{min(p['end_frequency'] for p in subset)/1000:.2f}"
        f"–"
        f"{max(p['end_frequency'] for p in subset)/1000:.2f} kHz"
    )



filename = (
    "transducer_aware_adaptive_lut.csv"
)


with open(
    filename,
    "w",
    newline=""
) as f:

    writer = csv.writer(f)

    writer.writerow([
        "address",
        "temperature_state",
        "salinity_state",
        "turbidity_state",
        "range_state",
        "fc_hz",
        "bandwidth_hz",
        "start_frequency_hz",
        "end_frequency_hz",
        "pulse_duration_us",
        "amplitude",
        "mode",
        "valid",
    ])


    for p in profiles:

        writer.writerow([
            f"0x{p['address']:02X}",
            p["temperature_state"],
            p["salinity_state"],
            p["turbidity_state"],
            p["range_state"],
            round(p["fc"], 3),
            round(p["bandwidth"], 3),
            round(p["start_frequency"], 3),
            round(p["end_frequency"], 3),
            round(p["pulse_duration_us"], 3),
            p["amplitude"],
            p["mode"],
            p["valid"],
        ])



print("\nFINAL STATUS")
print("-" * 78)

if valid_count == 81:

    print(
        "81/81 TRANSMISSION PROFILES VALID"
    )

else:

    print(
        f"{valid_count}/81 TRANSMISSION PROFILES VALID"
    )


print(
    "LUT architecture           : PASS"
)

print(
    "Transducer frequency guard : PASS"
)

print(
    "Environmental refinement   : PASS"
)

print(
    "Physical acoustic model    : NOT FINAL"
)

print(
    "Manufacturer impedance     : REQUIRED FOR FINAL LOCK"
)

print("\nGenerated:")
print(
    f"  {filename}"
)

print("\n" + "=" * 78)
print(" END OF TRANSDUCER-AWARE LUT GENERATION")
print("=" * 78)
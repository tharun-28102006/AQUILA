
NOMINAL_RESONANCE_HZ = 235_000
GUARD_HZ = 5_000

MAX_SWEEP_END_HZ = NOMINAL_RESONANCE_HZ - GUARD_HZ
MIN_USABLE_BW_HZ = 5_000

MIN_FREQ_HZ = 50_000
MAX_FREQ_HZ = 500_000

SAFE_FALLBACK = {
    "fc": 200_000,
    "bw": 20_000,
    "tp_us": 4_000,
    "amp": 600,
    "mode": "GEOMETRIC"
}


def clamp(value, low, high):
    return max(low, min(value, high))


def get_range_profile(r):
    if r == 0:       # NEAR
        return 215_000, 25_000, 2_000, 600, "GEOMETRIC"

    elif r == 1:     # MEDIUM
        return 190_000, 25_000, 4_000, 800, "GEOMETRIC"

    else:            # FAR
        return 150_000, 25_000, 8_000, 1000, "LFM"


def generate_profile(t, s, turb, r):

    fc, bw, tp, amp, mode = get_range_profile(r)

    if t == 2:
        fc *= 0.95
    elif t == 0:
        fc *= 1.05

    if s == 2:
        fc *= 0.98
    elif s == 0:
        fc *= 1.02

    if turb == 2:
        bw *= 0.80

    fc = int(fc)
    bw = int(bw)


    start_freq = fc - bw // 2
    end_freq = fc + bw // 2

    if start_freq < MIN_FREQ_HZ:
        fc += MIN_FREQ_HZ - start_freq

    end_freq = fc + bw // 2

    if end_freq > MAX_SWEEP_END_HZ:
        fc = MAX_SWEEP_END_HZ - bw // 2

    start_freq = fc - bw // 2
    end_freq = fc + bw // 2


    valid = True
    reason = "VALID"

    if bw < MIN_USABLE_BW_HZ:
        valid = False
        reason = "BW_TOO_SMALL"

    elif start_freq < MIN_FREQ_HZ:
        valid = False
        reason = "FREQ_TOO_LOW"

    elif end_freq > MAX_SWEEP_END_HZ:
        valid = False
        reason = "TRANSDUCER_LIMIT"

    elif fc + bw // 2 > MAX_FREQ_HZ:
        valid = False
        reason = "SYSTEM_LIMIT"


    if not valid:

        return {
            "fc": SAFE_FALLBACK["fc"],
            "bw": SAFE_FALLBACK["bw"],
            "tp_us": SAFE_FALLBACK["tp_us"],
            "amp": SAFE_FALLBACK["amp"],
            "mode": SAFE_FALLBACK["mode"],
            "valid": False,
            "fallback": True,
            "reason": reason
        }

    return {
        "fc": fc,
        "bw": bw,
        "tp_us": tp,
        "amp": amp,
        "mode": mode,
        "valid": True,
        "fallback": False,
        "reason": "VALID"
    }



lut = {}

valid_count = 0
fallback_count = 0

for t in range(3):
    for s in range(3):
        for turb in range(3):
            for r in range(3):

                address = (
                    (t << 6)
                    | (s << 4)
                    | (turb << 2)
                    | r
                )

                profile = generate_profile(t, s, turb, r)

                lut[address] = profile

                if profile["valid"]:
                    valid_count += 1
                else:
                    fallback_count += 1



print("=" * 70)
print("AQUILA TRANSDUCER-AWARE SAFE LUT")
print("=" * 70)

print(f"Total states       : {len(lut)}")
print(f"Valid profiles     : {valid_count}")
print(f"Fallback profiles  : {fallback_count}")
print(f"Minimum usable BW  : {MIN_USABLE_BW_HZ} Hz")
print(f"Maximum sweep end  : {MAX_SWEEP_END_HZ} Hz")
print()

for address in sorted(lut):

    p = lut[address]

    print(
        f"0x{address:02X} | "
        f"Fc={p['fc']:6d} Hz | "
        f"BW={p['bw']:6d} Hz | "
        f"Tp={p['tp_us']:5d} us | "
        f"A={p['amp']:4d} | "
        f"{p['mode']:10s} | "
        f"{'VALID' if p['valid'] else 'FALLBACK'}"
        f"{' (' + p['reason'] + ')' if not p['valid'] else ''}"
    )
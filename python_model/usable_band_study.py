"""
AQUILA — Transducer Usable-Band Study
=====================================
Compares candidate LFM operating bands against the preliminary
BVD transducer model.

IMPORTANT:
- BVD parameters are derived estimates, not manufacturer values.
- This study is for engineering screening only.
- It does NOT establish acoustic response.
- Final band selection requires measured/manufacturer impedance data.

Outputs:
    aquila_usable_band_study.csv
    aquila_usable_band_impedance.png
    aquila_usable_band_current.png
"""

import csv
import numpy as np
import matplotlib.pyplot as plt

FR = 235e3
C0 = 645e-12
K33 = 0.58
RM = 45.0

K2 = K33**2
CM = (K2 * C0) / (1.0 - K2)
LM = 1.0 / ((2 * np.pi * FR)**2 * CM)

V_PEAK = 2.575

F = np.linspace(100e3, 300e3, 20001)
W = 2 * np.pi * F

ZMOT = RM + 1j * W * LM + 1 / (1j * W * CM)
Z = 1 / (1 / ZMOT + 1j * W * C0)

ZMAG = np.abs(Z)
I_PEAK = V_PEAK / ZMAG
P_REAL = (V_PEAK / np.sqrt(2))**2 * np.real(1 / Z)

bands = [
    ("165-220 kHz", 165e3, 220e3),
    ("170-225 kHz", 170e3, 225e3),
    ("180-230 kHz", 180e3, 230e3),
    ("190-235 kHz", 190e3, 235e3),
]

def band_metrics(f1, f2):
    mask = (F >= f1) & (F <= f2)

    z = ZMAG[mask]
    i = I_PEAK[mask]
    p = P_REAL[mask]

    z_ratio = np.max(z) / np.min(z)

    i_ratio = np.max(i) / np.min(i)

    pct_below_200 = np.mean(z <= 200.0) * 100

    return {
        "bandwidth_khz": (f2 - f1) / 1e3,
        "z_min_ohm": np.min(z),
        "z_max_ohm": np.max(z),
        "z_ratio": z_ratio,
        "ipeak_min_ma": np.min(i) * 1e3,
        "ipeak_max_ma": np.max(i) * 1e3,
        "current_ratio": i_ratio,
        "real_power_min_w": np.min(p),
        "real_power_max_w": np.max(p),
        "pct_z_below_200": pct_below_200,
    }

print("=" * 76)
print(" AQUILA TRANSDUCER USABLE-BAND STUDY")
print("=" * 76)

print("\n1. PRELIMINARY BVD MODEL")
print("-" * 76)
print(f"Nominal resonance           : {FR/1e3:.1f} kHz")
print(f"Static capacitance C0       : {C0*1e12:.1f} pF")
print(f"Assumed K33                 : {K33:.3f}")
print(f"Derived Cm                  : {CM*1e12:.2f} pF")
print(f"Derived Lm                  : {LM*1e3:.3f} mH")
print(f"Assumed Rm                  : {RM:.1f} ohm")
print("Status                      : SCREENING MODEL ONLY")

print("\n2. CANDIDATE BAND COMPARISON")
print("-" * 76)
print(
    f"{'Band':<16}"
    f"{'BW':>8}"
    f"{'Zmin':>10}"
    f"{'Zmax':>10}"
    f"{'Imin':>10}"
    f"{'Imax':>10}"
    f"{'Zratio':>10}"
)
print("-" * 76)

results = []

for name, f1, f2 in bands:
    m = band_metrics(f1, f2)
    results.append((name, f1, f2, m))

    print(
        f"{name:<16}"
        f"{m['bandwidth_khz']:>7.1f}"
        f"{m['z_min_ohm']:>10.2f}"
        f"{m['z_max_ohm']:>10.2f}"
        f"{m['ipeak_min_ma']:>10.2f}"
        f"{m['ipeak_max_ma']:>10.2f}"
        f"{m['z_ratio']:>10.2f}"
    )

print("\n3. INTERPRETATION")
print("-" * 76)
print("Zratio = maximum modeled |Z| / minimum modeled |Z| in each band.")
print("A smaller Zratio means a less variable electrical load in this")
print("preliminary model. It does NOT mean better acoustic performance.")
print()
print("The 235-kHz resonance is at the upper edge of the original")
print("165–235 kHz AQUILA chirp, so bands ending below resonance avoid")
print("the immediate resonance point but reduce the available bandwidth.")

print("\n4. ORIGINAL AQUILA BAND")
print("-" * 76)
original = band_metrics(165e3, 235e3)
print(f"165–235 kHz modeled |Z|    : "
      f"{original['z_min_ohm']:.2f}–{original['z_max_ohm']:.2f} ohm")
print(f"165–235 kHz modeled Ipeak  : "
      f"{original['ipeak_min_ma']:.2f}–{original['ipeak_max_ma']:.2f} mA")
print(f"Impedance variation ratio  : {original['z_ratio']:.2f} x")

print("\n5. ENGINEERING DECISION STATUS")
print("-" * 76)
print("NO FINAL FREQUENCY BAND IS SELECTED BY THIS SCRIPT.")
print("Reason: acoustic response and manufacturer impedance data are")
print("not available in the model.")
print()
print("NEXT HARDWARE REQUIREMENT:")
print("Measure or obtain the actual transducer impedance curve, then")
print("fit/update the BVD model and repeat this study.")

with open("aquila_usable_band_study.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "band",
        "bandwidth_khz",
        "z_min_ohm",
        "z_max_ohm",
        "z_ratio",
        "ipeak_min_ma",
        "ipeak_max_ma",
        "current_ratio",
        "real_power_min_w",
        "real_power_max_w",
        "pct_z_below_200",
    ])

    for name, _, _, m in results:
        writer.writerow([
            name,
            m["bandwidth_khz"],
            m["z_min_ohm"],
            m["z_max_ohm"],
            m["z_ratio"],
            m["ipeak_min_ma"],
            m["ipeak_max_ma"],
            m["current_ratio"],
            m["real_power_min_w"],
            m["real_power_max_w"],
            m["pct_z_below_200"],
        ])

fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(F / 1e3, ZMAG, label="BVD |Z|")
ax.axvline(165, linestyle="--", label="Original start")
ax.axvline(235, linestyle="--", label="Nominal resonance")
ax.axvspan(165, 235, alpha=0.12, label="Original 165–235 kHz band")

for name, f1, f2, _ in results:
    ax.axvline(f1 / 1e3, linestyle=":", alpha=0.6)
    ax.axvline(f2 / 1e3, linestyle=":", alpha=0.6)

ax.set_xlabel("Frequency (kHz)")
ax.set_ylabel("|Z| (ohm)")
ax.set_title("AQUILA Candidate Transducer — Preliminary BVD Impedance")
ax.grid(True)
ax.legend()
fig.tight_layout()
fig.savefig("aquila_usable_band_impedance.png", dpi=160)
plt.close(fig)

fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(F / 1e3, I_PEAK * 1e3, label="Modeled Ipeak")
ax.axvline(165, linestyle="--")
ax.axvline(235, linestyle="--")
ax.axvspan(165, 235, alpha=0.12, label="Original 165–235 kHz band")
ax.set_xlabel("Frequency (kHz)")
ax.set_ylabel("Peak current (mA)")
ax.set_title("AQUILA Candidate Transducer — Preliminary Driver Current")
ax.grid(True)
ax.legend()
fig.tight_layout()
fig.savefig("aquila_usable_band_current.png", dpi=160)
plt.close(fig)

print("\nGenerated files:")
print("  aquila_usable_band_study.csv")
print("  aquila_usable_band_impedance.png")
print("  aquila_usable_band_current.png")
print("\n" + "=" * 76)

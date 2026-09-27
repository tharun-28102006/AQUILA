"""
AQUILA — Preliminary BVD Piezoelectric Transducer Model
=========================================================
Uses the published candidate-transducer parameters as a starting
point and derives an APPROXIMATE Butterworth–Van Dyke (BVD) model.

Candidate:
    STEMINC SMD25T85F234S
    fr  = 235 kHz ±2%
    Zm  <= 45 ohm
    Cs  = 645 pF ±14% @ 1 kHz
    K33 >= 58%

IMPORTANT:
The manufacturer page does NOT provide a complete BVD equivalent
circuit in the retrieved specifications. Therefore Cm/Lm below are
derived from the minimum stated coupling coefficient as a preliminary
engineering model. This is NOT a manufacturer-validated SPICE model.

Final matching-network design requires measured or manufacturer
impedance-vs-frequency data.
"""

import numpy as np
import matplotlib.pyplot as plt

FR = 235e3
K33 = 0.58
C0 = 645e-12
RM = 45.0

F_START = 100e3
F_END = 300e3
F_LFM_START = 165e3
F_LFM_END = 235e3

V_PEAK = 2.575
V_RMS = V_PEAK / np.sqrt(2)

K2 = K33**2
CM = (K2 * C0) / (1.0 - K2)

LM = 1.0 / ((2*np.pi*FR)**2 * CM)

F = np.linspace(F_START, F_END, 10001)
W = 2*np.pi*F

ZMOT = RM + 1j*W*LM + 1/(1j*W*CM)
Y = 1/ZMOT + 1j*W*C0
Z = 1/Y

ZMAG = np.abs(Z)
ZPHASE = np.angle(Z, deg=True)

I_PEAK = V_PEAK / ZMAG
I_RMS = I_PEAK / np.sqrt(2)
P_LOAD = V_RMS**2 * np.real(1/Z)

idx_min_z = np.argmin(ZMAG)
f_min_z = F[idx_min_z]
z_min = ZMAG[idx_min_z]

idx_max_z = np.argmax(ZMAG)
f_max_z = F[idx_max_z]
z_max = ZMAG[idx_max_z]

band = (F >= F_LFM_START) & (F <= F_LFM_END)
z_band_min = np.min(ZMAG[band])
z_band_max = np.max(ZMAG[band])
i_band_max = np.max(I_PEAK[band])

print("=" * 72)
print(" AQUILA PRELIMINARY BVD TRANSDUCER MODEL")
print("=" * 72)

print("\n1. CANDIDATE TRANSDUCER")
print("-" * 72)
print("Part                        : STEMINC SMD25T85F234S")
print("Published resonance        : 235 kHz ±2%")
print("Published resonant Z      : <=45 ohm")
print("Published static C        : 645 pF ±14% @ 1 kHz")
print("Published K33              : >=58%")

print("\n2. DERIVED BVD PARAMETERS")
print("-" * 72)
print(f"C0 (static capacitance)    : {C0*1e12:.2f} pF")
print(f"Assumed K33                : {K33:.3f}")
print(f"Derived Cm                 : {CM*1e12:.2f} pF")
print(f"Derived Lm                 : {LM*1e3:.3f} mH")
print(f"Assumed Rm                 : {RM:.2f} ohm")
print("NOTE: Cm/Lm are derived estimates, not manufacturer values.")

print("\n3. MODEL RESONANCE")
print("-" * 72)
print(f"Minimum |Z| in sweep       : {z_min:.2f} ohm")
print(f"Frequency of minimum |Z|   : {f_min_z/1e3:.2f} kHz")
print(f"Maximum |Z| in sweep       : {z_max:.2f} ohm")
print(f"Frequency of maximum |Z|   : {f_max_z/1e3:.2f} kHz")

print("\n4. AQUILA LFM BAND")
print("-" * 72)
print(f"LFM band                   : {F_LFM_START/1e3:.1f}–{F_LFM_END/1e3:.1f} kHz")
print(f"|Z| range in LFM band      : {z_band_min:.2f}–{z_band_max:.2f} ohm")
print(f"Maximum modeled Ipeak      : {i_band_max*1e3:.2f} mA")

print("\n5. IMPORTANT INTERPRETATION")
print("-" * 72)
print("The candidate is resonant near the upper edge of AQUILA's")
print("165–235 kHz LFM band. Therefore the REAL acoustic/electrical")
print("response will not be flat across the entire chirp.")
print("The previous R||C model cannot show this resonance behavior.")
print("A measured impedance curve is required before matching-network")
print("values are frozen.")

print("\n6. ENGINEERING STATUS")
print("-" * 72)
print("BVD BEHAVIORAL MODEL       : COMPLETE")
print("REAL TRANSDUCER MODEL      : NOT YET CLOSED")
print("MATCHING NETWORK           : NOT YET FROZEN")
print("PCB                         : DO NOT FREEZE YET")

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(F/1e3, ZMAG)
ax.axvline(F_LFM_START/1e3, linestyle="--", label="165 kHz")
ax.axvline(F_LFM_END/1e3, linestyle="--", label="235 kHz")
ax.axvline(FR/1e3, linestyle=":", label="235 kHz nominal resonance")
ax.set_xlabel("Frequency (kHz)")
ax.set_ylabel("|Z| (ohm)")
ax.set_title("AQUILA Preliminary BVD Transducer Impedance")
ax.grid(True)
ax.legend()
fig.tight_layout()
fig.savefig("aquila_bvd_impedance.png", dpi=160)
plt.close(fig)

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(F/1e3, ZPHASE)
ax.axvline(F_LFM_START/1e3, linestyle="--")
ax.axvline(F_LFM_END/1e3, linestyle="--")
ax.axvline(FR/1e3, linestyle=":")
ax.set_xlabel("Frequency (kHz)")
ax.set_ylabel("Phase (degrees)")
ax.set_title("AQUILA Preliminary BVD Transducer Phase")
ax.grid(True)
fig.tight_layout()
fig.savefig("aquila_bvd_phase.png", dpi=160)
plt.close(fig)

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(F/1e3, I_PEAK*1e3)
ax.axvline(F_LFM_START/1e3, linestyle="--", label="165 kHz")
ax.axvline(F_LFM_END/1e3, linestyle="--", label="235 kHz")
ax.axvline(FR/1e3, linestyle=":", label="235 kHz resonance")
ax.set_xlabel("Frequency (kHz)")
ax.set_ylabel("Driver current peak (mA)")
ax.set_title("AQUILA Preliminary THS3091 Current into BVD Model")
ax.grid(True)
ax.legend()
fig.tight_layout()
fig.savefig("aquila_bvd_current.png", dpi=160)
plt.close(fig)

print("\nGenerated files:")
print("  aquila_bvd_impedance.png")
print("  aquila_bvd_phase.png")
print("  aquila_bvd_current.png")
print("\n" + "=" * 72)

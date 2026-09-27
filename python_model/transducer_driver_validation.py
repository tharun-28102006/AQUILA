"""
AQUILA — Transducer / THS3091 Behavioral Validation
----------------------------------------------------
Behavioral electrical-load study for a candidate piezoelectric
transducer using a simple R || C model.

This is NOT a piezoelectric equivalent-circuit characterization
and NOT a SPICE/hardware proof. The actual transducer impedance
must be measured or obtained from the manufacturer's impedance
curve/model before final PCB values are locked.
"""

import numpy as np
import matplotlib.pyplot as plt

F_START = 165e3
F_END = 235e3
F_CENTER = 200e3

V_PEAK = 2.575          # V, modeled THS3091 output peak
V_RMS = V_PEAK / np.sqrt(2)

C_PIEZO = 645e-12
R_LOAD = 45.0

THS_CURRENT_TYP = 0.310  # A

F = np.linspace(100e3, 300e3, 2001)
W = 2 * np.pi * F

Y = 1 / R_LOAD + 1j * W * C_PIEZO
Z = 1 / Y

Z_MAG = np.abs(Z)
Z_PHASE = np.angle(Z, deg=True)

I_PEAK = V_PEAK / Z_MAG
I_RMS = I_PEAK / np.sqrt(2)

P_APPROX = V_RMS**2 / R_LOAD * np.ones_like(F)

check_freqs = np.array([100e3, 165e3, 200e3, 235e3, 300e3])

def interp(arr):
    return np.interp(check_freqs, F, arr)

z_check = interp(Z_MAG)
phase_check = interp(Z_PHASE)
ipeak_check = interp(I_PEAK)
irms_check = interp(I_RMS)

print("=" * 72)
print(" AQUILA TRANSDUCER / THS3091 BEHAVIORAL VALIDATION")
print("=" * 72)

print("\n1. INPUT / DRIVER")
print("-" * 72)
print(f"LFM frequency range          : {F_START/1e3:.1f} to {F_END/1e3:.1f} kHz")
print(f"Driver output Vpeak         : {V_PEAK:.3f} V")
print(f"Driver output Vrms          : {V_RMS:.3f} V")
print(f"THS3091 typical current ref : {THS_CURRENT_TYP*1e3:.1f} mA")

print("\n2. PRELIMINARY TRANSDUCER MODEL")
print("-" * 72)
print(f"Capacitance                 : {C_PIEZO*1e12:.1f} pF")
print(f"Parallel resistance         : {R_LOAD:.1f} ohm")
print("Model                       : R || C")
print("IMPORTANT                   : Preliminary electrical model only")

print("\n3. FREQUENCY CHECK")
print("-" * 72)
print(f"{'Frequency':>12} {'|Z|':>12} {'Phase':>12} {'Ipeak':>12} {'Irms':>12}")
for f, z, ph, ip, ir in zip(check_freqs, z_check, phase_check,
                             ipeak_check, irms_check):
    print(f"{f/1e3:9.1f} kHz {z:9.2f} ohm {ph:9.2f} deg "
          f"{ip*1e3:9.2f} mA {ir*1e3:9.2f} mA")

max_i = np.max(I_PEAK)
max_i_f = F[np.argmax(I_PEAK)]

print("\n4. CURRENT CHECK — PRELIMINARY")
print("-" * 72)
print(f"Maximum modeled Ipeak       : {max_i*1e3:.2f} mA")
print(f"Frequency of maximum Ipeak  : {max_i_f/1e3:.1f} kHz")
print(f"THS3091 typical current ref : {THS_CURRENT_TYP*1e3:.1f} mA")
print(f"Current ratio               : {THS_CURRENT_TYP/max_i:.2f} x")

if max_i < THS_CURRENT_TYP:
    print("PRELIMINARY CURRENT CHECK   : PASS")
else:
    print("PRELIMINARY CURRENT CHECK   : FAIL")

print("\n5. POWER — PRELIMINARY")
print("-" * 72)
print(f"Approx. resistive-load power : {P_APPROX[0]:.3f} W")
print("NOTE: This is NOT acoustic power and does not include")
print("      the true piezoelectric motional branch or matching network.")

print("\n6. LFM BAND")
print("-" * 72)
band = (F >= F_START) & (F <= F_END)
z_min = np.min(Z_MAG[band])
z_max = np.max(Z_MAG[band])
i_max_band = np.max(I_PEAK[band])
i_min_band = np.min(I_PEAK[band])

print(f"|Z| range, 165–235 kHz     : {z_min:.2f} to {z_max:.2f} ohm")
print(f"Ipeak range, 165–235 kHz  : {i_min_band*1e3:.2f} to "
      f"{i_max_band*1e3:.2f} mA")

print("\n7. ENGINEERING STATUS")
print("-" * 72)
print("PRELIMINARY ELECTRICAL MODEL: COMPLETE")
print("FINAL TRANSDUCER VALIDATION:   NOT CLOSED")

print("\nRequired before final PCB:")
print("1. Manufacturer impedance-vs-frequency data or measured impedance.")
print("2. Actual resonant/anti-resonant behavior.")
print("3. Final THS3091 supply voltage and output swing.")
print("4. Transducer mounting/water-loading characterization.")
print("5. Matching/protection network, if required.")
print("6. Thermal and continuous-duty validation.")

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(F/1e3, Z_MAG)
ax.axvline(F_START/1e3, linestyle="--", label="165 kHz")
ax.axvline(F_END/1e3, linestyle="--", label="235 kHz")
ax.set_xlabel("Frequency (kHz)")
ax.set_ylabel("|Z| (ohm)")
ax.set_title("AQUILA Preliminary Transducer Impedance Model")
ax.grid(True)
ax.legend()
fig.tight_layout()
fig.savefig("aquila_transducer_impedance.png", dpi=160)
plt.close(fig)

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(F/1e3, I_PEAK * 1e3)
ax.axhline(THS_CURRENT_TYP * 1e3, linestyle="--",
           label="THS3091 typical current reference")
ax.axvline(F_START/1e3, linestyle="--")
ax.axvline(F_END/1e3, linestyle="--")
ax.set_xlabel("Frequency (kHz)")
ax.set_ylabel("Output current peak (mA)")
ax.set_title("AQUILA Preliminary THS3091 Output Current")
ax.grid(True)
ax.legend()
fig.tight_layout()
fig.savefig("aquila_transducer_current.png", dpi=160)
plt.close(fig)

print("\nGenerated files:")
print("  aquila_transducer_impedance.png")
print("  aquila_transducer_current.png")
print("\n" + "=" * 72)

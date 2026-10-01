"""Independent linearized numerical checks. Does NOT run LTspice or TI's model.

Requires numpy, scipy and matplotlib. Run from any working directory.
Finite-GBW single-pole OPA2835 surrogate; exact physical SK feedback topology.
Nominal outputs are not clipped: exceeding a limit is reported, never hidden.
"""
from pathlib import Path
import csv
import json
import re
import numpy as np
from scipy import signal, optimize
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
for directory in ("transient", "fft", "ac_response"):
    (RESULTS / directory).mkdir(parents=True, exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.alpha": 0.17,
                     "figure.facecolor": "white", "savefig.facecolor": "white"})
COLORS = ["#8c98a8", "#167f78", "#193854"]
FS = 5e6
DT = 5e-9
START = 20e-6
DURATION = 2e-3
STOP = START + DURATION + 80e-6
R = 1020.0
C = 220e-12
K = (1.15, 2.24)
GAIN_DC = np.prod(K)
TAU_DAC = 100e-9 / np.log(1000)
WT = 2 * np.pi * 30e6
A0 = 1e5
RZ = 355e3
CZ = 1.15e-12
RF = 806.0
RIN = 4.0
LOAD = 50.0
ISO = 10.0
PEAK = .350
CODE = np.array([1, 1, -1, 1, -1, -1, 1])
t = np.arange(round(STOP / DT)) * DT
u = t - START
active = (u >= -1e-15) & (u < DURATION - 1e-15)
steady = (u >= 200e-6) & (u < DURATION - 20e-6)
pulse = (u >= 0) & (u < DURATION)


def stage_tf(k):
    # vo = A(s)*(n2 - vo/k), A(s)=A0/(1+s*A0/wt).
    # KCL: (1+3*s*RC+s^2*R^2*C^2)*n2 - s*RC*vo = vin.
    tau = R * C
    a = 1 + k / A0
    b = k / WT
    return np.array([k]), np.array([b*tau*tau, a*tau*tau+3*b*tau,
                                   3*a*tau+b-k*tau, a])


def response(num, den, frequencies):
    s = 2j * np.pi * np.asarray(frequencies)
    return np.polyval(num, s) / np.polyval(den, s)


def filt_response(frequencies):
    return response(*stage_tf(K[0]), frequencies) * response(*stage_tf(K[1]), frequencies)


def apply_tf(x, num, den):
    # Bilinear integration at 200 MS/s; target band is <=0.25% of sample rate.
    b, a = signal.bilinear(num, den, fs=1/DT)
    return signal.lfilter(b, a, x)


RZ_LOADED = RZ / (1 + 1 / (LOAD + ISO))
DRIVER_GAIN = 2 * RZ_LOADED / (RZ_LOADED + RF + 2*RIN)
DRIVER_TAU = RZ*CZ*(RF+2*RIN)/(RZ_LOADED+RF+2*RIN)


def waveform(mode=1, frequency=300e3, window=False, zoh=True):
    n = np.floor(np.maximum(u, 0)*FS + 1e-8)
    s = n/FS if zoh else np.maximum(u, 0)
    x = np.minimum(n, DURATION*FS-1)/(DURATION*FS-1) if zoh else np.clip(s/DURATION, 0, 1)
    envelope = .42-.5*np.cos(2*np.pi*x)+.08*np.cos(4*np.pi*x) if window else np.ones_like(t)
    if mode == 1:
        carrier = np.sin(2*np.pi*frequency*s)
    elif mode == 2:
        carrier = np.sin(2*np.pi*(200e3*s+(400e3-200e3)*s*s/(2*DURATION)))
    elif mode == 3:
        carrier = np.sin(2*np.pi*200e3*DURATION*np.expm1(np.log(2)*s/DURATION)/np.log(2))
    elif mode == 4:
        chips = np.minimum(6, np.floor(s*7/DURATION).astype(int))
        carrier = CODE[chips]*np.sin(2*np.pi*frequency*s)
    else:
        raise ValueError("mode must be 1..4")
    return PEAK*active*envelope*carrier, envelope*active


def simulate(mode=1, frequency=300e3, window=False):
    command, envelope = waveform(mode, frequency, window)
    q = 2.5/65535
    quant = q*np.floor((1.25+command)/q+.5)
    baseline = q*np.floor(1.25/q+.5)
    a = np.exp(-DT/TAU_DAC)
    dac = signal.lfilter([1-a], [1, -a], quant-baseline)
    coupled = apply_tf(dac, [0.01, 0], [0.01, 1])
    buffered = apply_tf(coupled, [1], [1/WT, 1+1/A0])
    first = apply_tf(buffered, *stage_tf(K[0]))
    filtered = apply_tf(first, *stage_tf(K[1]))
    amp = apply_tf(filtered, [DRIVER_GAIN], [DRIVER_TAU, 1])
    load = amp * LOAD/(LOAD+ISO)
    return dict(command=command, dac=dac, buffer=buffered, first=first,
                filtered=filtered, amp=amp, load=load, envelope=envelope)


def metrics(y, mask):
    v = y["load"][mask]
    a = y["amp"][mask]
    rms = float(np.sqrt(np.mean(v*v)))
    load_current = v/LOAD
    driver_current = load_current+a/(2*RF)
    slew = np.gradient(y["amp"], DT)[mask] / 1e6
    return dict(vpp_V=float(np.ptp(v)), vrms_V=rms,
                current_rms_A=rms/LOAD, current_peak_A=float(np.max(np.abs(load_current))),
                power_W=rms*rms/LOAD, driver_current_peak_A=float(np.max(np.abs(driver_current))),
                amplifier_peak_V=float(np.max(np.abs(a))),
                driver_rail_headroom_V=float(5-np.max(np.abs(a))),
                slew_V_per_us=float(np.max(np.abs(slew))),
                filter_output_peak_V=float(np.max(np.abs(y["filtered"][mask]))),
                gain_peak_ratio=float(np.ptp(v)/np.ptp(y["dac"][mask])))


def csv_out(path, columns, rows):
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(columns)
        writer.writerows(rows)


def label_figure(fig, title):
    fig.suptitle(title, x=.07, ha="left", fontsize=15, fontweight="bold", color=COLORS[2])
    fig.text(.07, .015, "Independent linearized numerical simulation | not LTspice / not TI macromodel results",
             color="#687789", fontsize=8)
    fig.tight_layout(rect=[.02, .045, .98, .93])


f = np.geomspace(1e3, 30e6, 6000)
h = filt_response(f)
db = 20*np.log10(abs(h)/GAIN_DC)
f3 = optimize.brentq(lambda v: 20*np.log10(abs(filt_response(v))/GAIN_DC)+3.01029995664, 5e5, 1e6)
ideal = np.prod(np.array(K)[:,None]/(1+(2j*np.pi*f*R*C)**2+(3-np.array(K)[:,None])*2j*np.pi*f*R*C),axis=0)
fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
axes[0].semilogx(f/1e3, 20*np.log10(abs(ideal)/GAIN_DC), color=COLORS[0], ls="--", label="Ideal op amps")
axes[0].semilogx(f/1e3, db, color=COLORS[1], lw=2, label="30 MHz GBW surrogate")
axes[0].axvspan(100, 500, color=COLORS[1], alpha=.08, label="Required band")
axes[0].axvline(f3/1e3, color=COLORS[2], ls=":")
axes[0].set(ylabel="Normalized gain (dB)", ylim=(-100, 3))
axes[0].legend(loc="lower left")
axes[1].semilogx(f/1e3, np.unwrap(np.angle(h))*180/np.pi, color=COLORS[2])
axes[1].set(xlabel="Frequency (kHz)", ylabel="Phase (degrees)", xlim=(10, 10000))
label_figure(fig, "AQUILA / fourth-order reconstruction filter")
fig.savefig(RESULTS/"ac_response"/"filter_response.png", dpi=170)
plt.close(fig)
csv_out(RESULTS/"ac_response"/"filter_response.csv", ["frequency_Hz", "surrogate_gain_dB_normalized", "ideal_gain_dB_normalized", "surrogate_phase_deg"],
        zip(f, db, 20*np.log10(abs(ideal)/GAIN_DC), np.unwrap(np.angle(h))*180/np.pi))

band_rows = []
sine300 = None
for frequency in (100e3, 200e3, 300e3, 400e3, 500e3):
    y = simulate(1, frequency, False)
    row = {"frequency_Hz": frequency, **metrics(y, steady)}
    row["filter_gain_dB_normalized"] = float(20*np.log10(abs(filt_response(frequency))/GAIN_DC))
    band_rows.append(row)
    if frequency == 300e3:
        sine300 = y
csv_out(RESULTS/"transient"/"sine_band_measurements.csv", list(band_rows[0]), [list(r.values()) for r in band_rows])

pulse_rows = {}
for mode, name in ((2, "lfm"), (3, "geometric"), (4, "phase_code")):
    y = simulate(mode, window=True)
    pulse_rows[name] = metrics(y, pulse)
    pulse_rows[name]["energy_including_tail_J"] = float(np.sum(y["load"]**2/LOAD)*DT)
    every = slice(None, None, 10)
    csv_out(RESULTS/"transient"/f"{name}_waveforms.csv",
            ["time_s", "VIN_DAC_ac_V", "V_I_V_V", "V_FILTER_V", "V_AMP_V", "V_LOAD_V"],
            zip(t[every], y["dac"][every], y["buffer"][every], y["filtered"][every], y["amp"][every], y["load"][every]))
    fig, axes = plt.subplots(3, 1, figsize=(11, 8))
    axes[0].plot(t*1e3, y["load"], color=COLORS[2], lw=.45)
    axes[0].plot(t*1e3, 1.5*y["envelope"], color=COLORS[1], ls="--", lw=1, label="Nominal +1.5 V envelope")
    axes[0].set(xlabel="Time (ms)", ylabel="Load voltage (V)")
    axes[0].legend(loc="upper right", fontsize=8)
    zoom = (t > START+.995e-3) & (t < START+1.010e-3)
    for key, color, label in zip(("dac", "filtered", "load"), COLORS,
                                 ("DAC (DC removed)", "Filtered", "50 ohm load")):
        axes[1].plot((t[zoom]-START)*1e6, y[key][zoom], color=color, lw=1.2, label=label)
    axes[1].set(xlabel="Time within pulse (us)", ylabel="Voltage (V)")
    axes[1].legend(fontsize=8, ncol=3)
    if mode != 4:
        analytic = signal.hilbert(y["load"])
        inst_f = np.gradient(np.unwrap(np.angle(analytic)), DT)/(2*np.pi)
        keep = (u > .2e-3) & (u < 1.8e-3)
        expected = 200e3 + 200e3*u/DURATION if mode == 2 else 200e3*2**(u/DURATION)
        axes[2].plot(u[keep][::100]*1e3, inst_f[keep][::100]/1e3, color=COLORS[2], lw=1, label="Output instantaneous frequency")
        axes[2].plot(u[keep][::100]*1e3, expected[keep][::100]/1e3, color=COLORS[1], ls="--", label="Command law")
        pulse_rows[name]["median_frequency_error_Hz"] = float(np.median(abs(inst_f[keep]-expected[keep])))
        axes[2].set(xlabel="Time within pulse (ms)", ylabel="Frequency (kHz)")
        axes[2].legend(fontsize=8)
    else:
        edge = DURATION*2/7
        zoom2 = (u > edge-12e-6) & (u < edge+12e-6)
        axes[2].plot(u[zoom2]*1e6, y["command"][zoom2]*GAIN_DC*DRIVER_GAIN*50/60,
                     color=COLORS[0], label="Scaled command")
        axes[2].plot(u[zoom2]*1e6, y["load"][zoom2], color=COLORS[2], label="Filtered code reversal")
        axes[2].axvline(edge*1e6, color=COLORS[1], ls=":")
        axes[2].set(xlabel="Time within pulse (us)", ylabel="Voltage (V)")
        axes[2].legend(fontsize=8)
    label_figure(fig, f"AQUILA / {name.replace('_', ' ')} / 2 ms Blackman pulse")
    fig.savefig(RESULTS/"transient"/f"{name}.png", dpi=155)
    plt.close(fig)

# Coherent tone FFT across the complete record, including its intentional gating.
ff = np.fft.rfftfreq(len(t), DT)
fig, axes = plt.subplots(2, 1, figsize=(11, 7))
spectra = {}
for key, color, label in zip(("dac", "filtered", "load"), COLORS, ("DAC", "Filtered", "Load")):
    spectrum = 2*abs(np.fft.rfft(sine300[key]))/len(t)
    spectra[key] = spectrum
    peak = spectrum[np.argmin(abs(ff-300e3))]
    axes[0].plot(ff/1e6, 20*np.log10(np.maximum(spectrum, 1e-14)), color=color, lw=.8, label=label)
    axes[1].plot(ff/1e6, 20*np.log10(np.maximum(spectrum/peak, 1e-14)), color=color, lw=.8, label=label)
axes[0].set(ylabel="Amplitude (dBV peak)", xlim=(0, 6), ylim=(-130, 5))
axes[1].set(xlabel="Frequency (MHz)", ylabel="Relative to carrier (dBc)", xlim=(4.3, 5.7), ylim=(-120, -10))
axes[0].legend(ncol=3)
label_figure(fig, "AQUILA / 300 kHz sampled-tone spectrum and DAC images")
fig.savefig(RESULTS/"fft"/"dac_image_suppression.png", dpi=170)
plt.close(fig)
image_rows = []
for frequency in (4.7e6, 5.3e6):
    i, carrier_i = np.argmin(abs(ff-frequency)), np.argmin(abs(ff-300e3))
    row = {"image_frequency_Hz": frequency}
    for key in spectra:
        row[key+"_dBc"] = float(20*np.log10(spectra[key][i]/spectra[key][carrier_i]))
    row["additional_filter_suppression_dB"] = row["filtered_dBc"]-row["dac_dBc"]
    image_rows.append(row)
csv_out(RESULTS/"fft"/"image_measurements.csv", list(image_rows[0]), [list(r.values()) for r in image_rows])

# Zero-padding reveals sidelobes without changing the 2 ms time aperture.
fig, axes = plt.subplots(2, 1, figsize=(11, 8))
for mode, axis, title in ((1, axes[0], "300 kHz carrier pulse"), (2, axes[1], "200-400 kHz LFM pulse")):
    for win, color, label in ((False, COLORS[0], "Rectangular"), (True, COLORS[1], "Blackman")):
        command, _ = waveform(mode, window=win)
        nfft = 2**21
        spec = abs(np.fft.rfft(command, n=nfft))
        freq = np.fft.rfftfreq(nfft, DT)
        power = 20*np.log10(np.maximum(spec/spec.max(), 1e-14))
        axis.plot(freq/1e3, power, color=color, lw=1.2, label=label)
    axis.set(title=title, ylabel="Normalized spectrum (dB)", ylim=(-100, 2))
    axis.set_xlim((295, 305) if mode == 1 else (100, 500))
    axis.legend()
axes[1].set_xlabel("Frequency (kHz)")
label_figure(fig, "AQUILA / digital windowing comparison (before analog filter)")
fig.savefig(RESULTS/"fft"/"blackman_comparison.png", dpi=170)
plt.close(fig)

# A topology-based, one-pole surrogate step response; no saturation imposed.
step = PEAK*((u >= 0) & (u < 10e-6))
y = apply_tf(apply_tf(step, [0.01, 0], [0.01, 1]), [1], [1/WT, 1+1/A0])
for k in K:
    y = apply_tf(y, *stage_tf(k))
y = apply_tf(y, [DRIVER_GAIN*50/60], [DRIVER_TAU, 1])
fig, ax = plt.subplots(figsize=(10, 4))
keep = (u >= -2e-6) & (u < 20e-6)
ax.plot(u[keep]*1e6, y[keep], color=COLORS[2])
ax.set(xlabel="Time after step (us)", ylabel="Load voltage (V)")
label_figure(fig, "AQUILA / linearized analog step response")
fig.savefig(RESULTS/"transient"/"step_response.png", dpi=150)
plt.close(fig)

checks = {
    "sine_amplitude_within_2p8_to_3p2_Vpp": all(2.8 < r["vpp_V"] < 3.2 for r in band_rows),
    "cutoff_within_650_to_750_kHz": 650e3 < f3 < 750e3,
    "driver_peak_below_conservative_3p5_V": all(r["amplifier_peak_V"] < 3.5 for r in band_rows),
    "driver_peak_current_below_conservative_80mA": all(r["driver_current_peak_A"] < .08 for r in band_rows),
    "driver_slew_below_750_V_per_us": all(r["slew_V_per_us"] < 750 for r in band_rows),
    "filter_output_below_2V_peak": all(r["filter_output_peak_V"] < 2 for r in band_rows),
    "image_filter_suppression_exceeds_55dB": all(r["additional_filter_suppression_dB"] < -55 for r in image_rows),
    "lfm_median_frequency_error_below_1kHz": pulse_rows["lfm"]["median_frequency_error_Hz"] < 1000,
    "geometric_median_frequency_error_below_1kHz": pulse_rows["geometric"]["median_frequency_error_Hz"] < 1000,
    "blackman_sample_endpoints_zero": bool(np.allclose([.42-.5+.08, .42-.5*np.cos(2*np.pi)+.08*np.cos(4*np.pi)], 0)),
}
summary = dict(
    provenance="Independent Python/SciPy LINEARIZED numerical simulation. Not LTspice; does not execute TI model.",
    native_LTspice_executed=False, alternate_SPICE_executed=False,
    environment_note="No LTspice/Wine installed. ngspice unavailable in configured RPM repositories; alternate Debian binary has incompatible runtime dependencies. No native SPICE measurements fabricated.",
    numerical_method="200 MS/s bilinear integration of physical Sallen-Key topology with one-pole 30 MHz GBW / 100 dB OPA2835 surrogate; exact-discrete first-order DAC settling; current-feedback small-signal driver approximation.",
    component_pole_Hz=1/(2*np.pi*R*C), filter_Q=[1/(3-k) for k in K],
    filter_DC_gain=float(GAIN_DC), nominal_chain_gain=float(GAIN_DC*2*50/60),
    surrogate_filter_cutoff_Hz=f3, sine_band=band_rows, pulses=pulse_rows,
    images=image_rows, surrogate_checks=checks,
    power_estimates=dict(OPA2835_four_channels_quiescent_W=4*.00025*5,
                         buffer_channel_quiescent_W=.00025*5,
                         filter_two_channels_quiescent_W=2*.00025*5,
                         spare_OPA2835_quiescent_W=.00025*5,
                         OPA2684_two_channels_quiescent_W=2*.0017*10,
                         DAC_power_W=None,
                         note="Datasheet-typical estimates. Class-B load-dependent draw is separate; DAC and converter losses remain unknown."))
(RESULTS/"validation_summary.json").write_text(json.dumps(summary, indent=2)+"\n")

# Structural checks resolve all includes and ensure symbol SpiceOrder matches models.
manifest = json.loads((ROOT/"scripts"/"component_manifest.json").read_text())
for component in manifest["main"]:
    spec = manifest["symbols"][component["kind"]]
    assert len(component["nodes"]) == len(spec["pins"])
    text = (ROOT/"symbols"/(component["kind"]+".asy")).read_text()
    assert [int(n) for n in re.findall(r"PINATTR SpiceOrder (\d+)", text)] == list(range(1, len(spec["pins"])+1))
for path in list(ROOT.glob("*.cir"))+list(ROOT.glob("*.inc"))+list(ROOT.glob("*.asc")):
    for name in re.findall(r"(?:^|!|\n)\.include\s+([^\s]+)", path.read_text(), re.I):
        assert (ROOT/name.strip('"')).is_file(), (path, name)
assert all(checks.values()), checks
print(json.dumps({"provenance": summary["provenance"], "cutoff_Hz": f3,
                  "sine_band": band_rows, "images": image_rows,
                  "pulse_frequency_errors_Hz": {k: v.get("median_frequency_error_Hz") for k,v in pulse_rows.items()},
                  "checks": checks}, indent=2))

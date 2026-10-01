"""Generate LTspice symbols, matching schematics/netlists, and test profiles."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
SYMS = ROOT / "symbols"
SYMS.mkdir(exist_ok=True)
registry = {}


def symbol(name, value, pins, drawing, prefix="X", windows=(0, -36)):
    lines = ["Version 4", "SymbolType CELL", *drawing,
             f"WINDOW 0 {windows[0]} {windows[1]} Left 2",
             f"WINDOW 3 {windows[0]} {windows[1] + 20} Left 2",
             f"SYMATTR Prefix {prefix}", f"SYMATTR Value {value}"]
    for order, (label, x, y, side) in enumerate(pins, 1):
        lines += [f"PIN {x} {y} {side} 8", f"PINATTR PinName {label}",
                  f"PINATTR SpiceOrder {order}"]
    (SYMS / f"{name}.asy").write_text("\n".join(lines) + "\n")
    registry[name] = {"value": value, "pins": pins, "prefix": prefix}


amp_pins = [("+IN", 0, -32, "LEFT"), ("-IN", 0, 32, "LEFT"),
            ("V+", 64, -96, "BOTTOM"), ("V-", 64, 96, "TOP"),
            ("OUT", 160, 0, "RIGHT"), ("REF", 112, 96, "TOP")]
amp_shape = ["LINE Normal 0 -32 32 -32", "LINE Normal 0 32 32 32",
             "LINE Normal 32 -64 32 64", "LINE Normal 32 -64 144 0",
             "LINE Normal 32 64 144 0", "LINE Normal 144 0 160 0",
             "LINE Normal 64 -96 64 -46", "LINE Normal 64 96 64 46",
             "LINE Normal 112 96 112 19", "TEXT 40 -32 Left 2 +",
             "TEXT 40 32 Left 2 -"]
symbol("OPA2835", "OPA2835_CH", amp_pins, amp_shape, windows=(16, -144))
symbol("OPA2684", "OPA2684_EQ", amp_pins, amp_shape, windows=(16, -144))

symbol("AQUILA_WAVEFORM_SOURCE", "AQUILA_WAVEFORM_SOURCE",
       [("CMD", 192, 64, "RIGHT"), ("REF", 96, 160, "TOP")],
       ["RECTANGLE Normal 0 0 192 128", "LINE Normal 96 128 96 160",
        "TEXT 12 38 Left 2 FPGA equivalent", "TEXT 12 70 Left 2 sampled / windowed"])
symbol("AD3541R", "AD3541R_EQ",
       [("CMD", 0, 64, "LEFT"), ("OUT", 256, 64, "RIGHT"),
        ("AGND", 32, 192, "TOP"), ("AVDD", 48, -48, "BOTTOM"),
        ("DVDD", 112, -48, "BOTTOM"), ("VLOGIC", 192, -48, "BOTTOM"),
        ("PVDD", 48, 256, "TOP"), ("PVSS", 144, 256, "TOP"),
        ("DGND", 224, 192, "TOP")],
       ["RECTANGLE Normal 0 0 256 128", "LINE Normal 32 128 32 192",
        "LINE Normal 48 0 48 -48", "LINE Normal 112 0 112 -48",
        "LINE Normal 192 0 192 -48", "LINE Normal 48 128 48 256",
        "LINE Normal 144 128 144 256", "LINE Normal 224 128 224 192",
        "TEXT 16 30 Left 2 AD3541R equivalent", "TEXT 16 82 Left 2 16 bit / 0..2.5 V"], windows=(0, -112))
symbol("AQUILA_SK", "AQUILA_SK",
       [("IN", 0, 64, "LEFT"), ("OUT", 256, 64, "RIGHT"),
        ("V+", 48, -48, "BOTTOM"), ("V-", 144, -48, "BOTTOM"),
        ("REF", 128, 176, "TOP")],
       ["RECTANGLE Normal 0 0 256 128", "LINE Normal 48 -48 48 0",
        "LINE Normal 144 -48 144 0", "LINE Normal 128 128 128 176",
        "TEXT 16 28 Left 2 Sallen-Key / OPA2835", "TEXT 16 86 Left 2 1.02k / 220pF"], windows=(0, -112))

for part, prefix, shape in [
    ("R", "R", ["LINE Normal 0 0 16 0", "LINE Normal 16 0 24 -8",
                 "LINE Normal 24 -8 36 8", "LINE Normal 36 8 48 -8",
                 "LINE Normal 48 -8 60 8", "LINE Normal 60 8 72 -8",
                 "LINE Normal 72 -8 80 0", "LINE Normal 80 0 96 0"]),
    ("C", "C", ["LINE Normal 0 0 40 0", "LINE Normal 40 -16 40 16",
                 "LINE Normal 56 -16 56 16", "LINE Normal 56 0 96 0"]),
    ("V", "V", ["LINE Normal 0 0 24 0", "CIRCLE Normal 24 -24 72 24",
                 "LINE Normal 72 0 96 0", "TEXT 30 0 Left 1 +",
                 "TEXT 55 0 Left 1 -"]),
]:
    symbol(f"AQ_{part}", "1", [("A", 0, 0, "NONE"), ("B", 96, 0, "NONE")],
           shape, prefix, (16, -48))
    if part in ("R", "C"):
        vertical = []
        for line in shape:
            fields = line.split()
            vertical.append(f"LINE Normal {-int(fields[3])} {fields[2]} {-int(fields[5])} {fields[4]}")
        symbol(f"AQ_{part}V", "1", [("A", 0, 0, "NONE"), ("B", 0, 96, "NONE")],
               vertical, prefix, (20, 16))

for part in ("OPA2835", "OPA2684"):
    symbol(part + "_DUAL", part + "_DUAL",
           [("OUTA", 0, 32, "LEFT"), ("INA-", 0, 80, "LEFT"),
            ("INA+", 0, 128, "LEFT"), ("V-", 0, 176, "LEFT"),
            ("INB+", 256, 176, "RIGHT"), ("INB-", 256, 128, "RIGHT"),
            ("OUTB", 256, 80, "RIGHT"), ("V+", 256, 32, "RIGHT")],
           ["RECTANGLE Normal 0 0 256 208", "TEXT 72 64 Left 2 SOIC-8",
            "TEXT 72 108 Left 2 physical order"])

components = []


def add(name, kind, nodes, value=None, params="", pos=(0, 0)):
    spec = registry[kind]
    assert len(nodes.split()) == len(spec["pins"]), name
    components.append(dict(name=name, kind=kind, nodes=nodes.split(),
                           value=value or spec["value"], params=params, pos=pos))


add("XWAVE", "AQUILA_WAVEFORM_SOURCE", "CMD_DAC AGND", pos=(32, 256))
add("XDAC", "AD3541R", "CMD_DAC VIN_DAC AGND AVDD DVDD VLOGIC PVDD PVSS DGND", pos=(352, 256))
add("CDC", "AQ_C", "VIN_DAC VIN_AC", "{CCOUPLE}", pos=(736, 320))
add("RBIAS", "AQ_RV", "VIN_AC AGND", "{RBIAS}", pos=(864, 464))
add("XU1A", "OPA2835", "VIN_AC V_I_V OP_P OP_N V_I_V AGND", pos=(1008, 352))
add("XSK1", "AQUILA_SK", "V_I_V V_FILTER1 OP_P OP_N AGND", params="RF={RF1} RG={RG1}", pos=(1360, 256))
add("XSK2", "AQUILA_SK", "V_FILTER1 V_FILTER OP_P OP_N AGND", params="RF={RF2} RG={RG2}", pos=(1808, 256))
add("XU3A", "OPA2684", "V_FILTER DRV_NEG DRV_P DRV_N V_AMP_RAW AGND", pos=(2256, 352))
add("RFD", "AQ_R", "V_AMP DRV_NEG", "{RDRVF}", pos=(2272, 592))
add("RGD", "AQ_RV", "DRV_NEG AGND", "{RDRVG}", pos=(2464, 528))
add("VAMP_SENSE", "AQ_V", "V_AMP_RAW V_AMP", "0", pos=(2576, 352))
add("RISO", "AQ_R", "V_AMP LOAD_PRE", "{RISO}", pos=(2784, 352))
add("VLOAD_SENSE", "AQ_V", "LOAD_PRE V_LOAD", "0", pos=(2992, 352))
add("RLOAD", "AQ_RV", "V_LOAD AGND", "{RLOAD}", pos=(3200, 432))


def net(c):
    suffix = (" " + c["params"]) if c["params"] else ""
    return f"{c['name']} {' '.join(c['nodes'])} {c['value']}{suffix}"


(ROOT / "aquila_signal_chain.inc").write_text(
    "* Generated from the same component list as AQUILA_TX_ANALOG.asc.\n" +
    "\n".join(net(c) for c in components[2:]) + "\n")
(ROOT / "aquila_dac_stimulus.inc").write_text(
    "\n".join(net(c) for c in components[:2]) + "\n" +
    "* Isolated clock enforces solver breakpoints at every DAC sample.\n" +
    "VSAMPLE_CLOCK SAMPLE_CLOCK AGND PULSE(0 1 {TSTART} 0.1n 0.1n {TS/2-0.1n} {TS})\n")

main_directives = [".include aquila_parameters.inc", ".include aquila_models_and_power.inc",
                   "VSAMPLE_CLOCK SAMPLE_CLOCK AGND PULSE(0 1 {TSTART} 0.1n 0.1n {TS/2-0.1n} {TS})",
                   ".tran 0 {TSTOP} 0 {TMAX}", ".include aquila_transient_measurements.inc"]
(ROOT / "AQUILA_TX_ANALOG.cir").write_text(
    "AQUILA TX - sampled Blackman LFM, 200 to 400 kHz, 2 ms\n" +
    "\n".join(main_directives[:2]) + "\n.include aquila_dac_stimulus.inc\n" +
    ".include aquila_signal_chain.inc\n" + "\n".join(main_directives[3:]) + "\n.end\n")


def schematic(items, directives, notes, width=3456):
    lines = ["Version 4", f"SHEET 1 {width} 1152"]
    for c in items:
        x, y = c["pos"]
        spec = registry[c["kind"]]
        for node, (_, px, py, side) in zip(c["nodes"], spec["pins"]):
            ax, ay = x + px, y + py
            dx, dy = {"LEFT": (-32, 0), "RIGHT": (32, 0), "TOP": (0, 32),
                      "BOTTOM": (0, -32), "NONE": (0, 0)}[side]
            if side == "NONE":
                dx, dy = ((-16, 0) if px == 0 and py == 0 else (16, 0))
                if c["kind"].endswith("V"):
                    dx, dy = (0, -16 if py == 0 else 16)
            if dx or dy:
                lines.append(f"WIRE {ax} {ay} {ax+dx} {ay+dy}")
            lines.append(f"FLAG {ax+dx} {ay+dy} {node}")
        lines += [f"SYMBOL symbols\\{c['kind']} {x} {y} R0",
                  f"SYMATTR InstName {c['name']}", f"SYMATTR Value {c['value']}"]
        if c["params"]:
            lines.append(f"SYMATTR SpiceLine {c['params']}")
    for x, y, text in notes:
        lines.append(f"TEXT {x} {y} Left 2 ;{text}")
    for i, d in enumerate(directives):
        lines.append(f"TEXT 32 {832+i*32} Left 2 !{d}")
    return "\n".join(lines) + "\n"


notes = [(32, 32, "AQUILA | LOW-POWER SONAR TRANSMITTER | 100-500 kHz"),
         (32, 72, "Open aquila_parameters.inc to select waveform. Main run: 5 MSPS, Blackman LFM 200-400 kHz, 2 ms."),
         (32, 112, "FUNCTIONAL DAC / SUBSTITUTE OPA2684. TI OPA835 cores represent OPA2835 channels. LTspice execution not verified here."),
         (32, 704, "Left to right: FPGA command -> voltage-output DAC -> AC coupling/buffer -> low-Q SK -> high-Q SK -> current-feedback driver -> 50 ohm."),
         (32, 744, "Net labels are electrical connections. All supply sources, package bypasses and unused channels are in aquila_models_and_power.inc."),
         (1360, 560, "K1=1.150; Q1=0.54054"), (1808, 560, "K2=2.240; Q2=1.31579"),
         (1360, 608, "Both sections: R1=R2=1.02k, Cfb=Cg=220p. f0=709.247 kHz."),
         (2256, 704, "Driver: gain 2, RF=RG=806 ohm. 10 ohm isolation is NOT a matched 50 ohm source."),
         (352, 624, "DAC: AVDD/PVDD +5V; PVSS -2.5V; DVDD/VLOGIC 1.8V."),
         (32, 664, "OPA2835 +/-2.5V; OPA2684 +/-5V. Grounds joined at VGROUND_TIE. No FPGA/SPI/power-converter simulation.")]
(ROOT / "AQUILA_TX_ANALOG.asc").write_text(schematic(components, main_directives, notes))

# Standalone physical filter schematic makes every R/C and feedback node editable.
main_components = components
components = []
add("VAC", "AQ_V", "V_I_V 0", "AC 1", pos=(32, 288))
for i, x in enumerate((320, 1280), 1):
    inn = "V_I_V" if i == 1 else "V_FILTER1"
    out = "V_FILTER1" if i == 1 else "V_FILTER"
    add(f"R{i}A", "AQ_R", f"{inn} n{i}a", "{RFILT}", pos=(x, 288))
    add(f"R{i}B", "AQ_R", f"n{i}a n{i}b", "{RFILT}", pos=(x + 208, 288))
    add(f"C{i}F", "AQ_C", f"n{i}a {out}", "{CFILT}", pos=(x + 208, 128))
    add(f"C{i}G", "AQ_CV", f"n{i}b 0", "{CFILT}", pos=(x + 384, 432))
    add(f"XU{i}", "OPA2835", f"n{i}b n{i}neg OP_P OP_N {out} 0", pos=(x + 480, 320))
    add(f"R{i}F", "AQ_R", f"{out} n{i}neg", f"{{RF{i}}}", pos=(x + 496, 576))
    add(f"R{i}G", "AQ_RV", f"n{i}neg 0", f"{{RG{i}}}", pos=(x + 720, 432))
add("RREPLOAD", "AQ_RV", "V_FILTER 0", "50k", pos=(2192, 432))
filter_directives = [".include aquila_parameters.inc", ".include vendor/OPA2835/OPA835.lib",
                     ".include models/OPA2835_model.lib", "VOPP OP_P 0 2.5", "VOPN OP_N 0 -2.5",
                     ".ac dec 300 1k 30Meg", ".include aquila_ac_measurements_filter_only.inc"]
(ROOT / "AQUILA_FILTER_DETAIL.asc").write_text(schematic(
    components, filter_directives,
    [(32, 32, "AQUILA | PHYSICAL 4TH-ORDER ACTIVE FILTER | schematic detail"),
     (32, 72, "Same Sallen-Key topology as main block subcircuits. AC source is unity. Grounds/rails are ideal in this detail test."),
     (32, 704, "Positive feedback capacitor: first R junction -> amplifier OUTPUT. Shunt capacitor: +IN -> ground."),
     (32, 752, "Edit matching values in aquila_hardware_parameters.inc; this sheet is an independent filter test, not the complete transmitter.")], 2432))
(ROOT / "aquila_ac_measurements_filter_only.inc").write_text(
    "\n".join((ROOT / "aquila_ac_measurements.inc").read_text().splitlines()[:15]) + "\n")


def bench(filename, title, mode=1, window=0, zoh=1, extra="", analysis=None, source="dac", measurements=True):
    text = (f"AQUILA - {title}\n.param MODE={mode} WAVE=2 ZOH={zoh} WIN={window}\n"
            ".param FCAR=300k FSTART=200k FEND=400k TPULSE=2m SCALE=1\n"
            ".include aquila_hardware_parameters.inc\n.include aquila_models_and_power.inc\n")
    text += {"dac": ".include aquila_dac_stimulus.inc\n",
             "ac": "VAC VIN_DAC AGND DC {DAC_MID} AC 1\n",
             "step": "VSTEP VIN_DAC AGND PULSE({DAC_MID} {DAC_MID+DAC_PEAK} {TSTART} 20n 20n 10u 100u)\n"}[source]
    text += ".include aquila_signal_chain.inc\n" + extra + "\n"
    text += (analysis or ".tran 0 {TSTOP} 0 {TMAX}") + "\n"
    if measurements:
        text += ".include aquila_transient_measurements.inc\n"
    text += ".end\n"
    (ROOT / filename).write_text(text)


bench("TEST_01_SINE_BAND.cir", "five sine frequencies, steady-state measurements",
      extra=".step param FCAR list 100k 200k 300k 400k 500k\n"
            ".meas TRAN STEADY_VPP PP V(V_LOAD) FROM {TSTART+200u} TO {TSTART+TPULSE-20u}\n"
            ".meas TRAN STEADY_RMS RMS V(V_LOAD) FROM {TSTART+200u} TO {TSTART+TPULSE-20u}\n"
            ".meas TRAN STEADY_POWER AVG V(P_LOAD_W) FROM {TSTART+200u} TO {TSTART+TPULSE-20u}")
bench("TEST_02_LFM.cir", "sampled Blackman LFM", mode=2, window=1)
bench("TEST_03_GEOMETRIC.cir", "sampled Blackman exponential frequency sweep", mode=3, window=1)
bench("TEST_04_PHASE_CODE.cir", "seven-chip BPSK with Blackman envelope", mode=4, window=1)
bench("TEST_05_ZOH.cir", "MODE 5 forces staircase; WAVE=2 means LFM", mode=5, window=1, zoh=0)
bench("TEST_06_AC.cir", "continuous-time analog-chain AC response (NOT sampled DAC AC)",
      source="ac", analysis=".ac dec 400 1k 30Meg\n.include aquila_ac_measurements.inc", measurements=False)
bench("TEST_07_WINDOW_COMPARE.cir", "rectangular versus Blackman LFM", mode=2,
      extra=".step param WIN list 0 1")
bench("TEST_08_FOURIER.cir", "steady 300 kHz Fourier check; stop before the burst ends",
      analysis=".tran 0 {TSTART+TPULSE-20u} 0 {TMAX}\n.four {FCAR} 15 60 V(V_LOAD)",
      extra=".meas TRAN FOURIER_RMS RMS V(V_LOAD) FROM {TSTART+1m} TO {TSTART+TPULSE-20u}",
      measurements=False)
bench("TEST_09_STEP.cir", "analog step response; DAC replaced by ideal 20 ns step",
      source="step", analysis=".tran 0 60u 0 2n", measurements=False,
      extra=".meas TRAN STEP_PEAK MAX V(V_LOAD) FROM 20u TO 30u\n"
            ".meas TRAN STEP_LEVEL AVG V(V_LOAD) FROM 27u TO 29u")
bench("TEST_10_OVERDRIVE.cir", "deliberate overload; clipping is EXPECTED",
      extra=".step param SCALE list 1 3 6")
bench("TEST_11_SINE_WINDOW_COMPARE.cir", "spectral sidelobe comparison, 300 kHz pulse",
      extra=".step param WIN list 0 1")

(ROOT / "scripts" / "component_manifest.json").write_text(json.dumps(
    {"main": main_components, "symbols": registry}, indent=2) + "\n")
print(f"Generated {len(registry)} symbols, two schematics, and 11 test benches.")

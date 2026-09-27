# AQUILA
FPGA-based sonar waveform generation and DAC streaming, with SystemVerilog RTL and Python simulation and validation models.

AQUILA is an FPGA-oriented sonar waveform generation and validation project. It combines SystemVerilog RTL for sensor-state classification, waveform selection, sample generation, safety checks, and DAC interfaces with Python models for LUT generation, analog-path analysis, and system-level validation.

The repository contains RTL and behavioral models, testbenches, reference captures, analysis results, and plots. The simulations are engineering models; they do not replace validation on the target FPGA, DAC, analog circuitry, or in water.

## What It Does

The system maps temperature, salinity, turbidity, and range inputs to a 4-dimensional environmental state. The state encoder selects one of 81 adaptive waveform profiles. Profiles cover three waveform modes:

- **LFM:** linear frequency-modulated chirp.
- **Geometric:** logarithmic/geometric frequency sweep.
- **Phase coded:** carrier with phase-coded chips.

The active profile is checked against the configured frequency and amplitude limits, then held through a ping by the profile latch. The waveform path generates samples, applies windowing and output gating, and models DAC output. The Python validation additionally models analog filtering, output metrics, FFTs, spectrograms, and power estimates.

The main Python validation checks all 81 LUT entries and a demo input (`28 C`, `450` salinity, `35` turbidity, `2.5 m` range), which encodes to address `0x55`.

## Repository Layout

| Path | Contents |
|---|---|
| `python_model/` | Python waveform, classifier, LUT, analog, power, and validation models. |
| `python_model/results/` | CSV summaries and generated Python-analysis plots. |
| `rtl/` | SystemVerilog modules, RTL testbenches, captured sample CSVs, and waveform-analysis scripts. |
| `AQUILA_AUDIT_REPORT.md` | Design audit, active-path notes, and hardware-validation caveats. |
| `aquila_lfm_spectrogram.png` | Example project-level waveform analysis plot. |

Some CSV, PNG, VCD, and simulator output files are included as reference artifacts from project runs. The `.gitignore` excludes Python caches and future generated RTL simulation outputs from ordinary Git adds.

## Requirements

### Python model

- Python 3 with `pip` (validated with Python 3.14.7).
- NumPy
- SciPy
- Matplotlib
- pandas (used by capture-analysis scripts)

### RTL simulation

- Icarus Verilog with SystemVerilog support (`iverilog` and `vvp`; validated with Icarus Verilog 12.0).
- A terminal with the repository as the working directory.

On Windows, install Python from [python.org](https://www.python.org/downloads/) or the Microsoft Store, and install Icarus Verilog using a Windows build/package manager. Ensure `python`, `iverilog`, and `vvp` are available on `PATH`. On Linux, install Python and Icarus Verilog from the distribution package manager. On macOS, install them with Homebrew.

## Set Up the Python Environment

Run these commands from the repository root.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install numpy scipy matplotlib pandas
```

If PowerShell blocks activation, use the environment's executable directly:

```powershell
.\.venv\Scripts\python.exe -m pip install numpy scipy matplotlib pandas
```

### Linux or macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install numpy scipy matplotlib pandas
```

## Run the Python System Validation

From the repository root, with the environment activated:

```bash
python python_model/system_simulation.py
```

The script validates the classifier and state encoding, all 81 adaptive LUT profiles, frequency limits, 5 MSPS sample-enable timing, all three waveform modes, Hann windowing, the behavioral DAC and analog models, FFT and spectrogram generation, ping-boundary profile changes, and estimated power. A successful run ends with `AQUILA VALIDATION COMPLETE` and prints `PASS` for each check.

### Expected Python output

The exact numeric values below are from a validated run. Paths, package versions, and plot metadata can differ by machine.

```text
==========================================
			AQUILA SYSTEM VALIDATION
==========================================
Environment model              PASS
Demo address                   : 0x55 (1111)
81-state LUT                   PASS
LUT summary                    : 81/81 valid, modes={'GEOMETRIC': 27, 'LFM': 27, 'PHASE_CODED': 27}
Frequency range                : 137580 to 468400 Hz
Pulse duration range           : 2000 to 8000 us
Amplitude range                : 600 to 1000
100-500 kHz safety             PASS
5 MSPS sample timing           PASS
Sample timing                  : 10 FPGA cycles, 5000000 Hz
Geometric                      PASS
	geometric: address=0x50, Fc=400000 Hz, sweep=360000-440000 Hz, N=10000, Vpp=1.1954 V, Vrms=0.2588 V, P=0.001339 W
Lfm                            PASS
	lfm: address=0x51, Fc=300000 Hz, sweep=260000-340000 Hz, N=20000, Vpp=1.5988 V, Vrms=0.3463 V, P=0.002398 W
Phase_Coded                    PASS
	phase: address=0x52, Fc=180000 Hz, sweep=150000-210000 Hz, N=40000, Vpp=2.0176 V, Vrms=0.4330 V, P=0.003750 W
Hann window                    PASS
Ping-boundary adaptation       PASS
DAC model                      PASS
Analog filter                  PASS
Output amplifier model        PASS
FFT                           PASS
Spectrogram                   PASS
DAC interface audit            PASS
Single-lane SPI max rate      : 416667 samples/s (NOT 5 MSPS capable)
Dual-SPI/DDR stream estimate  : 520833 samples/s (below 5 MSPS target)
Power calculation              PASS
Electronics power estimate    : 0.8331 W
50-ohm load power estimate    : 0.010000 W

==========================================
			AQUILA VALIDATION COMPLETE
==========================================
Results directory              : python_model/results
Demo environment               : Environment(temperature=28.0, salinity=450.0, turbidity=35.0, range_m=2.5)
```

The run writes summary data and plots under `python_model/results/`, including:

- `system_summary.csv` with the three demo waveform cases and modeled output metrics.
- `analog_response.csv` with the modeled analog-filter response.
- Time-domain, FFT, and spectrogram plots for geometric and LFM waveforms, and time-domain and FFT plots for the phase-coded waveform.

Useful related scripts include `python_model/adaptive_lut.py` for building and validating the adaptive LUT, `python_model/generate_adaptive_lut_sv.py` for generating the corresponding SystemVerilog LUT, and `python_model/analyze_lfm_capture.py` for analyzing an LFM CSV capture.

## Run the RTL Simulation

The main system-level testbench is `tb_aquila_system_5msps`. From the repository root, compile the RTL sources and testbenches, selecting that testbench as the simulation top.

### Windows PowerShell

```powershell
New-Item -ItemType Directory -Force .\build | Out-Null
$rtl = Get-ChildItem .\rtl -Filter *.sv | ForEach-Object { $_.FullName }
iverilog -g2012 -s tb_aquila_system_5msps -o .\build\aquila_5msps.vvp $rtl
if ($LASTEXITCODE -eq 0) { vvp .\build\aquila_5msps.vvp }
```

### Linux or macOS

```bash
mkdir -p build
iverilog -g2012 -s tb_aquila_system_5msps -o build/aquila_5msps.vvp rtl/*.sv
vvp build/aquila_5msps.vvp
```

The testbench checks initial and ping-boundary profiles, profile limits, and sample-enable timing. A successful run prints `PASS: Aquila 5-MSPS system-level RTL simulation`. It also writes `aquila_5msps.vcd` in the current working directory; open that file in a waveform viewer such as GTKWave to inspect signal timing.

### Expected RTL output

Icarus Verilog 12.0 emits the following non-fatal warnings before the testbench results. The source paths shown here are relative to the repository root.

```text
rtl/digital_window.sv:89: sorry: constant selects in always_* processes are not currently supported (all bits will be included).
rtl/digital_window.sv:89: sorry: constant selects in always_* processes are not currently supported (all bits will be included).
rtl/digital_window.sv:89: sorry: constant selects in always_* processes are not currently supported (all bits will be included).
rtl/digital_window.sv:89: sorry: constant selects in always_* processes are not currently supported (all bits will be included).
rtl/phase_coded_waveform_engine.sv:48: sorry: constant selects in always_* processes are not currently supported (all bits will be included).
VCD info: dumpfile aquila_5msps.vcd opened for output.
INITIAL: addr=aa mode=2 Fc=167580 BW=48000 Tp_us=8000 Amp=1000 valid=1
BOUNDARY: addr=00 requested_mode=0 active_mode=0 active_Fc=428400
TIMING: sample_enable interval=200 ns frequency=5 MHz events=5380
PASS: Aquila 5-MSPS system-level RTL simulation
rtl/tb_aquila_system_5msps.sv:134: $finish called at 1076210000 (1ps)
```

Icarus may print `sorry: constant selects in always_* processes are not currently supported` warnings for some RTL constructs. With the validated Icarus version, these warnings are non-fatal and the testbench completes successfully.

For a smaller sample-rate-generator-only test, compile `rtl/sample_rate_generator.sv` and `rtl/tb_final_5msps.sv`, selecting `tb_final_5msps` as the top:

```bash
iverilog -g2012 -s tb_final_5msps -o build/sample_rate.vvp rtl/sample_rate_generator.sv rtl/tb_final_5msps.sv
vvp build/sample_rate.vvp
```

Other testbenches in `rtl/` cover the controller, LUT, waveform engines, windowing, safety checks, streaming, SPI, and DAC paths. To run a different testbench, change the `-s` top-module name to that bench's module name; include the RTL files it instantiates.

## Important Simulation Limitation

The behavioral system and sample-rate tests validate a 5 MHz sample-enable target. The current physical DAC interface designs do **not** sustain that rate: the single-lane 24-bit SPI path is estimated at about 416.7 kSPS, and the dual-SPI/DDR stream path at about 520.8 kSPS. These are below 5 MSPS. The Python report and `AQUILA_AUDIT_REPORT.md` document this distinction. FPGA timing closure, sustained DAC throughput, analog output measurements, hardware integration, and underwater propagation still require hardware validation.

## Reference Results

The committed CSV captures and plots are reference outputs and input data, not a substitute for rerunning the commands above. Re-running simulations may update files in `python_model/results/` or create new VCD and compiled simulation outputs locally.

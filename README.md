# AQUILA

**AQUILA is a prototype adaptive software-defined sonar transmitter payload for autonomous underwater vehicles (AUVs).** It combines environmental-state classification, profile selection, FPGA waveform generation, an analog transmitter design, a PCB layout, and a mechanical enclosure model.

This repository collects the digital models and RTL, KiCad PCB, LTspice project, and FreeCAD/CadQuery mechanical package. It is an engineering development and simulation project, not a claim of a completed, certified, waterproof, or field-tested sonar payload.

## System Overview

The intended signal and control path is:

```text
Temperature / salinity / turbidity / range-depth inputs
                         |
                         v
            LOW / MEDIUM / HIGH classification
                         |
                         v
        8-bit state address selects one of 81 profiles
                         |
                         v
    Profile latched at ping boundary (frequency, bandwidth,
        duration, amplitude, waveform mode)
                         |
                         v
         FPGA waveform generation and digital windowing
                         |
                         v
           DAC interface -> analog filter -> driver
                         |
                         v
        Analog output / future transducer integration
```

The Python model and SystemVerilog testbenches exercise digital behavior and modeled analog behavior. The LTspice folder contains a separate analog circuit design and independent numerical analysis artifacts. The PCB and enclosure are design deliverables for review and integration; neither simulation results nor CAD validity establish physical hardware performance.

## Repository Contents

| Path | Contents |
|---|---|
| `python_model/` | Environment and classifier models, state encoder, adaptive LUT, waveform generation, DAC/analog behavioral models, validation, and analysis scripts. |
| `rtl/` | SystemVerilog classifier, LUT/profile logic, waveform engines, sample timing, DAC interface and stream logic, and testbenches. |
| `Aquila_pcb/` | KiCad PCB layout source. |
| `AQUILA_LTSPICE/` | Analog schematics, SPICE decks/includes, symbols, models, validation scripts, and published numerical plots/CSV results. Simulator `.raw` and `.log` run files are excluded. |
| `aquila-freecad/` | Assembly and exploded STEP exports, individual STEP/STL parts, printable-parts ZIP, parametric CadQuery source, drawings, and validation/build documentation. |
| `AQUILA_AUDIT_REPORT.md` | Digital architecture audit, interface throughput observations, and open hardware-validation work. |

## Digital Model and RTL

The Python reference and RTL implement a prototype LOW/MEDIUM/HIGH classification of temperature, salinity, turbidity, and AUV-to-seabed range/depth. Four 2-bit classifications form an 8-bit state address. The three valid classes across four inputs yield 81 environmental profiles. The LUT selects a center frequency, bandwidth, pulse duration, amplitude, and waveform mode; the active profile is held for a ping and updated at a ping boundary.

Three waveform modes are represented: linear-frequency-modulated (LFM) chirp, geometric frequency sweep, and phase-coded pulse. Digital windowing, including Hann windowing, and profile safety checks are also modeled.

The system-level RTL test targets a 50 MHz clock with a 5 MSPS sample-enable interval. This is not the same as a sustained DAC output rate: the audited single-lane SPI path is estimated at about 416.7 kSPS, and the dual-SPI/DDR stream path at about 520.8 kSPS. Neither audited interface reaches 5 MSPS.

### Python Setup and Validation

Requirements: Python 3, NumPy, SciPy, Matplotlib, and pandas (pandas is used by capture-analysis scripts).

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install numpy scipy matplotlib pandas
python python_model/system_simulation.py
```

Linux or macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install numpy scipy matplotlib pandas
python python_model/system_simulation.py
```

The system simulation checks classification and state encoding, the 81 LUT profiles, waveform modes, sample timing, profile changes at ping boundaries, behavioral DAC and analog models, FFT/spectrogram analysis, and estimated power. Results are written under `python_model/results/`.

### RTL Test

Install Icarus Verilog (`iverilog` and `vvp`) and run from the repository root.

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force .\build | Out-Null
$rtl = Get-ChildItem .\rtl -Filter *.sv | ForEach-Object { $_.FullName }
iverilog -g2012 -s tb_aquila_system_5msps -o .\build\aquila_5msps.vvp $rtl
if ($LASTEXITCODE -eq 0) { vvp .\build\aquila_5msps.vvp }
```

Linux or macOS:

```bash
mkdir -p build
iverilog -g2012 -s tb_aquila_system_5msps -o build/aquila_5msps.vvp rtl/*.sv
vvp build/aquila_5msps.vvp
```

The testbench is expected to report `PASS: Aquila 5-MSPS system-level RTL simulation`. It writes a VCD waveform dump in the current working directory. Icarus may print non-fatal warnings about constant selects in `always_*` processes.

## PCB Layout

`Aquila_pcb/AQUILA_TX_PCB_FIXED.kicad_pcb` is the included KiCad PCB layout. This repository snapshot contains the board file; it does not establish fabrication, electrical rule-check clearance, assembly, or physical test results. Confirm footprints, constraints, routing, and the matching schematic/BOM before manufacturing.

## LTspice Analog Design

`AQUILA_LTSPICE/` contains the transmitter analog schematics (`AQUILA_TX_ANALOG.asc` and `AQUILA_FILTER_DETAIL.asc`), circuit decks, reusable includes, custom symbols and models, test decks, scripts, and numerical result files. The LTspice-specific README and engineering report describe the circuit assumptions and model provenance.

The checked-in `results/` plots and CSV files are from an independent Python/SciPy numerical analysis. `results/validation_summary.json` explicitly records that native LTspice and alternate SPICE execution were not performed for those results. They must not be represented as native LTspice measurements. The DAC, op-amp, output-driver, and analog-chain models have stated limitations; see `AQUILA_LTSPICE/README_AQUILA_LTSPICE.md` before using the design.

Python requirements for the numerical analysis are listed in `AQUILA_LTSPICE/scripts/requirements.txt`. From that folder, run:

```bash
python -m pip install -r scripts/requirements.txt
python scripts/validate_numerically.py
```

`scripts/build_project.py` regenerates generated schematic and symbol files from its component manifest; review its documentation and local edits before running it.

## Mechanical CAD

`aquila-freecad/AQUILA_assembly.step` is the assembled named-part model; `AQUILA_exploded.step` is a presentation view and must not be used as an assembly-position reference. Individual STEP and STL exports are in `aquila-freecad/parts/`; the printable-parts ZIP contains the custom printable components. The editable parametric generator is `aquila-freecad/source/aquila.py`.

The documented nominal enclosure is about 330 mm long, with a 110 mm shell outside diameter and 102 mm bore. The package includes a build note, parameter files, drawings, a part manifest, validation metadata, and SHA-256 checksums. The validation records B-rep and selected fit/STEP round-trip checks; it is not a tolerance, pressure, thermal, fatigue, or certification analysis. PCB/component envelopes and several mechanical interfaces are placeholders that require measurement against selected real hardware. The model is not pressure-rated or certified waterproof. Review `aquila-freecad/BUILD_NOTES.md` before printing or manufacturing.

## Validation Scope and Limitations

- The Python and RTL checks validate model and simulated digital behavior; they do not establish FPGA timing closure or operation on a physical board.
- The Python analog and power results are estimates based on configured assumptions, not oscilloscope measurements or measured power consumption.
- The LTspice numerical plots are not the result of a native SPICE execution.
- The KiCad file and CAD exports are design artifacts, not evidence of fabricated, assembled, or tested hardware.
- No transducer, hydrophone, tank, or underwater propagation validation is included.
- The enclosure has no assigned depth rating and is not certified waterproof.

The prototype's 100-500 kHz profile/safety region is an electrical design range, not a demonstrated acoustic operating band or proof of sonar range or imaging performance. Sensor thresholds and LUT policies are prototype assumptions, not calibrated environmental measurements or propagation-optimized profiles.

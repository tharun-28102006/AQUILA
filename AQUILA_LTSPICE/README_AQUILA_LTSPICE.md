# AQUILA — analog transmitter LTspice project

**Engineering simulation package, not a fabrication release.** This folder contains actual `.asc`, `.cir`, `.inc`, `.lib`, and `.asy` files. No external model installation is required for the supplied project.

## Validation status — read first

- **Native LTspice: NOT EXECUTED in the authoring environment.** LTspice/Wine was unavailable. ngspice was absent from the configured RPM repositories; a downloaded alternate binary required incompatible runtime libraries. Native parsing, convergence, vendor-model response and schematic rendering therefore remain unverified.
- **Independent Python/SciPy numerical simulation: EXECUTED.** It uses the same physical filter topology and component values, but a one-pole OPA2835 approximation, NOT the TI macromodel. CSV/JSON/PNG results are explicitly labeled. They must not be quoted as LTspice results.
- **Structural checks: EXECUTED.** Local include paths, schematic component pin counts and sequential symbol SpiceOrder fields were checked. These checks do not replace an LTspice parser.
- **Hardware, THD/SFDR, stability with a cable/transducer, thermal operation and all production corners: NOT VERIFIED.**

See `ENGINEERING_REPORT.md` for equations, numerical results, status by requirement, power accounting and PCB hold points.

## 1. Open and run — no command line required

1. Download the ZIP and **extract the entire `AQUILA_LTSPICE` folder**. Do not open a schematic inside the compressed archive.
2. Install/open a current Analog Devices LTspice release for your operating system.
3. Choose **File → Open → `AQUILA_TX_ANALOG.asc`**. This is the left-to-right main schematic. Choose **Simulate → Run**.
4. The default is a 2 ms Blackman-windowed, 200–400 kHz LFM, sampled at 5 MSPS. The simulation includes 20 us of idle time before the pulse and 80 us after it.
5. Click or add the traces `V(VIN_DAC)`, `V(V_I_V)`, `V(V_FILTER)`, `V(V_AMP)`, `V(V_LOAD)`. `VIN_DAC` includes a 1.25 V common-mode level; use `V(VIN_DAC)-1.25` to overlay AC components.
6. Add `I(VLOAD_SENSE)` for load current and `I(VAMP_SENSE)` for driver output current. The latter includes feedback-network current.
7. Open **View → SPICE Error Log** (Ctrl+L on Windows) for `.meas` results. If there is an error, retain the log; native compatibility has not been certified here.
8. If schematic symbol resolution is a problem, first try **File → Open → `AQUILA_TX_ANALOG.cir`**, then Run. It contains the same signal chain and does not need graphical symbols.

### Symbol placement

Keep `symbols/` directly beside the main `.asc`. The schematic uses relative references such as `symbols\OPA2835`. On an LTspice installation that does not find project-relative subdirectories, add the **project root** to the symbol search paths in LTspice settings. Do not copy project files into the program installation directory. If necessary on macOS, replace the symbol path separator with `/` in the `SYMBOL` lines.

The `.cir` and `.inc` include paths use `/` and are relative to the project root. Open the test files from that root, not a moved copy. Keep the vendor directory intact.

## 2. Project contents

- `AQUILA_TX_ANALOG.asc` — main schematic, with functional block symbols and real net connections.
- `AQUILA_TX_ANALOG.cir` — equivalent main simulation deck.
- `AQUILA_FILTER_DETAIL.asc` — independently runnable AC schematic showing every filter resistor, capacitor and op-amp connection.
- `aquila_parameters.inc` — user-editable main-run controls.
- `aquila_hardware_parameters.inc` — common hardware, sample-rate, timing and code values.
- `aquila_waveform_source.inc` — mathematical sampled FPGA output command.
- `aquila_dac_stimulus.inc` — source, DAC instance and sample-clock breakpoint source.
- `aquila_signal_chain.inc` — coupling, buffer, filter sections, driver, sensors and load.
- `aquila_analog_blocks.inc` — physical Sallen-Key sections and spare driver feedback configuration.
- `aquila_models_and_power.inc` — model includes, supplies, local/bulk bypass capacitors, unused channels and monitors.
- `aquila_*measurements*.inc` — transient and AC automatic measurements.
- `models/AD3541R_model.lib` — clearly labeled behavioral equivalent.
- `models/OPA2835_model.lib` — channel/dual wrappers for the downloaded TI OPA835 core.
- `models/OPA2684_model.lib` — explicitly labeled current-feedback substitute.
- `vendor/OPA2835/OPA835.lib` — unmodified TI PSpice model, Final 1.2, downloaded from TI's OPA2835 model link.
- `vendor/OPA2835_original.zip` — original TI archive; preserve its copyright/disclaimer.
- `symbols/*.asy` — **12 actual symbol files**, including single-channel and SOIC-8 dual amplifier variants.
- `TEST_*.cir` — **11 ready-configured test benches**, listed below.
- `results/` — executed independent numerical results; not native SPICE results.
- `scripts/` — reproducible project generator, numerical validator and component manifest.

## 3. Stimulus controls

Edit `aquila_parameters.inc` for the main schematic/deck. Standalone tests declare their own controls and share `aquila_hardware_parameters.inc`.

| Control | Meaning | Default |
|---|---|---:|
| MODE | 1 sine; 2 LFM; 3 geometric; 4 phase-coded; 5 forced staircase | 2 |
| WAVE | Underlying waveform 1–4 when MODE=5 | 2 |
| ZOH | 1 sample/hold all modes; 0 continuous mathematical command | 1 |
| WIN | 1 digital-equivalent Blackman envelope; 0 rectangular pulse | 1 |
| FCAR | Sine/phase-code carrier frequency | 300 kHz |
| FSTART, FEND | Sweep endpoints; both positive | 200, 400 kHz |
| TPULSE | Pulse duration; choose an integer number of DAC periods | 2 ms |
| SCALE | Multiply the 350 mV DAC AC peak | 1 |
| FS | Sample rate, in the hardware parameter file | 5 MSPS |

Use MODE=5/WAVE=1 for a sampled sine; MODE=5/WAVE=2 for a sampled LFM. MODE=5 forces ZOH regardless of the ZOH setting. Even with ZOH=0, the DAC equivalent still applies 16-bit quantization and its settling pole: it is a diagnostic continuous-time command, not a physical unsampled DAC.

Do not use zero/negative sweep frequencies or pulses shorter than two samples. NCHIPS is fixed at 7 by this implementation; change the seven CODE parameters to +1 or -1, not NCHIPS, unless you also extend the source function. Idle output is DAC midscale, not 0 V.

### Equations

Local time is measured from TSTART. For the sampled version:

$$n=\lfloor (t-T_{start})F_s\rfloor,\qquad t_s=n/F_s,\qquad N=\operatorname{round}(T_pF_s).$$

The command is held at the value evaluated at that sample time. The isolated `VSAMPLE_CLOCK` is not part of the signal path; it forces time-step breakpoints at the sample boundaries.

$$v_{cmd}=1.25+0.350\,SCALE\,w[n]\sin\phi(t_s)\ \mathrm{V}.$$

$$w[n]=0.42-0.5\cos\left(\frac{2\pi n}{N-1}\right)+0.08\cos\left(\frac{4\pi n}{N-1}\right).$$

For an LFM:

$$\phi(t_s)=2\pi\left(f_0t_s+\frac{f_1-f_0}{2T_p}t_s^2\right).$$

For the geometric sweep, with positive ratio:

$$r=\frac{f_1}{f_0},\qquad f(t_s)=f_0r^{t_s/T_p},\qquad \phi(t_s)=2\pi\frac{f_0T_p}{\ln r}\left(r^{t_s/T_p}-1\right).$$

Equal endpoints reduce to a sine. Descending sweeps are supported. The last sampled LFM frequency is just below the mathematical endpoint because the final update occurs one sample period before the pulse ends.

For phase coding, the carrier is multiplied by `[+1,+1,-1,+1,-1,-1,+1]` across seven equal nominal chip intervals. A -1 chip is a 180-degree carrier phase reversal. At 5 MSPS, boundaries move to the next available sample; chip lengths alternate as needed because 10000 is not divisible by seven. This is a simple illustrative BPSK sequence, **not claimed to be a Barker code**. The analog LPF rounds the phase transitions; it does not preserve infinitely sharp phase steps.

The FPGA window is represented mathematically at the **input only**. The analog circuit does not contain a Blackman LUT or an analog Blackman circuit.

## 4. Test bench matrix

Open a `.cir` with File → Open, then Run. These are independent decks: do not paste all analyses into one file.

| File | Analysis |
|---|---|
| TEST_01_SINE_BAND.cir | Five stepped frequencies: 100/200/300/400/500 kHz, unwindowed, sampled; steady Vpp/RMS/power |
| TEST_02_LFM.cir | Primary 2 ms sampled Blackman LFM |
| TEST_03_GEOMETRIC.cir | True exponential-frequency sweep, not linear |
| TEST_04_PHASE_CODE.cir | Seven-chip BPSK, 300 kHz, 2 ms |
| TEST_05_ZOH.cir | Explicit MODE=5 staircase test |
| TEST_06_AC.cir | Analog AC response and normalized cutoff/image measurements |
| TEST_07_WINDOW_COMPARE.cir | LFM with WIN stepped 0/1 |
| TEST_08_FOURIER.cir | 300 kHz steady-tone Fourier calculation, stopping before pulse turn-off |
| TEST_09_STEP.cir | Analog step response, 350 mV input step |
| TEST_10_OVERDRIVE.cir | SCALE 1/3/6; higher levels intentionally exceed limits |
| TEST_11_SINE_WINDOW_COMPARE.cir | Sine-burst rectangular/Blackman sidelobe comparison |

An AC analysis is **not** an analysis of the time-varying sample/hold. TEST_06 substitutes a 1 V AC source at VIN_DAC. It measures only the analog chain; sampled images are tested in transient/FFT.

## 5. FFT procedure

1. Run the tone, LFM, or window-comparison transient test.
2. Plot the DAC AC component, V_FILTER, and V_LOAD.
3. Select the identical time interval for all signals. Use the complete pulse plus enough quiet tail to include filter ringing for pulse-spectrum comparisons.
4. Select **View → FFT**, select the traces, and use a rectangular FFT analysis window when comparing the already-Blackman-windowed pulse against the rectangular pulse. An additional FFT window would conflate two different windows.
5. Use the same FFT length, time aperture and amplitude convention. At least 262144 points over the 2.1 ms record is recommended; 524288 or more is useful. `plotwinsize=0` disables waveform compression. The transient maximum step is 10 ns.
6. For images inspect 4.5–5.5 MHz, including 4.7 and 5.3 MHz for a 300 kHz carrier. Compare each image relative to that trace's carrier, not just its absolute voltage; the filter and driver have gain.
7. For intrinsic THD, use a settled, coherent unwindowed sine interval, not the chirp. TEST_08 stops before the pulse ends so `.four` does not examine silence. The substitute driver lacks real device harmonic distortion: its reported THD is **not a hardware THD prediction**.

## 6. Pin order and physical pin mapping

`SpiceOrder` indexes the **subcircuit argument list**, not an invented IC package. Every custom symbol follows its matching `.subckt` order.

| Symbol | Subcircuit argument order |
|---|---|
| AQUILA_WAVEFORM_SOURCE | CMD, REF |
| AD3541R | CMD, OUT, AGND, AVDD, DVDD, VLOGIC, PVDD, PVSS, DGND |
| OPA2835 | +IN, -IN, V+, V-, OUT, REF |
| OPA2684 | +IN, -IN, V+, V-, OUT, REF |
| AQUILA_SK | IN, OUT, V+, V-, REF |
| OPA2835_DUAL / OPA2684_DUAL | OUTA, INA-, INA+, V-, INB+, INB-, OUTB, V+ |

The single-channel symbols are simulation abstractions with an extra REF pin; **do not use them as PCB footprints**. The dual symbols use the actual SOIC-8 order for the chosen D packages: pins 1/2/3 = output/inverting/noninverting A; pin 4 = negative rail; pins 5/6/7 = noninverting/inverting/output B; pin 8 = positive rail. The TI core's own order is `VEE VCC VINM VINP VOUT PD`; the wrapper ties PD high. REF must be SPICE ground because TI's unmodified core uses node 0 internally.

Physical allocation: U1A buffer, U1B low-Q filter, U2A high-Q filter, U2B spare follower. U3A driver, U3B spare gain-2 stage with its noninverting input grounded. **Never short output to the inverting input of the unused current-feedback channel**; retain its 806-ohm feedback resistor.

The DAC symbol is a nine-terminal behavioral block, not a physical AD3541R package pinout; CMD is a mathematical voltage command, not an actual DAC pin. Map the real DAC package, reference and digital pins from the selected AD3541R data sheet before PCB work.

## 7. Model provenance and limitations

- ADI's product page explicitly lists an **official AD3541R model in LTspice**. An attempted direct download was not retrievable. This package therefore uses a disclosed approximation; it does **not** claim no official model exists. The actual official model should replace this block after its interface, range and limitations are inspected in an updated LTspice installation. It is not assumed to be pin-compatible.
- The OPA2835 product model download `https://www.ti.com/lit/zip/slom221` contains `OPA835.lib`. The unmodified single-channel TI core is used for each channel, with the original archive preserved. Dual-channel coupling and shared thermal effects are not represented. PSpice-to-LTspice compatibility is not runtime-certified here.
- A usable OPA2684 manufacturer model was not obtained in this environment. Its replacement is explicitly current-feedback: finite transimpedance, 4-ohm inverting-input resistance, a slew-limited compensation capacitor, output swing/current limits and quiescent current. It is not an unrelated ideal op-amp silently renamed.
- The DAC model quantizes to 16 bits over 0–2.5 V and uses one RC pole with a 100 ns 0.1% settling assumption and 0.5-ohm output resistance. It omits nonlinear settling, glitches, reference noise, INL/DNL, digital interface timing and supply consumption. Its power pins document the intended domains but do not enforce them.

## 8. Reproduction and edits

The packaged numerical plots are the executed **nominal** independent check. `scripts/validate_numerically.py` documents its fixed numerical assumptions. It does not parse and run arbitrary SPICE decks and it does not execute the TI model. Its Python package requirements are in `scripts/requirements.txt`.

`build_project.py` regenerates the two schematics, the custom symbols, shared chain and test profiles from one component manifest. Do not run it after manually editing generated files unless you intend to replace those edits. The main `.asc` and `.cir` initially match, but later schematic edits do not automatically update the separate `.cir`.

Nothing in the web download page executes SPICE or changes circuit parameters. The actual simulation files, not a web mockup, are the deliverable.

# AQUILA transmitter — engineering report

## Release decision

**Suitable for engineering review and local LTspice testing; NOT approved for PCB fabrication.** Native LTspice execution and TI model compatibility remain unverified. The executed results below are independent linearized numerical simulations, not fabricated LTspice measurements.

## System input → system output

**Input:** a mathematical FPGA command feeding a 16-bit, 5 MSPS, voltage-output AD3541R equivalent. Nominal DAC output is 1.25 V common-mode with 350 mV AC peak. Modes include sine, LFM, geometric sweep and seven-chip phase code, with selectable digital-equivalent Blackman weighting and ZOH.

**Output:** a ground-centered electrical waveform of approximately 3 Vpp across one 50-ohm test termination, over the 100–500 kHz operating band. This is a low-power instrument demonstration, not an underwater transducer power amplifier.

**Chain:** sampled command → voltage DAC/settling → 100 nF AC coupling and 100 kohm bias → OPA2835 buffer → two physical Sallen-Key sections → OPA2684 current-feedback driver → 10-ohm isolation → 50-ohm load.

### Important architecture correction

The AD3541R is a **voltage-output DAC with an internal transimpedance amplifier**. Adding another external I/V converter is not appropriate for its configured voltage output. `V_I_V` retains the requested measurement label but is actually the buffered, AC-coupled voltage node. No external I/V power is required.

## Component values and rails

| Function | Values / configuration |
|---|---|
| DAC selected span | 0–2.5 V; midscale 1.25 V; 0.350 V AC peak |
| DAC settling equivalent | 1 kohm / 14.476 pF, buffered; 0.5-ohm output resistance |
| AC conditioning | 100 nF coupling, 100 kohm bias to AGND; approximately 15.9 Hz high-pass, before input loading |
| Buffer | U1A, OPA2835 represented by TI OPA835 core, unity voltage follower |
| Filter stage 1 | R1=R2=1.02 kohm; Cfb=Cg=220 pF; Rf=1.50 kohm; Rg=10.0 kohm |
| Filter stage 2 | R1=R2=1.02 kohm; Cfb=Cg=220 pF; Rf=12.4 kohm; Rg=10.0 kohm |
| Driver | U3A OPA2684 equivalent, noninverting gain 2; Rf=Rg=806 ohm |
| Output | 10-ohm series isolation, single 50-ohm load; feedback senses before isolation resistor |
| OPA2835 rails | +2.5 / -2.5 V, 5 V total; within 2.5–5.5 V operating range |
| OPA2684 rails | +5 / -5 V, 10 V total; within 5–12 V operating range |
| DAC domain plan | AVDD +5 V; DVDD +1.8 V; VLOGIC +1.8 V; PVDD +5 V; PVSS -2.5 V |
| Grounds | AGND at SPICE node 0, DGND joined through VGROUND_TIE |
| Local bypass | 100 nF per package/rail; 20 milliohm illustrative ESR |
| Bulk bypass | 4.7 uF on buffer/filter rails and most DAC rails; 10 uF per driver rail; 1 uF logic |

The DAC power pins are functional model terminals, not package pins. Its complete reference decoupling, rail sequencing and selected-range register configuration are not represented. Confirm those against the exact AD3541R ordering code and latest data sheet before fabrication. The extra negative DAC amplifier rail provides room around the bottom of the unipolar range; it does not imply a bipolar DAC output configuration.

No regulators, FPGA, SPI engine or digital switching-current model are included. Ideal voltage sources plus bypass capacitors cannot establish power-integrity performance.

## Filter design equations

With equal resistors and equal capacitors in each noninverting Sallen-Key section:

$$H_i(s)=\frac{K_i}{(sRC)^2+(3-K_i)sRC+1},\qquad K_i=1+\frac{R_{fi}}{R_{gi}}.$$

$$f_0=\frac{1}{2\pi RC},\qquad Q_i=\frac{1}{3-K_i}.$$

Fourth-order Butterworth target section Q values:

$$Q_{1,\mathrm{target}}=0.5411961,\qquad Q_{2,\mathrm{target}}=1.3065630.$$

They imply gains of approximately 1.152241 and 2.234633. E-series values were selected rather than claiming exact ideal coefficients:

$$K_1=1.150,\ Q_1=0.5405405;\qquad K_2=2.240,\ Q_2=1.3157895.$$

$$f_0=\frac{1}{2\pi(1020)(220\times10^{-12})}=709246.6\ \mathrm{Hz}.$$

This is a **near-Butterworth** filter, not an exact textbook Butterworth realization. Low-Q precedes high-Q to reduce intermediate peaking. Finite amplifier gain/phase shifts both Q and overall cutoff; the independent 30 MHz GBW surrogate gives **704.4 kHz** for the overall normalized -3.0103 dB crossing. A 709.25 kHz component pole is not automatically the actual cascaded cutoff.

For unequal real components, useful for tolerance checks:

$$f_0=\frac{1}{2\pi\sqrt{R_1R_2C_{fb}C_g}},\qquad Q=\frac{\sqrt{R_1R_2C_{fb}C_g}}{C_g(R_1+R_2)+C_{fb}R_1(1-K)}.$$

Use C0G/NP0 capacitors, preferably 1%, and 0.1–1% thin-film resistors. The high-Q section is especially sensitive to ratios and finite GBW. A corner/Monte Carlo study with real tolerances remains a PCB release prerequisite.

## Gain and output-drive calculations

$$G_{filter}=1.15\times2.24=2.576.$$

$$G_{driver}=1+\frac{806}{806}=2,\qquad G_{load}=2\frac{50}{50+10}=1.666667.$$

$$G_{chain,DC}=2.576\times1.666667=4.293333.$$

$$V_{load,pp,ideal}=2(0.350)(4.293333)=3.00533\ \mathrm{V}.$$

For the rounded target of 3 Vpp into 50 ohms:

$$V_{pk}=1.5\ \mathrm{V},\quad V_{rms}=\frac{3}{2\sqrt2}=1.06066\ \mathrm{V}.$$

$$I_{pk}=\frac{1.5}{50}=30.0\ \mathrm{mA},\quad I_{rms}=21.213\ \mathrm{mA},\quad P_L=\frac{1.06066^2}{50}=22.5\ \mathrm{mW}.$$

The driver must produce 3.6 Vpp before the 10-ohm resistor. Peak feedback current is approximately 1.117 mA, making total peak drive about 31.1 mA rather than only the 30 mA load current. The selected current-feedback stage and split rails have ample nominal headroom; no idealized 3 Vpp claim is made on a marginal single supply.

$$SR_{required}=2\pi fV_{amp,pk}=2\pi(500\,\mathrm{kHz})(1.8\,\mathrm{V})=5.655\ \mathrm{V/\mu s}.$$

For the OPA2684 at gain +2, the data sheet gives about **750 V/us** typical at +/-5 V (780 V/us refers to its inverting test). Its typical 170 MHz gain-2 bandwidth uses an approximately 800-ohm feedback resistor. A current-feedback amplifier does **not** obey a constant-GBW gain law; the resistor magnitude must be retained. The substitute uses a conservative 80 mA clamp and 1.5 V rail headroom, not the 120 mA headline as a guaranteed distortion-free linear current rating.

The OPA2835 advertises 56 MHz unity-gain small-signal bandwidth, but its gain-bandwidth product is approximately **30 MHz** in the tabulated gain-10 condition. The numerical cross-check uses the conservative 30 MHz single-pole approximation; it does not silently treat 56 MHz as an exact one-pole GBW. Typical slew rate is about 160 V/us and output drive about 40 mA. Nominal filter outputs below 0.93 V peak and amplifier inputs near ground leave useful margin on +/-2.5 V rails; the +rail input common-mode restriction still matters under overload.

## Executed numerical results — not LTspice measurements

Method: 5 ns time grid (200 MS/s numerical integration), 5 MSPS 16-bit ZOH input, explicit first-order settling, physical Sallen-Key transfer equations, 100 dB/30 MHz single-pole voltage-feedback surrogate and finite-transimpedance driver approximation. Nominal outputs were **not clipped in software** to force a pass; limit margins were checked after the linear solution.

| Sine frequency | Load Vpp | Load Vrms | Load Irms | Load power | Normalized filter gain |
|---:|---:|---:|---:|---:|---:|
| 100 kHz | 3.0049 V | 1.0624 V | 21.248 mA | 22.573 mW | +0.025 dB |
| 200 kHz | 3.0248 V | 1.0694 V | 21.389 mA | 22.874 mW | +0.101 dB |
| 300 kHz | 3.0561 V | 1.0805 V | 21.609 mA | 23.348 mW | +0.221 dB |
| 400 kHz | 3.0826 V | 1.0898 V | 21.796 mA | 23.754 mW | +0.339 dB |
| 500 kHz | 3.0290 V | 1.0710 V | 21.419 mA | 22.939 mW | +0.243 dB |

These results include finite-GBW peaking: the analog filter is not perfectly flat. Frequency-dependent DAC ZOH droop is also present. Peak-to-peak DAC samples do not necessarily sample the carrier's mathematical peak (notably at 500 kHz); use the AC transfer function or a fundamental-amplitude fit for gain flatness, not only the Vpp ratio.

- Maximum predicted steady driver output: **1.850 V peak**; minimum physical rail distance about **3.150 V**.
- Maximum predicted driver current including feedback: **31.98 mA peak**.
- Maximum steady driver slew over these tests: **5.71 V/us**.
- Overall filter -3 dB frequency: **704.4 kHz**.
- All ten nominal numerical/algorithmic checks passed. This is not a statement that all hardware requirements passed.

| 2 ms Blackman pulse | Load Vpp | Pulse-window Vrms | Pulse-window power | Output energy including tail |
|---|---:|---:|---:|---:|
| LFM 200–400 kHz | 3.0560 V | 0.5963 V | 7.111 mW | 14.223 uJ |
| Geometric 200–400 kHz | 3.0501 V | 0.5952 V | 7.086 mW | 14.172 uJ |
| Seven-chip phase code | 3.0561 V | 0.5960 V | 7.103 mW | 14.207 uJ |

Blackman-pulse RMS is lower than continuous-sine RMS. For a flat chain and many carrier cycles, the mean-square Blackman factor is approximately 0.3046, giving about 6.85 mW pulse-average power at a 3 Vpp envelope peak. Whole-record average additionally includes pre/post silence; repetition-average power depends on the actual duty cycle.

The central 80% output-frequency check shows median error around **94 Hz LFM** and **90 Hz geometric** relative to the undelayed command. These are numerical sanity checks, not frequency-accuracy specifications; filter group delay and Hilbert-transform edge behavior contribute. The geometric midpoint command is about 282.84 kHz, distinctly different from the 300 kHz LFM midpoint.

### DAC images and window comparison

For a 300 kHz sampled tone:

| Image | DAC image/carrier | Filtered image/carrier | Added suppression through buffer/filter |
|---:|---:|---:|---:|
| 4.7 MHz | -24.61 dBc | -92.52 dBc | 67.91 dB |
| 5.3 MHz | -25.83 dBc | -98.10 dBc | 72.27 dB |

These are **idealized surrogate predictions**, not a promised -90 dBc hardware noise floor. Real output impedance, parasitic feedthrough, noise, DAC glitches and op-amp higher poles can substantially reduce rejection. The numerical input spectrum is a deterministic quantized pulse, not a measured DAC spectrum.

`results/fft/blackman_comparison.png` compares rectangular and Blackman **input** pulses at equal peak amplitude, with each spectrum normalized to its own peak. Blackman lowers sidelobes at the cost of a broader main lobe and lower pulse energy. Applying the window to an LFM also weights the swept frequency band; it does not preserve a flat sweep spectrum. LPF image rejection and digital pulse-window sidelobe reduction are different mechanisms.

### Native SPICE actual results

**Not available.** There are no authentic LTspice `.raw` or `.log` results in this release. `.meas`, `.ac`, `.tran`, and `.four` are configured for local execution. A results directory is not evidence that LTspice has been run. The unmodified TI model and the OPA2684 nonlinear substitute still need native convergence and waveform validation.

## Power accounting

| Category | Value / status |
|---|---|
| External I/V stage | Not applicable; AD3541R already provides voltage output |
| Buffer U1A quiescent | 1.25 mW, data-sheet-typical estimate |
| Two active filter channels | 2.50 mW, data-sheet-typical estimate |
| Spare OPA2835 channel | 1.25 mW, included rather than silently ignored |
| All OPA2835 channels | 5.00 mW quiescent estimate at 5 V total |
| Both OPA2684 channels | 34.0 mW quiescent estimate at 10 V total |
| Total amplifier quiescent | 39.0 mW typical estimate |
| Load | 22.5 mW target sine; 23.35 mW numerical 300 kHz result |
| DAC including internal TIA/reference | **Unknown here**; equivalent does not model supply current |
| FPGA/interface/regulators | Out of simulation scope; not zero |

Quiescent power plus load power is **not** total supply input power. As a rough class-B estimate at the nominal target, including feedback current:

$$P_{driver,signal}\approx\frac{2V_sI_{amp,pk}}{\pi}=\frac{2(5)(0.031117)}{\pi}\approx99.0\ \mathrm{mW}.$$

Adding both amplifier packages' quiescent estimates gives about **138 mW amplifier-rail input** during a continuous target sine, before additional dynamic/filter losses. Add the actual DAC power, regulator losses and other electronics to obtain system power. Do **not** add the 22.5 mW load again: it is already supplied by those rails. The 10-ohm resistor dissipates approximately 4.5 mW; the driver feedback network about 1.0 mW.

For a Blackman pulse, mean absolute amplitude is about 0.42 of the unwindowed level, so the same rough model predicts about 80.6 mW amplifier input averaged over the pulse, excluding DAC and regulator losses. Idle still consumes quiescent power unless a real power-management scheme is implemented.

LTspice monitors distinguish `P_OPA2835_MODEL` (TI modeled supply draw) from `P_OPA2684_PROXY` (explicit quiescent plus approximate class-B signal-current bookkeeping). They are not hardware power measurements. The analog total cannot be honestly reported as an exact number without the missing DAC and regulator data.

## Requirement-by-requirement disposition

**PASS-N** means the independent nominal numerical approximation passed; **PENDING** means native model or bench evidence is still required. No PENDING item should be read as a PASS.

| Requirement | Status | Evidence / limitation |
|---|---|---|
| Actual files and symbols | PASS-STRUCTURAL | Two .asc sheets, matching main .cir, 12 .asy, model/include files |
| Correct voltage-DAC conditioning | PASS-DESIGN / PENDING | Buffer and AC coupling; no erroneous extra I/V; official DAC model pending |
| 5 MSPS staircase / settling | PASS-N / PENDING | Sampled source, 16-bit quantization, 14.476 ns pole; real DAC effects omitted |
| Full 100–500 kHz passband | PASS-N | 3.00–3.08 Vpp; physical amplifier corners pending |
| Approx. 700 kHz fourth-order LPF | PASS-N | 709.25 kHz component pole; 704.4 kHz surrogate cutoff |
| DAC image suppression | PASS-N / PENDING | 67.9/72.3 dB extra suppression; PCB parasitics/noise not represented |
| 3 Vpp into 50 ohms | PASS-N | 30–31 mA load peak; single termination assumed |
| Driver voltage/current/slew limits | PASS-N / PENDING | Nominal margins calculated; native overload and stability tests pending |
| Preserve LFM and geometric sweeps | PASS-N | Output plots and frequency-law checks; phase/delay are not zero |
| Preserve phase code | CONDITIONAL | Code waveform present with expected rounded transitions; no matched-filter/correlation validation |
| Preserve Blackman envelope | PASS-N | Pulse plots and sample endpoint checks; no analog window implementation |
| No instability | PENDING | Linear surrogate has stable poles; real loop/cable/PCB stability not established |
| Distortion / SFDR | PENDING | Driver equivalent lacks calibrated nonlinear distortion/noise |
| Power measurement | PARTIAL | Load simulated numerically; Iq estimated; DAC/total supply power unknown |
| Supplies and decoupling | DESIGN PROVIDED / PENDING | Amplifier rails checked; complete DAC/reference/sequencing review still required |
| All native LTspice tests run | NOT COMPLETED | Runtime unavailable; executable test decks supplied |
| Physically buildable topology | YES, CONDITIONAL | Real R/C/op-amp topology; not a production schematic or released PCB design |
| Ready for PCB fabrication | NO | Close the release hold points below |

## PCB recommendations and release hold points

1. **Models first:** obtain the official AD3541R model from updated LTspice; inspect its actual interface before replacing the equivalent. Obtain/validate the OPA2684 manufacturer model where possible. Run all supplied native tests, inspect error logs and compare plots, including deliberate overdrive. Do not certify substitute-model THD.
2. **DAC implementation:** verify actual package pinout, AVDD/DVDD/VLOGIC and amplifier-rail requirements, power sequence, reference bypassing, reset and chosen span. The nine-terminal simulation symbol is not a PCB pinout. Budget the real DAC power from the exact operating mode, not a made-up current source.
3. **Package choice:** use the explicitly mapped SOIC-8 OPA2835D/OPA2684D packages for the stated pin map, or remap a different package from its data sheet. U1/U2/U3 each have both channels accounted for. Do not parallel spare outputs or leave amplifier inputs floating.
4. **Filter parts:** populate 220 pF C0G/NP0 and accurate resistors. Provide alternate feedback-resistor footprints to tune the high-Q section after native/model/measurement comparison. Assess tolerance, temperature, noise gain and supply corners before freezing values. No nominal IC replacement was required by the amplitude/current calculations, but substitutes in the simulation must be replaced/validated, and final filter tuning may change resistors.
5. **Grounding:** prefer a continuous low-impedance ground plane with functional analog/digital placement and controlled return paths. The ideal AGND/DGND net tie in SPICE is not a recommendation to split the plane under fast signals. Do not route SPI/clock return currents through filter or DAC reference returns.
6. **Bypass placement:** place one 100 nF capacitor at each supply pin/rail with short ground vias and nearby bulk capacitance. Implement the manufacturer's reference and amplifier bypass recommendations, not just the simplified rail list. Add real regulator impedance and capacitor ESL in a power-integrity test.
7. **Filter layout:** keep the 220 pF nodes and positive-feedback loops short. Avoid ground-plane/trace capacitance that materially alters those values. Keep stage two away from the digital clock, connector and driver output. Avoid loading high-impedance filter nodes with a 50-ohm scope input.
8. **Driver layout:** place the 806-ohm feedback parts immediately at the current-feedback amplifier pins. Do not add a feedback capacitor casually; CFB stability is sensitive to it. Keep output/current loops short, add footprints for output isolation/snubbing, and verify with the intended capacitive/cable load.
9. **Connector/termination:** use a ground-referenced BNC/SMA demonstration output. Use either the physical 50-ohm resistor with a high-impedance probe, **or** the oscilloscope's 50-ohm termination, not both in parallel. The 10-ohm series resistor is isolation, not a matched source. A long 50-ohm coax may require 49.9-ohm back termination and a gain/headroom redesign: preserving 3 Vpp at the load would require about 6 Vpp at the amplifier, not 3.6 Vpp.
10. **Instrumentation:** provide buffered/high-impedance test points for VIN_DAC, V_I_V, V_FILTER and V_AMP. Verify oscilloscope bandwidth/sample rate/noise floor before comparing -90 dBc numerical images. Keep the real DAC output within the range of the AC-coupling capacitor and receiver during power-up/down.
11. **Power and temperature:** measure DAC and amplifier rail currents separately with the actual burst duty cycle; account for regulator efficiency and converter ripple. Confirm output swing/current at worst-case temperature and power. A downstream piezoelectric load requires a new impedance/resonance, protection and power-stage design.

## Manufacturer sources

- AD3541R product description and official LTspice-model listing: https://www.analog.com/en/products/ad3541r.html
- AD3542R evaluation hardware also applicable to AD3541R: https://www.analog.com/en/resources/evaluation-hardware-and-software/evaluation-boards-kits/eval-ad3542r.html
- OPA2835 / OPAx835 data sheet SLOS713J: https://www.ti.com/lit/ds/symlink/opa2835.pdf
- TI OPA2835 model archive (contains OPA835 core): https://www.ti.com/lit/zip/slom221
- OPA2684 data sheet SBOS239D: https://www.ti.com/lit/ds/symlink/opa2684.pdf
- OPA2684 product resources: https://www.ti.com/product/OPA2684

Manufacturer limits/typicals, engineering assumptions and numerical results have deliberately been kept separate. Preserve the TI model's copyright and disclaimer when using the project.

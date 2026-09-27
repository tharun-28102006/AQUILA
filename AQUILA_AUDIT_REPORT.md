# AQUILA Repository Audit

Audit performed before the integration changes on 2026-09-27.

| Occurrence | File or area | Purpose | Decision |
|---|---|---|---|
| `50_000` / `230_000` / `235_000` | `python_model/transducer_aware_*.py` | Historical transducer-aware studies and validation artifacts | Keep as legacy reference; not used by the final prototype path |
| `165_000` / `235_000` | `rtl/geometric_frequency_lut.sv`, legacy waveform benches | Historical geometric sweep LUT and tests | Keep as legacy tests; not used by the final adaptive system validation |
| `2_000_000` | Legacy 2 MSPS capture benches and generated captures | Historical regression data | Keep for comparison; final integration bench uses 5 MSPS |
| `5_000_000` | Active waveform engines, system top, sample generator | Final digital waveform target | Keep |
| `100_000` / `500_000` | `adaptive_lut.py`, `safety_validator.sv`, final tests | Prototype electrical sweep boundaries | Keep as final safety limits |
| `SAMPLE_RATE_HZ` | Waveform engines and sample generator | Timing parameter passed through the FPGA waveform path | Keep; final active path is 5 MHz |
| `OPA2354` / `THS3091` | No active occurrence in the final analog model | Obsolete analog-chain target | Removed from the active analog simulation |

## Architecture Findings

- Python classification and state encoding already produce the required demo address `0x55` for `28 C`, `450` salinity, `35` turbidity, and `2.5 m` range.
- The 81-state LUT is generated from `adaptive_lut.py` and emits both `python_model/adaptive_lut.sv` and `rtl/adaptive_lut.sv`.
- The active profile is held by `ping_profile_latch.sv` until `ping_done`.
- The final sample-enable path is a 50 MHz clock divided by 10 for 5 MSPS.
- The single-lane AD3541R SPI path sends 24 bits at 10 MHz, limiting it to approximately 416.7 kSPS.
- The dual-SPI/DDR stream engine transfers 16 SCLK cycles per sample at approximately 8.333 MHz, limiting the present implementation to approximately 520.8 kSPS.
- Neither present DAC interface is sufficient for a sustained 5 MSPS physical stream; the waveform engine and behavioral DAC model can still be validated at 5 MSPS.
- The physical enclosure, sensor wiring, DAC analog output, oscilloscope measurements, and underwater propagation remain hardware-validation items.

## Validation Scope

The master simulation validates classification, LUT bounds, all three waveform modes, Hann windowing, DAC quantization, analog filtering, amplifier/load metrics, FFT, spectrogram generation, power estimates, sample timing, and ping-boundary adaptation.

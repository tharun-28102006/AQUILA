from pathlib import Path

from adaptive_lut import (
    MAX_SWEEP_END_HZ,
    MIN_SWEEP_START_HZ,
    SAFE_FALLBACK,
    build_lut,
    save_lut_csv,
    validate_lut,
)


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_FILES = (
    BASE_DIR / "adaptive_lut.sv",
    BASE_DIR.parent / "rtl" / "adaptive_lut.sv",
)
REFERENCE_FILE = BASE_DIR / "adaptive_lut_reference.csv"
MODE_ENCODING = {
    "GEOMETRIC": "2'b00",
    "LFM": "2'b01",
    "PHASE_CODED": "2'b10",
}


def write_sv(lut):
    fallback = SAFE_FALLBACK
    for output_file in OUTPUT_FILES:
        with output_file.open("w", encoding="utf-8") as file:
            file.write("module adaptive_lut (\n")
            file.write("    input logic [7:0] address,\n")
            file.write("    output logic [31:0] fc_hz,\n")
            file.write("    output logic [31:0] bandwidth_hz,\n")
            file.write("    output logic [31:0] pulse_duration_us,\n")
            file.write("    output logic [15:0] amplitude,\n")
            file.write("    output logic [1:0] mode\n")
            file.write(");\n\n")
            file.write("    always_comb begin\n")
            file.write(f"        fc_hz = 32'd{fallback['fc']};\n")
            file.write(f"        bandwidth_hz = 32'd{fallback['bandwidth']};\n")
            file.write(f"        pulse_duration_us = 32'd{fallback['pulse_duration_us']};\n")
            file.write(f"        amplitude = 16'd{fallback['amplitude']};\n")
            file.write(f"        mode = {MODE_ENCODING[fallback['mode']]};\n\n")
            file.write("        case (address)\n")
            for address, data in sorted(lut.items()):
                profile = data["profile"]
                file.write(f"            8'h{address:02X}: begin\n")
                file.write(f"                fc_hz = 32'd{profile.fc};\n")
                file.write(f"                bandwidth_hz = 32'd{profile.bandwidth};\n")
                file.write(f"                pulse_duration_us = 32'd{profile.pulse_duration_us};\n")
                file.write(f"                amplitude = 16'd{profile.amplitude};\n")
                file.write(f"                mode = {MODE_ENCODING[profile.mode]};\n")
                file.write("            end\n")
            file.write("            default: begin end\n")
            file.write("        endcase\n")
            file.write("    end\n")
            file.write("endmodule\n")


def main():
    lut = build_lut()
    validate_lut(lut)
    save_lut_csv(lut, REFERENCE_FILE)
    write_sv(lut)
    print(f"Generated {len(lut)}/81 valid profiles")
    print(f"Sweep bounds: {MIN_SWEEP_START_HZ} Hz to {MAX_SWEEP_END_HZ} Hz")
    print(f"Reference: {REFERENCE_FILE}")
    for output_file in OUTPUT_FILES:
        print(f"SystemVerilog: {output_file}")


if __name__ == "__main__":
    main()

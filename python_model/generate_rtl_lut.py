import csv

INPUT_FILE = "adaptive_lut_reference.csv"
OUTPUT_FILE = "../rtl/adaptive_lut.sv"

MODE_MAP = {
    "LFM": "MODE_LFM",
    "GEOMETRIC": "MODE_GEOMETRIC",
    "PHASE_CODED": "MODE_PHASE",
}

entries = []

with open(INPUT_FILE, newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        address = int(row["address"], 16)

        fc = round(float(row["fc"]))
        bandwidth = round(float(row["bandwidth"]))

        pulse_duration = round(float(row["pulse_duration"]) * 1_000_000)

        amplitude = round(float(row["amplitude"]) * 1000)

        mode = MODE_MAP[row["mode"]]

        entries.append(
            (address, fc, bandwidth, pulse_duration, amplitude, mode)
        )

entries.sort()

with open(OUTPUT_FILE, "w") as file:

    file.write("""module adaptive_lut (
    input  logic [7:0]  lut_address,
    output logic [31:0] fc,
    output logic [31:0] bandwidth,
    output logic [31:0] pulse_duration,
    output logic [15:0] amplitude,
    output logic [1:0]  mode
);

    localparam logic [1:0] MODE_LFM       = 2'b00;
    localparam logic [1:0] MODE_GEOMETRIC = 2'b01;
    localparam logic [1:0] MODE_PHASE     = 2'b10;

    always_comb begin

        fc              = 32'd0;
        bandwidth       = 32'd0;
        pulse_duration  = 32'd0;
        amplitude       = 16'd0;
        mode            = MODE_LFM;

        case (lut_address)
""")

    for address, fc, bw, tp, amp, mode in entries:

        file.write(
            f"            8'h{address:02X}: begin "
            f"fc=32'd{fc}; "
            f"bandwidth=32'd{bw}; "
            f"pulse_duration=32'd{tp}; "
            f"amplitude=16'd{amp}; "
            f"mode={mode}; "
            f"end\n"
        )

    file.write("""
            default: begin
                fc              = 32'd0;
                bandwidth       = 32'd0;
                pulse_duration  = 32'd0;
                amplitude       = 16'd0;
                mode            = MODE_LFM;
            end

        endcase
    end

endmodule
""")

print("==========================================")
print(" AQUILA RTL LUT GENERATOR")
print("==========================================")
print(f"Input : {INPUT_FILE}")
print(f"Output: {OUTPUT_FILE}")
print(f"Entries generated: {len(entries)}")

if len(entries) == 81:
    print("STATUS: 81/81 LUT STATES GENERATED")
else:
    print("ERROR: Expected 81 states!")
import csv

INPUT_FILE = "adaptive_lut_reference.csv"
OUTPUT_FILE = "../rtl/tb_lut_outputs.sv"

MODE_MAP = {
    "LFM": "2'b00",
    "GEOMETRIC": "2'b01",
    "PHASE_CODED": "2'b10"
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

    file.write("""
`timescale 1ns/1ps

module tb_lut_outputs;

    reg  [7:0]  lut_address;

    wire [31:0] fc;
    wire [31:0] bandwidth;
    wire [31:0] pulse_duration;
    wire [15:0] amplitude;
    wire [1:0]  mode;

    integer pass_count;
    integer fail_count;
    integer i;

    adaptive_lut dut (
        .lut_address(lut_address),
        .fc(fc),
        .bandwidth(bandwidth),
        .pulse_duration(pulse_duration),
        .amplitude(amplitude),
        .mode(mode)
    );

    task check_state;

        input [7:0]  expected_address;
        input [31:0] expected_fc;
        input [31:0] expected_bandwidth;
        input [31:0] expected_pulse_duration;
        input [15:0] expected_amplitude;
        input [1:0]  expected_mode;

        begin

            lut_address = expected_address;

            #1;

            if (
                fc == expected_fc &&
                bandwidth == expected_bandwidth &&
                pulse_duration == expected_pulse_duration &&
                amplitude == expected_amplitude &&
                mode == expected_mode
            ) begin

                $display(
                    "PASS Address=%02X | Fc=%0d | BW=%0d | Tp=%0d us | A=%0d | Mode=%02b",
                    expected_address,
                    fc,
                    bandwidth,
                    pulse_duration,
                    amplitude,
                    mode
                );

                pass_count = pass_count + 1;

            end
            else begin

                $display(
                    "FAIL Address=%02X",
                    expected_address
                );

                $display(
                    "     Expected: Fc=%0d BW=%0d Tp=%0d A=%0d Mode=%02b",
                    expected_fc,
                    expected_bandwidth,
                    expected_pulse_duration,
                    expected_amplitude,
                    expected_mode
                );

                $display(
                    "     Actual  : Fc=%0d BW=%0d Tp=%0d A=%0d Mode=%02b",
                    fc,
                    bandwidth,
                    pulse_duration,
                    amplitude,
                    mode
                );

                fail_count = fail_count + 1;

            end

        end

    endtask


    initial begin

        pass_count = 0;
        fail_count = 0;
        lut_address = 8'h00;

        $display("");
        $display("==============================================");
        $display("       AQUILA LUT OUTPUT VERIFICATION");
        $display("==============================================");
        $display("");

""")

    for address, fc, bw, tp, amp, mode in entries:

        file.write(
            f"        check_state("
            f"8'h{address:02X}, "
            f"32'd{fc}, "
            f"32'd{bw}, "
            f"32'd{tp}, "
            f"16'd{amp}, "
            f"{mode}"
            f");\n"
        )

    file.write("""
        $display("");
        $display("----------------------------------------------");
        $display("TOTAL TESTS : %0d", pass_count + fail_count);
        $display("PASS        : %0d", pass_count);
        $display("FAIL        : %0d", fail_count);
        $display("----------------------------------------------");

        if (fail_count == 0)
            $display("AQUILA ADAPTIVE LUT VERIFIED");
        else
            $display("AQUILA ADAPTIVE LUT VERIFICATION FAILED");

        $display("==============================================");
        $display("");

        $finish;

    end

endmodule
""")

print("==========================================")
print(" AQUILA TESTBENCH GENERATOR")
print("==========================================")
print(f"Input : {INPUT_FILE}")
print(f"Output: {OUTPUT_FILE}")
print(f"Tests generated: {len(entries)}")

if len(entries) == 81:
    print("STATUS: 81/81 TESTS GENERATED")
else:
    print("ERROR: Expected 81 tests!")
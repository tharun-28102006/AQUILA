import math

OUTPUT_FILE = "../rtl/hann_lut.sv"

TABLE_SIZE = 256
Q15_MAX = 32767

with open(OUTPUT_FILE, "w") as file:

    file.write("""module hann_lut (
    input  logic [7:0] address,
    output logic [15:0] coefficient
);

    always_comb begin

        case (address)
""")

    for i in range(TABLE_SIZE):

        window = 0.5 * (
            1.0 -
            math.cos(
                2.0 * math.pi * i / (TABLE_SIZE - 1)
            )
        )

        coefficient = round(window * Q15_MAX)

        file.write(
            f"            8'd{i}: coefficient = 16'd{coefficient};\n"
        )

    file.write("""
            default:
                coefficient = 16'd0;

        endcase

    end

endmodule
""")

print("==========================================")
print("       AQUILA HANN LUT GENERATOR")
print("==========================================")
print(f"Entries generated : {TABLE_SIZE}")
print(f"Format             : Q15")
print(f"Output             : {OUTPUT_FILE}")
print("STATUS             : COMPLETE")
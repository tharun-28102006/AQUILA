import math

OUTPUT_FILE = "../rtl/sine_lut.sv"

TABLE_SIZE = 256
DAC_BITS = 12
MID = 2 ** (DAC_BITS - 1)
MAX = MID - 1


with open(OUTPUT_FILE, "w") as file:

    file.write("""module sine_lut (
    input  logic [7:0] address,
    output logic [11:0] sine_value
);

    always_comb begin

        case (address)
""")

    for i in range(TABLE_SIZE):

        angle = 2.0 * math.pi * i / TABLE_SIZE

        value = round(
            MID + MAX * math.sin(angle)
        )

        value = max(0, min(4095, value))

        file.write(
            f"            8'd{i}: sine_value = 12'd{value};\n"
        )

    file.write("""
            default:
                sine_value = 12'd2048;

        endcase

    end

endmodule
""")

print("==========================================")
print("       AQUILA SINE LUT GENERATOR")
print("==========================================")
print(f"Entries generated : {TABLE_SIZE}")
print(f"Resolution         : {DAC_BITS}-bit")
print(f"Output             : {OUTPUT_FILE}")
print("STATUS             : COMPLETE")
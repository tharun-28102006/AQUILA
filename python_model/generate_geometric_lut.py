import math

TABLE_SIZE = 256

F_START = 165000
F_END = 235000

OUTPUT_FILE = "../rtl/geometric_frequency_lut.sv"


with open(OUTPUT_FILE, "w") as file:

    file.write("""module geometric_frequency_lut (

    input  logic [7:0] address,

    output logic [31:0] frequency

);

    always_comb begin

        case(address)

""")


    for i in range(TABLE_SIZE):

        ratio = i / (TABLE_SIZE - 1)

        frequency = (
            F_START *
            ((F_END / F_START) ** ratio)
        )

        frequency = round(frequency)

        file.write(
            f"            8'd{i}: frequency = 32'd{frequency};\n"
        )


    file.write("""
            default:
                frequency = 32'd0;

        endcase

    end

endmodule
""")


print("==============================================")
print("   AQUILA GEOMETRIC FREQUENCY LUT")
print("==============================================")
print(f"Entries : {TABLE_SIZE}")
print(f"Start   : {F_START} Hz")
print(f"End     : {F_END} Hz")
print("STATUS  : COMPLETE")
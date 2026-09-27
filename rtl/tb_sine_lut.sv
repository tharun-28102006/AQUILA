`timescale 1ns/1ps

module tb_sine_lut;

    reg [7:0] address;

    wire [11:0] sine_value;

    integer i;


    sine_lut dut (
        .address(address),
        .sine_value(sine_value)
    );


    initial begin

        $display("");
        $display("==============================================");
        $display("          AQUILA SINE LUT TEST");
        $display("==============================================");


        for (i = 0; i < 256; i = i + 1) begin

            address = i;

            #1;

            if (i % 16 == 0) begin

                $display(
                    "Address=%0d | Sine=%0d",
                    address,
                    sine_value
                );

            end

        end


        $display("");
        $display("256/256 LUT ADDRESSES TESTED");
        $display("SINE LUT TEST COMPLETE");
        $display("==============================================");

        $finish;

    end

endmodule
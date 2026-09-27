`timescale 1ns/1ps

module tb_window_multiplier;

    reg [11:0] sample_in;
    reg [15:0] window_coefficient;

    wire [11:0] sample_out;


    window_multiplier dut (

        .sample_in(sample_in),

        .window_coefficient(window_coefficient),

        .sample_out(sample_out)

    );


    initial begin

        $display("");
        $display("==============================================");
        $display("       AQUILA WINDOW MULTIPLIER TEST");
        $display("==============================================");


        sample_in = 12'd3000;
        window_coefficient = 16'd0;

        #1;

        $display(
            "Window=0.0 | Input=%0d | Output=%0d",
            sample_in,
            sample_out
        );


        sample_in = 12'd3000;
        window_coefficient = 16'd16384;

        #1;

        $display(
            "Window=0.5 | Input=%0d | Output=%0d",
            sample_in,
            sample_out
        );


        sample_in = 12'd3000;
        window_coefficient = 16'd32767;

        #1;

        $display(
            "Window=1.0 | Input=%0d | Output=%0d",
            sample_in,
            sample_out
        );


        $display("");
        $display("WINDOW MULTIPLIER TEST COMPLETE");
        $display("==============================================");

        $finish;

    end

endmodule
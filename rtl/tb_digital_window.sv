
`timescale 1ns/1ps

module tb_digital_window;

    logic clk;
    logic reset;
    logic enable;

    logic [31:0] sample_count;
    logic [31:0] total_samples;

    logic [11:0] sample_in;

    logic [11:0] sample_out;



    digital_window dut (

        .clk(clk),
        .reset(reset),
        .enable(enable),

        .sample_count(sample_count),
        .total_samples(total_samples),

        .sample_in(sample_in),

        .sample_out(sample_out)

    );



    always #250 clk = ~clk;


    initial begin

        clk = 0;

        reset = 0;

        enable = 1;

        total_samples = 32'd256;


        $display("");
        $display("==============================================");
        $display("       AQUILA DIGITAL WINDOW TEST");
        $display("==============================================");



        sample_in = 12'd2048;

        sample_count = 32'd128;

        #1;

        $display(
            "Center input  = %0d | Output = %0d",
            sample_in,
            sample_out
        );



        sample_in = 12'd4095;

        sample_count = 32'd128;

        #1;

        $display(
            "Positive max  = %0d | Output = %0d",
            sample_in,
            sample_out
        );



        sample_in = 12'd0;

        sample_count = 32'd128;

        #1;

        $display(
            "Negative max  = %0d | Output = %0d",
            sample_in,
            sample_out
        );



        sample_in = 12'd4095;

        sample_count = 32'd0;

        #1;

        $display(
            "Pulse start   = %0d | Output = %0d",
            sample_in,
            sample_out
        );



        sample_in = 12'd4095;

        sample_count = 32'd255;

        #1;

        $display(
            "Pulse end     = %0d | Output = %0d",
            sample_in,
            sample_out
        );


        $display("");
        $display("==============================================");
        $display("DIGITAL WINDOW TEST COMPLETE");
        $display("==============================================");

        $finish;

    end

endmodule

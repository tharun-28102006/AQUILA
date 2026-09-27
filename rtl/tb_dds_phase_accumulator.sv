`timescale 1ns/1ps

module tb_dds_phase_accumulator;

    reg clk;
    reg reset;
    reg enable;

    reg [31:0] frequency_hz;

    wire [31:0] phase;


    dds_phase_accumulator #(
        .PHASE_BITS(32),
        .CLK_FREQ_HZ(2_000_000)
    )
    dut (
        .clk(clk),
        .reset(reset),
        .enable(enable),
        .frequency_hz(frequency_hz),
        .phase(phase)
    );


    always #250 clk = ~clk;


    initial begin

        clk = 0;
        reset = 1;
        enable = 0;

        frequency_hz = 250000;


        $display("");
        $display("==============================================");
        $display("       AQUILA DDS PHASE ACCUMULATOR");
        $display("==============================================");

        $display("");
        $display("Clock Frequency = 2 MHz");
        $display("Output Frequency = 250 kHz");
        $display("Phase Bits = 32");


        #1000;

        reset = 0;
        enable = 1;


        #10000;

        enable = 0;


        $display("");
        $display("Final Phase = %0d", phase);

        $display("");
        $display("DDS TEST COMPLETE");
        $display("==============================================");

        $finish;

    end


    always @(posedge clk) begin

        if (enable) begin

            $display(
                "TIME=%0t ns | Phase=%0d",
                $time,
                phase
            );

        end

    end

endmodule   
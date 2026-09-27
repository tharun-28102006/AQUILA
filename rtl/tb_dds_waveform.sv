`timescale 1ns/1ps

module tb_dds_waveform;

    reg clk;
    reg reset;
    reg enable;

    reg [31:0] frequency_hz;
    reg [15:0] amplitude;

    wire [11:0] dac_sample;


    dds_waveform #(
        .PHASE_BITS(32),
        .CLK_FREQ_HZ(2_000_000)
    )
    dut (
        .clk(clk),
        .reset(reset),
        .enable(enable),
        .frequency_hz(frequency_hz),
        .amplitude(amplitude),
        .dac_sample(dac_sample)
    );


    always #250 clk = ~clk;


    integer i;


    initial begin

        clk = 0;
        reset = 1;
        enable = 0;

        frequency_hz = 250000;
        amplitude = 1000;


        $display("");
        $display("==============================================");
        $display("       AQUILA DDS WAVEFORM TEST");
        $display("==============================================");

        $display("");
        $display("Clock     = 2 MHz");
        $display("Frequency = 250 kHz");
        $display("Amplitude = 100%%");


        #1000;

        reset = 0;
        enable = 1;


        for (i = 0; i < 32; i = i + 1) begin

            @(posedge clk);

            #1;

            $display(
                "Sample %0d | Phase=%0d | DAC=%0d",
                i,
                dut.phase,
                dac_sample
            );

        end


        enable = 0;


        $display("");
        $display("DDS WAVEFORM TEST COMPLETE");
        $display("==============================================");

        $finish;

    end

endmodule
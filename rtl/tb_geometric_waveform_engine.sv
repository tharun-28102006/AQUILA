`timescale 1ns/1ps

module tb_geometric_waveform_engine;

    logic clk;
    logic reset;
    logic enable;

    logic [31:0] start_frequency_hz;
    logic [31:0] end_frequency_hz;
    logic [31:0] pulse_duration_us;

    logic [15:0] amplitude;

    logic [11:0] dac_sample;
    logic ping_done;


    geometric_waveform_engine #(
        .PHASE_BITS(32),
        .CLK_FREQ_HZ(2_000_000)
    )

    dut (

        .clk(clk),
        .reset(reset),
        .enable(enable),

        .start_frequency_hz(start_frequency_hz),
        .end_frequency_hz(end_frequency_hz),

        .pulse_duration_us(pulse_duration_us),

        .amplitude(amplitude),

        .dac_sample(dac_sample),
        .ping_done(ping_done)

    );



    always #250 clk = ~clk;


    integer i;


    initial begin

        clk = 0;

        reset = 1;
        enable = 0;

        start_frequency_hz = 32'd165000;
        end_frequency_hz   = 32'd235000;

        pulse_duration_us = 32'd4000;

        amplitude = 16'd800;


        #1000;

        reset = 0;
        enable = 1;


        $display("");
        $display("==============================================");
        $display("   AQUILA GEOMETRIC WAVEFORM ENGINE TEST");
        $display("==============================================");

        $display(
            "Start Frequency = %0d Hz",
            start_frequency_hz
        );

        $display(
            "End Frequency   = %0d Hz",
            end_frequency_hz
        );

        $display(
            "Pulse Duration  = %0d us",
            pulse_duration_us
        );

        $display(
            "Amplitude       = %0d",
            amplitude
        );

        $display("");
        $display("Sample     DAC");
        $display("----------------------------------------------");


        for (i = 0; i < 20; i = i + 1) begin

            @(posedge clk);
            #1;

            $display(
                "%0d         %0d",
                i,
                dac_sample
            );

        end


        wait(ping_done == 1'b1);


        $display("");
        $display("GEOMETRIC PING COMPLETE");
        $display("ping_done = %b", ping_done);

        $display("");
        $display("==============================================");
        $display("GEOMETRIC ENGINE TEST COMPLETE");
        $display("==============================================");

        $finish;

    end

endmodule
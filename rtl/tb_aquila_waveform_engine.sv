`timescale 1ns/1ps

module tb_aquila_waveform_engine;

    logic clk;
    logic reset;
    logic enable;

    logic [31:0] fc_hz;
    logic [31:0] bandwidth_hz;
    logic [31:0] pulse_duration_us;

    logic [15:0] amplitude;

    logic [11:0] dac_sample;
    logic ping_done;



    aquila_waveform_engine #(
        .PHASE_BITS(32),
        .CLK_FREQ_HZ(2_000_000)
    )

    dut (

        .clk(clk),
        .reset(reset),
        .enable(enable),

        .fc_hz(fc_hz),
        .bandwidth_hz(bandwidth_hz),
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

        fc_hz = 32'd200000;

        bandwidth_hz = 32'd70000;

        pulse_duration_us = 32'd4000;

        amplitude = 16'd800;


        #1000;

        reset = 0;

        enable = 1;


        $display("");
        $display("==============================================");
        $display("     AQUILA WAVEFORM ENGINE TEST");
        $display("==============================================");

        $display("Fc        = %0d Hz", fc_hz);
        $display("BW        = %0d Hz", bandwidth_hz);
        $display("Tp        = %0d us", pulse_duration_us);
        $display("Amplitude = %0d", amplitude);

        $display("");
        $display("Sample       DAC");
        $display("----------------------------------------------");


        for (i = 0; i < 20; i = i + 1) begin

            @(posedge clk);

            #1;

            $display(
                "%0d           %0d",
                i,
                dac_sample
            );

        end



        wait(ping_done == 1'b1);

        $display("");
        $display("PING COMPLETE");
        $display("ping_done = %b", ping_done);

        $display("");
        $display("==============================================");
        $display("AQUILA WAVEFORM ENGINE TEST COMPLETE");
        $display("==============================================");


        $finish;

    end

endmodule

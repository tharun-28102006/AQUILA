`timescale 1ns/1ps

module tb_aquila_waveform_top;

    logic clk;
    logic reset;
    logic enable;

    logic [31:0] fc_hz;
    logic [31:0] bandwidth_hz;
    logic [31:0] pulse_duration_us;

    logic [15:0] amplitude;

    logic [1:0] mode;

    logic [11:0] dac_sample;
    logic ping_done;



    aquila_waveform_top #(
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

        .mode(mode),

        .dac_sample(dac_sample),

        .ping_done(ping_done)

    );



    always #250 clk = ~clk;



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
        $display("       AQUILA FULL MODE TEST");
        $display("==============================================");



        mode = 2'b00;

        $display("");
        $display("MODE = LFM");

        repeat (10) begin

            @(posedge clk);
            #1;

            $display(
                "DAC = %0d",
                dac_sample
            );

        end



        mode = 2'b01;

        $display("");
        $display("MODE = GEOMETRIC");

        repeat (10) begin

            @(posedge clk);
            #1;

            $display(
                "DAC = %0d",
                dac_sample
            );

        end



        mode = 2'b10;

        $display("");
        $display("MODE = PHASE CODED");

        repeat (10) begin

            @(posedge clk);
            #1;

            $display(
                "DAC = %0d",
                dac_sample
            );

        end


        $display("");
        $display("==============================================");
        $display("FULL MODE TEST COMPLETE");
        $display("==============================================");


        $finish;

    end

endmodule

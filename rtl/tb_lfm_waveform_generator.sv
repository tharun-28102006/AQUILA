`timescale 1ns/1ps

module tb_lfm_waveform_generator;

    reg clk;
    reg reset;
    reg enable;

    reg [31:0] fc_hz;
    reg [31:0] bandwidth_hz;
    reg [31:0] pulse_duration_us;

    reg [15:0] amplitude;

    wire [11:0] dac_sample;

    wire ping_done;


    lfm_waveform_generator #(
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



        fc_hz = 200000;

        bandwidth_hz = 70000;

        pulse_duration_us = 4000;

        amplitude = 800;


        $display("");
        $display("==============================================");
        $display("       AQUILA LFM WAVEFORM GENERATOR");
        $display("==============================================");

        $display("");
        $display("Fc        = %0d Hz", fc_hz);
        $display("BW        = %0d Hz", bandwidth_hz);
        $display("Tp        = %0d us", pulse_duration_us);
        $display("Amplitude = %0d", amplitude);


        #1000;

        reset = 0;

        enable = 1;



        for (i = 0; i < 100; i = i + 1) begin

            @(posedge clk);

            #1;

            $display(
                "Sample=%0d | Frequency=%0d Hz | Phase=%0d | DAC=%0d",
                dut.sample_count,
                dut.current_frequency,
                dut.phase,
                dac_sample
            );

        end


        enable = 0;


        $display("");
        $display("LFM WAVEFORM GENERATOR TEST COMPLETE");
        $display("==============================================");

        $finish;

    end

endmodule
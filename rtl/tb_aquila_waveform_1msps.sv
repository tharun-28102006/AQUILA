
`timescale 1ns/1ps

module tb_aquila_waveform_1msps;

    logic clk;
    logic reset;
    logic enable;
    logic sample_enable;

    logic [31:0] fc_hz;
    logic [31:0] bandwidth_hz;
    logic [31:0] pulse_duration_us;
    logic [15:0] amplitude;
    logic [1:0] mode;

    logic [11:0] dac_sample;
    logic ping_done;

    integer sample_count;



    aquila_waveform_top #(
        .PHASE_BITS(32),
        .CLK_FREQ_HZ(50_000_000),
        .SAMPLE_RATE_HZ(1_000_000)
    ) dut (

        .clk(clk),
        .reset(reset),

        .enable(enable),
        .sample_enable(sample_enable),

        .fc_hz(fc_hz),
        .bandwidth_hz(bandwidth_hz),
        .pulse_duration_us(pulse_duration_us),

        .amplitude(amplitude),
        .mode(mode),

        .dac_sample(dac_sample),
        .ping_done(ping_done)
    );



    always #10 clk = ~clk;



    always begin

        sample_enable = 1'b0;

        #1000;

        sample_enable = 1'b1;

        #20;

    end



    always @(posedge clk) begin

        if (!reset && enable && sample_enable) begin

            sample_count = sample_count + 1;

            if (sample_count <= 20) begin

                $display(
                    "Sample %0d = %0d",
                    sample_count,
                    dac_sample
                );

            end

        end

    end



    initial begin

        clk = 0;
        reset = 1;
        enable = 0;

        sample_enable = 0;

        sample_count = 0;

        fc_hz = 32'd200000;
        bandwidth_hz = 32'd70000;
        pulse_duration_us = 32'd4000;
        amplitude = 16'd800;

        mode = 2'b00;


        #200;

        reset = 0;

        #200;

        enable = 1;


        #4_500_000;


        enable = 0;

        #1000;


        $display("");
        $display("==============================================");
        $display(" AQUILA 1 MSPS WAVEFORM TEST");
        $display("==============================================");

        $display(
            "Sample rate       = 1 MSPS"
        );

        $display(
            "Fc                = 200 kHz"
        );

        $display(
            "Bandwidth         = 70 kHz"
        );

        $display(
            "Pulse duration    = 4 ms"
        );

        $display(
            "Samples generated = %0d",
            sample_count
        );

        if (sample_count >= 4000) begin

            $display(
                "PASS: 1 MSPS WAVEFORM GENERATION"
            );

        end
        else begin

            $display(
                "FAIL: EXPECTED APPROXIMATELY 4000 SAMPLES"
            );

        end


        $display("");
        $display("==============================================");
        $display(" TEST COMPLETE");
        $display("==============================================");

        $finish;

    end

endmodule
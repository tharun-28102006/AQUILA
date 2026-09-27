`timescale 1ns/1ps

module tb_aquila_lfm_2msps_capture;

    localparam integer CLK_FREQ_HZ    = 50_000_000;
    localparam integer SAMPLE_RATE_HZ = 2_000_000;
    localparam integer PULSE_US       = 4000;
    localparam integer EXPECTED_SAMPLES = 8000;

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
    integer csv_file;

    integer divider_count;

    aquila_waveform_top #(
        .PHASE_BITS(32),
        .CLK_FREQ_HZ(CLK_FREQ_HZ),
        .SAMPLE_RATE_HZ(SAMPLE_RATE_HZ)
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

    initial begin
        clk = 1'b0;

        forever #10 clk = ~clk;
    end

    always_ff @(posedge clk) begin

        if (reset) begin
            divider_count <= 0;
            sample_enable <= 1'b0;
        end
        else begin

            sample_enable <= 1'b0;

            if (divider_count == 24) begin
                divider_count <= 0;
                sample_enable <= 1'b1;
            end
            else begin
                divider_count <= divider_count + 1;
            end

        end
    end

    always @(posedge clk) begin

        if (!reset && enable && sample_enable) begin

            if (sample_count < EXPECTED_SAMPLES) begin

                $fwrite(
                    csv_file,
                    "%0d,%0d\n",
                    sample_count,
                    dac_sample
                );

                sample_count = sample_count + 1;

            end

        end

    end

    initial begin

        $display("");
        $display("==============================================");
        $display(" AQUILA 2 MSPS LFM WAVEFORM CAPTURE");
        $display("==============================================");

        fc_hz             = 32'd200000;
        bandwidth_hz      = 32'd70000;
        pulse_duration_us = 32'd4000;
        amplitude         = 16'd800;

        mode = 2'b00;

        enable = 1'b0;
        reset  = 1'b1;

        sample_count  = 0;
        divider_count = 0;

        csv_file = $fopen(
            "aquila_lfm_2msps_samples.csv",
            "w"
        );

        $fwrite(
            csv_file,
            "sample_index,dac_sample\n"
        );

        #200;

        reset = 1'b0;

        $display("RESET RELEASED");

        enable = 1'b1;

        $display("STREAM ENABLED");
        $display("");
        $display("Sample rate       = 2.000 MSPS");
        $display("Center frequency  = 200 kHz");
        $display("Bandwidth         = 70 kHz");
        $display("Pulse duration    = 4 ms");
        $display("Expected samples  = 8000");
        $display("");

        wait(sample_count == EXPECTED_SAMPLES);

        enable = 1'b0;

        $fclose(csv_file);

        $display("");
        $display("==============================================");
        $display(" CAPTURE COMPLETE");
        $display("==============================================");

        $display("Expected samples  = %0d", EXPECTED_SAMPLES);
        $display("Captured samples  = %0d", sample_count);

        if (sample_count == EXPECTED_SAMPLES)
            $display("PASS: 8000 SAMPLES CAPTURED");
        else
            $display("FAIL: SAMPLE COUNT MISMATCH");

        $display("");
        $display("CSV FILE: aquila_lfm_2msps_samples.csv");
        $display("");

        $finish;

    end

endmodule
`timescale 1ns/1ps

module aquila_waveform_top_tb;


    logic clk;
    logic reset;
    logic enable;
    logic sample_enable;


    logic [31:0] fc_hz;
    logic [31:0] bandwidth_hz;
    logic [31:0] pulse_duration_us;
    logic [15:0] amplitude;
    logic [1:0]  mode;


    logic [11:0] dac_sample;
    logic ping_done;


    aquila_waveform_top #(
        .PHASE_BITS(32),
        .CLK_FREQ_HZ(50_000_000),
        .SAMPLE_RATE_HZ(2_000_000)
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


    integer clk_count;

    always @(posedge clk) begin

        if (reset) begin
            clk_count    <= 0;
            sample_enable <= 1'b0;
        end
        else begin

            if (clk_count == 24) begin
                clk_count    <= 0;
                sample_enable <= 1'b1;
            end
            else begin
                clk_count    <= clk_count + 1;
                sample_enable <= 1'b0;
            end

        end

    end


    integer sample_count;
    integer nonzero_count;
    integer mode_test;


    always @(posedge clk) begin

        if (sample_enable && enable) begin

            sample_count = sample_count + 1;

            if (dac_sample != 12'd0)
                nonzero_count = nonzero_count + 1;

        end

    end


    task run_mode_test;

        input [1:0] test_mode;
        input [31:0] test_fc;
        input [31:0] test_bw;
        input [31:0] test_duration;
        input [15:0] test_amplitude;
        input [127:0] mode_name;

        integer timeout;
        integer start_samples;

        begin

            mode = test_mode;
            fc_hz = test_fc;
            bandwidth_hz = test_bw;
            pulse_duration_us = test_duration;
            amplitude = test_amplitude;

            sample_count = 0;
            nonzero_count = 0;

            enable = 1'b1;

            start_samples = 0;

            $display("");
            $display("================================================");
            $display("TESTING MODE: %s", mode_name);
            $display("Mode       = %02b", test_mode);
            $display("Fc         = %0d Hz", test_fc);
            $display("Bandwidth  = %0d Hz", test_bw);
            $display("Pulse      = %0d us", test_duration);
            $display("Amplitude  = %0d", test_amplitude);
            $display("================================================");

            timeout = 0;

            while (!ping_done && timeout < 600000) begin

                @(posedge clk);

                timeout = timeout + 1;

            end

            enable = 1'b0;

            if (ping_done) begin

                $display("PASS: ping_done detected");
                $display("Samples generated = %0d", sample_count);
                $display("Non-zero samples  = %0d", nonzero_count);

                if (nonzero_count > 0)
                    $display("PASS: DAC waveform samples detected");
                else
                    $display("FAIL: DAC samples remained zero");

            end
            else begin

                $display("FAIL: ping_done timeout");
                $display("Samples generated = %0d", sample_count);
            end

            #1000;

        end

    endtask


    initial begin

        reset = 1'b1;
        enable = 1'b0;

        sample_enable = 1'b0;

        fc_hz = 32'd200000;
        bandwidth_hz = 32'd25000;
        pulse_duration_us = 32'd2000;
        amplitude = 16'd600;
        mode = 2'b00;

        sample_count = 0;
        nonzero_count = 0;

        #200;

        reset = 1'b0;

        #200;


        run_mode_test(
            2'b00,
            32'd200000,
            32'd25000,
            32'd2000,
            16'd600,
            "GEOMETRIC"
        );


        run_mode_test(
            2'b01,
            32'd200000,
            32'd25000,
            32'd2000,
            16'd600,
            "LFM"
        );


        run_mode_test(
            2'b10,
            32'd200000,
            32'd25000,
            32'd2000,
            16'd600,
            "PHASE_CODED"
        );


        mode = 2'b11;
        enable = 1'b1;

        #1000;

        enable = 1'b0;

        if (!ping_done)
            $display("PASS: Invalid mode 11 produces no ping_done");
        else
            $display("FAIL: Invalid mode generated ping_done");


        $display("");
        $display("================================================");
        $display("AQUILA WAVEFORM TOP VERIFICATION COMPLETE");
        $display("================================================");

        $finish;

    end

endmodule
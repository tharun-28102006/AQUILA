`timescale 1ns/1ps

module aquila_waveform_capture_tb;

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
    integer file;
    integer timeout;
    integer clk_count;


    // ============================================================
    // 50 MHz FPGA clock
    // 20 ns period
    // ============================================================

    initial begin
        clk = 1'b0;
        forever #10 clk = ~clk;
    end


    // ============================================================
    // Aquila waveform engine
    // NEW TARGET: 5 MSPS
    // ============================================================

    aquila_waveform_top #(
        .PHASE_BITS(32),
        .CLK_FREQ_HZ(50_000_000),
        .SAMPLE_RATE_HZ(5_000_000)
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


    // ============================================================
    // 5 MSPS SAMPLE ENABLE
    //
    // 50 MHz / 10 = 5 MHz
    //
    // One sample every 10 FPGA clock cycles.
    // ============================================================

    always @(posedge clk) begin

        if (reset) begin

            clk_count     <= 0;
            sample_enable <= 1'b0;

        end

        else begin

            if (clk_count == 9) begin

                clk_count     <= 0;
                sample_enable <= 1'b1;

            end

            else begin

                clk_count     <= clk_count + 1;
                sample_enable <= 1'b0;

            end

        end

    end


    // ============================================================
    // WAVEFORM CAPTURE TASK
    // ============================================================

    task capture_waveform;

        input [1:0] test_mode;
        input string filename;
        input string waveform_name;

        begin

            mode = test_mode;

            // ----------------------------------------------------
            // Aquila system test profile
            //
            // Fc = 300 kHz
            // BW = 200 kHz
            //
            // Start = 200 kHz
            // End   = 400 kHz
            //
            // Pulse = 2 ms
            // ----------------------------------------------------

            fc_hz = 32'd300000;
            bandwidth_hz = 32'd200000;
            pulse_duration_us = 32'd2000;
            amplitude = 16'd600;

            sample_count = 0;
            timeout = 0;

            file = $fopen(filename, "w");

            $fwrite(
                file,
                "sample_index,time_us,dac_sample\n"
            );

            enable = 1'b1;

            $display("");
            $display("==============================================");
            $display("CAPTURING %s", waveform_name);
            $display("Mode          = %02b", test_mode);
            $display("Fc            = %0d Hz", fc_hz);
            $display("Bandwidth     = %0d Hz", bandwidth_hz);
            $display("Start         = %0d Hz",
                     fc_hz - bandwidth_hz/2);
            $display("End           = %0d Hz",
                     fc_hz + bandwidth_hz/2);
            $display("Pulse         = %0d us", pulse_duration_us);
            $display("Sample rate   = 5 MSPS");
            $display("Output        = %s", filename);
            $display("==============================================");

            // ----------------------------------------------------
            // Capture until ping is complete
            // ----------------------------------------------------

            while (!ping_done && timeout < 600000) begin

                @(posedge clk);

                if (sample_enable && enable) begin

                    $fwrite(
                        file,
                        "%0d,%0.6f,%0d\n",
                        sample_count,
                        (sample_count * 0.2),
                        dac_sample
                    );

                    sample_count = sample_count + 1;

                end

                timeout = timeout + 1;

            end

            enable = 1'b0;

            $fclose(file);


            // ----------------------------------------------------
            // Validation
            // ----------------------------------------------------

            if (ping_done) begin

                $display(
                    "PASS: %0d samples captured",
                    sample_count
                );

                // 2 ms × 5 MSPS = 10,000 samples
                if (sample_count != 10000) begin

                    $display(
                        "WARNING: Expected 10000 samples, got %0d",
                        sample_count
                    );

                end

            end

            else begin

                $display("FAIL: capture timeout");

            end

            #1000;

        end

    endtask


    // ============================================================
    // MAIN TEST
    // ============================================================

    initial begin

        reset = 1'b1;
        enable = 1'b0;

        sample_enable = 1'b0;

        fc_hz = 32'd300000;
        bandwidth_hz = 32'd200000;
        pulse_duration_us = 32'd2000;
        amplitude = 16'd600;
        mode = 2'b00;


        // Reset
        #200;

        reset = 1'b0;

        #200;


        // --------------------------------------------------------
        // 1. GEOMETRIC
        // --------------------------------------------------------

        capture_waveform(
            2'b00,
            "geometric_capture_5msps.csv",
            "GEOMETRIC"
        );


        // --------------------------------------------------------
        // 2. LFM
        // --------------------------------------------------------

        capture_waveform(
            2'b01,
            "lfm_capture_5msps.csv",
            "LFM"
        );


        // --------------------------------------------------------
        // 3. PHASE CODED
        // --------------------------------------------------------

        capture_waveform(
            2'b10,
            "phase_capture_5msps.csv",
            "PHASE_CODED"
        );


        $display("");
        $display("==============================================");
        $display("ALL 5-MSPS WAVEFORM CAPTURES COMPLETE");
        $display("==============================================");

        $finish;

    end

endmodule
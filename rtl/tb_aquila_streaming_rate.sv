
`timescale 1ns/1ps

module tb_aquila_streaming_rate;

    logic clk;
    logic reset;
    logic enable;

    logic [31:0] fc_hz;
    logic [31:0] bandwidth_hz;
    logic [31:0] pulse_duration_us;
    logic [15:0] amplitude;
    logic [1:0]  mode;

    logic dac_cs_n;
    logic dac_sclk;
    logic dac_sdi;

    logic dac_busy;
    logic sample_done;
    logic ping_done;

    logic [11:0] waveform_sample;
    logic sample_enable;

    integer sample_count;
    integer accepted_count;
    integer completed_count;
    integer dropped_count;



    aquila_waveform_dac_system dut (

        .clk(clk),
        .reset(reset),
        .enable(enable),

        .fc_hz(fc_hz),
        .bandwidth_hz(bandwidth_hz),
        .pulse_duration_us(pulse_duration_us),
        .amplitude(amplitude),
        .mode(mode),

        .dac_cs_n(dac_cs_n),
        .dac_sclk(dac_sclk),
        .dac_sdi(dac_sdi),

        .dac_busy(dac_busy),
        .sample_done(sample_done),
        .ping_done(ping_done),

        .waveform_sample(waveform_sample),
        .sample_enable(sample_enable)
    );



    always #10 clk = ~clk;



    always @(posedge clk) begin

        if (!reset && enable && sample_enable) begin

            sample_count = sample_count + 1;

            if (!dac_busy)
                accepted_count = accepted_count + 1;
            else
                dropped_count = dropped_count + 1;

        end

    end



    always @(posedge sample_done) begin

        completed_count = completed_count + 1;

    end



    initial begin

        clk = 0;
        reset = 1;
        enable = 0;

        fc_hz = 32'd200000;
        bandwidth_hz = 32'd70000;
        pulse_duration_us = 32'd4000;
        amplitude = 16'd800;

        mode = 2'b00;

        sample_count = 0;
        accepted_count = 0;
        completed_count = 0;
        dropped_count = 0;



        #200;

        reset = 0;

        #200;

        enable = 1;



        #100000;


        enable = 0;

        #5000;



        $display("");
        $display("==============================================");
        $display(" AQUILA STREAMING THROUGHPUT TEST");
        $display("==============================================");

        $display(
            "Sample requests     = %0d",
            sample_count
        );

        $display(
            "Samples accepted    = %0d",
            accepted_count
        );

        $display(
            "DAC transactions    = %0d",
            completed_count
        );

        $display(
            "Dropped samples     = %0d",
            dropped_count
        );

        $display("");



        if (sample_count == 0) begin

            $display("FAIL: No sample events generated");

        end
        else if (dropped_count != 0) begin

            $display("WARNING: Samples were dropped");

        end
        else begin

            $display("PASS: No samples dropped during test");

        end


        $display("");
        $display("==============================================");
        $display(" STREAMING TEST COMPLETE");
        $display("==============================================");

        $finish;

    end

endmodule
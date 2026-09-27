
`timescale 1ns/1ps

module tb_aquila_waveform_dac_system;

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



    initial begin

        clk = 0;
        reset = 1;
        enable = 0;

        fc_hz = 32'd200000;
        bandwidth_hz = 32'd70000;
        pulse_duration_us = 32'd4000;
        amplitude = 16'd800;

        mode = 2'b00;



        #200;

        reset = 0;

        #200;

        enable = 1;



        $display("");
        $display("==============================================");
        $display(" AQUILA FULL WAVEFORM + DAC SYSTEM TEST");
        $display("==============================================");

        $display("Mode              = GEOMETRIC");
        $display("Fc                 = %0d Hz", fc_hz);
        $display("Bandwidth          = %0d Hz", bandwidth_hz);
        $display("Pulse Duration     = %0d us", pulse_duration_us);
        $display("Amplitude          = %0d", amplitude);
        $display("Sample Rate        = 5 MSPS");

        $display("");
        $display("Starting waveform generation...");
        $display("");



        #30000;



        enable = 0;

        #1000;

        $display("");
        $display("==============================================");
        $display(" FULL SYSTEM TEST COMPLETE");
        $display("==============================================");

        $finish;

    end



    always @(posedge clk) begin

        if (sample_enable) begin

            $display(
                "SAMPLE: waveform=%0d | DAC_busy=%b | CS=%b",
                waveform_sample,
                dac_busy,
                dac_cs_n
            );

        end

    end



    always @(posedge sample_done) begin

        $display(
            "DAC TRANSACTION COMPLETE | waveform=%0d",
            waveform_sample
        );

    end



    always @(posedge ping_done) begin

        $display("");
        $display(">>> PING COMPLETE <<<");
        $display("");
    end

endmodule
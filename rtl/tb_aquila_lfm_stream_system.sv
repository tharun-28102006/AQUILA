`timescale 1ns/1ps

module tb_aquila_lfm_stream_system;

    logic clk;
    logic reset;
    logic enable;

    logic dac_cs_n;
    logic dac_sclk;
    logic dac_sdio0;
    logic dac_sdio1;

    logic dac_busy;
    logic sample_done;

    logic ping_done;

    logic [11:0] waveform_sample;
    logic sample_enable;

    integer sample_count;
    integer completed_count;



    aquila_lfm_stream_system dut (

        .clk(clk),
        .reset(reset),
        .enable(enable),

        .dac_cs_n(dac_cs_n),
        .dac_sclk(dac_sclk),

        .dac_sdio0(dac_sdio0),
        .dac_sdio1(dac_sdio1),

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

        end

    end



    always @(posedge sample_done) begin

        completed_count = completed_count + 1;

        if (completed_count <= 10) begin

            $display(
                "DAC sample complete #%0d",
                completed_count
            );

        end

    end



    initial begin

        $display("");
        $display("==============================================");
        $display(" AQUILA LFM + DAC STREAM TEST START");
        $display("==============================================");


        clk = 0;
        reset = 1;
        enable = 0;

        sample_count = 0;
        completed_count = 0;



        $display("RESET...");

        #200;

        reset = 0;

        $display("RESET RELEASED");



        #200;

        enable = 1;

        $display("STREAM ENABLED");



        #20_000;

        $display("");
        $display("20 us checkpoint");
        $display(
            "Generated samples = %0d",
            sample_count
        );
        $display(
            "DAC completions   = %0d",
            completed_count
        );



        #80_000;

        enable = 0;

        $display("");
        $display("STREAM DISABLED");


        #500;



        $display("");
        $display("==============================================");
        $display(" AQUILA LFM + DAC STREAM TEST");
        $display("==============================================");

        $display(
            "Samples generated = %0d",
            sample_count
        );

        $display(
            "DAC completions   = %0d",
            completed_count
        );

        $display(
            "Final waveform    = %0d",
            waveform_sample
        );

        $display(
            "CS                 = %b",
            dac_cs_n
        );

        $display(
            "Busy               = %b",
            dac_busy
        );


        if (sample_count > 50) begin
            $display("PASS: LFM SAMPLES GENERATED");
        end
        else begin
            $display("FAIL: SAMPLE GENERATION");
        end


        if (completed_count > 0) begin
            $display("PASS: DAC STREAM ACTIVE");
        end
        else begin
            $display("FAIL: NO DAC TRANSACTIONS");
        end


        $display("");
        $display("==============================================");
        $display(" TEST COMPLETE");
        $display("==============================================");

        $finish;

    end

endmodule
`timescale 1ns/1ps

module tb_aquila_lfm_capture;

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
    integer file_handle;



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

            if (sample_count < 4000) begin

                $fwrite(
                    file_handle,
                    "%0d,%0d\n",
                    sample_count,
                    waveform_sample
                );

                sample_count = sample_count + 1;

            end

        end

    end



    initial begin

        $display("");
        $display("==============================================");
        $display(" AQUILA LFM WAVEFORM CAPTURE");
        $display("==============================================");

        clk = 0;
        reset = 1;
        enable = 0;

        sample_count = 0;



        file_handle =
            $fopen("aquila_lfm_samples.csv", "w");

        $fwrite(
            file_handle,
            "sample_index,dac_sample\n"
        );



        #200;

        reset = 0;

        $display("RESET RELEASED");



        #200;

        enable = 1;

        $display("CAPTURE STARTED");



        #4_100_000;

        enable = 0;

        #1000;



        $fclose(file_handle);



        $display("");
        $display("==============================================");
        $display(" CAPTURE COMPLETE");
        $display("==============================================");

        $display(
            "Samples captured = %0d",
            sample_count
        );

        $display(
            "Expected samples = 4000"
        );

        if (sample_count >= 4000) begin
            $display("PASS: 4000 SAMPLES CAPTURED");
        end
        else begin
            $display("FAIL: SAMPLE CAPTURE");
        end

        $display("");
        $display("CSV FILE: aquila_lfm_samples.csv");

        $display("");
        $display("==============================================");


        $finish;

    end

endmodule
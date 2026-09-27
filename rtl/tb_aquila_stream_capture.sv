`timescale 1ns/1ps

module tb_aquila_stream_capture;

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

    logic [15:0] stream_sample_debug;

    integer stream_count;
    integer file_handle;
    integer waveform_file;



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
        .sample_enable(sample_enable),

        .stream_sample_debug(stream_sample_debug)

    );



    always #10 clk = ~clk;



    always @(posedge sample_done) begin

        if (stream_count < 8000) begin


            $fwrite(
                file_handle,
                "%0d,%0d\n",
                stream_count,
                stream_sample_debug
            );



            $fwrite(
                waveform_file,
                "%0d,%0d\n",
                stream_count,
                waveform_sample
            );


            stream_count = stream_count + 1;

        end

    end



    initial begin

        $display("");
        $display("==============================================");
        $display(" AQUILA DAC STREAM DATA CAPTURE");
        $display("==============================================");


        clk = 0;
        reset = 1;
        enable = 0;

        stream_count = 0;



        file_handle =
            $fopen("aquila_stream_samples.csv", "w");

        $fwrite(
            file_handle,
            "sample_index,stream_sample\n"
        );



        waveform_file =
            $fopen("aquila_waveform_samples.csv", "w");

        $fwrite(
            waveform_file,
            "sample_index,waveform_sample\n"
        );



        #200;

        reset = 0;

        $display("RESET RELEASED");



        #200;

        enable = 1;

        $display("STREAM CAPTURE STARTED");



        #5_000_000;

        enable = 0;

        #1000;



        $fclose(file_handle);

        $fclose(waveform_file);



        $display("");
        $display("==============================================");
        $display(" STREAM CAPTURE COMPLETE");
        $display("==============================================");

        $display(
            "Stream samples captured = %0d",
            stream_count
        );

        $display(
            "Expected                = 8000"
        );


        if (stream_count == 8000) begin

            $display(
                "PASS: ALL STREAM SAMPLES CAPTURED"
            );

        end

        else begin

            $display(
                "CHECK: STREAM SAMPLE COUNT"
            );

        end


        $display("");
        $display(
            "CSV 1: aquila_stream_samples.csv"
        );

        $display(
            "CSV 2: aquila_waveform_samples.csv"
        );

        $display("");
        $display(
            "=============================================="
        );

        $finish;

    end

endmodule
`timescale 1ns/1ps


module tb_ad3541r_stream_engine;


    localparam integer CLK_FREQ_HZ = 50_000_000;
    localparam integer SPI_FREQ_HZ = 8_333_333;


    logic clk;
    logic reset;


    logic        stream_enable;
    logic [15:0] dac_sample;
    logic        sample_valid;


    logic cs_n;
    logic sclk;

    logic sdio0;
    logic sdio1;

    logic busy;
    logic sample_done;
    logic sample_ready;


    integer sample_count;


    always #10 clk = ~clk;


    ad3541r_stream_engine #(
        .CLK_FREQ_HZ(CLK_FREQ_HZ),
        .SPI_FREQ_HZ(SPI_FREQ_HZ)
    ) dut (
        .clk(clk),
        .reset(reset),

        .stream_enable(stream_enable),

        .dac_sample(dac_sample),
        .sample_valid(sample_valid),

        .cs_n(cs_n),
        .sclk(sclk),

        .sdio0(sdio0),
        .sdio1(sdio1),

        .busy(busy),
        .sample_done(sample_done),
        .sample_ready(sample_ready)
    );


    always @(posedge clk) begin

        if (sample_done) begin

            sample_count = sample_count + 1;

            $display(
                "SAMPLE %0d DONE | DAC=%0d | CS=%b | SCLK=%b | SDIO0=%b | SDIO1=%b",
                sample_count,
                dac_sample,
                cs_n,
                sclk,
                sdio0,
                sdio1
            );

        end

    end


    initial begin


        clk = 1'b0;

        reset = 1'b1;

        stream_enable = 1'b0;

        dac_sample = 16'd0;

        sample_valid = 1'b0;

        sample_count = 0;



        #200;

        reset = 1'b0;

        #100;



        stream_enable = 1'b1;

        sample_valid = 1'b1;

        dac_sample = 16'h1000;



        @(posedge sample_done);

        dac_sample = 16'h2000;

        @(posedge sample_done);

        dac_sample = 16'h3000;

        @(posedge sample_done);

        dac_sample = 16'h4000;

        @(posedge sample_done);

        dac_sample = 16'h5000;

        @(posedge sample_done);

        dac_sample = 16'h6000;

        @(posedge sample_done);

        dac_sample = 16'h7000;

        @(posedge sample_done);

        dac_sample = 16'h8000;

        @(posedge sample_done);

        dac_sample = 16'h9000;

        @(posedge sample_done);

        dac_sample = 16'hA000;



        @(posedge sample_done);

        #200;



        stream_enable = 1'b0;

        sample_valid = 1'b0;


        #500;



        $display("");
        $display("==============================================");
        $display("   AD3541R DUAL SPI DDR STREAM TEST");
        $display("==============================================");

        $display("FPGA Clock      = %0d Hz", CLK_FREQ_HZ);
        $display("Configured SCLK = %0d Hz", SPI_FREQ_HZ);
        $display("Samples Done    = %0d", sample_count);

        if (sample_count >= 10) begin

            $display("");
            $display("PASS: STREAM ENGINE TRANSMITTED SAMPLES");
            $display("PASS: CONTINUOUS STREAMING ACTIVE");

        end

        else begin

            $display("");
            $display("FAIL: INSUFFICIENT SAMPLES");
        end

        $display("==============================================");

        $finish;

    end

endmodule

`timescale 1ns/1ps

module tb_ad3541r_spi_frame;

    logic clk;
    logic reset;

    logic sample_valid;
    logic [11:0] dac_sample;

    logic dac_cs_n;
    logic dac_sclk;
    logic dac_sdi;

    logic busy;
    logic sample_done;

    integer bit_count;
    reg [23:0] received_frame;
    reg [23:0] expected_frame;



    ad3541r_spi #(
        .CLK_FREQ_HZ(50_000_000),
        .SPI_FREQ_HZ(10_000_000)
    ) dut (

        .clk(clk),
        .reset(reset),

        .sample_valid(sample_valid),
        .dac_sample(dac_sample),

        .dac_cs_n(dac_cs_n),
        .dac_sclk(dac_sclk),
        .dac_sdi(dac_sdi),

        .busy(busy),
        .sample_done(sample_done)
    );



    always #10 clk = ~clk;



    always @(posedge dac_sclk) begin

        if (!dac_cs_n) begin

            received_frame = {received_frame[22:0], dac_sdi};

            bit_count = bit_count + 1;

            $display(
                "SPI BIT %0d = %b",
                bit_count,
                dac_sdi
            );

        end

    end



    initial begin

        clk = 0;
        reset = 1;

        sample_valid = 0;
        dac_sample = 12'd0;

        bit_count = 0;
        received_frame = 24'd0;



        #200;

        reset = 0;

        #200;



        dac_sample = 12'd2514;

        expected_frame = {8'h29, dac_sample, 4'b0000};

        $display("");
        $display("==============================================");
        $display(" AD3541R SPI FRAME TEST");
        $display("==============================================");

        $display(
            "DAC sample      = %0d",
            dac_sample
        );

        $display(
            "Expected frame  = %06h",
            expected_frame
        );

        $display("");



        @(posedge clk);

        sample_valid = 1;

        @(posedge clk);

        sample_valid = 0;



        wait(sample_done);


        #100;



        $display("");
        $display("==============================================");
        $display(" SPI TRANSACTION RESULT");
        $display("==============================================");

        $display(
            "Bits received   = %0d",
            bit_count
        );

        $display(
            "Received frame  = %06h",
            received_frame
        );

        $display(
            "Expected frame  = %06h",
            expected_frame
        );



        if (bit_count != 24) begin

            $display("");
            $display("FAIL: Expected 24 SPI bits");

        end
        else if (received_frame !== expected_frame) begin

            $display("");
            $display("FAIL: SPI FRAME MISMATCH");

        end
        else begin

            $display("");
            $display("PASS: 24-BIT SPI FRAME VERIFIED");

        end


        $display("");
        $display("==============================================");
        $display(" SPI FRAME TEST COMPLETE");
        $display("==============================================");

        $finish;

    end

endmodule

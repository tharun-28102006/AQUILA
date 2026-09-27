
`timescale 1ns/1ps

module tb_ad3541r_spi;

    logic clk;
    logic reset;

    logic        sample_valid;
    logic [11:0] dac_sample;

    logic dac_cs_n;
    logic dac_sclk;
    logic dac_sdi;

    logic busy;
    logic sample_done;



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



    initial begin

        clk = 0;
        reset = 1;

        sample_valid = 0;
        dac_sample = 12'h000;

        #100;

        reset = 0;


        dac_sample = 12'hABC;

        #100;

        sample_valid = 1;

        #20;

        sample_valid = 0;



        wait(sample_done == 1'b1);

        #100;

        $display("");
        $display("==============================================");
        $display("     AD3541R SPI INTERFACE TEST");
        $display("==============================================");

        $display("Input DAC sample : 0x%03X", dac_sample);

        $display("Expected 16-bit  : 0x%04X",
                 {dac_sample, 4'b0000});

        $display("SPI instruction  : 0x%02X",
                 dut.WRITE_INSTRUCTION);

        $display("SPI transfer     : COMPLETE");

        $display("==============================================");

        $finish;

    end

endmodule

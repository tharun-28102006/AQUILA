
`timescale 1ns/1ps

module tb_aquila_dac_path;

    logic clk;
    logic reset;

    logic [11:0] waveform_sample;
    logic        waveform_valid;

    logic dac_cs_n;
    logic dac_sclk;
    logic dac_sdi;

    logic dac_busy;
    logic sample_done;



    aquila_dac_path dut (

        .clk(clk),
        .reset(reset),

        .waveform_sample(waveform_sample),
        .waveform_valid(waveform_valid),

        .dac_cs_n(dac_cs_n),
        .dac_sclk(dac_sclk),
        .dac_sdi(dac_sdi),

        .dac_busy(dac_busy),
        .sample_done(sample_done)
    );



    always #10 clk = ~clk;



    initial begin

        clk = 0;
        reset = 1;

        waveform_sample = 12'd2048;
        waveform_valid  = 0;

        #100;

        reset = 0;

        $display("");
        $display("==============================================");
        $display("       AQUILA DAC PATH TEST");
        $display("==============================================");



        send_sample(12'd2048);


        wait(sample_done == 1'b1);

        #100;



        send_sample(12'd3000);

        wait(sample_done == 1'b1);

        #100;



        send_sample(12'd1000);

        wait(sample_done == 1'b1);

        #100;


        $display("");
        $display("==============================================");
        $display("DAC PATH TEST COMPLETE");
        $display("==============================================");

        $finish;

    end



    task send_sample(input logic [11:0] value);

        begin

            @(posedge clk);

            waveform_sample = value;
            waveform_valid  = 1'b1;

            @(posedge clk);

            waveform_valid  = 1'b0;

            $display(
                "Waveform sample sent: %0d (0x%03X)",
                value,
                value
            );

        end

    endtask

endmodule
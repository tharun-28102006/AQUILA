`timescale 1ns/1ps

module tb_mode_selector;

    logic [1:0] mode;

    logic [11:0] lfm_sample;
    logic [11:0] geometric_sample;
    logic [11:0] phase_sample;

    logic [11:0] dac_sample;


    mode_selector dut (

        .mode(mode),

        .lfm_sample(lfm_sample),

        .geometric_sample(geometric_sample),

        .phase_sample(phase_sample),

        .dac_sample(dac_sample)

    );


    initial begin

        lfm_sample       = 12'd1000;
        geometric_sample = 12'd2000;
        phase_sample     = 12'd3000;


        $display("");
        $display("==============================================");
        $display("        AQUILA MODE SELECTOR TEST");
        $display("==============================================");



        mode = 2'b00;

        #1;

        $display(
            "MODE LFM       | Output = %0d",
            dac_sample
        );



        mode = 2'b01;

        #1;

        $display(
            "MODE GEOMETRIC | Output = %0d",
            dac_sample
        );



        mode = 2'b10;

        #1;

        $display(
            "MODE PHASE     | Output = %0d",
            dac_sample
        );



        mode = 2'b11;

        #1;

        $display(
            "MODE INVALID   | Output = %0d",
            dac_sample
        );


        $display("");
        $display("MODE SELECTOR TEST COMPLETE");
        $display("==============================================");

        $finish;

    end

endmodule

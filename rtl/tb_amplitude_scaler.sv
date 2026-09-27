`timescale 1ns/1ps

module tb_amplitude_scaler;

    reg [11:0] sine_in;
    reg [15:0] amplitude;

    wire [11:0] dac_out;


    amplitude_scaler dut (
        .sine_in(sine_in),
        .amplitude(amplitude),
        .dac_out(dac_out)
    );


    initial begin

        $display("");
        $display("==============================================");
        $display("        AQUILA AMPLITUDE SCALER TEST");
        $display("==============================================");


        sine_in = 12'd4095;
        amplitude = 16'd0;

        #1;

        $display(
            "Amplitude=0%%    Input=%0d Output=%0d",
            sine_in,
            dac_out
        );


        sine_in = 12'd4095;
        amplitude = 16'd600;

        #1;

        $display(
            "Amplitude=60%%   Input=%0d Output=%0d",
            sine_in,
            dac_out
        );


        sine_in = 12'd4095;
        amplitude = 16'd800;

        #1;

        $display(
            "Amplitude=80%%   Input=%0d Output=%0d",
            sine_in,
            dac_out
        );


        sine_in = 12'd4095;
        amplitude = 16'd1000;

        #1;

        $display(
            "Amplitude=100%%  Input=%0d Output=%0d",
            sine_in,
            dac_out
        );


        $display("");
        $display("AMPLITUDE SCALER TEST COMPLETE");
        $display("==============================================");

        $finish;

    end

endmodule
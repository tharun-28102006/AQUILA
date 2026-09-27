`timescale 1ns/1ps

module tb_safety_validator;

    logic [31:0] fc_hz;
    logic [31:0] bandwidth_hz;
    logic [31:0] pulse_duration_us;

    logic [15:0] amplitude;

    logic [1:0] mode;

    logic profile_valid;


    safety_validator dut (

        .fc_hz(fc_hz),

        .bandwidth_hz(bandwidth_hz),

        .pulse_duration_us(pulse_duration_us),

        .amplitude(amplitude),

        .mode(mode),

        .profile_valid(profile_valid)

    );


    task check_profile;

        input [31:0] fc;
        input [31:0] bw;
        input [31:0] tp;
        input [15:0] amp;
        input [1:0] md;

        begin

            fc_hz = fc;
            bandwidth_hz = bw;
            pulse_duration_us = tp;
            amplitude = amp;
            mode = md;

            #1;

            $display(
                "Fc=%0d BW=%0d Tp=%0d Amp=%0d Mode=%b -> VALID=%b",
                fc_hz,
                bandwidth_hz,
                pulse_duration_us,
                amplitude,
                mode,
                profile_valid
            );

        end

    endtask


    initial begin

        $display("");
        $display("==============================================");
        $display("       AQUILA SAFETY VALIDATOR TEST");
        $display("==============================================");



        check_profile(
            32'd200000,
            32'd70000,
            32'd4000,
            16'd800,
            2'b00
        );



        check_profile(
            32'd10000,
            32'd70000,
            32'd4000,
            16'd800,
            2'b00
        );



        check_profile(
            32'd200000,
            32'd300000,
            32'd4000,
            16'd800,
            2'b00
        );



        check_profile(
            32'd200000,
            32'd70000,
            32'd50000,
            16'd800,
            2'b00
        );



        check_profile(
            32'd200000,
            32'd70000,
            32'd4000,
            16'd1500,
            2'b00
        );



        check_profile(
            32'd200000,
            32'd70000,
            32'd4000,
            16'd800,
            2'b11
        );


        $display("");
        $display("==============================================");
        $display("SAFETY VALIDATOR TEST COMPLETE");
        $display("==============================================");

        $finish;

    end

endmodule

`timescale 1ns/1ps

module tb_ping_profile_latch;

    logic clk;
    logic reset;

    logic [31:0] requested_fc;
    logic [31:0] requested_bandwidth;
    logic [31:0] requested_pulse_duration;

    logic [15:0] requested_amplitude;

    logic [1:0] requested_mode;

    logic requested_valid;

    logic ping_done;


    logic [31:0] active_fc;
    logic [31:0] active_bandwidth;
    logic [31:0] active_pulse_duration;

    logic [15:0] active_amplitude;

    logic [1:0] active_mode;

    logic active_valid;



    ping_profile_latch dut (

        .clk(clk),
        .reset(reset),

        .requested_fc(requested_fc),
        .requested_bandwidth(requested_bandwidth),
        .requested_pulse_duration(requested_pulse_duration),

        .requested_amplitude(requested_amplitude),
        .requested_mode(requested_mode),

        .requested_valid(requested_valid),

        .ping_done(ping_done),

        .active_fc(active_fc),
        .active_bandwidth(active_bandwidth),
        .active_pulse_duration(active_pulse_duration),

        .active_amplitude(active_amplitude),
        .active_mode(active_mode),

        .active_valid(active_valid)

    );



    always #5 clk = ~clk;


    initial begin

        clk = 0;

        reset = 1;

        requested_valid = 0;

        ping_done = 0;

        requested_fc = 0;
        requested_bandwidth = 0;
        requested_pulse_duration = 0;

        requested_amplitude = 0;
        requested_mode = 0;



        #20;

        reset = 0;



        requested_fc = 32'd200000;

        requested_bandwidth = 32'd70000;

        requested_pulse_duration = 32'd4000;

        requested_amplitude = 16'd800;

        requested_mode = 2'b01;

        requested_valid = 1;


        @(posedge clk);
        #1;


        $display("");
        $display("==============================================");
        $display("     AQUILA PROFILE LATCH TEST");
        $display("==============================================");

        $display("");
        $display("PROFILE 1 LOADED");

        $display(
            "Active Fc = %0d",
            active_fc
        );

        $display(
            "Active BW = %0d",
            active_bandwidth
        );

        $display(
            "Active Tp = %0d",
            active_pulse_duration
        );

        $display(
            "Active A  = %0d",
            active_amplitude
        );

        $display(
            "Active Mode = %b",
            active_mode
        );



        requested_fc = 32'd120000;

        requested_bandwidth = 32'd40000;

        requested_pulse_duration = 32'd8000;

        requested_amplitude = 16'd1000;

        requested_mode = 2'b00;


        @(posedge clk);
        #1;


        $display("");
        $display("REQUESTED PROFILE CHANGED DURING PING");

        $display(
            "Requested Fc = %0d",
            requested_fc
        );

        $display(
            "Active Fc    = %0d",
            active_fc
        );

        $display(
            "Active Mode  = %b",
            active_mode
        );



        ping_done = 1;


        @(posedge clk);
        #1;

        ping_done = 0;



        $display("");
        $display("PING COMPLETE");

        $display(
            "New Active Fc = %0d",
            active_fc
        );

        $display(
            "New Active BW = %0d",
            active_bandwidth
        );

        $display(
            "New Active Tp = %0d",
            active_pulse_duration
        );

        $display(
            "New Active A  = %0d",
            active_amplitude
        );

        $display(
            "New Active Mode = %b",
            active_mode
        );


        $display("");
        $display("==============================================");
        $display("PROFILE LATCH TEST COMPLETE");
        $display("==============================================");

        $finish;

    end

endmodule

`timescale 1ns/1ps

module tb_aquila_controller;

    logic clk;
    logic reset;
    logic enable;

    logic [11:0] temperature;
    logic [11:0] salinity;
    logic [11:0] turbidity;
    logic [11:0] range;

    logic [1:0] temperature_state;
    logic [1:0] salinity_state;
    logic [1:0] turbidity_state;
    logic [1:0] range_state;

    logic [7:0] lut_address;

    logic [31:0] requested_fc;
    logic [31:0] requested_bandwidth;
    logic [31:0] requested_pulse_duration;

    logic [15:0] requested_amplitude;

    logic [1:0] requested_mode;


    logic [31:0] active_fc;
    logic [31:0] active_bandwidth;
    logic [31:0] active_pulse_duration;

    logic [15:0] active_amplitude;

    logic [1:0] active_mode;


    logic active_profile_valid;
    logic profile_valid;

    logic [11:0] dac_sample;

    logic ping_done;



    aquila_controller #(
        .PHASE_BITS(32),
        .CLK_FREQ_HZ(2_000_000)
    )

    dut (

        .clk(clk),
        .reset(reset),
        .enable(enable),

        .temperature(temperature),
        .salinity(salinity),
        .turbidity(turbidity),
        .range(range),

        .temperature_state(temperature_state),
        .salinity_state(salinity_state),
        .turbidity_state(turbidity_state),
        .range_state(range_state),

        .lut_address(lut_address),

        .requested_fc(requested_fc),
        .requested_bandwidth(requested_bandwidth),
        .requested_pulse_duration(requested_pulse_duration),
        .requested_amplitude(requested_amplitude),
        .requested_mode(requested_mode),

        .active_fc(active_fc),
        .active_bandwidth(active_bandwidth),
        .active_pulse_duration(active_pulse_duration),
        .active_amplitude(active_amplitude),
        .active_mode(active_mode),

        .active_profile_valid(active_profile_valid),

        .profile_valid(profile_valid),

        .dac_sample(dac_sample),

        .ping_done(ping_done)

    );



    always #250 clk = ~clk;



    task display_profile;

        begin

            $display("");
            $display("----------------------------------------------");

            $display(
                "Requested: Fc=%0d BW=%0d Tp=%0d A=%0d Mode=%b",
                requested_fc,
                requested_bandwidth,
                requested_pulse_duration,
                requested_amplitude,
                requested_mode
            );

            $display(
                "Active:    Fc=%0d BW=%0d Tp=%0d A=%0d Mode=%b",
                active_fc,
                active_bandwidth,
                active_pulse_duration,
                active_amplitude,
                active_mode
            );

            $display(
                "Valid=%b  PingDone=%b  DAC=%0d",
                profile_valid,
                ping_done,
                dac_sample
            );

            $display("----------------------------------------------");

        end

    endtask


    initial begin

        clk = 0;

        reset = 1;
        enable = 0;



        temperature = 12'd25;
        salinity   = 12'd450;
        turbidity  = 12'd50;
        range      = 12'd2;


        #1000;

        reset = 0;
        enable = 1;



        @(posedge clk);
        #1;

        $display("");
        $display("==============================================");
        $display("     AQUILA PING PROFILE INTEGRATION");
        $display("==============================================");

        $display("");
        $display("INITIAL PROFILE");

        display_profile();



        temperature = 12'd35;
        salinity   = 12'd700;
        turbidity  = 12'd150;
        range      = 12'd5;



        #1000;

        $display("");
        $display("ENVIRONMENT CHANGED DURING PING");

        display_profile();



        if (active_fc == 32'd200000 &&
            active_bandwidth == 32'd70000 &&
            active_pulse_duration == 32'd4000 &&
            active_amplitude == 16'd800 &&
            active_mode == 2'b01)

            $display("PASS: ACTIVE PROFILE HELD DURING PING");

        else

            $display("FAIL: ACTIVE PROFILE CHANGED DURING PING");



        wait(ping_done == 1'b1);

        $display("");
        $display("PING COMPLETED");

        display_profile();


        @(posedge clk);
        #1;

        $display("");
        $display("NEXT PING PROFILE");

        display_profile();


        if (active_fc == 32'd111720 &&
            active_bandwidth == 32'd32000 &&
            active_pulse_duration == 32'd8000 &&
            active_amplitude == 16'd1000 &&
            active_mode == 2'b10)

            $display("PASS: NEW PROFILE LOADED AT PING BOUNDARY");

        else

            $display("FAIL: NEW PROFILE NOT LOADED");



        if (active_fc == 32'd111720 &&
            active_bandwidth == 32'd32000 &&
            active_pulse_duration == 32'd8000 &&
            active_amplitude == 16'd1000 &&
            active_mode == 2'b10)

            $display("PASS: NEW PROFILE LOADED AT PING BOUNDARY");

        else

            $display("FAIL: NEW PROFILE NOT LOADED");


        $display("");
        $display("==============================================");
        $display("PING PROFILE INTEGRATION TEST COMPLETE");
        $display("==============================================");


        $finish;

    end

endmodule
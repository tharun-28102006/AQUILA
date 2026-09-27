`timescale 1ns/1ps

module tb_aquila_top;

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

    logic [31:0] fc_hz;
    logic [31:0] bandwidth_hz;
    logic [31:0] pulse_duration_us;

    logic [15:0] amplitude;

    logic [1:0] mode;

    logic profile_valid;

    logic [11:0] dac_sample;

    logic ping_done;



    aquila_top #(
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

        .fc_hz(fc_hz),
        .bandwidth_hz(bandwidth_hz),
        .pulse_duration_us(pulse_duration_us),

        .amplitude(amplitude),

        .mode(mode),

        .profile_valid(profile_valid),

        .dac_sample(dac_sample),

        .ping_done(ping_done)

    );



    always #250 clk = ~clk;



    task show_environment;

        begin

            #1;

            $display("");
            $display("----------------------------------------------");

            $display(
                "T=%0d  S=%0d  Tu=%0d  R=%0d",
                temperature,
                salinity,
                turbidity,
                range
            );

            $display(
                "States = %b %b %b %b",
                temperature_state,
                salinity_state,
                turbidity_state,
                range_state
            );

            $display(
                "LUT Address = 0x%02h",
                lut_address
            );

            $display(
                "Fc=%0d Hz",
                fc_hz
            );

            $display(
                "BW=%0d Hz",
                bandwidth_hz
            );

            $display(
                "Tp=%0d us",
                pulse_duration_us
            );

            $display(
                "Amplitude=%0d",
                amplitude
            );

            $display(
                "Mode=%b",
                mode
            );

            $display(
                "Profile Valid=%b",
                profile_valid
            );

            $display("----------------------------------------------");

        end

    endtask


    initial begin

        clk = 0;

        reset = 1;
        enable = 0;



        temperature = 32'd25;
        salinity   = 32'd450;
        turbidity  = 32'd50;
        range      = 32'd2;


        #1000;

        reset = 0;
        enable = 1;

        show_environment();



        #2000;

        temperature = 32'd35;
        salinity   = 32'd700;
        turbidity  = 32'd150;
        range      = 32'd5;


        show_environment();



        #2000;

        temperature = 32'd10;
        salinity   = 32'd100;
        turbidity  = 32'd10;
        range      = 32'd0;


        show_environment();


        $display("");
        $display("==============================================");
        $display("        AQUILA TOP LEVEL TEST COMPLETE");
        $display("==============================================");

        $finish;

    end

endmodule
`timescale 1us/1ns

module tb_ping_boundary;

    reg clk;
    reg reset;

    reg profile_valid;

    reg [31:0] fc_in;
    reg [31:0] bandwidth_in;
    reg [31:0] pulse_duration_in;
    reg [15:0] amplitude_in;
    reg [1:0] mode_in;

    wire [31:0] fc_active;
    wire [31:0] bandwidth_active;
    wire [31:0] pulse_duration_active;
    wire [15:0] amplitude_active;
    wire [1:0] mode_active;

    wire ping_active;
    wire profile_update;


    ping_boundary_fsm dut (

        .clk(clk),
        .reset(reset),

        .profile_valid(profile_valid),

        .fc_in(fc_in),
        .bandwidth_in(bandwidth_in),
        .pulse_duration_in(pulse_duration_in),
        .amplitude_in(amplitude_in),
        .mode_in(mode_in),

        .fc_active(fc_active),
        .bandwidth_active(bandwidth_active),
        .pulse_duration_active(pulse_duration_active),
        .amplitude_active(amplitude_active),
        .mode_active(mode_active),

        .ping_active(ping_active),
        .profile_update(profile_update)
    );



    always #0.5 clk = ~clk;


    initial begin

        clk = 0;
        reset = 1;

        profile_valid = 0;

        fc_in = 0;
        bandwidth_in = 0;
        pulse_duration_in = 0;
        amplitude_in = 0;
        mode_in = 0;


        $display("");
        $display("==============================================");
        $display("   AQUILA PULSE-DURATION FSM TEST");
        $display("==============================================");



        #2;

        reset = 0;



        fc_in = 200000;
        bandwidth_in = 70000;
        pulse_duration_in = 2000;
        amplitude_in = 800;
        mode_in = 2'b01;

        profile_valid = 1;

        $display("");
        $display("PROFILE 1");
        $display("Fc=%0d Hz", fc_in);
        $display("BW=%0d Hz", bandwidth_in);
        $display("Tp=%0d us", pulse_duration_in);
        $display("Amplitude=%0d", amplitude_in);
        $display("Mode=%02b", mode_in);

        #1;

        profile_valid = 0;


        #2100;



        fc_in = 120000;
        bandwidth_in = 40000;
        pulse_duration_in = 8000;
        amplitude_in = 1000;
        mode_in = 2'b00;

        profile_valid = 1;

        $display("");
        $display("PROFILE 2");
        $display("Fc=%0d Hz", fc_in);
        $display("BW=%0d Hz", bandwidth_in);
        $display("Tp=%0d us", pulse_duration_in);
        $display("Amplitude=%0d", amplitude_in);
        $display("Mode=%02b", mode_in);

        #1;

        profile_valid = 0;


        #8100;


        $display("");
        $display("==============================================");
        $display("             TEST COMPLETE");
        $display("==============================================");

        $finish;

    end


    initial begin

        forever begin

            #100;

            $display(
                "TIME=%0t us | STATE=%0d | PING=%b | UPDATE=%b | COUNTER=%0d | Tp=%0d",
                $time,
                dut.state,
                ping_active,
                profile_update,
                dut.pulse_counter,
                pulse_duration_active
            );

        end

    end

endmodule
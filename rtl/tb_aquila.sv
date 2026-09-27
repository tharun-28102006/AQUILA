
`timescale 1ns/1ps

module tb_aquila;


    reg [11:0] temperature;
    reg [11:0] salinity;
    reg [11:0] turbidity;
    reg [11:0] range;


    wire [1:0] temperature_state;
    wire [1:0] salinity_state;
    wire [1:0] turbidity_state;
    wire [1:0] range_state;

    wire [7:0] lut_address;

    wire [31:0] fc;
    wire [31:0] bandwidth;
    wire [31:0] pulse_duration;
    wire [15:0] amplitude;
    wire [1:0] mode;


    integer t;
    integer s;
    integer tu;
    integer r;

    integer test_number;
    integer pass_count;
    integer fail_count;
    integer expected_address;


    aquila_top dut (
        .temperature(temperature),
        .salinity(salinity),
        .turbidity(turbidity),
        .range(range),

        .temperature_state(temperature_state),
        .salinity_state(salinity_state),
        .turbidity_state(turbidity_state),
        .range_state(range_state),

        .lut_address(lut_address),

        .fc(fc),
        .bandwidth(bandwidth),
        .pulse_duration(pulse_duration),
        .amplitude(amplitude),
        .mode(mode)
    );


    initial begin

        test_number = 0;
        pass_count = 0;
        fail_count = 0;

        $dumpfile("aquila_81state.vcd");
        $dumpvars(0, tb_aquila);

        $display("");
        $display("==============================================");
        $display("      AQUILA 81-STATE RTL VERIFICATION");
        $display("==============================================");
        $display("");


        for (t = 0; t < 3; t = t + 1) begin
            for (s = 0; s < 3; s = s + 1) begin
                for (tu = 0; tu < 3; tu = tu + 1) begin
                    for (r = 0; r < 3; r = r + 1) begin

                        test_number = test_number + 1;


                        if (t == 0)
                            temperature = 12'd10;
                        else if (t == 1)
                            temperature = 12'd25;
                        else
                            temperature = 12'd35;


                        if (s == 0)
                            salinity = 12'd100;
                        else if (s == 1)
                            salinity = 12'd450;
                        else
                            salinity = 12'd700;


                        if (tu == 0)
                            turbidity = 12'd10;
                        else if (tu == 1)
                            turbidity = 12'd50;
                        else
                            turbidity = 12'd150;


                        if (r == 0)
                            range = 12'd0;
                        else if (r == 1)
                            range = 12'd2;
                        else
                            range = 12'd5;


                        expected_address =
                            (t * 64) +
                            (s * 16) +
                            (tu * 4) +
                            r;


                        #1;


                        if (lut_address == expected_address) begin

                            pass_count = pass_count + 1;

                            $display(
                                "PASS %0d: T=%0d S=%0d Tu=%0d R=%0d Address=%02h",
                                test_number,
                                t,
                                s,
                                tu,
                                r,
                                lut_address
                            );

                        end
                        else begin

                            fail_count = fail_count + 1;

                            $display(
                                "FAIL %0d: Expected=%02h Actual=%02h",
                                test_number,
                                expected_address,
                                lut_address
                            );

                        end

                    end
                end
            end
        end


        $display("");
        $display("==============================================");
        $display("             VERIFICATION RESULT");
        $display("==============================================");

        $display("Total Tests = %0d", test_number);
        $display("PASS        = %0d", pass_count);
        $display("FAIL        = %0d", fail_count);

        $display("==============================================");

        if (fail_count == 0) begin
            $display("AQUILA 81-STATE TEST PASSED");
        end
        else begin
            $display("AQUILA 81-STATE TEST FAILED");
        end

        $display("");

        #10;
        $finish;

    end

endmodule
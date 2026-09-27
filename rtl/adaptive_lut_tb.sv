`timescale 1ns/1ps

module adaptive_lut_tb;


    logic [7:0] address;


    logic [31:0] fc_hz;
    logic [31:0] bandwidth_hz;
    logic [31:0] pulse_duration_us;

    logic [15:0] amplitude;
    logic [1:0] mode;



    adaptive_lut dut (

        .address(address),

        .fc_hz(fc_hz),

        .bandwidth_hz(bandwidth_hz),

        .pulse_duration_us(pulse_duration_us),

        .amplitude(amplitude),

        .mode(mode)

    );



    integer pass_count;
    integer fail_count;
    integer i;



    initial begin

        pass_count = 0;
        fail_count = 0;

        address = 8'h00;

        #10;


        $display("");
        $display("==============================================");
        $display("       AQUILA LUT VERIFICATION");
        $display("==============================================");
        $display("");



        for (i = 0; i < 256; i = i + 1) begin

            address = i[7:0];

            #1;



            if (
                ((i >> 6) < 3) &&
                (((i >> 4) & 3) < 3) &&
                (((i >> 2) & 3) < 3) &&
                ((i & 3) < 3)
            ) begin


                if (
                    (^fc_hz === 1'bx) ||
                    (^bandwidth_hz === 1'bx) ||
                    (^pulse_duration_us === 1'bx) ||
                    (^amplitude === 1'bx) ||
                    (^mode === 1'bx)
                ) begin

                    $display(
                        "Address 0x%02X : FAIL - Unknown output",
                        i
                    );

                    fail_count = fail_count + 1;

                end

                else begin

                    $display(
                        "Address 0x%02X : PASS | Fc=%0d | BW=%0d | Tp=%0d | A=%0d | Mode=%b",
                        i,
                        fc_hz,
                        bandwidth_hz,
                        pulse_duration_us,
                        amplitude,
                        mode
                    );

                    pass_count = pass_count + 1;

                end

            end

            else begin


                if (
                    fc_hz !== 32'd200000 ||
                    bandwidth_hz !== 32'd20000 ||
                    pulse_duration_us !== 32'd4000 ||
                    amplitude !== 16'd600 ||
                    mode !== 2'b00
                ) begin

                    $display(
                        "Address 0x%02X : FAIL - Invalid address fallback incorrect",
                        i
                    );

                    fail_count = fail_count + 1;

                end

            end

        end



        $display("");
        $display("==============================================");
        $display("           AQUILA LUT TEST RESULT");
        $display("==============================================");

        $display(
            "Valid states tested : %0d",
            pass_count
        );

        $display(
            "Failures            : %0d",
            fail_count
        );

        $display("Expected valid states : 81");


        if (
            pass_count == 81 &&
            fail_count == 0
        ) begin

            $display("");
            $display("==============================================");
            $display("        LUT VERIFICATION : PASS");
            $display("        81 / 81 STATES PASSED");
            $display("==============================================");

        end

        else begin

            $display("");
            $display("==============================================");
            $display("        LUT VERIFICATION : FAIL");
            $display("==============================================");

        end


        $finish;

    end

endmodule
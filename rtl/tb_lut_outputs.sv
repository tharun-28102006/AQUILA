
`timescale 1ns/1ps

module tb_lut_outputs;

    reg  [7:0]  lut_address;

    wire [31:0] fc;
    wire [31:0] bandwidth;
    wire [31:0] pulse_duration;
    wire [15:0] amplitude;
    wire [1:0]  mode;

    integer pass_count;
    integer fail_count;
    integer i;

    adaptive_lut dut (
        .lut_address(lut_address),
        .fc(fc),
        .bandwidth(bandwidth),
        .pulse_duration(pulse_duration),
        .amplitude(amplitude),
        .mode(mode)
    );

    task check_state;

        input [7:0]  expected_address;
        input [31:0] expected_fc;
        input [31:0] expected_bandwidth;
        input [31:0] expected_pulse_duration;
        input [15:0] expected_amplitude;
        input [1:0]  expected_mode;

        begin

            lut_address = expected_address;

            #1;

            if (
                fc == expected_fc &&
                bandwidth == expected_bandwidth &&
                pulse_duration == expected_pulse_duration &&
                amplitude == expected_amplitude &&
                mode == expected_mode
            ) begin

                $display(
                    "PASS Address=%02X | Fc=%0d | BW=%0d | Tp=%0d us | A=%0d | Mode=%02b",
                    expected_address,
                    fc,
                    bandwidth,
                    pulse_duration,
                    amplitude,
                    mode
                );

                pass_count = pass_count + 1;

            end
            else begin

                $display(
                    "FAIL Address=%02X",
                    expected_address
                );

                $display(
                    "     Expected: Fc=%0d BW=%0d Tp=%0d A=%0d Mode=%02b",
                    expected_fc,
                    expected_bandwidth,
                    expected_pulse_duration,
                    expected_amplitude,
                    expected_mode
                );

                $display(
                    "     Actual  : Fc=%0d BW=%0d Tp=%0d A=%0d Mode=%02b",
                    fc,
                    bandwidth,
                    pulse_duration,
                    amplitude,
                    mode
                );

                fail_count = fail_count + 1;

            end

        end

    endtask


    initial begin

        pass_count = 0;
        fail_count = 0;
        lut_address = 8'h00;

        $display("");
        $display("==============================================");
        $display("       AQUILA LUT OUTPUT VERIFICATION");
        $display("==============================================");
        $display("");

        check_state(8'h00, 32'd321300, 32'd100000, 32'd2000, 16'd600, 2'b01);
        check_state(8'h01, 32'd214200, 32'd70000, 32'd4000, 16'd800, 2'b01);
        check_state(8'h02, 32'd128520, 32'd40000, 32'd8000, 16'd1000, 2'b00);
        check_state(8'h04, 32'd321300, 32'd100000, 32'd2000, 16'd600, 2'b01);
        check_state(8'h05, 32'd214200, 32'd70000, 32'd4000, 16'd800, 2'b01);
        check_state(8'h06, 32'd128520, 32'd40000, 32'd8000, 16'd1000, 2'b00);
        check_state(8'h08, 32'd321300, 32'd80000, 32'd2000, 16'd600, 2'b10);
        check_state(8'h09, 32'd214200, 32'd56000, 32'd4000, 16'd800, 2'b10);
        check_state(8'h0A, 32'd128520, 32'd32000, 32'd8000, 16'd1000, 2'b10);
        check_state(8'h10, 32'd315000, 32'd100000, 32'd2000, 16'd600, 2'b01);
        check_state(8'h11, 32'd210000, 32'd70000, 32'd4000, 16'd800, 2'b01);
        check_state(8'h12, 32'd126000, 32'd40000, 32'd8000, 16'd1000, 2'b00);
        check_state(8'h14, 32'd315000, 32'd100000, 32'd2000, 16'd600, 2'b01);
        check_state(8'h15, 32'd210000, 32'd70000, 32'd4000, 16'd800, 2'b01);
        check_state(8'h16, 32'd126000, 32'd40000, 32'd8000, 16'd1000, 2'b00);
        check_state(8'h18, 32'd315000, 32'd80000, 32'd2000, 16'd600, 2'b10);
        check_state(8'h19, 32'd210000, 32'd56000, 32'd4000, 16'd800, 2'b10);
        check_state(8'h1A, 32'd126000, 32'd32000, 32'd8000, 16'd1000, 2'b10);
        check_state(8'h20, 32'd308700, 32'd100000, 32'd2000, 16'd600, 2'b01);
        check_state(8'h21, 32'd205800, 32'd70000, 32'd4000, 16'd800, 2'b01);
        check_state(8'h22, 32'd123480, 32'd40000, 32'd8000, 16'd1000, 2'b00);
        check_state(8'h24, 32'd308700, 32'd100000, 32'd2000, 16'd600, 2'b01);
        check_state(8'h25, 32'd205800, 32'd70000, 32'd4000, 16'd800, 2'b01);
        check_state(8'h26, 32'd123480, 32'd40000, 32'd8000, 16'd1000, 2'b00);
        check_state(8'h28, 32'd308700, 32'd80000, 32'd2000, 16'd600, 2'b10);
        check_state(8'h29, 32'd205800, 32'd56000, 32'd4000, 16'd800, 2'b10);
        check_state(8'h2A, 32'd123480, 32'd32000, 32'd8000, 16'd1000, 2'b10);
        check_state(8'h40, 32'd306000, 32'd100000, 32'd2000, 16'd600, 2'b01);
        check_state(8'h41, 32'd204000, 32'd70000, 32'd4000, 16'd800, 2'b01);
        check_state(8'h42, 32'd122400, 32'd40000, 32'd8000, 16'd1000, 2'b00);
        check_state(8'h44, 32'd306000, 32'd100000, 32'd2000, 16'd600, 2'b01);
        check_state(8'h45, 32'd204000, 32'd70000, 32'd4000, 16'd800, 2'b01);
        check_state(8'h46, 32'd122400, 32'd40000, 32'd8000, 16'd1000, 2'b00);
        check_state(8'h48, 32'd306000, 32'd80000, 32'd2000, 16'd600, 2'b10);
        check_state(8'h49, 32'd204000, 32'd56000, 32'd4000, 16'd800, 2'b10);
        check_state(8'h4A, 32'd122400, 32'd32000, 32'd8000, 16'd1000, 2'b10);
        check_state(8'h50, 32'd300000, 32'd100000, 32'd2000, 16'd600, 2'b01);
        check_state(8'h51, 32'd200000, 32'd70000, 32'd4000, 16'd800, 2'b01);
        check_state(8'h52, 32'd120000, 32'd40000, 32'd8000, 16'd1000, 2'b00);
        check_state(8'h54, 32'd300000, 32'd100000, 32'd2000, 16'd600, 2'b01);
        check_state(8'h55, 32'd200000, 32'd70000, 32'd4000, 16'd800, 2'b01);
        check_state(8'h56, 32'd120000, 32'd40000, 32'd8000, 16'd1000, 2'b00);
        check_state(8'h58, 32'd300000, 32'd80000, 32'd2000, 16'd600, 2'b10);
        check_state(8'h59, 32'd200000, 32'd56000, 32'd4000, 16'd800, 2'b10);
        check_state(8'h5A, 32'd120000, 32'd32000, 32'd8000, 16'd1000, 2'b10);
        check_state(8'h60, 32'd294000, 32'd100000, 32'd2000, 16'd600, 2'b01);
        check_state(8'h61, 32'd196000, 32'd70000, 32'd4000, 16'd800, 2'b01);
        check_state(8'h62, 32'd117600, 32'd40000, 32'd8000, 16'd1000, 2'b00);
        check_state(8'h64, 32'd294000, 32'd100000, 32'd2000, 16'd600, 2'b01);
        check_state(8'h65, 32'd196000, 32'd70000, 32'd4000, 16'd800, 2'b01);
        check_state(8'h66, 32'd117600, 32'd40000, 32'd8000, 16'd1000, 2'b00);
        check_state(8'h68, 32'd294000, 32'd80000, 32'd2000, 16'd600, 2'b10);
        check_state(8'h69, 32'd196000, 32'd56000, 32'd4000, 16'd800, 2'b10);
        check_state(8'h6A, 32'd117600, 32'd32000, 32'd8000, 16'd1000, 2'b10);
        check_state(8'h80, 32'd290700, 32'd100000, 32'd2000, 16'd600, 2'b01);
        check_state(8'h81, 32'd193800, 32'd70000, 32'd4000, 16'd800, 2'b01);
        check_state(8'h82, 32'd116280, 32'd40000, 32'd8000, 16'd1000, 2'b00);
        check_state(8'h84, 32'd290700, 32'd100000, 32'd2000, 16'd600, 2'b01);
        check_state(8'h85, 32'd193800, 32'd70000, 32'd4000, 16'd800, 2'b01);
        check_state(8'h86, 32'd116280, 32'd40000, 32'd8000, 16'd1000, 2'b00);
        check_state(8'h88, 32'd290700, 32'd80000, 32'd2000, 16'd600, 2'b10);
        check_state(8'h89, 32'd193800, 32'd56000, 32'd4000, 16'd800, 2'b10);
        check_state(8'h8A, 32'd116280, 32'd32000, 32'd8000, 16'd1000, 2'b10);
        check_state(8'h90, 32'd285000, 32'd100000, 32'd2000, 16'd600, 2'b01);
        check_state(8'h91, 32'd190000, 32'd70000, 32'd4000, 16'd800, 2'b01);
        check_state(8'h92, 32'd114000, 32'd40000, 32'd8000, 16'd1000, 2'b00);
        check_state(8'h94, 32'd285000, 32'd100000, 32'd2000, 16'd600, 2'b01);
        check_state(8'h95, 32'd190000, 32'd70000, 32'd4000, 16'd800, 2'b01);
        check_state(8'h96, 32'd114000, 32'd40000, 32'd8000, 16'd1000, 2'b00);
        check_state(8'h98, 32'd285000, 32'd80000, 32'd2000, 16'd600, 2'b10);
        check_state(8'h99, 32'd190000, 32'd56000, 32'd4000, 16'd800, 2'b10);
        check_state(8'h9A, 32'd114000, 32'd32000, 32'd8000, 16'd1000, 2'b10);
        check_state(8'hA0, 32'd279300, 32'd100000, 32'd2000, 16'd600, 2'b01);
        check_state(8'hA1, 32'd186200, 32'd70000, 32'd4000, 16'd800, 2'b01);
        check_state(8'hA2, 32'd111720, 32'd40000, 32'd8000, 16'd1000, 2'b00);
        check_state(8'hA4, 32'd279300, 32'd100000, 32'd2000, 16'd600, 2'b01);
        check_state(8'hA5, 32'd186200, 32'd70000, 32'd4000, 16'd800, 2'b01);
        check_state(8'hA6, 32'd111720, 32'd40000, 32'd8000, 16'd1000, 2'b00);
        check_state(8'hA8, 32'd279300, 32'd80000, 32'd2000, 16'd600, 2'b10);
        check_state(8'hA9, 32'd186200, 32'd56000, 32'd4000, 16'd800, 2'b10);
        check_state(8'hAA, 32'd111720, 32'd32000, 32'd8000, 16'd1000, 2'b10);

        $display("");
        $display("----------------------------------------------");
        $display("TOTAL TESTS : %0d", pass_count + fail_count);
        $display("PASS        : %0d", pass_count);
        $display("FAIL        : %0d", fail_count);
        $display("----------------------------------------------");

        if (fail_count == 0)
            $display("AQUILA ADAPTIVE LUT VERIFIED");
        else
            $display("AQUILA ADAPTIVE LUT VERIFICATION FAILED");

        $display("==============================================");
        $display("");

        $finish;

    end

endmodule

`timescale 1ns/1ps

module tb_final_lut;
    logic [7:0] address;
    logic [31:0] fc_hz;
    logic [31:0] bandwidth_hz;
    logic [31:0] pulse_duration_us;
    logic [15:0] amplitude;
    logic [1:0] mode;
    integer temperature;
    integer salinity;
    integer turbidity;
    integer range_state;
    integer checked;
    integer start_frequency;
    integer end_frequency;

    adaptive_lut dut (
        .address(address),
        .fc_hz(fc_hz),
        .bandwidth_hz(bandwidth_hz),
        .pulse_duration_us(pulse_duration_us),
        .amplitude(amplitude),
        .mode(mode)
    );

    initial begin
        checked = 0;
        for (temperature = 0; temperature < 3; temperature = temperature + 1) begin
            for (salinity = 0; salinity < 3; salinity = salinity + 1) begin
                for (turbidity = 0; turbidity < 3; turbidity = turbidity + 1) begin
                    for (range_state = 0; range_state < 3; range_state = range_state + 1) begin
                        address = (temperature << 6) | (salinity << 4) | (turbidity << 2) | range_state;
                        #1;
                        start_frequency = fc_hz - bandwidth_hz / 2;
                        end_frequency = fc_hz + bandwidth_hz / 2;
                        if (start_frequency < 100000 || end_frequency > 500000 || bandwidth_hz == 0 || mode == 2'b11)
                            $fatal(1, "Invalid profile at address 0x%02h", address);
                        checked = checked + 1;
                    end
                end
            end
        end
        if (checked != 81)
            $fatal(1, "Expected 81 profiles, checked %0d", checked);
        $display("PASS: final LUT profiles %0d/81", checked);
        $finish;
    end
endmodule

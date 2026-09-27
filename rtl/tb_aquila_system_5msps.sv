`timescale 1ns/1ps

module tb_aquila_system_5msps;
    logic clk = 0;
    logic reset = 1;
    logic enable = 0;
    logic sample_enable;
    logic [11:0] temperature, salinity, turbidity, range;
    logic [1:0] temperature_state, salinity_state, turbidity_state, range_state;
    logic [7:0] lut_address;
    logic [31:0] requested_fc, requested_bandwidth, requested_pulse_duration;
    logic [15:0] requested_amplitude;
    logic [1:0] requested_mode;
    logic [31:0] active_fc, active_bandwidth, active_pulse_duration;
    logic [15:0] active_amplitude;
    logic [1:0] active_mode;
    logic active_valid, profile_valid;
    logic [11:0] waveform_sample, dac_sample;
    logic ping_done;
    integer sample_enable_count = 0;
    time previous_sample_time = 0;
    time measured_sample_interval;

    always #10 clk = ~clk;

    always @(posedge clk) begin
        if (sample_enable) begin
            if (sample_enable_count > 0) begin
                measured_sample_interval = $time - previous_sample_time;
                if (measured_sample_interval != 200)
                    $fatal(1, "Expected 200 ns sample interval, got %0t ns", measured_sample_interval);
            end
            previous_sample_time = $time;
            sample_enable_count = sample_enable_count + 1;
        end
    end

    sample_rate_generator #(
        .CLK_FREQ_HZ(50_000_000),
        .SAMPLE_RATE_HZ(5_000_000)
    ) sr (
        .clk(clk),
        .reset(reset),
        .sample_enable(sample_enable)
    );

    aquila_system_top #(
        .PHASE_BITS(32),
        .CLK_FREQ_HZ(50_000_000),
        .SAMPLE_RATE_HZ(5_000_000)
    ) dut (
        .clk(clk),
        .reset(reset),
        .enable(enable),
        .sample_enable(sample_enable),
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
        .active_valid(active_valid),
        .profile_valid(profile_valid),
        .waveform_sample(waveform_sample),
        .dac_sample(dac_sample),
        .ping_done(ping_done)
    );

    initial begin
        $dumpfile("aquila_5msps.vcd");
        $dumpvars(0, tb_aquila_system_5msps);

        temperature = 12'd35;
        salinity = 12'd700;
        turbidity = 12'd150;
        range = 12'd4;

        #100;
        reset = 0;
        enable = 1;

        wait (active_valid && profile_valid);
        #100;

        $display("INITIAL: addr=%02h mode=%0d Fc=%0d BW=%0d Tp_us=%0d Amp=%0d valid=%b",
                 lut_address, active_mode, active_fc, active_bandwidth,
                 active_pulse_duration, active_amplitude, profile_valid);

        if (active_fc + active_bandwidth / 2 > 500_000 ||
            active_fc - active_bandwidth / 2 < 100_000)
            $fatal(1, "Initial profile violates 100-500 kHz bounds");

        #1_000_000;
        temperature = 12'd10;
        salinity = 12'd100;
        turbidity = 12'd5;
        range = 12'd0;

        if (active_mode != 2'b10)
            $fatal(1, "Active mode changed before ping boundary");

        wait (ping_done);
        #100;

        $display("BOUNDARY: addr=%02h requested_mode=%0d active_mode=%0d active_Fc=%0d",
                 lut_address, requested_mode, active_mode, active_fc);

        if (active_fc + active_bandwidth / 2 > 500_000 ||
            active_fc - active_bandwidth / 2 < 100_000)
            $fatal(1, "Updated profile violates 100-500 kHz bounds");

        if (active_mode != requested_mode)
            $fatal(1, "New profile did not latch at ping boundary");

        if (sample_enable_count == 0)
            $fatal(1, "No sample-enable pulses observed");

        $display("TIMING: sample_enable interval=%0d ns frequency=5 MHz events=%0d",
                 measured_sample_interval, sample_enable_count);
        $display("PASS: Aquila 5-MSPS system-level RTL simulation");
        $finish;
    end
endmodule

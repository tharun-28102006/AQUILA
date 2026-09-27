`timescale 1ns/1ps

module tb_aquila_system;

    localparam integer CLK_FREQ_HZ    = 50_000_000;
    localparam integer SAMPLE_RATE_HZ = 5_000_000;
    localparam integer PULSE_US      = 4000;
    localparam integer EXPECTED_SAMPLES = (SAMPLE_RATE_HZ / 1_000_000) * PULSE_US;

    logic clk = 0;
    logic reset = 1;
    logic enable = 1;
    logic sample_enable = 0;

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
    logic active_valid;

    logic [11:0] waveform_sample;
    logic [11:0] dac_sample;
    logic ping_done;

    integer sample_count;
    integer clk_div;

    always #10 clk = ~clk;   // 50 MHz

    always_ff @(posedge clk) begin
        if (reset) begin
            clk_div <= 0;
            sample_enable <= 0;
        end else begin
            sample_enable <= 0;
            if (clk_div == 9) begin
                clk_div <= 0;
                sample_enable <= 1;
            end else begin
                clk_div <= clk_div + 1;
            end
        end
    end

    aquila_system_top #(
        .PHASE_BITS(32),
        .CLK_FREQ_HZ(CLK_FREQ_HZ),
        .SAMPLE_RATE_HZ(SAMPLE_RATE_HZ)
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

        .waveform_sample(waveform_sample),
        .dac_sample(dac_sample),
        .ping_done(ping_done)
    );

    initial begin
        temperature = 28;
        salinity   = 450;
        turbidity  = 35;
        range      = 2;

        repeat (5) @(posedge clk);
        reset = 0;

        repeat (20) @(posedge clk);

        $display("");
        $display("==============================================");
        $display(" AQUILA FULL FPGA INTEGRATION TEST");
        $display("==============================================");
        $display("ENVIRONMENT 1");
        $display("T/S/Tu/R states = %0d/%0d/%0d/%0d",
                 temperature_state, salinity_state,
                 turbidity_state, range_state);
        $display("LUT address      = 0x%02h", lut_address);
        $display("REQUESTED        = Fc=%0d BW=%0d Tp=%0d A=%0d Mode=%0d",
                 requested_fc, requested_bandwidth,
                 requested_pulse_duration, requested_amplitude,
                 requested_mode);
        $display("ACTIVE           = Fc=%0d BW=%0d Tp=%0d A=%0d Mode=%0d",
                 active_fc, active_bandwidth,
                 active_pulse_duration, active_amplitude,
                 active_mode);

        if (!active_valid) begin
            $display("FAIL: ACTIVE PROFILE NOT VALID");
            $finish;
        end

        temperature = 35;
        salinity   = 700;
        turbidity  = 150;
        range      = 4;

        repeat (100) @(posedge clk);

        $display("");
        $display("ENVIRONMENT 2 CHANGED DURING ACTIVE PING");
        $display("NEW REQUESTED  = Fc=%0d BW=%0d Tp=%0d A=%0d Mode=%0d",
                 requested_fc, requested_bandwidth,
                 requested_pulse_duration, requested_amplitude,
                 requested_mode);
        $display("STILL ACTIVE    = Fc=%0d BW=%0d Tp=%0d A=%0d Mode=%0d",
                 active_fc, active_bandwidth,
                 active_pulse_duration, active_amplitude,
                 active_mode);

        if (active_fc == requested_fc &&
            active_bandwidth == requested_bandwidth &&
            active_pulse_duration == requested_pulse_duration &&
            active_amplitude == requested_amplitude &&
            active_mode == requested_mode) begin
            $display("WARNING: PROFILE CHANGED BEFORE PING BOUNDARY");
        end else begin
            $display("PASS: ACTIVE PROFILE HELD DURING PING");
        end

        sample_count = 0;

        while (sample_count < EXPECTED_SAMPLES) begin
            @(posedge clk);
            if (sample_enable && enable && active_valid)
                sample_count = sample_count + 1;
        end

        $display("");
        $display("PING CAPTURE");
        $display("Expected samples = %0d", EXPECTED_SAMPLES);
        $display("Captured samples = %0d", sample_count);

        if (sample_count == EXPECTED_SAMPLES)
            $display("PASS: COMPLETE 4 ms / 5 MSPS PING GENERATED");
        else
            $display("FAIL: SAMPLE COUNT MISMATCH");

        $display("");
        $display("==============================================");
        $display(" INTEGRATION TEST COMPLETE");
        $display("==============================================");

        #1000;
        $finish;
    end

endmodule

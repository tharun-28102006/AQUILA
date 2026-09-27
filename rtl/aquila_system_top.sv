module aquila_system_top #(
    parameter integer PHASE_BITS     = 32,
    parameter integer CLK_FREQ_HZ    = 50_000_000,
    parameter integer SAMPLE_RATE_HZ = 5_000_000
)(
    input  logic        clk,
    input  logic        reset,
    input  logic        enable,
    input  logic        sample_enable,

    input  logic [11:0] temperature,
    input  logic [11:0] salinity,
    input  logic [11:0] turbidity,
    input  logic [11:0] range,

    output logic [1:0]  temperature_state,
    output logic [1:0]  salinity_state,
    output logic [1:0]  turbidity_state,
    output logic [1:0]  range_state,
    output logic [7:0]  lut_address,

    output logic [31:0] requested_fc,
    output logic [31:0] requested_bandwidth,
    output logic [31:0] requested_pulse_duration,
    output logic [15:0] requested_amplitude,
    output logic [1:0]  requested_mode,

    output logic [31:0] active_fc,
    output logic [31:0] active_bandwidth,
    output logic [31:0] active_pulse_duration,
    output logic [15:0] active_amplitude,
    output logic [1:0]  active_mode,
    output logic        active_valid,
    output logic        profile_valid,

    output logic [11:0] waveform_sample,
    output logic [11:0] dac_sample,
    output logic        ping_done
);

    aquila_top control_core (
        .temperature(temperature),
        .salinity(salinity),
        .turbidity(turbidity),
        .range(range),

        .temperature_state(temperature_state),
        .salinity_state(salinity_state),
        .turbidity_state(turbidity_state),
        .range_state(range_state),

        .lut_address(lut_address),

        .fc(requested_fc),
        .bandwidth(requested_bandwidth),
        .pulse_duration(requested_pulse_duration),
        .amplitude(requested_amplitude),
        .mode(requested_mode)
    );

    safety_validator profile_validator (
        .fc_hz(requested_fc),
        .bandwidth_hz(requested_bandwidth),
        .pulse_duration_us(requested_pulse_duration),
        .amplitude(requested_amplitude),
        .mode(requested_mode),
        .profile_valid(profile_valid)
    );

    ping_profile_latch profile_latch (
        .clk(clk),
        .reset(reset),

        .requested_fc(requested_fc),
        .requested_bandwidth(requested_bandwidth),
        .requested_pulse_duration(requested_pulse_duration),
        .requested_amplitude(requested_amplitude),
        .requested_mode(requested_mode),
        .requested_valid(profile_valid),

        .ping_done(ping_done),

        .active_fc(active_fc),
        .active_bandwidth(active_bandwidth),
        .active_pulse_duration(active_pulse_duration),
        .active_amplitude(active_amplitude),
        .active_mode(active_mode),
        .active_valid(active_valid)
    );

    aquila_waveform_top #(
        .PHASE_BITS(PHASE_BITS),
        .CLK_FREQ_HZ(CLK_FREQ_HZ),
        .SAMPLE_RATE_HZ(SAMPLE_RATE_HZ)
    ) waveform_core (
        .clk(clk),
        .reset(reset),
        .enable(enable && active_valid),
        .sample_enable(sample_enable),

        .fc_hz(active_fc),
        .bandwidth_hz(active_bandwidth),
        .pulse_duration_us(active_pulse_duration),
        .amplitude(active_amplitude),
        .mode(active_mode),

        .dac_sample(waveform_sample),
        .ping_done(ping_done)
    );

    safe_output_gate output_gate (
        .profile_valid(active_valid),
        .waveform_sample(waveform_sample),
        .dac_sample(dac_sample)
    );

endmodule

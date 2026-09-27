module dds_waveform #(
    parameter integer PHASE_BITS = 32,
    parameter integer CLK_FREQ_HZ = 2_000_000
)(
    input logic        clk,
    input logic        reset,
    input logic        enable,

    input logic [31:0] frequency_hz,
    input logic [15:0] amplitude,

    output logic [11:0] dac_sample
);

    logic [31:0] phase;

    logic [7:0] sine_address;

    logic [11:0] sine_value;



    dds_phase_accumulator #(
        .PHASE_BITS(PHASE_BITS),
        .CLK_FREQ_HZ(CLK_FREQ_HZ)
    )
    dds (
        .clk(clk),
        .reset(reset),
        .enable(enable),
        .frequency_hz(frequency_hz),
        .phase(phase)
    );



    assign sine_address = phase[31:24];



    sine_lut sine (
        .address(sine_address),
        .sine_value(sine_value)
    );



    amplitude_scaler scaler (
        .sine_in(sine_value),
        .amplitude(amplitude),
        .dac_out(dac_sample)
    );


endmodule
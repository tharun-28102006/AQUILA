
module lfm_waveform_generator #(
    parameter integer PHASE_BITS     = 32,
    parameter integer CLK_FREQ_HZ    = 50_000_000,
    parameter integer SAMPLE_RATE_HZ = 5_000_000
)(
    input logic clk,
    input logic reset,

    input logic enable,

    input logic sample_enable,

    input logic [31:0] fc_hz,
    input logic [31:0] bandwidth_hz,
    input logic [31:0] pulse_duration_us,

    input logic [15:0] amplitude,

    output logic [11:0] dac_sample,
    output logic        ping_done
);

    logic [31:0] phase;
    logic [31:0] current_frequency;

    logic [7:0] sine_address;
    logic [11:0] sine_value;
    logic [11:0] scaled_sample;

    logic [63:0] sample_count;
    logic [63:0] total_samples;

    logic [63:0] pulse_product;



    always_comb begin

        pulse_product =
            {32'd0, pulse_duration_us} * SAMPLE_RATE_HZ;

        total_samples =
            pulse_product / 64'd1_000_000;

    end



    lfm_dds #(
        .PHASE_BITS(PHASE_BITS),
        .SAMPLE_RATE_HZ(SAMPLE_RATE_HZ)
    )
    lfm (
        .clk(clk),
        .reset(reset),

        .enable(enable && sample_enable),

        .fc_hz(fc_hz),
        .bandwidth_hz(bandwidth_hz),
        .pulse_duration_us(pulse_duration_us),

        .phase(phase),
        .current_frequency(current_frequency)
    );



    assign sine_address = phase[31:24];

    sine_lut sine (
        .address(sine_address),
        .sine_value(sine_value)
    );



    amplitude_scaler scaler (
        .sine_in(sine_value),
        .amplitude(amplitude),
        .dac_out(scaled_sample)
    );


    assign dac_sample = scaled_sample;



    always_ff @(posedge clk) begin

        if (reset) begin

            sample_count <= 64'd0;
            ping_done    <= 1'b0;

        end

        else if (enable && sample_enable) begin

            ping_done <= 1'b0;

            if (sample_count < (total_samples - 64'd1)) begin

                sample_count <= sample_count + 64'd1;

            end

            else begin

                sample_count <= 64'd0;
                ping_done    <= 1'b1;

            end

        end

        else begin

            sample_count <= sample_count;
            ping_done    <= 1'b0;

        end

    end

endmodule
module phase_coded_waveform_engine #(
    parameter integer PHASE_BITS     = 32,
    parameter integer CLK_FREQ_HZ    = 50_000_000,
    parameter integer SAMPLE_RATE_HZ = 5_000_000
)(
    input logic clk,
    input logic reset,
    input logic enable,
    input logic sample_enable,

    input  logic [31:0] frequency_hz,
    input  logic [31:0] pulse_duration_us,

    input  logic [15:0] amplitude,

    output logic [11:0] dac_sample,
    output logic        ping_done
);

    logic [31:0] total_samples;
    logic [31:0] sample_count;

    logic [2:0] code_index;
    logic phase_bit;

    logic [31:0] phase;
    logic [63:0] phase_increment;

    logic [7:0] sine_address;

    logic [11:0] sine_value;
    logic [11:0] phase_sample;
    logic [11:0] amplitude_sample;
    logic [11:0] windowed_sample;



    always_comb begin

        total_samples =
            (pulse_duration_us * SAMPLE_RATE_HZ)
            / 1_000_000;

    end



    always_comb begin

        if (total_samples <= 8)

            code_index = sample_count[2:0];

        else

            code_index =
                (sample_count * 8)
                / total_samples;

    end



    phase_code_lut code_generator (

        .address(code_index),

        .phase_bit(phase_bit)

    );



    always_comb begin

        phase_increment =
            (frequency_hz * (64'd1 << PHASE_BITS))
            / SAMPLE_RATE_HZ;

    end


    always_ff @(posedge clk) begin

        if (reset)

            phase <= 32'd0;

        else if (enable && sample_enable)

            phase <=
                phase +
                phase_increment[PHASE_BITS-1:0];

    end



    assign sine_address =
        phase[31:24];


    sine_lut sine_generator (

        .address(sine_address),

        .sine_value(sine_value)

    );



    always_comb begin

        if (phase_bit)

            phase_sample = sine_value;

        else

            phase_sample =
                12'd4095 - sine_value;

    end



    amplitude_scaler amplitude_stage (

        .sine_in(phase_sample),

        .amplitude(amplitude),

        .dac_out(amplitude_sample)

    );



    digital_window window_stage (

        .clk(clk),

        .reset(reset),

        .enable(enable),

        .sample_count(sample_count),

        .total_samples(total_samples),

        .sample_in(amplitude_sample),

        .sample_out(windowed_sample)

    );



    always_ff @(posedge clk) begin

        if (reset) begin

            sample_count <= 32'd0;
            ping_done <= 1'b0;

        end

        else if (enable && sample_enable) begin

            ping_done <= 1'b0;

            if (sample_count < total_samples - 1) begin

                sample_count <= sample_count + 1;

            end

            else begin

                sample_count <= 32'd0;
                ping_done <= 1'b1;

            end

        end

        else begin

            ping_done <= 1'b0;

        end

    end



    assign dac_sample =
        windowed_sample;


endmodule
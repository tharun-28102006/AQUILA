module aquila_waveform_engine #(
    parameter integer PHASE_BITS   = 32,
    parameter integer CLK_FREQ_HZ  = 2_000_000
)(
    input  logic        clk,
    input  logic        reset,
    input  logic        enable,

    input  logic [31:0] fc_hz,
    input  logic [31:0] bandwidth_hz,
    input  logic [31:0] pulse_duration_us,

    input  logic [15:0] amplitude,

    output logic [11:0] dac_sample,
    output logic        ping_done
);


    logic [31:0] sample_count;
    logic [31:0] total_samples;

    always_comb begin

        total_samples =
            (pulse_duration_us * CLK_FREQ_HZ) / 1_000_000;

    end



    logic [31:0] current_frequency;

    logic [31:0] start_frequency;

    logic [63:0] frequency_numerator;

    logic [63:0] phase_increment;


    always_comb begin

        start_frequency =
            fc_hz - (bandwidth_hz / 2);

        if (total_samples <= 1) begin

            current_frequency =
                start_frequency;

        end

        else begin

            frequency_numerator =
                bandwidth_hz * sample_count;

            current_frequency =
                start_frequency +
                (frequency_numerator /
                (total_samples - 1));

        end

    end



    always_comb begin

        phase_increment =
            (current_frequency * (64'd1 << PHASE_BITS))
            / CLK_FREQ_HZ;

    end



    logic [PHASE_BITS-1:0] phase;

    always_ff @(posedge clk) begin

        if (reset) begin

            phase <= '0;

        end

        else if (enable) begin

            phase <=
                phase + phase_increment[PHASE_BITS-1:0];

        end

    end



    logic [7:0] sine_address;

    logic [11:0] sine_value;

    assign sine_address =
        phase[31:24];


    sine_lut sine_generator (

        .address(sine_address),

        .sine_value(sine_value)

    );



    logic [11:0] amplitude_sample;

    amplitude_scaler amplitude_stage (

        .sine_in(sine_value),

        .amplitude(amplitude),

        .dac_out(amplitude_sample)

    );



    logic [11:0] windowed_sample;

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

        else if (enable) begin

            ping_done <= 1'b0;

            if (sample_count < total_samples - 1) begin

                sample_count <=
                    sample_count + 1;

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
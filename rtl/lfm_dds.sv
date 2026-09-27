
module lfm_dds #(
    parameter integer PHASE_BITS    = 32,
    parameter integer SAMPLE_RATE_HZ = 5_000_000
)(
    input  logic        clk,
    input  logic        reset,
    input  logic        enable,

    input  logic [31:0] fc_hz,
    input  logic [31:0] bandwidth_hz,
    input  logic [31:0] pulse_duration_us,

    output logic [31:0] phase,
    output logic [31:0] current_frequency
);


    logic [63:0] total_samples;
    logic [63:0] sample_count;

    logic [63:0] pulse_product;

    logic [31:0] start_frequency;

    logic [63:0] bw_product;
    logic [63:0] frequency_numerator;

    logic [63:0] phase_numerator;
    logic [63:0] phase_increment;



    always_comb begin

        pulse_product =
            {32'd0, pulse_duration_us} * SAMPLE_RATE_HZ;

        total_samples =
            pulse_product / 64'd1_000_000;

    end



    always_comb begin

        if (fc_hz >= (bandwidth_hz / 2)) begin

            start_frequency =
                fc_hz - (bandwidth_hz / 2);

        end
        else begin

            start_frequency = 32'd0;

        end

    end



    always_comb begin

        bw_product = 64'd0;
        frequency_numerator = 64'd0;

        if (total_samples <= 64'd1) begin

            current_frequency =
                start_frequency;

        end
        else begin

            bw_product =
                {32'd0, bandwidth_hz} *
                sample_count;

            frequency_numerator =
                bw_product;

            current_frequency =
                start_frequency +
                (
                    frequency_numerator /
                    (total_samples - 64'd1)
                );

        end

    end



    always_comb begin

        phase_numerator =
            {32'd0, current_frequency} *
            (64'd1 << PHASE_BITS);

        phase_increment =
            phase_numerator /
            SAMPLE_RATE_HZ;

    end



    always_ff @(posedge clk) begin

        if (reset) begin

            phase        <= 32'd0;
            sample_count <= 64'd0;

        end

        else if (enable) begin

            phase <=
                phase + phase_increment[31:0];


            if (total_samples <= 64'd1) begin

                sample_count <= 64'd0;

            end

            else if (sample_count <
                     (total_samples - 64'd1)) begin

                sample_count <=
                    sample_count + 64'd1;

            end

            else begin

                sample_count <= 64'd0;

            end

        end

    end

endmodule
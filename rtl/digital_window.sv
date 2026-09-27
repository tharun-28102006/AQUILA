
module digital_window (

    input  logic        clk,
    input  logic        reset,
    input  logic        enable,

    input  logic [31:0] sample_count,
    input  logic [31:0] total_samples,

    input  logic [11:0] sample_in,

    output logic [11:0] sample_out

);


    logic [7:0] window_address;

    logic [15:0] window_coefficient;



    logic signed [12:0] centered_sample;



    logic signed [27:0] window_product;



    always_comb begin

        if (total_samples <= 1) begin

            window_address = 8'd0;

        end

        else begin

            window_address =
                (sample_count * 255)
                / (total_samples - 1);

        end

    end



    hann_lut window_lut (

        .address(window_address),

        .coefficient(window_coefficient)

    );



    always_comb begin

        centered_sample =
            $signed({1'b0, sample_in})
            - 13'sd2048;

    end



    window_multiplier multiplier (

        .sample_in(centered_sample),

        .window_coefficient(window_coefficient),

        .product(window_product)

    );



    logic signed [27:0] scaled_sample;

    logic signed [13:0] reconstructed_sample;


    always_comb begin


        scaled_sample =
            window_product >>> 15;



        reconstructed_sample =
            scaled_sample[13:0] + 14'sd2048;



        if (reconstructed_sample < 0)

            sample_out = 12'd0;

        else if (reconstructed_sample > 4095)

            sample_out = 12'd4095;

        else

            sample_out =
                reconstructed_sample[11:0];

    end

endmodule
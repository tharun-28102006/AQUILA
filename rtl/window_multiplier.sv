
module window_multiplier (

    input  logic signed [12:0] sample_in,
    input  logic        [15:0] window_coefficient,

    output logic signed [27:0] product

);


    always_comb begin

        product =
            sample_in * $signed({1'b0, window_coefficient});

    end

endmodule
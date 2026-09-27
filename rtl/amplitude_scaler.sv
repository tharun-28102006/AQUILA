module amplitude_scaler (
    input  logic [11:0] sine_in,
    input  logic [15:0] amplitude,

    output logic [11:0] dac_out
);

    logic [27:0] multiplied;

    always_comb begin


        multiplied = sine_in * amplitude;

        dac_out = multiplied / 1000;

    end

endmodule
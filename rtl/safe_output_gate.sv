module safe_output_gate (

    input logic        profile_valid,
    input logic [11:0] waveform_sample,

    output logic [11:0] dac_sample

);

    always_comb begin

        if (profile_valid)

            dac_sample = waveform_sample;

        else

            dac_sample = 12'd2048;

    end

endmodule
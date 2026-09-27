
module dac_sample_formatter (

    input  logic [11:0] waveform_sample,

    output logic [15:0] dac_sample_16bit

);

    always_comb begin

        dac_sample_16bit =
            {waveform_sample, 4'b0000};

    end

endmodule
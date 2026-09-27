
module dac_sample_scheduler (

    input  logic        clk,
    input  logic        reset,

    input  logic [11:0] waveform_sample,
    input  logic        waveform_valid,

    input  logic        dac_busy,

    output logic        dac_sample_valid,
    output logic [11:0] dac_sample
);

    always_ff @(posedge clk) begin

        if (reset) begin

            dac_sample_valid <= 1'b0;
            dac_sample       <= 12'd2048;

        end else begin

            dac_sample_valid <= 1'b0;

            if (waveform_valid && !dac_busy) begin

                dac_sample       <= waveform_sample;
                dac_sample_valid <= 1'b1;

            end

        end
    end

endmodule
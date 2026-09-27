
module waveform_sample_controller (

    input  logic        clk,
    input  logic        reset,

    input  logic        sample_enable,

    input  logic [11:0] waveform_in,
    input  logic        waveform_done,

    output logic [11:0] waveform_sample,
    output logic        waveform_valid,

    output logic        ping_done
);

    always_ff @(posedge clk) begin

        if (reset) begin

            waveform_sample <= 12'd2048;
            waveform_valid  <= 1'b0;
            ping_done       <= 1'b0;

        end else begin

            waveform_valid <= 1'b0;
            ping_done      <= 1'b0;

            if (sample_enable) begin

                waveform_sample <= waveform_in;
                waveform_valid  <= 1'b1;

            end

            if (waveform_done) begin

                ping_done <= 1'b1;

            end

        end
    end

endmodule
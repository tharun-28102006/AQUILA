module dds_phase_accumulator #(
    parameter integer PHASE_BITS = 32,
    parameter integer CLK_FREQ_HZ = 2_000_000
)(
    input  logic                   clk,
    input  logic                   reset,

    input  logic                   enable,

    input  logic [31:0]            frequency_hz,

    output logic [PHASE_BITS-1:0]  phase
);

    logic [PHASE_BITS-1:0] phase_increment;


    always_comb begin

        phase_increment =
            (frequency_hz << PHASE_BITS) / CLK_FREQ_HZ;

    end


    always_ff @(posedge clk) begin

        if (reset) begin

            phase <= 0;

        end

        else if (enable) begin

            phase <= phase + phase_increment;

        end

        else begin

            phase <= phase;

        end

    end

endmodule
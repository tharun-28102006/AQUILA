
module sample_rate_generator #(
    parameter integer CLK_FREQ_HZ    = 50_000_000,
    parameter integer SAMPLE_RATE_HZ = 5_000_000
)(
    input  logic clk,
    input  logic reset,

    output logic sample_enable
);

    localparam integer SAMPLE_PERIOD =
        CLK_FREQ_HZ / SAMPLE_RATE_HZ;

    localparam integer COUNTER_WIDTH =
        (SAMPLE_PERIOD <= 2) ? 1 : $clog2(SAMPLE_PERIOD);

    logic [COUNTER_WIDTH-1:0] counter;

    always_ff @(posedge clk) begin

        if (reset) begin

            counter       <= '0;
            sample_enable <= 1'b0;

        end else begin

            sample_enable <= 1'b0;

            if (counter == SAMPLE_PERIOD-1) begin

                counter       <= '0;
                sample_enable <= 1'b1;

            end else begin

                counter <= counter + 1'b1;

            end
        end
    end

endmodule
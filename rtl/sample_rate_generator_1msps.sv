
module sample_rate_generator_1msps #(
    parameter integer CLK_FREQ_HZ    = 50_000_000,
    parameter integer SAMPLE_RATE_HZ = 1_000_000
)(
    input  logic clk,
    input  logic reset,

    output logic sample_enable
);

    localparam integer DIVIDER =
        CLK_FREQ_HZ / SAMPLE_RATE_HZ;

    integer counter;

    always_ff @(posedge clk) begin

        if (reset) begin

            counter      <= 0;
            sample_enable <= 1'b0;

        end
        else begin

            sample_enable <= 1'b0;

            if (counter == DIVIDER - 1) begin

                counter       <= 0;
                sample_enable <= 1'b1;

            end
            else begin

                counter <= counter + 1;

            end

        end

    end

endmodule
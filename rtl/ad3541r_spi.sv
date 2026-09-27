
module ad3541r_spi #(
    parameter CLK_FREQ_HZ = 50_000_000,
    parameter SPI_FREQ_HZ = 10_000_000
)(
    input  logic        clk,
    input  logic        reset,

    input  logic        sample_valid,
    input  logic [11:0] dac_sample,

    output logic        dac_cs_n,
    output logic        dac_sclk,
    output logic        dac_sdi,

    output logic        busy,
    output logic        sample_done
);


    localparam logic [6:0] CH0_DAC_ADDR = 7'h29;

    localparam logic [7:0] WRITE_INSTRUCTION =
                    {1'b0, CH0_DAC_ADDR};


    localparam integer SPI_DIV =
                    CLK_FREQ_HZ / (2 * SPI_FREQ_HZ);

    integer clk_count;


    logic [23:0] shift_reg;
    logic [4:0]  bit_count;


    typedef enum logic [1:0] {
        IDLE,
        TRANSFER,
        FINISH
    } state_t;

    state_t state;


    always_ff @(posedge clk) begin

        if (reset) begin

            dac_cs_n    <= 1'b1;
            dac_sclk    <= 1'b0;
            dac_sdi     <= 1'b0;

            busy        <= 1'b0;
            sample_done <= 1'b0;

            clk_count   <= 0;
            bit_count   <= 0;
            shift_reg   <= 24'd0;

            state       <= IDLE;

        end else begin

            sample_done <= 1'b0;

            case (state)


                IDLE: begin

                    dac_cs_n  <= 1'b1;
                    dac_sclk  <= 1'b0;
                    dac_sdi   <= 1'b0;

                    busy      <= 1'b0;
                    clk_count <= 0;
                    bit_count <= 0;

                    if (sample_valid) begin


                        shift_reg <= {
                            WRITE_INSTRUCTION,
                            dac_sample,
                            4'b0000
                        };

                        busy      <= 1'b1;
                        dac_cs_n  <= 1'b0;

                        dac_sdi   <= WRITE_INSTRUCTION[7];

                        clk_count <= 0;
                        bit_count <= 0;

                        state     <= TRANSFER;
                    end
                end



                TRANSFER: begin

                    if (clk_count == SPI_DIV-1) begin

                        clk_count <= 0;

                        if (dac_sclk == 1'b0) begin

                            dac_sclk <= 1'b1;

                        end else begin

                            dac_sclk <= 1'b0;

                            if (bit_count == 5'd23) begin

                                state <= FINISH;

                            end else begin

                                bit_count <= bit_count + 1'b1;

                                shift_reg <= {
                                    shift_reg[22:0],
                                    1'b0
                                };

                                dac_sdi <= shift_reg[22];
                            end
                        end

                    end else begin

                        clk_count <= clk_count + 1;
                    end
                end



                FINISH: begin

                    dac_cs_n    <= 1'b1;
                    dac_sclk    <= 1'b0;
                    dac_sdi     <= 1'b0;

                    busy        <= 1'b0;
                    sample_done <= 1'b1;

                    state       <= IDLE;
                end

                default: begin

                    state <= IDLE;

                end

            endcase
        end
    end

endmodule
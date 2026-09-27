
module ad3541r_stream_engine #(
    parameter integer CLK_FREQ_HZ = 50_000_000,
    parameter integer SPI_FREQ_HZ = 8_333_333
)(
    input  logic        clk,
    input  logic        reset,

    input  logic        stream_enable,

    input  logic [15:0] dac_sample,
    input  logic        sample_valid,

    output logic        cs_n,
    output logic        sclk,

    output logic        sdio0,
    output logic        sdio1,

    output logic        busy,
    output logic        sample_done,
    output logic        sample_ready
);


    localparam logic [7:0] DAC_STREAM_ADDRESS = 8'h2A;



    localparam integer SCLK_HALF_DIV =
        CLK_FREQ_HZ / (2 * SPI_FREQ_HZ);



    logic [7:0]  address_shift;
    logic [15:0] data_shift;

    integer clock_counter;

    integer address_bit;
    integer data_pair;



    typedef enum logic [2:0] {
        IDLE,
        ADDRESS,
        DATA,
        WAIT_SAMPLE,
        STOP
    } state_t;

    state_t state;



    always_comb begin

        if (!stream_enable)
            sample_ready = 1'b0;

        else if (state == IDLE)
            sample_ready = 1'b1;

        else if (state == WAIT_SAMPLE)
            sample_ready = 1'b1;

        else
            sample_ready = 1'b0;

    end



    always_ff @(posedge clk) begin

        if (reset) begin


            cs_n        <= 1'b1;
            sclk        <= 1'b0;

            sdio0       <= 1'b0;
            sdio1       <= 1'b0;

            busy        <= 1'b0;
            sample_done <= 1'b0;



            address_shift <= 8'd0;
            data_shift    <= 16'd0;

            clock_counter <= 0;

            address_bit <= 0;
            data_pair   <= 0;

            state <= IDLE;

        end

        else begin


            sample_done <= 1'b0;


            case (state)



                IDLE: begin

                    cs_n <= 1'b1;
                    sclk <= 1'b0;

                    busy <= 1'b0;

                    clock_counter <= 0;


                    if (stream_enable && sample_valid) begin


                        cs_n <= 1'b0;
                        busy <= 1'b1;

                        address_shift <= DAC_STREAM_ADDRESS;

                        data_shift <= dac_sample;

                        address_bit <= 0;
                        data_pair   <= 0;


                        sdio0 <= DAC_STREAM_ADDRESS[7];
                        sdio1 <= 1'b0;

                        sclk <= 1'b0;

                        state <= ADDRESS;

                    end

                end



                ADDRESS: begin

                    if (clock_counter == SCLK_HALF_DIV-1) begin

                        clock_counter <= 0;



                        if (sclk == 1'b0) begin

                            sclk <= 1'b1;



                            if (address_bit == 7) begin


                                sdio0 <= data_shift[15];
                                sdio1 <= data_shift[14];

                                data_pair <= 0;

                                state <= DATA;

                            end

                            else begin

                                address_bit <= address_bit + 1;

                            end

                        end



                        else begin

                            sclk <= 1'b0;

                            if (address_bit < 7) begin

                                sdio0 <=
                                    address_shift[7-(address_bit+1)];

                                sdio1 <= 1'b0;

                            end

                        end

                    end

                    else begin

                        clock_counter <=
                            clock_counter + 1;

                    end

                end



                DATA: begin

                    if (clock_counter == SCLK_HALF_DIV-1) begin

                        clock_counter <= 0;



                        sclk <= ~sclk;



                        if (data_pair < 7) begin

                            data_pair <= data_pair + 1;


                            case (data_pair)

                                0: begin
                                    sdio0 <= data_shift[13];
                                    sdio1 <= data_shift[12];
                                end

                                1: begin
                                    sdio0 <= data_shift[11];
                                    sdio1 <= data_shift[10];
                                end

                                2: begin
                                    sdio0 <= data_shift[9];
                                    sdio1 <= data_shift[8];
                                end

                                3: begin
                                    sdio0 <= data_shift[7];
                                    sdio1 <= data_shift[6];
                                end

                                4: begin
                                    sdio0 <= data_shift[5];
                                    sdio1 <= data_shift[4];
                                end

                                5: begin
                                    sdio0 <= data_shift[3];
                                    sdio1 <= data_shift[2];
                                end

                                6: begin
                                    sdio0 <= data_shift[1];
                                    sdio1 <= data_shift[0];
                                end

                                default: begin
                                    sdio0 <= 1'b0;
                                    sdio1 <= 1'b0;
                                end

                            endcase

                        end



                        else begin


                            sample_done <= 1'b1;



                            if (stream_enable && sample_valid) begin

                                data_shift <= dac_sample;

                                data_pair <= 0;


                                sdio0 <= dac_sample[15];
                                sdio1 <= dac_sample[14];

                                state <= DATA;

                                busy <= 1'b1;

                            end



                            else if (stream_enable) begin

                                state <= WAIT_SAMPLE;

                                busy <= 1'b1;

                            end



                            else begin

                                state <= STOP;

                                busy <= 1'b1;

                            end

                        end

                    end

                    else begin

                        clock_counter <=
                            clock_counter + 1;

                    end

                end



                WAIT_SAMPLE: begin

                    cs_n <= 1'b0;
                    busy <= 1'b1;

                    sclk <= 1'b1;

                    clock_counter <= 0;



                    if (!stream_enable) begin

                        state <= STOP;

                    end



                    else if (sample_valid) begin

                        data_shift <= dac_sample;

                        data_pair <= 0;

                        sdio0 <= dac_sample[15];
                        sdio1 <= dac_sample[14];

                        state <= DATA;

                    end

                end



                STOP: begin

                    cs_n <= 1'b0;
                    busy <= 1'b1;

                    sclk <= 1'b1;

                    if (clock_counter == SCLK_HALF_DIV-1) begin

                        clock_counter <= 0;

                        cs_n <= 1'b1;
                        sclk <= 1'b0;

                        sdio0 <= 1'b0;
                        sdio1 <= 1'b0;

                        busy <= 1'b0;

                        state <= IDLE;

                    end

                    else begin

                        clock_counter <=
                            clock_counter + 1;

                    end

                end



                default: begin

                    cs_n <= 1'b1;
                    sclk <= 1'b0;

                    sdio0 <= 1'b0;
                    sdio1 <= 1'b0;

                    busy <= 1'b0;
                    sample_done <= 1'b0;

                    clock_counter <= 0;

                    state <= IDLE;

                end

            endcase

        end

    end

endmodule
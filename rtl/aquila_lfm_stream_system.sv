
module aquila_lfm_stream_system (

    input  logic clk,
    input  logic reset,
    input  logic enable,

    output logic dac_cs_n,
    output logic dac_sclk,

    output logic dac_sdio0,
    output logic dac_sdio1,

    output logic dac_busy,
    output logic sample_done,

    output logic ping_done,

    output logic [11:0] waveform_sample,
    output logic sample_enable,

    output logic [15:0] stream_sample_debug,
    output logic        stream_valid_debug

);

    // Hardware-timed FPGA streaming engine provides deterministic DAC sample delivery without CPU intervention.

    sample_rate_generator #(
        .CLK_FREQ_HZ(50_000_000),
        .SAMPLE_RATE_HZ(5_000_000)
    ) sample_gen (
        .clk(clk),
        .reset(reset),
        .sample_enable(sample_enable)
    );



    aquila_waveform_top #(

        .PHASE_BITS(32),
        .CLK_FREQ_HZ(50_000_000),
        .SAMPLE_RATE_HZ(5_000_000)

    ) waveform (

        .clk(clk),
        .reset(reset),

        .enable(enable),
        .sample_enable(sample_enable),

        .fc_hz(32'd300000),
        .bandwidth_hz(32'd80000),
        .pulse_duration_us(32'd4000),

        .amplitude(16'd800),
        .mode(2'd0),

        .dac_sample(waveform_sample),
        .ping_done(ping_done)

    );



    logic [15:0] dac_sample_16bit;

    dac_sample_formatter formatter (

        .waveform_sample(waveform_sample),
        .dac_sample_16bit(dac_sample_16bit)

    );



    logic [15:0] fifo_read_data;

    logic fifo_write;
    logic fifo_read;

    logic fifo_full;
    logic fifo_empty;

    logic [4:0] fifo_count;



    assign fifo_write =
        enable &&
        sample_enable &&
        !fifo_full;


    sample_fifo #(
        .DEPTH(16)

    ) fifo (

        .clk(clk),
        .reset(reset),

        .write_data(dac_sample_16bit),
        .write_en(fifo_write),

        .read_en(fifo_read),
        .read_data(fifo_read_data),

        .full(fifo_full),
        .empty(fifo_empty),

        .count(fifo_count)

    );



    logic [15:0] stream_sample;

    logic stream_valid;

    logic fifo_data_pending;



    logic stream_ready;



    assign fifo_read =
        !fifo_empty &&
        stream_ready &&
        !fifo_data_pending;



    always_ff @(posedge clk) begin

        if (reset) begin

            stream_sample     <= 16'd0;
            stream_valid      <= 1'b0;
            fifo_data_pending <= 1'b0;

        end

        else begin

            stream_valid <= 1'b0;



            if (fifo_read) begin

                fifo_data_pending <= 1'b1;

            end



            if (fifo_data_pending) begin

                stream_sample <= fifo_read_data;

                stream_valid <= 1'b1;

                fifo_data_pending <= 1'b0;

            end

        end

    end



    ad3541r_stream_engine #(

        .CLK_FREQ_HZ(50_000_000),
        .SPI_FREQ_HZ(8_333_333)

    ) stream (

        .clk(clk),
        .reset(reset),

        .stream_enable(enable),

        .dac_sample(stream_sample),

        .sample_valid(stream_valid),

        .cs_n(dac_cs_n),

        .sclk(dac_sclk),

        .sdio0(dac_sdio0),
        .sdio1(dac_sdio1),

        .busy(dac_busy),

        .sample_done(sample_done),

        .sample_ready(stream_ready)

    );
    assign stream_sample_debug = stream_sample;
    assign stream_valid_debug  = stream_valid;

endmodule
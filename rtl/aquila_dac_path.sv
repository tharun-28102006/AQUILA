
module aquila_dac_path (

    input  logic        clk,
    input  logic        reset,

    input  logic [11:0] waveform_sample,
    input  logic        waveform_valid,

    output logic        dac_cs_n,
    output logic        dac_sclk,
    output logic        dac_sdi,

    output logic        dac_busy,
    output logic        sample_done

);

    logic [11:0] scheduled_sample;
    logic        scheduled_valid;



    dac_sample_scheduler scheduler (

        .clk(clk),
        .reset(reset),

        .waveform_sample(waveform_sample),
        .waveform_valid(waveform_valid),

        .dac_busy(dac_busy),

        .dac_sample_valid(scheduled_valid),
        .dac_sample(scheduled_sample)
    );



    ad3541r_spi #(
        .CLK_FREQ_HZ(50_000_000),
        .SPI_FREQ_HZ(10_000_000)
    ) dac_spi (

        .clk(clk),
        .reset(reset),

        .sample_valid(scheduled_valid),
        .dac_sample(scheduled_sample),

        .dac_cs_n(dac_cs_n),
        .dac_sclk(dac_sclk),
        .dac_sdi(dac_sdi),

        .busy(dac_busy),
        .sample_done(sample_done)
    );

endmodule

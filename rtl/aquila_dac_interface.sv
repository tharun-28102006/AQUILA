
module aquila_dac_interface (

    input  logic        clk,
    input  logic        reset,

    input  logic [11:0] waveform_sample,

    input  logic        sample_valid,

    output logic        dac_cs_n,
    output logic        dac_sclk,
    output logic        dac_sdi,

    output logic        dac_busy,
    output logic        sample_done
);


    ad3541r_spi #(
        .CLK_FREQ_HZ(50_000_000),
        .SPI_FREQ_HZ(10_000_000)
    ) dac_spi (

        .clk(clk),
        .reset(reset),

        .sample_valid(sample_valid),
        .dac_sample(waveform_sample),

        .dac_cs_n(dac_cs_n),
        .dac_sclk(dac_sclk),
        .dac_sdi(dac_sdi),

        .busy(dac_busy),
        .sample_done(sample_done)
    );

endmodule
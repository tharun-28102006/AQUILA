
module aquila_waveform_dac_system (

    input  logic clk,
    input  logic reset,

    input  logic enable,

    input  logic [31:0] fc_hz,
    input  logic [31:0] bandwidth_hz,
    input  logic [31:0] pulse_duration_us,
    input  logic [15:0] amplitude,
    input  logic [1:0]  mode,

    output logic dac_cs_n,
    output logic dac_sclk,
    output logic dac_sdi,

    output logic dac_busy,
    output logic sample_done,
    output logic ping_done,

    output logic [11:0] waveform_sample,
    output logic        sample_enable

);

    logic waveform_valid;

    logic [11:0] scheduled_sample;
    logic        scheduled_valid;



    sample_rate_generator #(
        .CLK_FREQ_HZ(50_000_000),
        .SAMPLE_RATE_HZ(5_000_000)
    ) sample_clock (

        .clk(clk),
        .reset(reset),

        .sample_enable(sample_enable)
    );



    assign waveform_valid =
        enable && sample_enable;



    aquila_waveform_top #(
        .PHASE_BITS(32),
        .CLK_FREQ_HZ(50_000_000),
        .SAMPLE_RATE_HZ(5_000_000)
    ) waveform (

        .clk(clk),
        .reset(reset),

        .enable(enable),
        .sample_enable(sample_enable),

        .fc_hz(fc_hz),
        .bandwidth_hz(bandwidth_hz),
        .pulse_duration_us(pulse_duration_us),

        .amplitude(amplitude),
        .mode(mode),

        .dac_sample(waveform_sample),
        .ping_done(ping_done)
    );



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
    ) dac (

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
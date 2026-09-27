
module aquila_waveform_top #(
    parameter integer PHASE_BITS     = 32,
    parameter integer CLK_FREQ_HZ    = 50_000_000,
    parameter integer SAMPLE_RATE_HZ = 5_000_000
)(
    input  logic clk,
    input logic reset,
    input logic enable,

    input logic sample_enable,

    input logic [31:0] fc_hz,
    input logic [31:0] bandwidth_hz,
    input logic [31:0] pulse_duration_us,

    input logic [15:0] amplitude,

    input logic [1:0] mode,

    output logic [11:0] dac_sample,

    output logic ping_done
);


    logic [31:0] start_frequency;
    logic [31:0] end_frequency;

    always_comb begin

        start_frequency =
            fc_hz - (bandwidth_hz / 2);

        end_frequency =
            fc_hz + (bandwidth_hz / 2);

    end



    logic [11:0] lfm_sample;
    logic [11:0] geometric_sample;
    logic [11:0] phase_sample;

    logic lfm_done;
    logic geometric_done;
    logic phase_done;



    lfm_waveform_generator #(
        .PHASE_BITS(PHASE_BITS),
        .CLK_FREQ_HZ(CLK_FREQ_HZ),
        .SAMPLE_RATE_HZ(SAMPLE_RATE_HZ)
    )

    lfm_engine (

        .clk(clk),
        .reset(reset),

        .enable(enable),
        .sample_enable(sample_enable),

        .fc_hz(fc_hz),
        .bandwidth_hz(bandwidth_hz),
        .pulse_duration_us(pulse_duration_us),

        .amplitude(amplitude),

        .dac_sample(lfm_sample),
        .ping_done(lfm_done)

    );



    geometric_waveform_engine #(
        .PHASE_BITS(PHASE_BITS),
        .CLK_FREQ_HZ(CLK_FREQ_HZ),
        .SAMPLE_RATE_HZ(SAMPLE_RATE_HZ)
    )

    geometric_engine (

        .clk(clk),
        .reset(reset),

        .enable(enable),
        .sample_enable(sample_enable),

        .start_frequency_hz(start_frequency),
        .end_frequency_hz(end_frequency),

        .pulse_duration_us(pulse_duration_us),

        .amplitude(amplitude),

        .dac_sample(geometric_sample),
        .ping_done(geometric_done)

    );



    phase_coded_waveform_engine #(
        .PHASE_BITS(PHASE_BITS),
        .CLK_FREQ_HZ(CLK_FREQ_HZ),
        .SAMPLE_RATE_HZ(SAMPLE_RATE_HZ)
    )

    phase_engine (

        .clk(clk),
        .reset(reset),

        .enable(enable),
        .sample_enable(sample_enable),

        .frequency_hz(fc_hz),

        .pulse_duration_us(pulse_duration_us),

        .amplitude(amplitude),

        .dac_sample(phase_sample),
        .ping_done(phase_done)

    );



    mode_selector selector (

        .mode(mode),

        .lfm_sample(lfm_sample),

        .geometric_sample(geometric_sample),

        .phase_sample(phase_sample),

        .dac_sample(dac_sample)

    );




    always_comb begin

        case (mode)

            2'b00:
                ping_done = geometric_done;

            2'b01:
                ping_done = lfm_done;

            2'b10:
                ping_done = phase_done;

            default:
                ping_done = 1'b0;

        endcase

    end

endmodule
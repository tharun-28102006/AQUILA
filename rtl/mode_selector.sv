module mode_selector (

    input logic [1:0] mode,

    input logic [11:0] lfm_sample,

    input logic [11:0] geometric_sample,

    input logic [11:0] phase_sample,

    output logic [11:0] dac_sample

);

    localparam logic [1:0] MODE_GEOMETRIC = 2'b00;
    localparam logic [1:0] MODE_LFM       = 2'b01;
    localparam logic [1:0] MODE_PHASE     = 2'b10;


    always_comb begin

        case (mode)

            MODE_LFM:
                dac_sample = lfm_sample;

            MODE_GEOMETRIC:
                dac_sample = geometric_sample;

            MODE_PHASE:
                dac_sample = phase_sample;

            default:
                dac_sample = 12'd2048;

        endcase

    end

endmodule
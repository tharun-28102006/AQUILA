module safety_validator (

    input logic [31:0] fc_hz,
    input logic [31:0] bandwidth_hz,
    input logic [31:0] pulse_duration_us,

    input logic [15:0] amplitude,

    input logic [1:0] mode,

    output logic profile_valid

);


    localparam logic [31:0] MIN_SWEEP_START = 32'd100000;
    localparam logic [31:0] MAX_SWEEP_END   = 32'd500000;

    localparam logic [31:0] BW_MIN = 32'd5000;

    localparam logic [31:0] BW_MAX = 32'd200000;


    localparam logic [31:0] TP_MIN = 32'd100;
    localparam logic [31:0] TP_MAX = 32'd20000;


    localparam logic [15:0] AMP_MAX = 16'd1000;


    logic [31:0] start_frequency;
    logic [31:0] end_frequency;


    always_comb begin

        profile_valid = 1'b1;


        if (bandwidth_hz / 2 > fc_hz)

            start_frequency = 32'd0;

        else

            start_frequency =
                fc_hz - (bandwidth_hz / 2);



        end_frequency =
            fc_hz + (bandwidth_hz / 2);



        if (bandwidth_hz < BW_MIN)
            profile_valid = 1'b0;

        if (bandwidth_hz > BW_MAX)
            profile_valid = 1'b0;



        if (start_frequency < MIN_SWEEP_START)
            profile_valid = 1'b0;



        if (end_frequency > MAX_SWEEP_END)
            profile_valid = 1'b0;



        if (pulse_duration_us < TP_MIN)
            profile_valid = 1'b0;

        if (pulse_duration_us > TP_MAX)
            profile_valid = 1'b0;



        if (amplitude > AMP_MAX)
            profile_valid = 1'b0;



        if (mode == 2'b11)
            profile_valid = 1'b0;

    end

endmodule
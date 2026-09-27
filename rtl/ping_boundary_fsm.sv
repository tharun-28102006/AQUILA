module ping_boundary_fsm (

    input  logic        clk,
    input  logic        reset,

    input  logic        profile_valid,

    input  logic [31:0] fc_in,
    input  logic [31:0] bandwidth_in,
    input  logic [31:0] pulse_duration_in,
    input  logic [15:0] amplitude_in,
    input  logic [1:0]  mode_in,

    output logic [31:0] fc_active,
    output logic [31:0] bandwidth_active,
    output logic [31:0] pulse_duration_active,
    output logic [15:0] amplitude_active,
    output logic [1:0]  mode_active,

    output logic        ping_active,
    output logic        profile_update
);

    typedef enum logic [1:0] {
        IDLE      = 2'b00,
        LOAD      = 2'b01,
        TRANSMIT  = 2'b10,
        UPDATE    = 2'b11
    } state_t;

    state_t state;

    logic [31:0] pulse_counter;


    always_ff @(posedge clk) begin

        if (reset) begin

            state = IDLE;

            pulse_counter = 0;

            fc_active = 0;
            bandwidth_active = 0;
            pulse_duration_active = 0;
            amplitude_active = 0;
            mode_active = 0;

            ping_active = 0;
            profile_update = 0;

        end

        else begin

            profile_update = 0;

            case (state)

                IDLE: begin

                    ping_active = 0;
                    pulse_counter = 0;

                    if (profile_valid)
                        state = LOAD;

                end


                LOAD: begin


                    fc_active = fc_in;

                    bandwidth_active = bandwidth_in;

                    pulse_duration_active = pulse_duration_in;

                    amplitude_active = amplitude_in;

                    mode_active = mode_in;

                    pulse_counter = 0;

                    profile_update = 1;

                    state = TRANSMIT;

                end


                TRANSMIT: begin

                    ping_active = 1;

                    if (pulse_counter < pulse_duration_active - 1) begin

                        pulse_counter = pulse_counter + 1;

                    end

                    else begin

                        pulse_counter = 0;

                        ping_active = 0;

                        state = UPDATE;

                    end

                end


                UPDATE: begin

                    ping_active = 0;


                    if (profile_valid)
                        state = LOAD;

                    else
                        state = IDLE;

                end


                default: begin

                    state = IDLE;

                    pulse_counter = 0;

                    ping_active = 0;

                end

            endcase

        end

    end

endmodule
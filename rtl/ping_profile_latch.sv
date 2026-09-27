
module ping_profile_latch (

    input logic clk,
    input logic reset,

    input logic [31:0] requested_fc,
    input logic [31:0] requested_bandwidth,
    input logic [31:0] requested_pulse_duration,
    input logic [15:0] requested_amplitude,
    input logic [1:0]  requested_mode,

    input logic requested_valid,

    input logic ping_done,

    output logic [31:0] active_fc,
    output logic [31:0] active_bandwidth,
    output logic [31:0] active_pulse_duration,
    output logic [15:0] active_amplitude,
    output logic [1:0]  active_mode,

    output logic active_valid

);

    // The active profile remains locked until the current ping completes.

    always_ff @(posedge clk) begin

        if (reset) begin

            active_fc <= 32'd0;

            active_bandwidth <= 32'd0;

            active_pulse_duration <= 32'd0;

            active_amplitude <= 16'd0;

            active_mode <= 2'b00;

            active_valid <= 1'b0;

        end

        else begin


            if (!active_valid) begin

                if (requested_valid) begin

                    active_fc <= requested_fc;

                    active_bandwidth <= requested_bandwidth;

                    active_pulse_duration <=
                        requested_pulse_duration;

                    active_amplitude <=
                        requested_amplitude;

                    active_mode <=
                        requested_mode;

                    active_valid <= 1'b1;

                end

            end



            else if (ping_done) begin

                if (requested_valid) begin

                    active_fc <= requested_fc;

                    active_bandwidth <= requested_bandwidth;

                    active_pulse_duration <=
                        requested_pulse_duration;

                    active_amplitude <=
                        requested_amplitude;

                    active_mode <=
                        requested_mode;

                end

            end

        end

    end

endmodule
module adaptive_lut (
    input logic [7:0] address,
    output logic [31:0] fc_hz,
    output logic [31:0] bandwidth_hz,
    output logic [31:0] pulse_duration_us,
    output logic [15:0] amplitude,
    output logic [1:0] mode
);

    always_comb begin
        fc_hz = 32'd300000;
        bandwidth_hz = 32'd20000;
        pulse_duration_us = 32'd4000;
        amplitude = 16'd600;
        mode = 2'b00;

        case (address)
            8'h00: begin
                fc_hz = 32'd428400;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd2000;
                amplitude = 16'd600;
                mode = 2'b00;
            end
            8'h01: begin
                fc_hz = 32'd321300;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd4000;
                amplitude = 16'd800;
                mode = 2'b01;
            end
            8'h02: begin
                fc_hz = 32'd192780;
                bandwidth_hz = 32'd60000;
                pulse_duration_us = 32'd8000;
                amplitude = 16'd1000;
                mode = 2'b10;
            end
            8'h04: begin
                fc_hz = 32'd428400;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd2000;
                amplitude = 16'd600;
                mode = 2'b00;
            end
            8'h05: begin
                fc_hz = 32'd321300;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd4000;
                amplitude = 16'd800;
                mode = 2'b01;
            end
            8'h06: begin
                fc_hz = 32'd192780;
                bandwidth_hz = 32'd60000;
                pulse_duration_us = 32'd8000;
                amplitude = 16'd1000;
                mode = 2'b10;
            end
            8'h08: begin
                fc_hz = 32'd428400;
                bandwidth_hz = 32'd64000;
                pulse_duration_us = 32'd2000;
                amplitude = 16'd600;
                mode = 2'b00;
            end
            8'h09: begin
                fc_hz = 32'd321300;
                bandwidth_hz = 32'd64000;
                pulse_duration_us = 32'd4000;
                amplitude = 16'd800;
                mode = 2'b01;
            end
            8'h0A: begin
                fc_hz = 32'd192780;
                bandwidth_hz = 32'd48000;
                pulse_duration_us = 32'd8000;
                amplitude = 16'd1000;
                mode = 2'b10;
            end
            8'h10: begin
                fc_hz = 32'd420000;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd2000;
                amplitude = 16'd600;
                mode = 2'b00;
            end
            8'h11: begin
                fc_hz = 32'd315000;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd4000;
                amplitude = 16'd800;
                mode = 2'b01;
            end
            8'h12: begin
                fc_hz = 32'd189000;
                bandwidth_hz = 32'd60000;
                pulse_duration_us = 32'd8000;
                amplitude = 16'd1000;
                mode = 2'b10;
            end
            8'h14: begin
                fc_hz = 32'd420000;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd2000;
                amplitude = 16'd600;
                mode = 2'b00;
            end
            8'h15: begin
                fc_hz = 32'd315000;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd4000;
                amplitude = 16'd800;
                mode = 2'b01;
            end
            8'h16: begin
                fc_hz = 32'd189000;
                bandwidth_hz = 32'd60000;
                pulse_duration_us = 32'd8000;
                amplitude = 16'd1000;
                mode = 2'b10;
            end
            8'h18: begin
                fc_hz = 32'd420000;
                bandwidth_hz = 32'd64000;
                pulse_duration_us = 32'd2000;
                amplitude = 16'd600;
                mode = 2'b00;
            end
            8'h19: begin
                fc_hz = 32'd315000;
                bandwidth_hz = 32'd64000;
                pulse_duration_us = 32'd4000;
                amplitude = 16'd800;
                mode = 2'b01;
            end
            8'h1A: begin
                fc_hz = 32'd189000;
                bandwidth_hz = 32'd48000;
                pulse_duration_us = 32'd8000;
                amplitude = 16'd1000;
                mode = 2'b10;
            end
            8'h20: begin
                fc_hz = 32'd411600;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd2000;
                amplitude = 16'd600;
                mode = 2'b00;
            end
            8'h21: begin
                fc_hz = 32'd308700;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd4000;
                amplitude = 16'd800;
                mode = 2'b01;
            end
            8'h22: begin
                fc_hz = 32'd185220;
                bandwidth_hz = 32'd60000;
                pulse_duration_us = 32'd8000;
                amplitude = 16'd1000;
                mode = 2'b10;
            end
            8'h24: begin
                fc_hz = 32'd411600;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd2000;
                amplitude = 16'd600;
                mode = 2'b00;
            end
            8'h25: begin
                fc_hz = 32'd308700;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd4000;
                amplitude = 16'd800;
                mode = 2'b01;
            end
            8'h26: begin
                fc_hz = 32'd185220;
                bandwidth_hz = 32'd60000;
                pulse_duration_us = 32'd8000;
                amplitude = 16'd1000;
                mode = 2'b10;
            end
            8'h28: begin
                fc_hz = 32'd411600;
                bandwidth_hz = 32'd64000;
                pulse_duration_us = 32'd2000;
                amplitude = 16'd600;
                mode = 2'b00;
            end
            8'h29: begin
                fc_hz = 32'd308700;
                bandwidth_hz = 32'd64000;
                pulse_duration_us = 32'd4000;
                amplitude = 16'd800;
                mode = 2'b01;
            end
            8'h2A: begin
                fc_hz = 32'd185220;
                bandwidth_hz = 32'd48000;
                pulse_duration_us = 32'd8000;
                amplitude = 16'd1000;
                mode = 2'b10;
            end
            8'h40: begin
                fc_hz = 32'd408000;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd2000;
                amplitude = 16'd600;
                mode = 2'b00;
            end
            8'h41: begin
                fc_hz = 32'd306000;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd4000;
                amplitude = 16'd800;
                mode = 2'b01;
            end
            8'h42: begin
                fc_hz = 32'd183600;
                bandwidth_hz = 32'd60000;
                pulse_duration_us = 32'd8000;
                amplitude = 16'd1000;
                mode = 2'b10;
            end
            8'h44: begin
                fc_hz = 32'd408000;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd2000;
                amplitude = 16'd600;
                mode = 2'b00;
            end
            8'h45: begin
                fc_hz = 32'd306000;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd4000;
                amplitude = 16'd800;
                mode = 2'b01;
            end
            8'h46: begin
                fc_hz = 32'd183600;
                bandwidth_hz = 32'd60000;
                pulse_duration_us = 32'd8000;
                amplitude = 16'd1000;
                mode = 2'b10;
            end
            8'h48: begin
                fc_hz = 32'd408000;
                bandwidth_hz = 32'd64000;
                pulse_duration_us = 32'd2000;
                amplitude = 16'd600;
                mode = 2'b00;
            end
            8'h49: begin
                fc_hz = 32'd306000;
                bandwidth_hz = 32'd64000;
                pulse_duration_us = 32'd4000;
                amplitude = 16'd800;
                mode = 2'b01;
            end
            8'h4A: begin
                fc_hz = 32'd183600;
                bandwidth_hz = 32'd48000;
                pulse_duration_us = 32'd8000;
                amplitude = 16'd1000;
                mode = 2'b10;
            end
            8'h50: begin
                fc_hz = 32'd400000;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd2000;
                amplitude = 16'd600;
                mode = 2'b00;
            end
            8'h51: begin
                fc_hz = 32'd300000;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd4000;
                amplitude = 16'd800;
                mode = 2'b01;
            end
            8'h52: begin
                fc_hz = 32'd180000;
                bandwidth_hz = 32'd60000;
                pulse_duration_us = 32'd8000;
                amplitude = 16'd1000;
                mode = 2'b10;
            end
            8'h54: begin
                fc_hz = 32'd400000;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd2000;
                amplitude = 16'd600;
                mode = 2'b00;
            end
            8'h55: begin
                fc_hz = 32'd300000;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd4000;
                amplitude = 16'd800;
                mode = 2'b01;
            end
            8'h56: begin
                fc_hz = 32'd180000;
                bandwidth_hz = 32'd60000;
                pulse_duration_us = 32'd8000;
                amplitude = 16'd1000;
                mode = 2'b10;
            end
            8'h58: begin
                fc_hz = 32'd400000;
                bandwidth_hz = 32'd64000;
                pulse_duration_us = 32'd2000;
                amplitude = 16'd600;
                mode = 2'b00;
            end
            8'h59: begin
                fc_hz = 32'd300000;
                bandwidth_hz = 32'd64000;
                pulse_duration_us = 32'd4000;
                amplitude = 16'd800;
                mode = 2'b01;
            end
            8'h5A: begin
                fc_hz = 32'd180000;
                bandwidth_hz = 32'd48000;
                pulse_duration_us = 32'd8000;
                amplitude = 16'd1000;
                mode = 2'b10;
            end
            8'h60: begin
                fc_hz = 32'd392000;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd2000;
                amplitude = 16'd600;
                mode = 2'b00;
            end
            8'h61: begin
                fc_hz = 32'd294000;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd4000;
                amplitude = 16'd800;
                mode = 2'b01;
            end
            8'h62: begin
                fc_hz = 32'd176400;
                bandwidth_hz = 32'd60000;
                pulse_duration_us = 32'd8000;
                amplitude = 16'd1000;
                mode = 2'b10;
            end
            8'h64: begin
                fc_hz = 32'd392000;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd2000;
                amplitude = 16'd600;
                mode = 2'b00;
            end
            8'h65: begin
                fc_hz = 32'd294000;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd4000;
                amplitude = 16'd800;
                mode = 2'b01;
            end
            8'h66: begin
                fc_hz = 32'd176400;
                bandwidth_hz = 32'd60000;
                pulse_duration_us = 32'd8000;
                amplitude = 16'd1000;
                mode = 2'b10;
            end
            8'h68: begin
                fc_hz = 32'd392000;
                bandwidth_hz = 32'd64000;
                pulse_duration_us = 32'd2000;
                amplitude = 16'd600;
                mode = 2'b00;
            end
            8'h69: begin
                fc_hz = 32'd294000;
                bandwidth_hz = 32'd64000;
                pulse_duration_us = 32'd4000;
                amplitude = 16'd800;
                mode = 2'b01;
            end
            8'h6A: begin
                fc_hz = 32'd176400;
                bandwidth_hz = 32'd48000;
                pulse_duration_us = 32'd8000;
                amplitude = 16'd1000;
                mode = 2'b10;
            end
            8'h80: begin
                fc_hz = 32'd387600;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd2000;
                amplitude = 16'd600;
                mode = 2'b00;
            end
            8'h81: begin
                fc_hz = 32'd290700;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd4000;
                amplitude = 16'd800;
                mode = 2'b01;
            end
            8'h82: begin
                fc_hz = 32'd174420;
                bandwidth_hz = 32'd60000;
                pulse_duration_us = 32'd8000;
                amplitude = 16'd1000;
                mode = 2'b10;
            end
            8'h84: begin
                fc_hz = 32'd387600;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd2000;
                amplitude = 16'd600;
                mode = 2'b00;
            end
            8'h85: begin
                fc_hz = 32'd290700;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd4000;
                amplitude = 16'd800;
                mode = 2'b01;
            end
            8'h86: begin
                fc_hz = 32'd174420;
                bandwidth_hz = 32'd60000;
                pulse_duration_us = 32'd8000;
                amplitude = 16'd1000;
                mode = 2'b10;
            end
            8'h88: begin
                fc_hz = 32'd387600;
                bandwidth_hz = 32'd64000;
                pulse_duration_us = 32'd2000;
                amplitude = 16'd600;
                mode = 2'b00;
            end
            8'h89: begin
                fc_hz = 32'd290700;
                bandwidth_hz = 32'd64000;
                pulse_duration_us = 32'd4000;
                amplitude = 16'd800;
                mode = 2'b01;
            end
            8'h8A: begin
                fc_hz = 32'd174420;
                bandwidth_hz = 32'd48000;
                pulse_duration_us = 32'd8000;
                amplitude = 16'd1000;
                mode = 2'b10;
            end
            8'h90: begin
                fc_hz = 32'd380000;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd2000;
                amplitude = 16'd600;
                mode = 2'b00;
            end
            8'h91: begin
                fc_hz = 32'd285000;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd4000;
                amplitude = 16'd800;
                mode = 2'b01;
            end
            8'h92: begin
                fc_hz = 32'd171000;
                bandwidth_hz = 32'd60000;
                pulse_duration_us = 32'd8000;
                amplitude = 16'd1000;
                mode = 2'b10;
            end
            8'h94: begin
                fc_hz = 32'd380000;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd2000;
                amplitude = 16'd600;
                mode = 2'b00;
            end
            8'h95: begin
                fc_hz = 32'd285000;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd4000;
                amplitude = 16'd800;
                mode = 2'b01;
            end
            8'h96: begin
                fc_hz = 32'd171000;
                bandwidth_hz = 32'd60000;
                pulse_duration_us = 32'd8000;
                amplitude = 16'd1000;
                mode = 2'b10;
            end
            8'h98: begin
                fc_hz = 32'd380000;
                bandwidth_hz = 32'd64000;
                pulse_duration_us = 32'd2000;
                amplitude = 16'd600;
                mode = 2'b00;
            end
            8'h99: begin
                fc_hz = 32'd285000;
                bandwidth_hz = 32'd64000;
                pulse_duration_us = 32'd4000;
                amplitude = 16'd800;
                mode = 2'b01;
            end
            8'h9A: begin
                fc_hz = 32'd171000;
                bandwidth_hz = 32'd48000;
                pulse_duration_us = 32'd8000;
                amplitude = 16'd1000;
                mode = 2'b10;
            end
            8'hA0: begin
                fc_hz = 32'd372400;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd2000;
                amplitude = 16'd600;
                mode = 2'b00;
            end
            8'hA1: begin
                fc_hz = 32'd279300;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd4000;
                amplitude = 16'd800;
                mode = 2'b01;
            end
            8'hA2: begin
                fc_hz = 32'd167580;
                bandwidth_hz = 32'd60000;
                pulse_duration_us = 32'd8000;
                amplitude = 16'd1000;
                mode = 2'b10;
            end
            8'hA4: begin
                fc_hz = 32'd372400;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd2000;
                amplitude = 16'd600;
                mode = 2'b00;
            end
            8'hA5: begin
                fc_hz = 32'd279300;
                bandwidth_hz = 32'd80000;
                pulse_duration_us = 32'd4000;
                amplitude = 16'd800;
                mode = 2'b01;
            end
            8'hA6: begin
                fc_hz = 32'd167580;
                bandwidth_hz = 32'd60000;
                pulse_duration_us = 32'd8000;
                amplitude = 16'd1000;
                mode = 2'b10;
            end
            8'hA8: begin
                fc_hz = 32'd372400;
                bandwidth_hz = 32'd64000;
                pulse_duration_us = 32'd2000;
                amplitude = 16'd600;
                mode = 2'b00;
            end
            8'hA9: begin
                fc_hz = 32'd279300;
                bandwidth_hz = 32'd64000;
                pulse_duration_us = 32'd4000;
                amplitude = 16'd800;
                mode = 2'b01;
            end
            8'hAA: begin
                fc_hz = 32'd167580;
                bandwidth_hz = 32'd48000;
                pulse_duration_us = 32'd8000;
                amplitude = 16'd1000;
                mode = 2'b10;
            end
            default: begin end
        endcase
    end
endmodule

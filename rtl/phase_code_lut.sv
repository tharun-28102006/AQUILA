module phase_code_lut (

    input  logic [2:0] address,

    output logic       phase_bit

);

    always_comb begin

        case (address)

            3'd0: phase_bit = 1'b1;
            3'd1: phase_bit = 1'b1;
            3'd2: phase_bit = 1'b1;
            3'd3: phase_bit = 1'b0;
            3'd4: phase_bit = 1'b0;
            3'd5: phase_bit = 1'b1;
            3'd6: phase_bit = 1'b0;
            3'd7: phase_bit = 1'b1;

            default:
                phase_bit = 1'b1;

        endcase

    end

endmodule
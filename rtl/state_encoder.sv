
module state_encoder (

    input logic [1:0] temperature_state,
    input logic [1:0] salinity_state,
    input logic [1:0] turbidity_state,
    input logic [1:0] range_state,

    output logic [7:0] lut_address

);

    always @(*) begin

        lut_address = {
            temperature_state,
            salinity_state,
            turbidity_state,
            range_state
        };

    end

endmodule
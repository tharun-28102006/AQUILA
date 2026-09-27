
module sensor_classifier (

    input  logic [11:0] temperature,
    input  logic [11:0] salinity,
    input  logic [11:0] turbidity,
    input  logic [11:0] range,

    output logic [1:0] temperature_state,
    output logic [1:0] salinity_state,
    output logic [1:0] turbidity_state,
    output logic [1:0] range_state

);


    localparam logic [11:0] TEMP_LOW  = 12'd20;
    localparam logic [11:0] TEMP_HIGH = 12'd30;

    localparam logic [11:0] SAL_LOW   = 12'd300;
    localparam logic [11:0] SAL_HIGH  = 12'd600;

    localparam logic [11:0] TURB_LOW  = 12'd20;
    localparam logic [11:0] TURB_HIGH = 12'd100;

    localparam logic [11:0] RANGE_NEAR = 12'd1;
    localparam logic [11:0] RANGE_FAR  = 12'd3;



    always_comb begin

        if (temperature < TEMP_LOW)
            temperature_state = 2'b00;       // LOW

        else if (temperature <= TEMP_HIGH)
            temperature_state = 2'b01;       // MEDIUM

        else
            temperature_state = 2'b10;       // HIGH

    end



    always_comb begin

        if (salinity < SAL_LOW)
            salinity_state = 2'b00;          // LOW

        else if (salinity <= SAL_HIGH)
            salinity_state = 2'b01;          // MEDIUM

        else
            salinity_state = 2'b10;          // HIGH

    end



    always_comb begin

        if (turbidity < TURB_LOW)
            turbidity_state = 2'b00;         // LOW

        else if (turbidity <= TURB_HIGH)
            turbidity_state = 2'b01;         // MEDIUM

        else
            turbidity_state = 2'b10;         // HIGH

    end



    always_comb begin

        if (range < RANGE_NEAR)
            range_state = 2'b00;             // NEAR / LOW

        else if (range <= RANGE_FAR)
            range_state = 2'b01;             // MEDIUM

        else
            range_state = 2'b10;             // FAR / HIGH

    end

endmodule

module aquila_top (

    input  logic [11:0] temperature,
    input  logic [11:0] salinity,
    input  logic [11:0] turbidity,
    input  logic [11:0] range,

    output logic [1:0] temperature_state,
    output logic [1:0] salinity_state,
    output logic [1:0] turbidity_state,
    output logic [1:0] range_state,

    output logic [7:0] lut_address,

    output logic [31:0] fc,
    output logic [31:0] bandwidth,
    output logic [31:0] pulse_duration,
    output logic [15:0] amplitude,
    output logic [1:0] mode

);



    sensor_classifier classifier_inst (

        .temperature(temperature),
        .salinity(salinity),
        .turbidity(turbidity),
        .range(range),

        .temperature_state(temperature_state),
        .salinity_state(salinity_state),
        .turbidity_state(turbidity_state),
        .range_state(range_state)

    );



    state_encoder encoder_inst (

        .temperature_state(temperature_state),
        .salinity_state(salinity_state),
        .turbidity_state(turbidity_state),
        .range_state(range_state),

        .lut_address(lut_address)

    );



    adaptive_lut lut_inst (

        .address(lut_address),

        .fc_hz(fc),
        .bandwidth_hz(bandwidth),
        .pulse_duration_us(pulse_duration),
        .amplitude(amplitude),
        .mode(mode)

    );


endmodule
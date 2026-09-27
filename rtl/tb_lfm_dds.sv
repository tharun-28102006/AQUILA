`timescale 1us/1ns

module tb_lfm_dds;

    reg clk;
    reg reset;
    reg enable;

    reg [31:0] fc_hz;
    reg [31:0] bandwidth_hz;
    reg [31:0] pulse_duration_us;

    wire [31:0] phase;
    wire [31:0] current_frequency;


    lfm_dds #(
        .PHASE_BITS(32),
        .CLK_FREQ_HZ(2_000_000)
    )
    dut (
        .clk(clk),
        .reset(reset),
        .enable(enable),

        .fc_hz(fc_hz),
        .bandwidth_hz(bandwidth_hz),
        .pulse_duration_us(pulse_duration_us),

        .phase(phase),
        .current_frequency(current_frequency)
    );



    always #0.25 clk = ~clk;


    integer i;


    initial begin

        clk = 0;

        reset = 1;

        enable = 0;



        fc_hz = 200000;

        bandwidth_hz = 70000;

        pulse_duration_us = 4000;


        $display("");
        $display("==============================================");
        $display("             AQUILA LFM DDS TEST");
        $display("==============================================");

        $display("");
        $display("Fc  = %0d Hz", fc_hz);
        $display("BW  = %0d Hz", bandwidth_hz);
        $display("Tp  = %0d us", pulse_duration_us);

        $display("");
        $display("Expected Start Frequency = 165000 Hz");
        $display("Expected End Frequency   = 235000 Hz");


        #2;

        reset = 0;

        enable = 1;



        for (i = 0; i < 10; i = i + 1) begin

            @(posedge clk);

            #0.01;

            $display(
                "Sample=%0d | Frequency=%0d Hz | Phase=%0d",
                dut.sample_count,
                current_frequency,
                phase
            );

        end


        #1000;


        $display("");
        $display(
            "MID CHIRP | Sample=%0d | Frequency=%0d Hz",
            dut.sample_count,
            current_frequency
        );


        #1000;


        enable = 0;


        $display("");
        $display(
            "END REGION | Sample=%0d | Frequency=%0d Hz",
            dut.sample_count,
            current_frequency
        );


        $display("");
        $display("LFM DDS TEST COMPLETE");
        $display("==============================================");

        $finish;

    end

endmodule
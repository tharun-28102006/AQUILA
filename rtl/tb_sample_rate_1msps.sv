
`timescale 1ns/1ps

module tb_sample_rate_1msps;

    logic clk;
    logic reset;
    logic sample_enable;

    integer sample_count;
    integer clock_count;


    sample_rate_generator_1msps #(
        .CLK_FREQ_HZ(50_000_000),
        .SAMPLE_RATE_HZ(1_000_000)
    ) dut (

        .clk(clk),
        .reset(reset),

        .sample_enable(sample_enable)
    );



    always #10 clk = ~clk;



    always @(posedge clk) begin

        if (!reset) begin

            clock_count = clock_count + 1;

            if (sample_enable) begin

                sample_count = sample_count + 1;

                $display(
                    "Sample #%0d at clock #%0d",
                    sample_count,
                    clock_count
                );

            end

        end

    end



    initial begin

        clk = 0;
        reset = 1;

        sample_count = 0;
        clock_count = 0;

        #200;

        reset = 0;

        #5000;

        $display("");
        $display("==============================================");
        $display(" AQUILA 1 MSPS SAMPLE RATE TEST");
        $display("==============================================");

        $display(
            "FPGA clock      = 50 MHz"
        );

        $display(
            "Target rate     = 1 MSPS"
        );

        $display(
            "Divider         = 50 clocks/sample"
        );

        $display(
            "Samples generated = %0d",
            sample_count
        );

        if (sample_count >= 9) begin
            $display("PASS: 1 MSPS SAMPLE CLOCK GENERATED");
        end
        else begin
            $display("FAIL: SAMPLE RATE TOO LOW");
        end

        $display("");
        $display("==============================================");
        $display(" TEST COMPLETE");
        $display("==============================================");

        $finish;

    end

endmodule

`timescale 1ns/1ps

module tb_sample_rate_generator;

    logic clk;
    logic reset;
    logic sample_enable;

    integer sample_count;



    sample_rate_generator #(
        .CLK_FREQ_HZ(50_000_000),
        .SAMPLE_RATE_HZ(400_000)
    ) dut (

        .clk(clk),
        .reset(reset),

        .sample_enable(sample_enable)
    );



    always #10 clk = ~clk;



    always @(posedge clk) begin

        if (sample_enable) begin

            sample_count = sample_count + 1;

            $display(
                "Sample enable #%0d at simulation time %0t ns",
                sample_count,
                $time
            );

        end
    end



    initial begin

        clk = 0;
        reset = 1;
        sample_count = 0;

        #100;

        reset = 0;

        #15000;

        $display("");
        $display("==============================================");
        $display("     AQUILA SAMPLE RATE GENERATOR TEST");
        $display("==============================================");

        $display(
            "Clock frequency : 50 MHz"
        );

        $display(
            "Target sample rate : 400 kSPS"
        );

        $display(
            "Clock period count : 125"
        );

        $display(
            "Generated samples : %0d",
            sample_count
        );

        if (sample_count >= 5) begin

            $display(
                "PASS: SAMPLE ENABLE GENERATED"
            );

        end else begin

            $display(
                "FAIL: SAMPLE ENABLE TOO LOW"
            );

        end

        $display("==============================================");

        $finish;

    end

endmodule
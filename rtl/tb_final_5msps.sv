`timescale 1ns/1ps

module tb_final_5msps;
    logic clk;
    logic reset;
    logic sample_enable;
    integer enable_count;
    time previous_enable;
    time interval;

    sample_rate_generator #(
        .CLK_FREQ_HZ(50_000_000),
        .SAMPLE_RATE_HZ(5_000_000)
    ) dut (
        .clk(clk),
        .reset(reset),
        .sample_enable(sample_enable)
    );

    always #10 clk = ~clk;

    always @(posedge clk) begin
        if (sample_enable) begin
            if (enable_count > 0) begin
                interval = $time - previous_enable;
                if (interval != 200)
                    $fatal(1, "Expected 200 ns sample interval, got %0t ns", interval);
            end
            previous_enable = $time;
            enable_count = enable_count + 1;
        end
    end

    initial begin
        clk = 0;
        reset = 1;
        enable_count = 0;
        previous_enable = 0;
        #100;
        reset = 0;
        #1200;
        if (enable_count < 5)
            $fatal(1, "Expected at least five sample enables, got %0d", enable_count);
        $display("PASS: 5 MSPS sample enable, %0d events", enable_count);
        $finish;
    end
endmodule

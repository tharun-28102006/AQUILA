
`timescale 1ns/1ps

module tb_ad3541r_continuous_stream;

    logic clk;
    logic reset;

    logic stream_enable;

    logic [15:0] dac_sample;
    logic sample_valid;

    logic cs_n;
    logic sclk;

    logic sdio0;
    logic sdio1;

    logic busy;
    logic sample_done;

    integer completed_samples;
    integer cs_rise_count;
    integer cs_fall_count;



    ad3541r_stream_engine #(
        .CLK_FREQ_HZ(50_000_000),
        .SPI_FREQ_HZ(10_000_000)
    ) dut (

        .clk(clk),
        .reset(reset),

        .stream_enable(stream_enable),

        .dac_sample(dac_sample),
        .sample_valid(sample_valid),

        .cs_n(cs_n),
        .sclk(sclk),

        .sdio0(sdio0),
        .sdio1(sdio1),

        .busy(busy),
        .sample_done(sample_done)
    );



    always #10 clk = ~clk;



    always @(posedge sample_done) begin

        completed_samples = completed_samples + 1;

        $display(
            "STREAM SAMPLE COMPLETE #%0d",
            completed_samples
        );

    end



    always @(negedge cs_n) begin

        cs_fall_count = cs_fall_count + 1;

        $display("CS LOW");

    end


    always @(posedge cs_n) begin

        cs_rise_count = cs_rise_count + 1;

        $display("CS HIGH");

    end



    initial begin

        clk = 0;
        reset = 1;

        stream_enable = 0;
        sample_valid = 0;

        dac_sample = 16'h0000;

        completed_samples = 0;
        cs_rise_count = 0;
        cs_fall_count = 0;



        #200;

        reset = 0;

        #200;



        stream_enable = 1;



        dac_sample = 16'h1000;

        @(posedge clk);
        sample_valid = 1;

        @(posedge clk);
        sample_valid = 0;



        wait(sample_done);



        dac_sample = 16'h2000;

        @(posedge clk);
        sample_valid = 1;

        @(posedge clk);
        sample_valid = 0;


        wait(sample_done);



        dac_sample = 16'h3000;

        @(posedge clk);
        sample_valid = 1;

        @(posedge clk);
        sample_valid = 0;


        wait(sample_done);



        dac_sample = 16'h4000;

        @(posedge clk);
        sample_valid = 1;

        @(posedge clk);
        sample_valid = 0;


        wait(sample_done);



        stream_enable = 0;

        #500;



        $display("");
        $display("==============================================");
        $display(" CONTINUOUS STREAM TEST");
        $display("==============================================");

        $display(
            "Samples completed = %0d",
            completed_samples
        );

        $display(
            "CS LOW events     = %0d",
            cs_fall_count
        );

        $display(
            "CS HIGH events    = %0d",
            cs_rise_count
        );



        if (completed_samples == 4) begin

            $display(
                "PASS: FOUR SAMPLES TRANSMITTED"
            );

        end
        else begin

            $display(
                "FAIL: SAMPLE COUNT INCORRECT"
            );

        end


        if (cs_fall_count == 1) begin

            $display(
                "PASS: SINGLE CONTINUOUS CS ASSERTION"
            );

        end
        else begin

            $display(
                "FAIL: CS WAS TOGGLED BETWEEN SAMPLES"
            );

        end


        $display("");
        $display("==============================================");
        $display(" TEST COMPLETE");
        $display("==============================================");

        $finish;

    end

endmodule
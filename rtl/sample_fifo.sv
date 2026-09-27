
module sample_fifo #(
    parameter integer DEPTH = 16
)(
    input  logic        clk,
    input  logic        reset,

    input  logic [15:0] write_data,
    input  logic        write_en,

    input  logic        read_en,
    output logic [15:0] read_data,

    output logic        full,
    output logic        empty,
    output logic [4:0]  count
);

    logic [15:0] memory [0:DEPTH-1];

    logic [4:0] write_ptr;
    logic [4:0] read_ptr;

    always_ff @(posedge clk) begin

        if (reset) begin

            write_ptr <= 5'd0;
            read_ptr  <= 5'd0;
            count     <= 5'd0;
            read_data <= 16'd0;

        end
        else begin

            if (write_en && !full) begin
                memory[write_ptr[3:0]] <= write_data;
                write_ptr <= write_ptr + 1'b1;
            end

            if (read_en && !empty) begin
                read_data <= memory[read_ptr[3:0]];
                read_ptr  <= read_ptr + 1'b1;
            end

            case ({write_en && !full, read_en && !empty})

                2'b10:
                    count <= count + 1'b1;

                2'b01:
                    count <= count - 1'b1;

                default:
                    count <= count;

            endcase

        end

    end

    always_comb begin
        full  = (count == DEPTH);
        empty = (count == 0);
    end

endmodule
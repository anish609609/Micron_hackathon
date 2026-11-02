module dram_model #(parameter LAT = 10) (
    input             clk,
    input             req,
    input      [31:0] addr,
    output reg        valid,
    output reg [127:0] data
);
    reg        busy = 0;
    integer    cnt  = 0;
    reg [31:0] base = 0;

    initial valid = 0;

    always @(posedge clk) begin
        valid <= 0;
        if (req && !busy) begin
            busy <= 1;
            cnt  <= LAT;
            base <= {addr[31:4], 4'b0000};
        end else if (busy) begin
            if (cnt <= 1) begin
                busy  <= 0;
                valid <= 1;
                // each 32-bit word holds its own byte address (easy to check)
                data  <= {base + 32'd12, base + 32'd8, base + 32'd4, base};
            end else
                cnt <= cnt - 1;
        end
    end
endmodule

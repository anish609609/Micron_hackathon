`timescale 1ns/1ps
module tb;
    parameter N        = 20000;
    parameter PF_EN    = 1;
    parameter CONF_MIN = 0;
    parameter LAT      = 10;

    reg clk = 0, rst_n = 0;
    always #5 clk = ~clk;

    reg [31:0] trace [0:N-1];
    reg        req_valid = 0;
    reg [31:0] req_addr  = 0;
    reg [31:0] cur       = 0;

    wire        resp_valid, done, dram_req, dram_valid;
    wire [31:0] rdata, dram_addr, hits, misses, pf_issued;
    wire [127:0] dram_data;

    cache_2way #(.PF_EN(PF_EN), .CONF_MIN(CONF_MIN)) dut (
        .clk(clk), .rst_n(rst_n),
        .req_valid(req_valid), .req_addr(req_addr),
        .resp_valid(resp_valid), .rdata(rdata), .done(done),
        .dram_req(dram_req), .dram_addr(dram_addr),
        .dram_valid(dram_valid), .dram_data(dram_data),
        .hits(hits), .misses(misses), .pf_issued(pf_issued));

    dram_model #(.LAT(LAT)) dram (
        .clk(clk), .req(dram_req), .addr(dram_addr),
        .valid(dram_valid), .data(dram_data));

    integer i;
    integer errors = 0;
    reg [8*64-1:0] fname;

    // every response must equal the word's own address
    always @(posedge clk)
        if (resp_valid && rdata !== (cur & 32'hFFFF_FFFC)) errors = errors + 1;

    initial begin
        if (!$value$plusargs("TRACE=%s", fname)) fname = "seq.hex";
        $readmemh(fname, trace);
        #25 rst_n = 1;
        @(posedge clk);
        for (i = 0; i < N; i = i + 1) begin
            req_addr <= trace[i]; cur <= trace[i]; req_valid <= 1;
            @(posedge clk);
            req_valid <= 0;
            @(posedge clk);
            while (!done) @(posedge clk);       // wait until request + prefetch finish
        end
        $display("trace=%0s", fname);
        $display("hits=%0d misses=%0d hit rate=%0f%% prefetches=%0d data errors=%0d",
                 hits, misses, 100.0*hits/N, pf_issued, errors);
        $finish;
    end
endmodule

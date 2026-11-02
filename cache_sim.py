LINE = 16  # bytes per cache line
SETS = 64     # number of slots

def load_trace(filename):
    addrs = []
    with open(filename) as f:
        for line in f:
            addrs.append(int(line.strip(), 16))
    return addrs

def simulate(addrs):
    tags = [None] * SETS          # tag stored in each slot; None = empty
    hits = 0
    misses = 0
    for addr in addrs:
        line_addr = addr // LINE      # which 16-byte chunk
        index = line_addr % SETS      # which slot it must go in
        tag = line_addr // SETS       # label for that chunk
        if tags[index] == tag:
            hits += 1                 # right chunk already in the slot
        else:
            misses += 1
            tags[index] = tag         # fetch from DRAM, store in the slot
    return hits, misses

for name in ["seq.txt", "stride.txt"]:
    addrs = load_trace(name)
    hits, misses = simulate(addrs)
    print(f"{name}: hits={hits} misses={misses} hit rate={100*hits/len(addrs):.2f}%")

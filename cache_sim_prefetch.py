LINE = 16     # bytes per cache line
SETS = 64     # number of slots

def load_trace(filename):
    addrs = []
    with open(filename) as f:
        for line in f:
            addrs.append(int(line.strip(), 16))
    return addrs

def simulate(addrs, mode):
    tags = [None] * SETS
    hits = 0
    misses = 0
    prev_addr = None                       # remembered for the stride prefetcher

    for addr in addrs:
        line_addr = addr // LINE
        index = line_addr % SETS
        tag = line_addr // SETS

        # normal cache lookup
        if tags[index] == tag:
            hits += 1
        else:
            misses += 1
            tags[index] = tag

        # prefetch engine: decide which address to fetch early
        pf_addr = None

        if mode == "nextline":
            pf_addr = (line_addr + 1) * LINE        # start of the next block

        elif mode == "stride":
            if prev_addr is not None:
                delta = addr - prev_addr            # gap since the last read
                pf_addr = addr + delta              # guess: same gap again

        # copy the guessed block into the cache
        if pf_addr is not None and pf_addr >= 0:
            pf_line = pf_addr // LINE
            tags[pf_line % SETS] = pf_line // SETS

        prev_addr = addr                            # remember for next time

    return hits, misses

for name in ["seq.txt", "stride.txt", "reuse.txt", "random.txt"]:
    addrs = load_trace(name)
    for mode in ["none", "nextline", "stride"]:
        hits, misses = simulate(addrs, mode)
        print(f"{name:11} {mode:9} hits={hits:5} misses={misses:5} "
              f"hit rate={100*hits/len(addrs):.2f}%")

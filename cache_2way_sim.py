LINE = 16     # bytes per cache line
SETS = 32     # number of sets
WAYS = 2      # lines per set  (32 x 2 = 64 lines = 1 KB)

def load_trace(filename):
    addrs = []
    with open(filename) as f:
        for line in f:
            addrs.append(int(line.strip(), 16))
    return addrs

def simulate(addrs):
    cache = [[] for _ in range(SETS)]   # each set is a list of up to 2 tags
    hits = 0
    misses = 0

    for addr in addrs:
        line_addr = addr // LINE        # which 16-byte block
        index = line_addr % SETS        # which set
        tag = line_addr // SETS         # label for that block
        s = cache[index]

        if tag in s:
            hits += 1
            s.remove(tag)
            s.append(tag)               # now the most recently used
        else:
            misses += 1
            if len(s) == WAYS:
                s.pop(0)                # set full: evict the least recently used
            s.append(tag)

    return hits, misses

for name in ["seq.txt", "stride.txt", "reuse.txt", "random.txt"]:
    addrs = load_trace(name)
    hits, misses = simulate(addrs)
    print(f"{name}: hits={hits} misses={misses} hit rate={100*hits/len(addrs):.2f}%")

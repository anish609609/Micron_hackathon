LINE = 16     # bytes per cache line
SETS = 32     # number of sets
WAYS = 2      # lines per set  (32 x 2 = 64 lines = 1 KB)

def load_trace(filename):
    addrs = []
    with open(filename) as f:
        for line in f:
            addrs.append(int(line.strip(), 16))
    return addrs

def insert(cache, line_addr):
    # put a block into the cache; if the set is full, evict the LRU one
    index = line_addr % SETS
    tag = line_addr // SETS
    s = cache[index]
    if len(s) == WAYS:
        s.pop(0)               # front = least recently used
    s.append(tag)              # back = most recently used

def simulate(addrs, mode):
    cache = [[] for _ in range(SETS)]    # each set is a list of up to 2 tags
    hits = 0
    misses = 0
    prev_addr = None

    for addr in addrs:
        line_addr = addr // LINE
        index = line_addr % SETS
        tag = line_addr // SETS
        s = cache[index]

        # normal cache lookup
        if tag in s:
            hits += 1
            s.remove(tag)
            s.append(tag)              # now the most recently used
        else:
            misses += 1
            insert(cache, line_addr)

        # prefetch engine: decide which address to fetch early
        pf_addr = None
        if mode == "nextline":
            pf_addr = (line_addr + 1) * LINE
        elif mode == "stride":
            if prev_addr is not None:
                pf_addr = addr + (addr - prev_addr)

        if pf_addr is not None and pf_addr >= 0:
            pf_line = pf_addr // LINE
            pf_tag = pf_line // SETS
            if pf_tag not in cache[pf_line % SETS]:    # only fill if not there
                insert(cache, pf_line)

        prev_addr = addr

    return hits, misses

for name in ["seq.txt", "stride.txt", "reuse.txt", "random.txt"]:
    addrs = load_trace(name)
    for mode in ["none", "nextline", "stride"]:
        hits, misses = simulate(addrs, mode)
        print(f"{name:11} {mode:9} hits={hits:5} misses={misses:5} "
              f"hit rate={100*hits/len(addrs):.2f}%")

N = 20000  # how many addresses in each trace
import random
def gen_sequential(n):
    addrs = []                    # empty list to collect addresses
    for i in range(n):            # i goes 0, 1, 2, ... n-1
        addrs.append(i * 4)       # 4 bytes per item: 0, 4, 8, 12, ...
    return addrs

def gen_strided(n, stride):
    addrs = []
    for i in range(n):
        addrs.append(i * stride)  # jump `stride` bytes each time
    return addrs
    
def gen_reuse(n, region_words):
    # sweep the same small region again and again (weights reused across a batch)
    addrs = []
    for i in range(n):
        addrs.append((i % region_words) * 4)
    return addrs

def gen_random_hot(n, hot_count, hot_prob):
    # recommender-style: mostly random lookups, but some "hot" entries come up often
    random.seed(42)                       # same numbers every run
    hot = [random.randrange(0, 1 << 20, 4) for _ in range(hot_count)]
    addrs = []
    for i in range(n):
        if random.random() < hot_prob:
            addrs.append(random.choice(hot))                # a popular address
        else:
            addrs.append(random.randrange(0, 1 << 20, 4))   # any address
    return addrs

def save_trace(filename, addrs):
    with open(filename, "w") as f:        # open file for writing
        for a in addrs:
            f.write(f"{a:#08x}\n")        # hex like 0x000040, then newline

if __name__ == "__main__":
    save_trace("seq.txt", gen_sequential(N))
    save_trace("stride.txt", gen_strided(N, 64))
    save_trace("reuse.txt",  gen_reuse(N, 256))
    save_trace("random.txt", gen_random_hot(N, 64, 0.8))
    print("done")

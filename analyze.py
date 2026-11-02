from collections import Counter

def load_trace(filename):
    addrs = []
    with open(filename) as f:            # open for reading
        for line in f:
            addrs.append(int(line.strip(), 16))   # "0x000040" -> 64
    return addrs

def analyze(filename):
    addrs = load_trace(filename)
    deltas = []
    for i in range(len(addrs) - 1):
        deltas.append(addrs[i + 1] - addrs[i])    # gap to the next address

    print(filename)
    for delta, count in Counter(deltas).most_common(3):
        pct = 100 * count / len(deltas)
        print(f"  delta {delta:>8}  occurs {pct:6.2f}%")

for name in ["seq.txt", "stride.txt", "reuse.txt", "random.txt"]:
    analyze(name)

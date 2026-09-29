import heapq


class Node:
    def __init__(self, freq, symbol, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq


def build_tree(frequencies):
    # Greedy: repeatedly merge the two least-frequent nodes.
    heap = [Node(freq, sym) for sym, freq in frequencies.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        heapq.heappush(heap, Node(left.freq + right.freq, None, left, right))
    return heap[0]


def build_codes(node, prefix="", codes=None):
    if codes is None:
        codes = {}
    if node.symbol is not None:            # leaf
        codes[node.symbol] = prefix or "0"  # single-symbol text edge case
    else:
        build_codes(node.left, prefix + "0", codes)
        build_codes(node.right, prefix + "1", codes)
    return codes


def huffman(text):
    frequencies = {}
    for ch in text:
        frequencies[ch] = frequencies.get(ch, 0) + 1
    root = build_tree(frequencies)
    codes = build_codes(root)
    encoded = "".join(codes[ch] for ch in text)
    return frequencies, codes, encoded


if __name__ == "__main__":
    text = input("Enter text to compress: ")
    frequencies, codes, encoded = huffman(text)

    print("\nSymbol frequencies:")
    for sym, freq in sorted(frequencies.items(), key=lambda kv: -kv[1]):
        print(f"  {sym!r}: {freq}")

    print("\nHuffman codes:")
    for sym, code in sorted(codes.items(), key=lambda kv: len(kv[1])):
        print(f"  {sym!r}: {code}")

    fixed_bits = len(text) * 8
    huff_bits = len(encoded)
    print("\nEncoded string:", encoded)
    print(f"Fixed-length (8-bit) size: {fixed_bits} bits")
    print(f"Huffman size:             {huff_bits} bits")
    if fixed_bits:
        print(f"Compression ratio: {huff_bits / fixed_bits:.2%}")

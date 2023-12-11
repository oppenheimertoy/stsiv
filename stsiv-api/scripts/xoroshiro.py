import os

class Xoroshiro128Plus:
    def __init__(self, seed):
        self.state = [seed, ~seed]

    def rotl(self, x, k):
        return ((x << k) | (x >> (64 - k))) & ((1 << 64) - 1)

    def next(self):
        s0, s1 = self.state
        result = (s0 + s1) & ((1 << 64) - 1)

        s1 ^= s0
        self.state[0] = self.rotl(s0, 24) ^ s1 ^ ((s1 << 16) & ((1 << 64) - 1))
        self.state[1] = self.rotl(s1, 37)

        return result

    def random_bytes(self, num_bytes):
        bytes_generated = bytearray()
        for _ in range(num_bytes // 8):
            bytes_generated += self.next().to_bytes(8, 'little')
        return bytes_generated

def create_binary_file(filename, size_mb, seed):
    prng = Xoroshiro128Plus(seed)
    size_bytes = size_mb * 1024 * 1024

    with open(filename, 'wb') as file:
        while size_bytes > 0:
            chunk_size = min(size_bytes, 65536)  # 64 KB chunks
            file.write(prng.random_bytes(chunk_size))
            size_bytes -= chunk_size

if __name__ == "__main__":
    filename = "random_data.bin"
    file_size_mb = 200
    seed = 123456789  # You can choose any seed value

    create_binary_file(filename, file_size_mb, seed)
    print(f"Generated {file_size_mb}MB binary file '{filename}'")

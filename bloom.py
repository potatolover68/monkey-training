import io
from math import log
from typing import Callable

from bitarray import bitarray
from fnv_1a import fnv_1a_32, fnv_1a_64


class BloomFilter:
    """A probabilistic data structure for fast membership testing.

    Uses multiple hash functions to store items in a bit array, allowing for
    fast membership queries with some probability of false positives but no
    false negatives.
    """

    filter: bitarray
    k: int
    size: int
    hash_f: Callable
    hash_f2: Callable

    def __init__(
        self,
        size: int,
        hash_f: Callable[[str], int],
        hash_f2: Callable[[str], int],
        estimated_n: int | None = None,
        k: int | None = None,
    ):
        """initalizes a empty bloom filter

        Args:
            size (int): How large the bloom filter is, in bits
            hash_f (Callable[[str], int]): A hash function. Has to be distinct
                from `hash_f2`.
            hash_f2 (Callable[[str], int]): A hash function. Has to be distinct
                from `hash_f`.
            estimated_n (int | None, optional): An estimate for N, the number
                of
                elements expected in the bloom filter - used to calculate the
                optimal K.
            k (int | None, optional): The amount of hash functions to use for
                each string, using h1 + i * h2. If both `k` and `estimated_n`
                are unset defaults to `log2(size)`.
        """
        self.filter = bitarray("0" * size)
        self.hash_f = hash_f
        self.hash_f2 = hash_f2
        self.size = size
        if k is not None:
            self.k = k
        elif k is None and estimated_n is not None:
            self.k = int(size / estimated_n * 0.6931471805)
        else:
            self.k = int(log(size, 2))

    def ingest(self, file: io.BytesIO) -> None:
        self.filter.clear()
        self.filter.fromfile(file)

    def dump(self, file: io.BytesIO) -> None:
        self.filter.tofile(file)

    def add(self, string: str) -> None:
        h1 = self.hash_f(string)
        h2 = self.hash_f2(string)
        for i in range(self.k):
            self.filter[(h1 + i * h2) % self.size] = 1
            # print(self.hash_f(string * i) % self.size)

    def adds(self, *args) -> None:
        for i in args:
            self.add(i)

    def check(self, string: str) -> bool:
        h1 = self.hash_f(string)
        h2 = self.hash_f2(string)
        for i in range(self.k):
            if self.filter[(h1 + i * h2) % self.size] != 1:
                return False
        return True

    def confidence(self, string: str) -> float:
        """NOTE: THIS IS NOT A STANDARD BLOOM FILTER FUNCTION

        Args:
            string (str): Check if the string given is in the hash function

        Returns:
            float: 0-1, number of correct hashes/K
        """
        h1 = self.hash_f(string)
        h2 = self.hash_f2(string)
        c = 0
        for i in range(self.k):
            if self.filter[(h1 + i * h2) % self.size] == 1:
                c += 1
        return c / self.k


if __name__ == "__main__":
    bloom = BloomFilter(100000, fnv_1a_64, fnv_1a_32, k=8)
    bloom.adds("mustard", "ketchup", "skibidi")
    print(bloom.check("mustard"))
    print(bloom.check("kendrick lamar"))
    print(bloom.confidence("funny"))

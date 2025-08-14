from bitarray import bitarray
from fnv_1a import *
import io
from math import log, e, floor
from typing import Callable

class BloomFilter:
    filter: bitarray
    k: int
    size: int
    hashF: Callable
    hashF2: Callable
    
    def __init__(self, size: int, hashF: Callable[[str], int], hashF2: Callable[[str], int], estimated_n: int | None = None, k: int | None = None):
        """initalizes a empty bloom filter

        Args:
            size (int): How large the bloom filter is, in bits
            hashF (Callable[[str], int]): A hash function. Has to be distinct from `hashF2`.
            hashF2 (Callable[[str], int]): A hash function. Has to be distinct from `hashF`.
            estimated_n (int | None, optional): An estimate for N, the number of elements expected in the bloom filter - used to calculate the optimal K.
            k (int | None, optional): The amount of hash functions to use for each string, using h1 + i * h2. If both `k` and `estimated_n` are unset defaults to `log2(size)`.
        """
        self.filter = bitarray("0" * size)
        self.hashF = hashF
        self.hashF2 = hashF2
        self.size = size
        if(k != None):
            self.k = k
        elif(k == None and estimated_n != None):
            self.k = size / estimated_n * 0.6931471805
        else:
            self.k = log(size, 2)
        self.k = floor(self.k)
    def ingest(self, file: io.BytesIO) -> None:
        self.filter.clear()
        self.filter.fromfile(file)
    def dump(self, file: io.BytesIO) -> None:
        self.filter.tofile(file)
    def add(self, string: str) -> None:
        h1 = self.hashF(string)
        h2 = self.hashF2(string)
        for i in range(self.k):
            self.filter[(h1 + i * h2) % self.size] = 1
            # print(self.hashF(string * i) % self.size)
    def adds(self, *args) -> None:
        for i in args:
            self.add(i)
    def check(self, string: str) -> bool:
        h1 = self.hashF(string)
        h2 = self.hashF2(string)
        for i in range(self.k):
            if (self.filter[(h1 + i * h2) % self.size] != 1):
                return False
        return True       
    def confidence(self, string: str) -> float:
        """NOTE: THIS IS NOT A STANDARD BLOOM FILTER FUNCTION

        Args:
            string (str): Check if the string given is in the hash function

        Returns:
            float: 0-1, number of correct hashes/K
        """
        h1 = self.hashF(string)
        h2 = self.hashF2(string)
        c = 0
        for i in range(self.k):
            if (self.filter[(h1 + i * h2) % self.size] == 1):
                c += 1
        return c / self.k
    
if __name__ == "__main__":
    bloom = BloomFilter(100000, fnv_1a_64, fnv_1a_32, k=8)
    bloom.adds("mustard", "ketchup", "skibidi")
    print(bloom.check("mustard"))
    print(bloom.check("kendrick lamar"))
    print(bloom.confidence("funny"))
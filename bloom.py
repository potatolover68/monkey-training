from bitarray import bitarray
from fnv_1a import *
import io
class BloomFilter:
    filter: bitarray
    k: int
    size: int
    
    def __init__(self, size: int, hashF, hashF2, k):
        """initalizes a empty bloom filter
        """
        self.filter = bitarray("0" * size)
        self.hashF = hashF
        self.hashF2 = hashF2
        self.size = size
        self.k = k
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
    bloom = BloomFilter(100000, fnv_1a_64, fnv_1a_32, 8)
    bloom.adds("mustard", "ketchup", "skibidi")
    print(bloom.check("mustard"))
    print(bloom.check("kendrick lamar"))
    print(bloom.confidence("funny"))
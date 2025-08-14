from bloom import BloomFilter
from fnv_1a import *
import math

class Flower(BloomFilter):
    def __init__(self, string: str):
        """Creates a flower! (bloom filter with preset settings)

        Args:
            string (str): the path to the file you want to open
        """
        super().__init__(2 ** 22, fnv_1a_32, fnv_1a_64, k = 12)
        self.adds(open(string, "rb"))    

def flower_power(a: Flower | BloomFilter, b: list[str]) -> float:
    """Compares a bloom filter against a list of words using logarithmic confidence scaling
    
    Args:
        a (Flower | BloomFilter): The bloom filter to check against
        b (list[str]): List of words to test
        
    Returns:
        float: Average logarithmic confidence score where 1.0 is exponentially more valuable than 0.5
    """
    if not b:
        return 0
    confidence = 0
    for word in b:
        confidence += -math.log(1 - a.confidence(word) + 1e-10)
    return confidence / len(b)    
    

if __name__ == "__main__":
    petal = Flower()
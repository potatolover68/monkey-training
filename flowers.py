from bloom import BloomFilter
from fnv_1a import *
import math
import re

class Flower(BloomFilter):
    def __init__(self, string: str):
        """Creates a flower! (bloom filter with preset settings)

        Args:
            string (str): the path to the file you want to open
        """
        super().__init__(2 ** 22, fnv_1a_32, fnv_1a_64, k = 12)
        self.adds(*[i.strip() for i in open(string, "r").readlines()])    

def _flower_power_perword(a: Flower | BloomFilter, b: str) -> float:
    """Compares a bloom filter against a list of words using exponential confidence scaling
    
    Args:
        a (Flower | BloomFilter): The bloom filter to check against
        b (str): word to test
        
    Returns:
        float: Average exponential confidence score (0-1) where 1.0 is exponentially more valuable than 0.5
    """
    return a.confidence(b) ** 3

def flower_power(a: Flower | BloomFilter, words: list[str], divide = True) -> float:
    """Calculates the flower power of a list of words
    
    Args:
        a (Flower | BloomFilter): The bloom filter to check against
        words (list[str]): List of words to analyze
        
    Returns:
        float: Average exponential confidence score (0-1) where 1.0 is exponentially more valuable than 0.5
    """
    if not words:
        return 0.0
    return sum(_flower_power_perword(a, word) for word in words) / (len(words) if divide else 1)    
    
def most_flower(a: Flower | BloomFilter, sentences: list[str]) -> tuple[str, float]:
    """Finds the most french sentence from a list of sentences
    
    Args:
        a (Flower | BloomFilter): The bloom filter to check against  
        sentences (list[str]): List of sentences to analyze
        
    Returns:
        tuple[str, float]: The most french sentence and its score
    """
    if not sentences:
        return "", 0
    best_sentence = ""
    best_score = 0
    for sentence in sentences:
        words = re.sub(r"[^\w']+", " ", sentence).strip().lower().split()
        score = flower_power(a, words, divide=False)
        if score > best_score:
            print(f"New best sentence: {sentence} with score {score}")
            best_score = score
            best_sentence = sentence
    return best_sentence, best_score

if __name__ == "__main__":
    petal = Flower()
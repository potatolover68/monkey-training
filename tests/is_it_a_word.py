from bloom import BloomFilter
from fnv_1a import *

bloom = BloomFilter(2**22, fnv_1a_128, fnv_1a_256, k=12)
bloom.ingest(open("data/bloom", "rb"))
while True:
    word = input('Check if this is an english word: ').lower()
    print(f"Is this an english word? {bloom.check(word)}\n Confidence: {bloom.confidence(word)}")
from bloom import BloomFilter
from fnv_1a import *
from os import remove

corpus = open("data/words_alpha.txt").readlines()
print(f"corpus words: {len(corpus)}")
corpus = [i.strip() for i in corpus]
bloom = BloomFilter(2**22, fnv_1a_128, fnv_1a_256, 12)
bloom.adds(*corpus)

remove("data/bloom")
bloom.dump(open("data/bloom", "xb"))

bloom2 = BloomFilter(2**22, fnv_1a_128, fnv_1a_256, 12)
bloom2.ingest(open("data/bloom", "rb"))
print(bloom2.check("abdom"))
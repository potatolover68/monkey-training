from fnv_1a import *
from bloom import BloomFilter

bloom2 = BloomFilter(2**22, fnv_1a_128, fnv_1a_256, 12)
bloom2.ingest(open("data/bloom", "rb"))
print(bloom2.check("abdom"))
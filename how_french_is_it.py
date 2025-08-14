import flowers
import re
import time

start_eng = time.time()
eng = flowers.Flower("data/words_alpha.txt")
end_eng = time.time()
print(f"English bloom filter created in {end_eng - start_eng:.3f} seconds")

start_fr = time.time()
fr = flowers.Flower("data/francais.txt")
end_fr = time.time()
print(f"French bloom filter created in {end_fr - start_fr:.3f} seconds")


import flowers
import re
import time
from colorama import Fore, Style, init

# Initialize colorama
init()

print(f"\n{Fore.CYAN}Creating Bloom Filters...{Style.RESET_ALL}")
print("=" * 50)

start_eng = time.time()
eng = flowers.Flower("data/words_alpha.txt")
end_eng = time.time()
print(f"{Fore.GREEN}✓ English bloom filter created in {Fore.YELLOW}{end_eng - start_eng:.3f}{Fore.GREEN} seconds{Style.RESET_ALL}")

start_fr = time.time()
fr = flowers.Flower("data/francais.txt")
end_fr = time.time()
print(f"{Fore.GREEN}✓ French bloom filter created in {Fore.YELLOW}{end_fr - start_fr:.3f}{Fore.GREEN} seconds{Style.RESET_ALL}")
print("=" * 50)

# How french are TF2 Spy's voice lines?
spy_lines = open("data/tf2_spy_voicelines.txt", "r").readlines()
# Updated regex: keep words with apostrophes (e.g., "n't", "'s", "'re")
spy_lines = [re.sub(r"[^\w']+", " ", i).strip().lower() for i in spy_lines if i.strip()]

# remove single characters or empty strings
spy_words = [i for i in spy_lines if len(i) > 1]
# remove duplicates
spy_words = list(set(spy_lines))

# print(f"Spy lines: {spy_lines}")

most_french_sentence, score = flowers.most_flower(fr, spy_lines)
print(f"\n{Fore.CYAN}Analysis Results:{Style.RESET_ALL}")
print("=" * 50)
print(f"{Fore.MAGENTA}Most French Sentence:{Style.RESET_ALL} {most_french_sentence}")
print(f"{Fore.MAGENTA}Frenchness Score:{Style.RESET_ALL} {Fore.YELLOW}{score:.3f}{Style.RESET_ALL}")
print("=" * 50)
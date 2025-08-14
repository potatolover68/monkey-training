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
print(
    f"{Fore.GREEN}✓ English bloom filter created in {Fore.YELLOW}{end_eng - start_eng:.3f}{Fore.GREEN} seconds{Style.RESET_ALL}"
)

start_fr = time.time()
fr = flowers.Flower("data/francais.txt")
end_fr = time.time()
print(
    f"{Fore.GREEN}✓ French bloom filter created in {Fore.YELLOW}{end_fr - start_fr:.3f}{Fore.GREEN} seconds{Style.RESET_ALL}"
)
print("=" * 50)


def analyze_text(text_file: str, bloom_filter: flowers.Flower, language: str) -> None:
    """Analyze how much a text matches a given language's bloom filter"""
    print(f"\n{Fore.YELLOW}Analyzing {text_file.split('/')[-1]}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'-' * 40}{Style.RESET_ALL}")

    try:
        # Try UTF-8 first
        with open(text_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        # Fall back to latin-1 if UTF-8 fails
        with open(text_file, "r", encoding="latin-1") as f:
            lines = f.readlines()

    lines = [re.sub(r"[^\w']+", " ", i).strip().lower() for i in lines if i.strip()]

    # remove single characters or empty strings and duplicates
    lines = [i for i in lines if len(i) > 1]
    lines = list(set(lines))

    most_matching_sentence, score = flowers.most_flower(bloom_filter, lines)
    print(f"\n{Fore.CYAN}Analyzing {text_file} for {language}-ness...{Style.RESET_ALL}")
    print("=" * 50)
    print(
        f"{Fore.MAGENTA}Most {language} Sentence:{Style.RESET_ALL} {most_matching_sentence}"
    )
    print(
        f"{Fore.MAGENTA}{language} Score:{Style.RESET_ALL} {Fore.YELLOW}{score:.3f}{Style.RESET_ALL}"
    )
    print("=" * 50)


def analyze_text_with_score(
    text_file: str, bloom_filter: flowers.Flower
) -> tuple[str, float]:
    """Analyze text and return the best sentence and score without printing"""
    try:
        # Try UTF-8 first
        with open(text_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        # Fall back to latin-1 if UTF-8 fails
        with open(text_file, "r", encoding="latin-1") as f:
            lines = f.readlines()

    lines = [re.sub(r"[^\w']+", " ", i).strip().lower() for i in lines if i.strip()]
    lines = [i for i in lines if len(i) > 1]
    lines = list(set(lines))
    return flowers.most_flower(bloom_filter, lines)


# Analyze various texts and store results
texts = ["data/tf2_spy_voicelines.txt", "data/hamlet.txt", "data/romeo.txt"]
results = []

for text_file in texts:
    # Get short name for display
    display_name = (
        text_file.split("/")[-1].replace(".txt", "").replace("_", " ").title()
    )

    # Analyze for both languages
    fr_sentence, fr_score = analyze_text_with_score(text_file, fr)
    eng_sentence, eng_score = analyze_text_with_score(text_file, eng)

    # Store results
    results.append(
        {
            "name": display_name,
            "fr_score": fr_score,
            "eng_score": eng_score,
            "ratio": fr_score / eng_score if eng_score > 0 else float("inf"),
            "fr_sentence": fr_sentence,
            "eng_sentence": eng_sentence,
        }
    )

    # Print detailed analysis
    print(f"\n{Fore.CYAN}{'=' * 20} FRENCH ANALYSIS {'=' * 20}{Style.RESET_ALL}")
    analyze_text(text_file, fr, "French")
    print(f"\n{Fore.CYAN}{'=' * 20} ENGLISH ANALYSIS {'=' * 20}{Style.RESET_ALL}")
    analyze_text(text_file, eng, "English")
    print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")

# Print final overview
print(f"\n{Fore.CYAN}Final Analysis Overview{Style.RESET_ALL}")
print("=" * 50)

# Format and print results
for result in sorted(results, key=lambda x: x["ratio"], reverse=True):
    name_color = Fore.GREEN if result["fr_score"] > result["eng_score"] else Fore.RED
    print(f"\n{name_color}{result['name']}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}French Score: {result['fr_score']:.3f}")
    print(f"English Score: {result['eng_score']:.3f}")
    print(f"French/English Ratio: {result['ratio']:.3f}{Style.RESET_ALL}")
    print(
        f"\n{Fore.MAGENTA}Most French Sentence:{Style.RESET_ALL}\n  \"{result['fr_sentence']}\""
    )
    print(
        f"{Fore.MAGENTA}Most English Sentence:{Style.RESET_ALL}\n  \"{result['eng_sentence']}\""
    )
    print("-" * 30)

print("\n" + "=" * 50)
# Print conclusion about most French text
most_french = max(results, key=lambda x: x["ratio"])
print(f"\n{Fore.CYAN}Conclusion:{Style.RESET_ALL}")
print(
    f"The most French-like text is {Fore.GREEN}{most_french['name']}{Style.RESET_ALL}"
)
print(
    f"with a French/English ratio of {Fore.YELLOW}{most_french['ratio']:.3f}{Style.RESET_ALL}"
)
print("=" * 50)

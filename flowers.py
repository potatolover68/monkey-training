from bloom import BloomFilter
from fnv_1a import fnv_1a_32, fnv_1a_64
import re
from colorama import Fore, Style, init

# pylint: disable=line-too-long


def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))


# Initialize colorama
init()


class Flower(BloomFilter):
    def __init__(self, string: str):
        """Creates a flower! (bloom filter with preset settings)

        Args:
            string (str): the path to the file you want to open
        """
        super().__init__(2**22, fnv_1a_32, fnv_1a_64, k=12)
        self.adds(*[i.strip() for i in open(string, "r", encoding="utf-8").readlines()])


def _flower_power_perword(a: Flower | BloomFilter, b: str) -> float:
    """Compares a bloom filter against a list of words using exponential confidence scaling

    Args:
        a (Flower | BloomFilter): The bloom filter to check against
        b (str): word to test

    Returns:
        float: Average exponential confidence score (0-1) where 1.0 is exponentially more valuable than 0.5
    """
    return clamp(a.confidence(b) ** 3, 0, 1)


def _raw_flower_power_perword(a: Flower | BloomFilter, b: str) -> float:
    """Gets the raw confidence score for a single word

    Args:
        a (Flower | BloomFilter): The bloom filter to check against
        b (str): word to test

    Returns:
        float: Raw confidence score (0-1) representing matches/k
    """
    return a.confidence(b)


def analyze_word_scores(
    a: Flower | BloomFilter, words: list[str]
) -> dict[str, dict[str, float]]:
    """Analyzes individual words and returns both raw and exponential scores

    Args:
        a (Flower | BloomFilter): The bloom filter to check against
        words (list[str]): List of words to analyze

    Returns:
        dict[str, dict[str, float]]: Dictionary mapping words to their raw confidence
        and flower power scores
    """
    word_scores = {}
    for word in words:
        raw_score = _raw_flower_power_perword(a, word)
        flower_score = _flower_power_perword(a, word)
        word_scores[word] = {
            "raw_confidence": raw_score,
            "flower_power": flower_score,
            "matches": round(raw_score * a.k),  # Number of hash matches
        }
    return word_scores


def flower_power(a: Flower | BloomFilter, words: list[str], divide=True) -> float:
    """Calculates the flower power of a list of words

    Args:
        a (Flower | BloomFilter): The bloom filter to check against
        words (list[str]): List of words to analyze
        divide (bool): Whether to divide by number of words (average) or not (total)

    Returns:
        float: Average or total exponential confidence score (0-1) where 1.0 is exponentially more valuable than 0.5
    """
    if not words:
        return 0.0
    return sum(_flower_power_perword(a, word) for word in words) / (
        len(words) if divide else 1
    )


def flower_power_detailed(
    a: Flower | BloomFilter, words: list[str], divide=True
) -> dict:
    """Calculates the flower power of a list of words with detailed per-word analysis

    Args:
        a (Flower | BloomFilter): The bloom filter to check against
        words (list[str]): List of words to analyze
        divide (bool): Whether to divide by number of words (average) or not (total)

    Returns:
        dict: Contains 'total_score', 'average_score', 'raw_total', 'raw_average', and 'word_details'
    """
    if not words:
        return {
            "total_score": 0.0,
            "average_score": 0.0,
            "raw_total": 0.0,
            "raw_average": 0.0,
            "word_details": {},
        }

    word_details = analyze_word_scores(a, words)
    total_flower_power = sum(
        details["flower_power"] for details in word_details.values()
    )
    total_raw = sum(details["raw_confidence"] for details in word_details.values())

    return {
        "total_score": total_flower_power,
        "average_score": total_flower_power / len(words),
        "raw_total": total_raw,
        "raw_average": total_raw / len(words),
        "word_details": word_details,
        "final_score": total_flower_power / (len(words) if divide else 1),
    }


def most_flower(a: Flower | BloomFilter, sentences: list[str]) -> tuple[str, float]:
    """Finds the most french sentence from a list of sentences

    Args:
        a (Flower | BloomFilter): The bloom filter to check against
        sentences (list[str]): List of sentences to analyze

    Returns:
        tuple[str, float]: The most french sentence and its score
    """
    if not sentences:
        return "", 0.0
    best_sentence = ""
    best_score = 0.0
    for sentence in sentences:
        words = re.sub(r"[^\w']+", " ", sentence).strip().lower().split()
        score = flower_power(a, words, divide=False)
        if score > best_score:
            print(f"{Fore.CYAN}New best sentence found!{Style.RESET_ALL}")
            print(f"{Fore.GREEN}→ {sentence}")
            print(f"{Fore.YELLOW}Score: {score:.3f}{Style.RESET_ALL}")
            best_score = score
            best_sentence = sentence
    return best_sentence, best_score


def most_flower_detailed(
    a: Flower | BloomFilter, sentences: list[str]
) -> tuple[str, dict]:
    """Finds the most french sentence with detailed word-by-word analysis

    Args:
        a (Flower | BloomFilter): The bloom filter to check against
        sentences (list[str]): List of sentences to analyze

    Returns:
        tuple[str, dict]: The most french sentence and its detailed analysis
    """
    if not sentences:
        return "", {}

    best_sentence = ""
    best_analysis = {}
    best_score = 0.0

    for sentence in sentences:
        words = re.sub(r"[^\w']+", " ", sentence).strip().lower().split()
        analysis = flower_power_detailed(a, words, divide=False)

        if analysis["final_score"] > best_score:
            print(f"{Fore.CYAN}New best sentence found!{Style.RESET_ALL}")
            print(f"{Fore.GREEN}→ {sentence}")
            print(
                f"{Fore.YELLOW}Total Score: {analysis['final_score']:.3f}{Style.RESET_ALL}"
            )
            print(
                f"{Fore.MAGENTA}Raw Average: {analysis['raw_average']:.3f}{Style.RESET_ALL}"
            )
            print(f"{Fore.BLUE}Word details:{Style.RESET_ALL}")
            for detail_word, details in list(analysis["word_details"].items())[
                :5
            ]:  # Show first 5 words
                print(
                    f"  {detail_word}: raw={details['raw_confidence']:.3f}, flower={details['flower_power']:.3f}"
                )
            if len(analysis["word_details"]) > 5:
                print(f"  ... and {len(analysis['word_details']) - 5} more words")

            best_score = analysis["final_score"]
            best_sentence = sentence
            best_analysis = analysis

    return best_sentence, best_analysis


if __name__ == "__main__":
    # Example usage of the new detailed analysis functions
    try:
        petal = Flower("data/words_alpha.txt")

        # Test words
        test_words = ["hello", "world", "python", "code", "asdfghjkl"]

        print(f"{Fore.CYAN}=== Individual Word Analysis ==={Style.RESET_ALL}")
        individual_scores = analyze_word_scores(petal, test_words)
        for test_word, scores in individual_scores.items():
            print(
                f"{Fore.GREEN}{test_word}:{Style.RESET_ALL} "
                f"raw={scores['raw_confidence']:.3f}, "
                f"flower={scores['flower_power']:.3f}, "
                f"matches={scores['matches']}/{petal.k}"
            )

        print(f"\n{Fore.CYAN}=== Detailed Flower Power Analysis ==={Style.RESET_ALL}")
        detailed = flower_power_detailed(petal, test_words)
        print(f"Total Score: {detailed['total_score']:.3f}")
        print(f"Average Score: {detailed['average_score']:.3f}")
        print(f"Raw Total: {detailed['raw_total']:.3f}")
        print(f"Raw Average: {detailed['raw_average']:.3f}")

    except FileNotFoundError:
        print(
            f"{Fore.RED}Error: data/words_alpha.txt not found. Please provide a valid word file.{Style.RESET_ALL}"
        )

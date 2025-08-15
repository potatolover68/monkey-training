import flowers
import re
import time
from colorama import Fore, Style, init
from spy_analysis import SpyLinguisticAnalyzer

# pylint: disable=line-too-long

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
texts = [
    "data/tf2_spy_voicelines.txt",
    "data/hamlet.txt",
    "data/romeo.txt",
    "data/jeeves.txt",
]
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
    name_color = (
        Fore.GREEN
        if float(result["fr_score"]) > float(result["eng_score"])
        else Fore.RED
    )
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

# ============================================================================
# COMPREHENSIVE ANALYSIS OF ALL TEXTS FOR PRESENTATION
# ============================================================================

print(f"\n{Fore.CYAN}Starting Comprehensive Analysis of All Texts...{Style.RESET_ALL}")
print("=" * 80)

# Initialize the advanced analyzer
spy_analyzer = SpyLinguisticAnalyzer(fr, eng)

# Analyze each text individually
all_text_analyses = {}
text_mapping = {
    "data/tf2_spy_voicelines.txt": {"name": "TF2 Spy", "short": "spy"},
    "data/hamlet.txt": {"name": "Hamlet", "short": "hamlet"},
    "data/romeo.txt": {"name": "Romeo & Juliet", "short": "romeo"},
    "data/jeeves.txt": {"name": "Jeeves & Wooster", "short": "jeeves"},
}

print(f"\n{Fore.YELLOW}📚 INDIVIDUAL TEXT ANALYSES{Style.RESET_ALL}")
print("=" * 60)

for text_file, info in text_mapping.items():
    print(f"\n{Fore.CYAN}Analyzing {info['name']}...{Style.RESET_ALL}")

    # Perform comprehensive analysis
    text_stats = spy_analyzer.analyze_voicelines(text_file)
    text_scores = spy_analyzer.calculate_language_scores(text_file)

    # Store results
    all_text_analyses[info["short"]] = {
        "name": info["name"],
        "file": text_file,
        "stats": text_stats,
        "scores": text_scores,
    }

    # Print summary for each
    print(f"  • Total lines: {text_stats['total_voicelines']:,}")
    print(f"  • Total words: {text_stats['total_words']:,}")
    print(f"  • Vocabulary richness: {text_stats['vocabulary_richness']:.2%}")
    print(f"  • French score: {text_scores['french_score']:.3f}")
    print(f"  • English score: {text_scores['english_score']:.3f}")
    print(f"  • French/English ratio: {text_scores['french_ratio']:.3f}")
    print(f"  • Language bias: {text_scores['language_bias']}")
    print(f"  • French expressions: {text_stats['total_french_expressions']}")
    print(f"  • Exclamatory %: {text_stats['exclamatory_percentage']:.1f}%")

# ============================================================================
# COMPREHENSIVE COMPARATIVE ANALYSIS
# ============================================================================

print(f"\n{Fore.YELLOW}📊 COMPREHENSIVE COMPARATIVE ANALYSIS{Style.RESET_ALL}")
print("=" * 60)

# Create comparison data structures
comparison_data = []
for short_name, data in all_text_analyses.items():
    comparison_data.append(
        {
            "name": data["name"],
            "short": short_name,
            "french_score": data["scores"]["french_score"],
            "english_score": data["scores"]["english_score"],
            "ratio": data["scores"]["french_ratio"],
            "vocab_richness": data["stats"]["vocabulary_richness"],
            "total_words": data["stats"]["total_words"],
            "french_expressions": data["stats"]["total_french_expressions"],
            "exclamatory_pct": data["stats"]["exclamatory_percentage"],
            "language_bias": data["scores"]["language_bias"],
        }
    )

# Sort by French ratio for presentation
comparison_data.sort(key=lambda x: x["ratio"], reverse=True)

print(
    f"\n{Fore.CYAN}🏆 RANKING BY FRENCH-NESS (French/English Ratio):{Style.RESET_ALL}"
)
for i, text in enumerate(comparison_data, 1):
    color = (
        Fore.GREEN
        if text["language_bias"] == "French"
        else Fore.YELLOW if text["ratio"] > 0.5 else Fore.RED
    )
    print(
        f"{i}. {color}{text['name']}{Style.RESET_ALL} - Ratio: {text['ratio']:.3f} ({text['language_bias']} bias)"
    )

print(f"\n{Fore.CYAN}📈 STATISTICAL COMPARISONS:{Style.RESET_ALL}")

# Find TF2 Spy data for comparisons
spy_data = next(item for item in comparison_data if item["short"] == "spy")
print(f"\n{Fore.MAGENTA}TF2 Spy vs Others:{Style.RESET_ALL}")
for text in comparison_data:
    if text["short"] != "spy":
        ratio_comparison = (
            spy_data["ratio"] / text["ratio"] if text["ratio"] > 0 else float("inf")
        )
        vocab_comparison = (
            spy_data["vocab_richness"] / text["vocab_richness"]
            if text["vocab_richness"] > 0
            else float("inf")
        )
        comparison_word = "more" if spy_data["ratio"] > text["ratio"] else "less"
        print(
            f"  • {ratio_comparison:.1f}x {comparison_word} French than {text['name']}"
        )
        print(f"    - Vocabulary richness: {vocab_comparison:.1f}x vs {text['name']}")
        print(
            f"    - French expressions: {spy_data['french_expressions']} vs {text['french_expressions']}"
        )

print(f"\n{Fore.CYAN}🎯 KEY INSIGHTS FOR PRESENTATION:{Style.RESET_ALL}")

# Generate insights
most_french = max(comparison_data, key=lambda x: x["ratio"])
least_french = min(comparison_data, key=lambda x: x["ratio"])
most_dramatic = max(comparison_data, key=lambda x: x["exclamatory_pct"])
largest_vocab = max(comparison_data, key=lambda x: x["total_words"])

print(
    f"• Most French-like: {Fore.GREEN}{most_french['name']}{Style.RESET_ALL} (ratio: {most_french['ratio']:.3f})"
)
print(
    f"• Least French-like: {Fore.RED}{least_french['name']}{Style.RESET_ALL} (ratio: {least_french['ratio']:.3f})"
)
print(
    f"• Most dramatic: {Fore.YELLOW}{most_dramatic['name']}{Style.RESET_ALL} ({most_dramatic['exclamatory_pct']:.1f}% exclamatory)"
)
print(
    f"• Largest vocabulary: {Fore.BLUE}{largest_vocab['name']}{Style.RESET_ALL} ({largest_vocab['total_words']:,} words)"
)

# Calculate percentile for Spy
spy_position = (
    next(i for i, item in enumerate(comparison_data) if item["short"] == "spy") + 1
)
spy_percentile = (len(comparison_data) - spy_position + 1) / len(comparison_data) * 100
print(
    f"• TF2 Spy ranks #{spy_position} of {len(comparison_data)} ({spy_percentile:.0f}th percentile for French-ness)"
)

# ============================================================================
# DETAILED TF2 SPY ANALYSIS FOR PRESENTATION
# ============================================================================

print(f"\n{Fore.CYAN}Starting Detailed TF2 Spy Analysis...{Style.RESET_ALL}")
print("=" * 80)

# Use the spy data we already analyzed
spy_stats = all_text_analyses["spy"]["stats"]
spy_scores = all_text_analyses["spy"]["scores"]

# Generate and display presentation summary
presentation_summary = spy_analyzer.generate_presentation_summary(spy_stats, spy_scores)
print(presentation_summary)

# Generate detailed word analysis
detailed_analysis = spy_analyzer.generate_detailed_word_analysis(spy_stats)
print(detailed_analysis)

# Additional comparative analysis using old results structure for compatibility
print(f"\n{Fore.YELLOW}📈 LEGACY COMPARATIVE ANALYSIS{Style.RESET_ALL}")
print("=" * 50)

# Compare Spy's French ratio with other texts using old results
spy_result = None
for result in results:
    if "spy" in result["name"].lower():
        spy_result = result
        break

if spy_result:
    spy_ratio = float(spy_result["ratio"])
    print(
        f"\n{Fore.CYAN}Legacy Analysis - TF2 Spy vs Original Three Texts:{Style.RESET_ALL}"
    )
    print(f"• Spy French/English Ratio: {spy_ratio:.3f}")

    for result in results:
        if result != spy_result:
            other_ratio = float(result["ratio"])
            comparison = "more" if spy_ratio > other_ratio else "less"
            factor = spy_ratio / other_ratio if other_ratio > 0 else float("inf")
            print(
                f"• {factor:.1f}x {comparison} French than {result['name']} ({other_ratio:.3f})"
            )

    # Statistical insights for original three texts
    print(f"\n{Fore.CYAN}Statistical Position (Original Analysis):{Style.RESET_ALL}")
    all_ratios = [float(r["ratio"]) for r in results]
    spy_percentile = (sorted(all_ratios).index(spy_ratio) + 1) / len(all_ratios) * 100
    avg_ratio = sum(all_ratios) / len(all_ratios)
    print(f"• Spy ranks in the {spy_percentile:.0f}th percentile for French-ness")
    print(f"• Average French ratio across all texts: {avg_ratio:.3f}")
    print(f"• Spy is {spy_ratio / avg_ratio:.1f}x more French than average")

# Export data for presentations
print(f"\n{Fore.YELLOW}💾 PRESENTATION DATA EXPORT{Style.RESET_ALL}")
print("=" * 50)

presentation_data = {
    "spy_analysis": {
        "basic_stats": {
            "total_voicelines": spy_stats["total_voicelines"],
            "total_words": spy_stats["total_words"],
            "unique_words": spy_stats["unique_words"],
            "vocab_richness": spy_stats["vocabulary_richness"],
        },
        "language_breakdown": {
            "french_words_count": spy_stats["distinctly_french_words"],
            "english_words_count": spy_stats["distinctly_english_words"],
            "french_percentage": spy_stats["french_word_percentage"],
            "english_percentage": spy_stats["english_word_percentage"],
        },
        "expressions": {
            "french_expressions": spy_stats["total_french_expressions"],
            "english_expressions": spy_stats["total_english_expressions"],
            "exclamatory_percent": spy_stats["exclamatory_percentage"],
        },
        "bloom_scores": {
            "french_score": spy_scores["french_score"],
            "english_score": spy_scores["english_score"],
            "ratio": spy_scores["french_ratio"],
        },
        "key_phrases": list(spy_stats["french_phrases_found"].keys())[:5],
    },
    "all_texts_comparison": comparison_data,
    "text_rankings": {
        "most_french": most_french["name"],
        "least_french": least_french["name"],
        "most_dramatic": most_dramatic["name"],
        "largest_vocab": largest_vocab["name"],
        "spy_position": spy_position,
        "spy_percentile": spy_percentile,
    },
    "individual_analyses": {
        short: {
            "name": data["name"],
            "total_words": data["stats"]["total_words"],
            "vocab_richness": data["stats"]["vocabulary_richness"],
            "french_ratio": data["scores"]["french_ratio"],
            "language_bias": data["scores"]["language_bias"],
            "french_expressions": data["stats"]["total_french_expressions"],
            "exclamatory_pct": data["stats"]["exclamatory_percentage"],
        }
        for short, data in all_text_analyses.items()
    },
}

print(f"{Fore.GREEN}✓ Analysis complete! Key presentation statistics:{Style.RESET_ALL}")
print(f"  • French vocabulary: {spy_stats['french_word_percentage']:.1f}% of total")
print(f"  • French expressions detected: {spy_stats['total_french_expressions']}")
print(f"  • Overall French bias ratio: {spy_scores['french_ratio']:.3f}")
print(f"  • Language bias: {spy_scores['language_bias']}")
print(f"  • Confidence level: {spy_scores['confidence_level']:.1%}")

print(f"\n{Fore.CYAN}🎯 PRESENTATION TALKING POINTS:{Style.RESET_ALL}")
print("1. TF2 Spy uses a mix of languages but leans toward French")
print("2. Specific French phrases add authentic character flavor")
print("3. High exclamatory usage shows dramatic personality")
print("4. Vocabulary analysis shows intentional linguistic choices")
print("5. Comparative analysis shows Spy's unique linguistic position")

print(f"\n{Fore.CYAN}{'=' * 80}")
print("ANALYSIS COMPLETE - READY FOR PRESENTATION!")
print(f"{'=' * 80}{Style.RESET_ALL}")

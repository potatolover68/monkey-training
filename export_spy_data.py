"""
Export TF2 Spy analysis data in presentation-friendly formats (JSON, CSV)
"""

import json
import csv
import flowers
from spy_analysis import SpyLinguisticAnalyzer
from datetime import datetime


def export_spy_analysis_data():
    """Export comprehensive analysis data for all texts including TF2 Spy"""

    # Initialize bloom filters and analyzer
    print("Loading bloom filters...")
    fr = flowers.Flower("data/francais.txt")
    eng = flowers.Flower("data/words_alpha.txt")
    spy_analyzer = SpyLinguisticAnalyzer(fr, eng)

    # Define all texts to analyze
    text_mapping = {
        "data/tf2_spy_voicelines.txt": {"name": "TF2 Spy", "short": "spy"},
        "data/hamlet.txt": {"name": "Hamlet", "short": "hamlet"},
        "data/romeo.txt": {"name": "Romeo & Juliet", "short": "romeo"},
        "data/jeeves.txt": {"name": "Jeeves & Wooster", "short": "jeeves"},
    }

    # Analyze all texts
    print("Analyzing all texts...")
    all_analyses = {}
    for text_file, info in text_mapping.items():
        print(f"  • Analyzing {info['name']}...")
        text_stats = spy_analyzer.analyze_voicelines(text_file)
        text_scores = spy_analyzer.calculate_language_scores(text_file)

        # Add detailed word analysis
        print("    → Getting detailed word analysis...")
        word_analysis = spy_analyzer.get_detailed_word_analysis(text_file)

        all_analyses[info["short"]] = {
            "name": info["name"],
            "stats": text_stats,
            "scores": text_scores,
            "word_analysis": word_analysis,
        }

    # Get specific Spy data for backwards compatibility
    spy_stats = all_analyses["spy"]["stats"]
    spy_scores = all_analyses["spy"]["scores"]
    spy_word_analysis = all_analyses["spy"]["word_analysis"]

    # Create comparison data
    comparison_data = []
    for short_name, analysis_data in all_analyses.items():
        comparison_data.append(
            {
                "name": analysis_data["name"],
                "short": short_name,
                "french_score": analysis_data["scores"]["french_score"],
                "english_score": analysis_data["scores"]["english_score"],
                "ratio": analysis_data["scores"]["french_ratio"],
                "vocab_richness": analysis_data["stats"]["vocabulary_richness"],
                "total_words": analysis_data["stats"]["total_words"],
                "french_expressions": analysis_data["stats"][
                    "total_french_expressions"
                ],
                "exclamatory_pct": analysis_data["stats"]["exclamatory_percentage"],
                "language_bias": analysis_data["scores"]["language_bias"],
            }
        )

    # Sort by French ratio
    comparison_data.sort(key=lambda x: x["ratio"], reverse=True)

    # Find rankings
    most_french = max(comparison_data, key=lambda x: x["ratio"])
    least_french = min(comparison_data, key=lambda x: x["ratio"])
    most_dramatic = max(comparison_data, key=lambda x: x["exclamatory_pct"])
    largest_vocab = max(comparison_data, key=lambda x: x["total_words"])
    spy_position = (
        next(i for i, item in enumerate(comparison_data) if item["short"] == "spy") + 1
    )

    # Prepare comprehensive export data
    export_data = {
        "metadata": {
            "analysis_date": datetime.now().isoformat(),
            "texts_analyzed": len(all_analyses),
            "texts_included": list(text_mapping.keys()),
        },
        "spy_focused_analysis": {
            "basic_statistics": {
                "total_words": spy_stats["total_words"],
                "unique_words": spy_stats["unique_words"],
                "vocabulary_richness": round(spy_stats["vocabulary_richness"], 4),
                "avg_words_per_line": round(spy_stats["average_words_per_line"], 2),
            },
            "language_analysis": {
                "french_words_count": spy_stats["distinctly_french_words"],
                "english_words_count": spy_stats["distinctly_english_words"],
                "ambiguous_words_count": spy_stats["ambiguous_words"],
                "french_word_percentage": round(spy_stats["french_word_percentage"], 2),
                "english_word_percentage": round(
                    spy_stats["english_word_percentage"], 2
                ),
            },
            "bloom_filter_scores": {
                "french_score": round(spy_scores["french_score"], 3),
                "english_score": round(spy_scores["english_score"], 3),
                "french_english_ratio": round(spy_scores["french_ratio"], 3),
                "language_bias": spy_scores["language_bias"],
                "confidence_level": round(spy_scores["confidence_level"], 3),
            },
            "expression_analysis": {
                "french_expressions_count": spy_stats["total_french_expressions"],
                "english_expressions_count": spy_stats["total_english_expressions"],
                "exclamatory_percentage": round(spy_stats["exclamatory_percentage"], 1),
                "question_percentage": round(spy_stats["question_percentage"], 1),
                "french_phrases": list(spy_stats["french_phrases_found"].keys()),
            },
            "linguistic_features": {
                "latin_like_words": spy_stats["latin_like_words"],
                "most_common_words": [
                    word for word, count in spy_stats["most_common_words"]
                ],
                "most_french_sentence": spy_scores["most_french_sentence"],
                "most_english_sentence": spy_scores["most_english_sentence"],
            },
            "detailed_word_analysis": {
                "total_unique_words_analyzed": spy_word_analysis["total_unique_words"],
                "average_french_confidence": round(
                    spy_word_analysis["avg_french_confidence"], 3
                ),
                "average_english_confidence": round(
                    spy_word_analysis["avg_english_confidence"], 3
                ),
                "words_favoring_french": spy_word_analysis["words_favoring_french"],
                "words_favoring_english": spy_word_analysis["words_favoring_english"],
                "neutral_words": spy_word_analysis["neutral_words"],
                "top_french_words": [
                    {
                        "word": word,
                        "raw_confidence": round(data["french_raw"], 3),
                        "flower_power": round(data["french_flower"], 3),
                        "matches": data["french_matches"],
                        "frequency": data["frequency"],
                    }
                    for word, data in spy_word_analysis["most_french_words"]
                ],
                "top_english_words": [
                    {
                        "word": word,
                        "raw_confidence": round(data["english_raw"], 3),
                        "flower_power": round(data["english_flower"], 3),
                        "matches": data["english_matches"],
                        "frequency": data["frequency"],
                    }
                    for word, data in spy_word_analysis["most_english_words"]
                ],
                "strongest_french_bias": [
                    {
                        "word": word,
                        "french_raw": round(data["french_raw"], 3),
                        "english_raw": round(data["english_raw"], 3),
                        "bias_score": round(data["french_bias"], 3),
                        "frequency": data["frequency"],
                    }
                    for word, data in spy_word_analysis["strongest_french_bias"]
                ],
                "most_frequent_words": [
                    {
                        "word": word,
                        "frequency": data["frequency"],
                        "french_raw": round(data["french_raw"], 3),
                        "english_raw": round(data["english_raw"], 3),
                        "french_bias": round(data["french_bias"], 3),
                    }
                    for word, data in spy_word_analysis["most_frequent_words"]
                ],
            },
        },
        "comprehensive_comparison": {
            "all_texts_data": comparison_data,
            "rankings": {
                "most_french": most_french["name"],
                "least_french": least_french["name"],
                "most_dramatic": most_dramatic["name"],
                "largest_vocab": largest_vocab["name"],
                "spy_position": spy_position,
                "spy_percentile": round(
                    (len(comparison_data) - spy_position + 1)
                    / len(comparison_data)
                    * 100,
                    1,
                ),
            },
        },
        "individual_text_analyses": {
            short: {
                "name": text_data["name"],
                "total_lines": text_data["stats"]["total_voicelines"],
                "total_words": text_data["stats"]["total_words"],
                "vocabulary_richness": round(
                    text_data["stats"]["vocabulary_richness"], 4
                ),
                "french_ratio": round(text_data["scores"]["french_ratio"], 3),
                "language_bias": text_data["scores"]["language_bias"],
                "french_expressions": text_data["stats"]["total_french_expressions"],
                "exclamatory_percentage": round(
                    text_data["stats"]["exclamatory_percentage"], 1
                ),
                "most_french_sentence": (
                    text_data["scores"]["most_french_sentence"][:100] + "..."
                    if len(text_data["scores"]["most_french_sentence"]) > 100
                    else text_data["scores"]["most_french_sentence"]
                ),
            }
            for short, text_data in all_analyses.items()
        },
    }

    # Export to JSON
    json_filename = f'spy_analysis_data_{datetime.now().strftime("%Y%m%d_%H%M")}.json'
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    print(f"✓ JSON data exported to: {json_filename}")

    # Export comparative analysis to CSV for easy spreadsheet use
    comparison_csv_filename = (
        f'all_texts_comparison_{datetime.now().strftime("%Y%m%d_%H%M")}.csv'
    )
    with open(comparison_csv_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Text Name",
                "French Score",
                "English Score",
                "French/English Ratio",
                "Language Bias",
                "Total Words",
                "Vocabulary Richness %",
                "French Expressions",
                "Exclamatory %",
                "Ranking",
            ]
        )

        for i, text in enumerate(comparison_data, 1):
            writer.writerow(
                [
                    text["name"],
                    f"{text['french_score']:.3f}",
                    f"{text['english_score']:.3f}",
                    f"{text['ratio']:.3f}",
                    text["language_bias"],
                    f"{text['total_words']:,}",
                    f"{text['vocab_richness']:.1%}",
                    text["french_expressions"],
                    f"{text['exclamatory_pct']:.1f}%",
                    i,
                ]
            )

    print(f"✓ Comparative analysis CSV exported to: {comparison_csv_filename}")

    # Export individual Spy stats to CSV for backwards compatibility
    spy_csv_filename = (
        f'spy_analysis_summary_{datetime.now().strftime("%Y%m%d_%H%M")}.csv'
    )
    with open(spy_csv_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Metric", "Value", "Description"])

        # Basic stats
        writer.writerow(
            [
                "Total Voicelines",
                spy_stats["total_voicelines"],
                "Number of individual voicelines",
            ]
        )
        writer.writerow(["Total Words", spy_stats["total_words"], "Total word count"])
        writer.writerow(
            ["Unique Words", spy_stats["unique_words"], "Size of vocabulary"]
        )
        writer.writerow(
            [
                "Vocabulary Richness",
                f"{spy_stats['vocabulary_richness']:.2%}",
                "Unique words / total words",
            ]
        )

        # Language breakdown
        writer.writerow(
            [
                "French Words %",
                f"{spy_stats['french_word_percentage']:.1f}%",
                "Percentage of distinctly French words",
            ]
        )
        writer.writerow(
            [
                "English Words %",
                f"{spy_stats['english_word_percentage']:.1f}%",
                "Percentage of distinctly English words",
            ]
        )
        writer.writerow(
            [
                "French Expressions",
                spy_stats["total_french_expressions"],
                "Number of French phrases detected",
            ]
        )

        # Bloom filter scores
        writer.writerow(
            [
                "French Bloom Score",
                f"{spy_scores['french_score']:.3f}",
                "Overall French language score",
            ]
        )
        writer.writerow(
            [
                "English Bloom Score",
                f"{spy_scores['english_score']:.3f}",
                "Overall English language score",
            ]
        )
        writer.writerow(
            [
                "French/English Ratio",
                f"{spy_scores['french_ratio']:.3f}",
                "French score divided by English score",
            ]
        )
        writer.writerow(
            ["Language Bias", spy_scores["language_bias"], "Primary language detected"]
        )

        # Comparative position
        writer.writerow(
            [
                "Position Ranking",
                spy_position,
                f"Rank among {len(comparison_data)} texts",
            ]
        )
        writer.writerow(
            [
                "Percentile Ranking",
                f"{(len(comparison_data) - spy_position + 1) / len(comparison_data) * 100:.1f}th",
                "Percentile for French-ness",
            ]
        )

        # Character traits
        writer.writerow(
            [
                "Exclamatory %",
                f"{spy_stats['exclamatory_percentage']:.1f}%",
                "Percentage of lines with exclamation marks",
            ]
        )
        writer.writerow(
            [
                "Question %",
                f"{spy_stats['question_percentage']:.1f}%",
                "Percentage of lines with question marks",
            ]
        )

    print(f"✓ Spy-focused CSV summary exported to: {spy_csv_filename}")

    # Export French phrases detail
    phrases_filename = (
        f'spy_french_phrases_{datetime.now().strftime("%Y%m%d_%H%M")}.csv'
    )
    with open(phrases_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["French Phrase", "Count", "English Meaning"])

        for phrase, data in spy_stats["french_phrases_found"].items():
            writer.writerow([phrase, data["count"], data["meaning"]])

    print(f"✓ French phrases exported to: {phrases_filename}")

    # Export detailed word analysis to CSV
    word_analysis_filename = (
        f'spy_detailed_word_analysis_{datetime.now().strftime("%Y%m%d_%H%M")}.csv'
    )
    with open(word_analysis_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Word",
                "Frequency",
                "French Raw Confidence",
                "French Flower Power",
                "French Matches",
                "English Raw Confidence",
                "English Flower Power",
                "English Matches",
                "French Bias Score",
                "Language Preference",
            ]
        )

        # Sort by frequency for main export
        sorted_words = sorted(
            spy_word_analysis["all_word_data"].items(),
            key=lambda x: x[1]["frequency"],
            reverse=True,
        )

        for word, data in sorted_words:
            # Determine language preference
            if data["french_bias"] > 0.1:
                preference = "French"
            elif data["french_bias"] < -0.1:
                preference = "English"
            else:
                preference = "Neutral"

            writer.writerow(
                [
                    word,
                    data["frequency"],
                    f"{data['french_raw']:.3f}",
                    f"{data['french_flower']:.3f}",
                    data["french_matches"],
                    f"{data['english_raw']:.3f}",
                    f"{data['english_flower']:.3f}",
                    data["english_matches"],
                    f"{data['french_bias']:.3f}",
                    preference,
                ]
            )

    print(f"✓ Detailed word analysis exported to: {word_analysis_filename}")

    # Export word analysis summary statistics
    word_stats_filename = (
        f'spy_word_statistics_{datetime.now().strftime("%Y%m%d_%H%M")}.csv'
    )
    with open(word_stats_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Category", "Count", "Percentage", "Description"])

        total_words = spy_word_analysis["total_unique_words"]

        writer.writerow(
            ["Total Unique Words", total_words, "100.0%", "Total vocabulary analyzed"]
        )
        writer.writerow(
            [
                "Words Favoring French",
                spy_word_analysis["words_favoring_french"],
                f"{spy_word_analysis['words_favoring_french']/total_words*100:.1f}%",
                "Words with >0.1 French bias",
            ]
        )
        writer.writerow(
            [
                "Words Favoring English",
                spy_word_analysis["words_favoring_english"],
                f"{spy_word_analysis['words_favoring_english']/total_words*100:.1f}%",
                "Words with <-0.1 English bias",
            ]
        )
        writer.writerow(
            [
                "Neutral Words",
                spy_word_analysis["neutral_words"],
                f"{spy_word_analysis['neutral_words']/total_words*100:.1f}%",
                "Words with -0.1 to 0.1 bias",
            ]
        )
        writer.writerow(
            [
                "Average French Confidence",
                f"{spy_word_analysis['avg_french_confidence']:.3f}",
                "",
                "Mean raw confidence across all words",
            ]
        )
        writer.writerow(
            [
                "Average English Confidence",
                f"{spy_word_analysis['avg_english_confidence']:.3f}",
                "",
                "Mean raw confidence across all words",
            ]
        )

    print(f"✓ Word analysis statistics exported to: {word_stats_filename}")

    return export_data


if __name__ == "__main__":
    print("🇫🇷 TF2 Spy Analysis Data Export")
    print("=" * 40)

    try:
        data = export_spy_analysis_data()

        print("\n✅ Export complete!")
        print("\nFiles created:")
        print("• JSON file: Complete comprehensive analysis data for all texts")
        print("• Comparison CSV: Side-by-side analysis of all texts")
        print("• Spy-focused CSV: Detailed TF2 Spy metrics for spreadsheet analysis")
        print("• French phrases CSV: Detailed French phrase usage by Spy")
        print(
            "• Word analysis CSV: Individual word confidence scores and raw bloom filter data"
        )
        print(
            "• Word statistics CSV: Summary statistics of word-level language analysis"
        )
        print("\nData includes analysis of:")
        print("  - TF2 Spy voicelines")
        print("  - Hamlet (Shakespeare)")
        print("  - Romeo & Juliet (Shakespeare)")
        print("  - Jeeves & Wooster (P.G. Wodehouse)")
        print(
            "\nThese files are ready for use in presentations, reports, or further analysis!"
        )

    except Exception as e:
        print(f"❌ Export failed: {e}")

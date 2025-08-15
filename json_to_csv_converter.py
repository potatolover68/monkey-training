"""
Convert TF2 Spy Analysis JSON data to multiple CSV files for easier analysis
"""

import json
import csv
import sys
from pathlib import Path
from datetime import datetime


def convert_spy_basic_stats(data, output_dir):
    """Convert spy basic statistics to CSV"""
    filename = output_dir / "spy_basic_statistics.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Metric", "Value", "Category"])
        
        # Basic statistics
        basic = data["spy_focused_analysis"]["basic_statistics"]
        writer.writerow(["Total Words", basic["total_words"], "Basic"])
        writer.writerow(["Unique Words", basic["unique_words"], "Basic"])
        writer.writerow(["Vocabulary Richness", f"{basic['vocabulary_richness']:.4f}", "Basic"])
        writer.writerow(["Avg Words Per Line", f"{basic['avg_words_per_line']:.2f}", "Basic"])
        
        # Language analysis
        lang = data["spy_focused_analysis"]["language_analysis"]
        writer.writerow(["French Words Count", lang["french_words_count"], "Language"])
        writer.writerow(["English Words Count", lang["english_words_count"], "Language"])
        writer.writerow(["Ambiguous Words Count", lang["ambiguous_words_count"], "Language"])
        writer.writerow(["French Word Percentage", f"{lang['french_word_percentage']:.2f}%", "Language"])
        writer.writerow(["English Word Percentage", f"{lang['english_word_percentage']:.2f}%", "Language"])
        
        # Bloom filter scores
        bloom = data["spy_focused_analysis"]["bloom_filter_scores"]
        writer.writerow(["French Score", bloom["french_score"], "Bloom Filter"])
        writer.writerow(["English Score", bloom["english_score"], "Bloom Filter"])
        writer.writerow(["French/English Ratio", bloom["french_english_ratio"], "Bloom Filter"])
        writer.writerow(["Language Bias", bloom["language_bias"], "Bloom Filter"])
        writer.writerow(["Confidence Level", bloom["confidence_level"], "Bloom Filter"])
        
        # Expression analysis
        expr = data["spy_focused_analysis"]["expression_analysis"]
        writer.writerow(["French Expressions Count", expr["french_expressions_count"], "Expression"])
        writer.writerow(["English Expressions Count", expr["english_expressions_count"], "Expression"])
        writer.writerow(["Exclamatory Percentage", f"{expr['exclamatory_percentage']:.1f}%", "Expression"])
        writer.writerow(["Question Percentage", f"{expr['question_percentage']:.1f}%", "Expression"])
        
    print(f"✓ Basic statistics exported to: {filename}")


def convert_detailed_word_analysis(data, output_dir):
    """Convert detailed word analysis to CSV"""
    filename = output_dir / "spy_detailed_word_scores.csv"
    
    word_analysis = data["spy_focused_analysis"]["detailed_word_analysis"]
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            "Word", "Raw Confidence", "Flower Power", "Matches", 
            "Frequency", "Category"
        ])
        
        # Top French words
        for word_data in word_analysis["top_french_words"]:
            writer.writerow([
                word_data["word"],
                word_data["raw_confidence"],
                word_data["flower_power"],
                word_data["matches"],
                word_data["frequency"],
                "Top French"
            ])
        
        # Top English words
        for word_data in word_analysis["top_english_words"]:
            writer.writerow([
                word_data["word"],
                word_data["raw_confidence"],
                word_data["flower_power"],
                word_data["matches"],
                word_data["frequency"],
                "Top English"
            ])
    
    print(f"✓ Detailed word scores exported to: {filename}")


def convert_french_bias_analysis(data, output_dir):
    """Convert French bias analysis to CSV"""
    filename = output_dir / "spy_french_bias_words.csv"
    
    word_analysis = data["spy_focused_analysis"]["detailed_word_analysis"]
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            "Word", "French Raw", "English Raw", "Bias Score", 
            "Frequency", "Analysis Type"
        ])
        
        # Strongest French bias
        for word_data in word_analysis["strongest_french_bias"]:
            writer.writerow([
                word_data["word"],
                word_data["french_raw"],
                word_data["english_raw"],
                word_data["bias_score"],
                word_data["frequency"],
                "French Bias"
            ])
        
        # Most frequent words with bias info
        for word_data in word_analysis["most_frequent_words"]:
            writer.writerow([
                word_data["word"],
                word_data["french_raw"],
                word_data.get("english_raw", "N/A"),  # Some entries might not have this
                word_data["french_bias"],
                word_data["frequency"],
                "Most Frequent"
            ])
    
    print(f"✓ French bias analysis exported to: {filename}")


def convert_text_comparisons(data, output_dir):
    """Convert text comparison data to CSV"""
    filename = output_dir / "all_texts_comparison.csv"
    
    comparison_data = data["comprehensive_comparison"]["all_texts_data"]
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            "Text Name", "Short Code", "French Score", "English Score", 
            "French/English Ratio", "Vocabulary Richness", "Total Words",
            "French Expressions", "Exclamatory %", "Language Bias"
        ])
        
        for text in comparison_data:
            writer.writerow([
                text["name"],
                text["short"],
                f"{text['french_score']:.3f}",
                f"{text['english_score']:.3f}",
                f"{text['ratio']:.3f}",
                f"{text['vocab_richness']:.4f}",
                text["total_words"],
                text["french_expressions"],
                f"{text['exclamatory_pct']:.1f}%",
                text["language_bias"]
            ])
    
    print(f"✓ Text comparisons exported to: {filename}")


def convert_individual_analyses(data, output_dir):
    """Convert individual text analyses to CSV"""
    filename = output_dir / "individual_text_analyses.csv"
    
    individual_data = data["individual_text_analyses"]
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            "Short Code", "Full Name", "Total Lines", "Total Words", 
            "Vocabulary Richness", "French Ratio", "Language Bias",
            "French Expressions", "Exclamatory %", "Most French Sentence Preview"
        ])
        
        for short_code, text_data in individual_data.items():
            # Truncate the sentence preview to 100 chars
            sentence_preview = text_data["most_french_sentence"][:100]
            if len(text_data["most_french_sentence"]) > 100:
                sentence_preview += "..."
                
            writer.writerow([
                short_code,
                text_data["name"],
                text_data["total_lines"],
                text_data["total_words"],
                text_data["vocabulary_richness"],
                text_data["french_ratio"],
                text_data["language_bias"],
                text_data["french_expressions"],
                f"{text_data['exclamatory_percentage']:.1f}%",
                sentence_preview
            ])
    
    print(f"✓ Individual text analyses exported to: {filename}")


def convert_rankings_summary(data, output_dir):
    """Convert rankings and summary data to CSV"""
    filename = output_dir / "analysis_summary_and_rankings.csv"
    
    metadata = data["metadata"]
    rankings = data["comprehensive_comparison"]["rankings"]
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Category", "Value", "Description"])
        
        # Metadata
        writer.writerow(["Analysis Date", metadata["analysis_date"], "When analysis was performed"])
        writer.writerow(["Texts Analyzed", metadata["texts_analyzed"], "Number of texts in comparison"])
        
        # Rankings
        writer.writerow(["Most French Text", rankings["most_french"], "Text with highest French ratio"])
        writer.writerow(["Least French Text", rankings["least_french"], "Text with lowest French ratio"])
        writer.writerow(["Most Dramatic Text", rankings["most_dramatic"], "Text with highest exclamatory %"])
        writer.writerow(["Largest Vocabulary", rankings["largest_vocab"], "Text with most total words"])
        writer.writerow(["Spy Position", rankings["spy_position"], f"Spy's rank out of {metadata['texts_analyzed']} texts"])
        writer.writerow(["Spy Percentile", f"{rankings['spy_percentile']:.1f}th", "Spy's percentile ranking for French-ness"])
        
        # Word analysis summary
        word_stats = data["spy_focused_analysis"]["detailed_word_analysis"]
        writer.writerow(["Total Words Analyzed", word_stats["total_unique_words_analyzed"], "Spy vocabulary size"])
        writer.writerow(["Avg French Confidence", f"{word_stats['average_french_confidence']:.3f}", "Mean French bloom filter score"])
        writer.writerow(["Avg English Confidence", f"{word_stats['average_english_confidence']:.3f}", "Mean English bloom filter score"])
        writer.writerow(["Words Favoring French", word_stats["words_favoring_french"], "Words with French bias > 0.1"])
        writer.writerow(["Words Favoring English", word_stats["words_favoring_english"], "Words with English bias > 0.1"])
        writer.writerow(["Neutral Words", word_stats["neutral_words"], "Words with bias between -0.1 and 0.1"])
        
    print(f"✓ Summary and rankings exported to: {filename}")


def convert_french_phrases(data, output_dir):
    """Convert French phrases to CSV"""
    filename = output_dir / "spy_french_phrases_detected.csv"
    
    french_phrases = data["spy_focused_analysis"]["expression_analysis"]["french_phrases"]
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["French Phrase", "Detection Status"])
        
        for phrase in french_phrases:
            writer.writerow([phrase, "Detected in Spy voicelines"])
    
    print(f"✓ French phrases exported to: {filename}")


def main():
    """Main conversion function"""
    if len(sys.argv) != 2:
        print("Usage: python json_to_csv_converter.py <json_filename>")
        print("Example: python json_to_csv_converter.py spy_analysis_data_20250814_2042.json")
        sys.exit(1)
    
    json_filename = sys.argv[1]
    json_path = Path(json_filename)
    
    if not json_path.exists():
        print(f"Error: File {json_filename} not found!")
        sys.exit(1)
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_dir = Path(f"csv_exports_{timestamp}")
    output_dir.mkdir(exist_ok=True)
    
    print(f"🔄 Converting {json_filename} to CSV files...")
    print(f"📁 Output directory: {output_dir}")
    print("=" * 50)
    
    # Load JSON data
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON file - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    # Convert each section
    try:
        convert_spy_basic_stats(data, output_dir)
        convert_detailed_word_analysis(data, output_dir)
        convert_french_bias_analysis(data, output_dir)
        convert_text_comparisons(data, output_dir)
        convert_individual_analyses(data, output_dir)
        convert_rankings_summary(data, output_dir)
        convert_french_phrases(data, output_dir)
        
        print("=" * 50)
        print("✅ Conversion complete!")
        print(f"\n📊 Created {len(list(output_dir.glob('*.csv')))} CSV files:")
        
        for csv_file in sorted(output_dir.glob('*.csv')):
            print(f"  • {csv_file.name}")
        
        print(f"\n📂 All files saved in: {output_dir}")
        print("\nThese CSV files are ready for:")
        print("  - Excel/Google Sheets analysis")
        print("  - Statistical analysis in R/Python") 
        print("  - Data visualization tools")
        print("  - Presentation charts and graphs")
        
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

"""
Advanced linguistic analysis module for TF2 Spy voicelines
Provides comprehensive statistics suitable for presentation purposes
"""

import re
from typing import Dict, Any
from collections import Counter
import flowers
from colorama import Fore, Style


class SpyLinguisticAnalyzer:
    """Advanced analyzer for TF2 Spy linguistic patterns"""

    def __init__(self, french_filter: flowers.Flower, english_filter: flowers.Flower):
        self.french_filter = french_filter
        self.english_filter = english_filter

        # Known French phrases/expressions commonly used by Spy
        self.french_expressions = {
            "mon dieu": "My God",
            "sacrebleu": "Damn it!",
            "merde": "Shit",
            "voila": "There it is",
            "tres bon": "Very good",
            "fantastique": "Fantastic",
            "bon": "Good",
            "amigo": "Friend (Spanish, but used by Spy)",
        }

        # English equivalents or expressions
        self.english_expressions = {
            "gentlemen": "Gentlemen",
            "excellent": "Excellent",
            "magnificent": "Magnificent",
            "splendid": "Splendid",
            "marvelous": "Marvelous",
        }

    def analyze_voicelines(self, voicelines_file: str) -> Dict[str, Any]:
        """
        Comprehensive analysis of TF2 Spy voicelines
        Returns dictionary with all statistics
        """

        # Read and process voicelines
        try:
            with open(voicelines_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            with open(voicelines_file, "r", encoding="latin-1") as f:
                lines = f.readlines()

        # Clean lines but preserve original for phrase detection
        original_lines = [line.strip() for line in lines if line.strip()]
        clean_lines = [
            re.sub(r"[^\w']+", " ", line).strip().lower() for line in original_lines
        ]
        clean_lines = [line for line in clean_lines if len(line) > 1]

        # Extract all words
        all_words = []
        for line in clean_lines:
            words = line.split()
            all_words.extend([word for word in words if len(word) > 1])

        # Basic statistics
        stats = {
            "total_voicelines": len(original_lines),
            "total_words": len(all_words),
            "unique_words": len(set(all_words)),
            "average_words_per_line": (
                len(all_words) / len(original_lines) if original_lines else 0
            ),
            "vocabulary_richness": (
                len(set(all_words)) / len(all_words) if all_words else 0
            ),
        }

        # Word-level language analysis
        french_words = []
        english_words = []
        ambiguous_words = []

        for word in set(all_words):
            french_conf = self.french_filter.confidence(word)
            english_conf = self.english_filter.confidence(word)

            if french_conf > 0.7 and english_conf < 0.3:
                french_words.append((word, french_conf))
            elif english_conf > 0.7 and french_conf < 0.3:
                english_words.append((word, english_conf))
            elif french_conf > 0.5 and english_conf > 0.5:
                ambiguous_words.append((word, french_conf, english_conf))

        stats.update(
            {
                "distinctly_french_words": len(french_words),
                "distinctly_english_words": len(english_words),
                "ambiguous_words": len(ambiguous_words),
                "french_word_percentage": (
                    len(french_words) / len(set(all_words)) * 100 if all_words else 0
                ),
                "english_word_percentage": (
                    len(english_words) / len(set(all_words)) * 100 if all_words else 0
                ),
            }
        )

        # Phrase and expression analysis
        french_phrases_found = {}
        english_phrases_found = {}

        full_text = " ".join(original_lines).lower()

        for phrase, meaning in self.french_expressions.items():
            count = len(re.findall(r"\b" + re.escape(phrase) + r"\b", full_text))
            if count > 0:
                french_phrases_found[phrase] = {"count": count, "meaning": meaning}

        for phrase, meaning in self.english_expressions.items():
            count = len(re.findall(r"\b" + re.escape(phrase) + r"\b", full_text))
            if count > 0:
                english_phrases_found[phrase] = {"count": count, "meaning": meaning}

        stats["french_phrases_found"] = french_phrases_found
        stats["english_phrases_found"] = english_phrases_found
        stats["total_french_expressions"] = len(french_phrases_found)
        stats["total_english_expressions"] = len(english_phrases_found)

        # Advanced linguistic patterns
        exclamatory_lines = [line for line in original_lines if "!" in line]
        question_lines = [line for line in original_lines if "?" in line]

        # Detect Latin phrases (Spy uses some fake Latin)
        latin_pattern = r"\b[a-z]+us\b|\b[a-z]+um\b|\b[a-z]+is\b"
        latin_matches = re.findall(latin_pattern, full_text)

        stats["exclamatory_percentage"] = (
            len(exclamatory_lines) / len(original_lines) * 100
        )
        stats["question_percentage"] = len(question_lines) / len(original_lines) * 100
        stats["latin_like_words"] = len(set(latin_matches))
        stats["most_common_words"] = Counter(all_words).most_common(10)

        # Store word lists for detailed output
        stats["french_words_detail"] = sorted(
            french_words, key=lambda x: x[1], reverse=True
        )[:10]
        stats["english_words_detail"] = sorted(
            english_words, key=lambda x: x[1], reverse=True
        )[:10]
        stats["ambiguous_words_detail"] = sorted(
            ambiguous_words, key=lambda x: max(x[1], x[2]), reverse=True
        )[:10]

        return stats

    def calculate_language_scores(self, voicelines_file: str) -> Dict[str, Any]:
        """Calculate overall language bias scores"""
        try:
            with open(voicelines_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            with open(voicelines_file, "r", encoding="latin-1") as f:
                lines = f.readlines()

        clean_lines = [
            re.sub(r"[^\w']+", " ", line).strip().lower()
            for line in lines
            if line.strip()
        ]
        clean_lines = [line for line in clean_lines if len(line) > 1]
        clean_lines = list(set(clean_lines))  # Remove duplicates

        # Use existing flower power analysis
        french_sentence, french_score = flowers.most_flower(
            self.french_filter, clean_lines
        )
        english_sentence, english_score = flowers.most_flower(
            self.english_filter, clean_lines
        )

        return {
            "french_score": french_score,
            "english_score": english_score,
            "french_ratio": (
                french_score / english_score if english_score > 0 else float("inf")
            ),
            "language_bias": "French" if french_score > english_score else "English",
            "confidence_level": (
                abs(french_score - english_score) / max(french_score, english_score)
                if max(french_score, english_score) > 0
                else 0
            ),
            "most_french_sentence": french_sentence,
            "most_english_sentence": english_sentence,
        }

    def generate_presentation_summary(
        self, stats: Dict[str, Any], scores: Dict[str, float]
    ) -> str:
        """Generate a presentation-friendly summary of the analysis"""

        summary = f"""
{Fore.CYAN}{'=' * 60}
TF2 SPY LINGUISTIC ANALYSIS - PRESENTATION SUMMARY
{'=' * 60}{Style.RESET_ALL}

{Fore.YELLOW}📊 CORE STATISTICS{Style.RESET_ALL}
• Total voicelines analyzed: {stats['total_voicelines']:,}
• Total words: {stats['total_words']:,}
• Unique vocabulary: {stats['unique_words']:,}
• Vocabulary richness: {stats['vocabulary_richness']:.2%}
• Average words per line: {stats['average_words_per_line']:.1f}

{Fore.YELLOW}🗣️ LANGUAGE BREAKDOWN{Style.RESET_ALL}
• Distinctly French words: {stats['distinctly_french_words']} ({stats['french_word_percentage']:.1f}% of vocabulary)
• Distinctly English words: {stats['distinctly_english_words']} ({stats['english_word_percentage']:.1f}% of vocabulary)
• Ambiguous/Mixed words: {stats['ambiguous_words']}

{Fore.YELLOW}🎭 EXPRESSION ANALYSIS{Style.RESET_ALL}
• French expressions used: {stats['total_french_expressions']} different types
• English expressions used: {stats['total_english_expressions']} different types
• Exclamatory lines: {stats['exclamatory_percentage']:.1f}% (shows emotion/intensity)
• Question lines: {stats['question_percentage']:.1f}% (shows interaction)

{Fore.YELLOW}🔍 BLOOM FILTER SCORES{Style.RESET_ALL}
• French bloom score: {scores['french_score']:.3f}
• English bloom score: {scores['english_score']:.3f}
• French/English ratio: {scores['french_ratio']:.3f}
• Overall language bias: {scores['language_bias']}
• Confidence level: {scores['confidence_level']:.2%}

{Fore.YELLOW}🎯 KEY INSIGHTS FOR PRESENTATION{Style.RESET_ALL}
"""

        # Generate key insights
        if scores["french_ratio"] > 1.5:
            summary += f"• {Fore.GREEN}STRONGLY FRENCH-LEANING{Style.RESET_ALL}: Spy shows significant French linguistic influence\n"
        elif scores["french_ratio"] > 1.1:
            summary += f"• {Fore.CYAN}MODERATELY FRENCH-LEANING{Style.RESET_ALL}: Spy has noticeable French characteristics\n"
        else:
            summary += f"• {Fore.RED}NOT PARTICULARLY FRENCH{Style.RESET_ALL}: Spy's language is predominantly English\n"

        if stats["french_word_percentage"] > 10:
            summary += f"• {Fore.GREEN}HIGH FRENCH VOCABULARY{Style.RESET_ALL}: {stats['french_word_percentage']:.1f}% distinctly French words\n"

        if stats["total_french_expressions"] > 3:
            summary += f"• {Fore.GREEN}RICH FRENCH EXPRESSIONS{Style.RESET_ALL}: Uses {stats['total_french_expressions']} different French phrases\n"

        if stats["exclamatory_percentage"] > 30:
            summary += f"• {Fore.CYAN}DRAMATIC CHARACTER{Style.RESET_ALL}: {stats['exclamatory_percentage']:.1f}% of lines are exclamatory\n"

        summary += f"\n{Fore.YELLOW}🏆 MOST NOTABLE EXAMPLES{Style.RESET_ALL}\n"
        summary += (
            f"• Most French sentence: \"{scores['most_french_sentence'][:80]}...\"\n"
        )
        summary += (
            f"• Most English sentence: \"{scores['most_english_sentence'][:80]}...\"\n"
        )

        if stats["french_phrases_found"]:
            summary += f"\n{Fore.YELLOW}🇫🇷 FRENCH PHRASES DETECTED{Style.RESET_ALL}\n"
            for phrase, data in list(stats["french_phrases_found"].items())[:5]:
                summary += (
                    f"• \"{phrase}\" ({data['meaning']}) - used {data['count']} times\n"
                )

        summary += f"\n{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n"

        return summary

    def generate_detailed_word_analysis(self, stats: Dict[str, Any]) -> str:
        """Generate detailed word-by-word analysis"""

        output = f"\n{Fore.YELLOW}🔤 DETAILED WORD ANALYSIS{Style.RESET_ALL}\n"
        output += "=" * 50 + "\n"

        if stats["french_words_detail"]:
            output += (
                f"\n{Fore.GREEN}Top French Words (with confidence):{Style.RESET_ALL}\n"
            )
            for word, conf in stats["french_words_detail"]:
                output += f"  • {word} ({conf:.3f})\n"

        if stats["english_words_detail"]:
            output += (
                f"\n{Fore.BLUE}Top English Words (with confidence):{Style.RESET_ALL}\n"
            )
            for word, conf in stats["english_words_detail"]:
                output += f"  • {word} ({conf:.3f})\n"

        if stats["ambiguous_words_detail"]:
            output += f"\n{Fore.MAGENTA}Top Ambiguous Words (French/English confidence):{Style.RESET_ALL}\n"
            for word_data in stats["ambiguous_words_detail"]:
                word, fr_conf, en_conf = word_data
                output += f"  • {word} (FR: {fr_conf:.3f}, EN: {en_conf:.3f})\n"

        output += f"\n{Fore.CYAN}Most Common Words Overall:{Style.RESET_ALL}\n"
        for word, count in stats["most_common_words"]:
            output += f"  • {word} ({count} times)\n"

        return output

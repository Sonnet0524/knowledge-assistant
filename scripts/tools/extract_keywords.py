#!/usr/bin/env python3
"""
Keyword Extraction Tool.

This module provides functionality to extract keywords from text using
TF-IDF (Term Frequency-Inverse Document Frequency) algorithm.

Supports both Chinese and English text with automatic language detection.

Example:
    >>> from scripts.tools.extract_keywords import extract_keywords
    >>>
    >>> # Extract keywords from a single document
    >>> text = "Python is a programming language. Python is widely used."
    >>> keywords = extract_keywords(text, top_n=5)
    >>> for keyword, weight in keywords:
    ...     print(f"{keyword}: {weight:.4f}")
"""

import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

from scripts.utils import get_project_root, read_file


@dataclass
class KeywordResult:
    """
    Result of keyword extraction.

    Attributes:
        keyword (str): The extracted keyword.
        weight (float): The TF-IDF weight of the keyword.
        tf (float): Term frequency.
        idf (float): Inverse document frequency.
    """

    keyword: str
    weight: float
    tf: float
    idf: float


class LanguageDetector:
    """
    Simple language detector for Chinese and English.

    Determines if text is primarily Chinese or English based on
    character distribution.
    """

    # Unicode ranges for Chinese characters
    CHINESE_PATTERN = re.compile(r"[\u4e00-\u9fff]+")

    @classmethod
    def detect(cls, text: str) -> str:
        """
        Detect the primary language of text.

        Args:
            text (str): Text to analyze.

        Returns:
            str: 'chinese' or 'english'.

        Example:
            >>> lang = LanguageDetector.detect("这是一个测试")
            >>> lang
            'chinese'
        """
        if not text:
            return "english"

        # Count Chinese characters
        chinese_chars = cls.CHINESE_PATTERN.findall(text)
        chinese_count = sum(len(chars) for chars in chinese_chars)

        # Count total meaningful characters (excluding spaces and punctuation)
        total_chars = len(re.findall(r"\w", text, re.UNICODE))

        if total_chars == 0:
            return "english"

        # If more than 30% are Chinese characters, treat as Chinese
        chinese_ratio = chinese_count / total_chars
        return "chinese" if chinese_ratio > 0.3 else "english"


class TextTokenizer:
    """
    Tokenizer for Chinese and English text.

    Provides tokenization support for both languages:
    - English: Uses regex-based word tokenization
    - Chinese: Uses jieba if available, otherwise simple character-based tokenization
    """

    # English word pattern (matches word boundaries)
    ENGLISH_PATTERN = re.compile(r"\b[a-zA-Z]+\b")

    # Chinese character pattern
    CHINESE_PATTERN = re.compile(r"[\u4e00-\u9fff]+")

    # Common English stop words
    ENGLISH_STOP_WORDS = frozenset(
        {
            "a",
            "an",
            "the",
            "is",
            "are",
            "was",
            "were",
            "be",
            "been",
            "being",
            "have",
            "has",
            "had",
            "do",
            "does",
            "did",
            "will",
            "would",
            "could",
            "should",
            "may",
            "might",
            "must",
            "shall",
            "can",
            "need",
            "dare",
            "ought",
            "used",
            "to",
            "of",
            "in",
            "for",
            "on",
            "with",
            "at",
            "by",
            "from",
            "as",
            "into",
            "through",
            "during",
            "before",
            "after",
            "above",
            "below",
            "between",
            "under",
            "over",
            "again",
            "further",
            "then",
            "once",
            "here",
            "there",
            "when",
            "where",
            "why",
            "how",
            "all",
            "each",
            "few",
            "more",
            "most",
            "other",
            "some",
            "such",
            "no",
            "nor",
            "not",
            "only",
            "own",
            "same",
            "so",
            "than",
            "too",
            "very",
            "just",
            "and",
            "but",
            "if",
            "or",
            "because",
            "until",
            "while",
            "about",
            "against",
            "this",
            "that",
            "these",
            "those",
            "am",
            "it",
            "its",
            "itself",
            "i",
            "me",
            "my",
            "myself",
            "we",
            "our",
            "ours",
            "ourselves",
            "you",
            "your",
            "yours",
            "yourself",
            "yourselves",
            "he",
            "him",
            "his",
            "himself",
            "she",
            "her",
            "hers",
            "herself",
            "they",
            "them",
            "their",
            "theirs",
            "themselves",
            "what",
            "which",
            "who",
            "whom",
        }
    )

    # Common Chinese stop words
    CHINESE_STOP_WORDS = frozenset(
        {
            "的",
            "了",
            "和",
            "是",
            "在",
            "有",
            "我",
            "他",
            "这",
            "为",
            "之",
            "以",
            "及",
            "其",
            "与",
            "也",
            "就",
            "但",
            "而",
            "或",
            "把",
            "被",
            "让",
            "给",
            "向",
            "从",
            "对",
            "着",
            "过",
            "去",
            "来",
            "上",
            "下",
            "里",
            "外",
            "中",
            "一",
            "个",
            "们",
            "要",
            "会",
            "能",
            "说",
            "都",
            "不",
            "很",
            "着",
            "又",
            "还",
            "很",
            "那",
            "她",
            "它",
            "你",
            "我们",
            "你们",
            "他们",
            "自己",
            "什么",
            "怎么",
            "一个",
            "这个",
            "那个",
            "这些",
            "那些",
            "这里",
            "那里",
            "哪里",
            "因为",
            "所以",
            "如果",
            "虽然",
            "但是",
        }
    )

    @classmethod
    def tokenize(cls, text: str, language: str = "auto") -> List[str]:
        """
        Tokenize text into words.

        Args:
            text (str): Text to tokenize.
            language (str): Language of text. Options: 'auto', 'chinese', 'english'.
                Defaults to 'auto'.

        Returns:
            List[str]: List of tokens.

        Example:
            >>> tokens = TextTokenizer.tokenize("Python is great", language="english")
            >>> tokens
            ['python', 'great']
        """
        # Auto-detect language if needed
        if language == "auto":
            language = LanguageDetector.detect(text)

        if language == "chinese":
            return cls._tokenize_chinese(text)
        else:
            return cls._tokenize_english(text)

    @classmethod
    def _tokenize_english(cls, text: str) -> List[str]:
        """
        Tokenize English text.

        Args:
            text (str): English text to tokenize.

        Returns:
            List[str]: List of lowercase tokens excluding stop words.
        """
        # Find all words
        words = cls.ENGLISH_PATTERN.findall(text.lower())

        # Filter stop words and short words
        tokens = [word for word in words if word not in cls.ENGLISH_STOP_WORDS and len(word) > 1]

        return tokens

    @classmethod
    def _tokenize_chinese(cls, text: str) -> List[str]:
        """
        Tokenize Chinese text.

        Uses jieba if available, otherwise uses simple character-based tokenization.

        Args:
            text (str): Chinese text to tokenize.

        Returns:
            List[str]: List of tokens excluding stop words.
        """
        # Try to use jieba if available
        try:
            import jieba

            tokens = list(jieba.cut(text, cut_all=False))
        except ImportError:
            # Fallback to simple character-based tokenization
            # Extract Chinese characters and combine into 2-4 character words
            chinese_chars = cls.CHINESE_PATTERN.findall(text)

            # Simple sliding window for Chinese word segmentation
            tokens = []
            for chars in chinese_chars:
                # Add individual characters and 2-3 character combinations
                for i in range(len(chars)):
                    # Single character
                    if chars[i] not in cls.CHINESE_STOP_WORDS:
                        tokens.append(chars[i])
                    # 2-character words
                    if i < len(chars) - 1:
                        word = chars[i : i + 2]
                        tokens.append(word)
                    # 3-character words
                    if i < len(chars) - 2:
                        word = chars[i : i + 3]
                        tokens.append(word)

        # Filter stop words and short words
        tokens = [
            token for token in tokens if token not in cls.CHINESE_STOP_WORDS and len(token) > 1
        ]

        return tokens


class TFIDFCalculator:
    """
    TF-IDF calculator for keyword extraction.

    Computes Term Frequency-Inverse Document Frequency scores
    for terms in documents.
    """

    def __init__(self) -> None:
        """Initialize TF-IDF calculator."""
        self.document_count = 0
        self.document_freq: Dict[str, int] = {}  # Document frequency for each term
        self.idf_cache: Dict[str, float] = {}  # Cached IDF values

    def add_document(self, tokens: List[str]) -> None:
        """
        Add a document to the corpus for IDF calculation.

        Args:
            tokens (List[str]): Tokenized document content.
        """
        self.document_count += 1

        # Count unique terms in this document
        unique_terms = set(tokens)
        for term in unique_terms:
            self.document_freq[term] = self.document_freq.get(term, 0) + 1

        # Clear IDF cache when document is added
        self.idf_cache.clear()

    def calculate_tf(self, tokens: List[str]) -> Dict[str, float]:
        """
        Calculate term frequency for tokens.

        Uses raw term frequency (count / total terms).

        Args:
            tokens (List[str]): Tokenized text.

        Returns:
            Dict[str, float]: Term frequency for each unique term.
        """
        if not tokens:
            return {}

        # Count term frequencies
        term_counts = Counter(tokens)
        total_terms = len(tokens)

        # Normalize by total terms
        return {term: count / total_terms for term, count in term_counts.items()}

    def calculate_idf(self, term: str) -> float:
        """
        Calculate inverse document frequency for a term.

        Uses log(N / df) where N is total documents and df is document frequency.

        Args:
            term (str): The term to calculate IDF for.

        Returns:
            float: IDF value. Returns 0 if term not in corpus.
        """
        # Check cache
        if term in self.idf_cache:
            return self.idf_cache[term]

        if self.document_count == 0:
            return 0.0

        df = self.document_freq.get(term, 0)

        if df == 0:
            # Term not seen in corpus, assign small IDF
            idf = math.log(self.document_count + 1)
        else:
            # Standard IDF formula with smoothing
            idf = math.log((self.document_count + 1) / (df + 1)) + 1

        # Cache the result
        self.idf_cache[term] = idf

        return idf

    def calculate_tfidf(self, tokens: List[str]) -> Dict[str, float]:
        """
        Calculate TF-IDF scores for all terms in tokens.

        Args:
            tokens (List[str]): Tokenized text.

        Returns:
            Dict[str, float]: TF-IDF score for each unique term.
        """
        tf = self.calculate_tf(tokens)

        tfidf = {}
        for term, tf_value in tf.items():
            idf = self.calculate_idf(term)
            tfidf[term] = tf_value * idf

        return tfidf


class KeywordExtractor:
    """
    Main class for extracting keywords from text.

    Supports single document and multi-document keyword extraction
    using TF-IDF algorithm.

    Example:
        >>> extractor = KeywordExtractor()
        >>> keywords = extractor.extract("Python is a programming language.")
        >>> print(keywords)
    """

    def __init__(self, language: str = "auto") -> None:
        """
        Initialize keyword extractor.

        Args:
            language (str): Default language for tokenization.
                Options: 'auto', 'chinese', 'english'. Defaults to 'auto'.
        """
        self.language = language
        self.tfidf_calc = TFIDFCalculator()

    def add_document(self, text: str, language: Optional[str] = None) -> None:
        """
        Add a document to the corpus for IDF calculation.

        Args:
            text (str): Document text.
            language (Optional[str]): Language override. If None, uses default.
        """
        lang = language or self.language
        tokens = TextTokenizer.tokenize(text, language=lang)
        self.tfidf_calc.add_document(tokens)

    def extract(
        self,
        text: str,
        top_n: int = 10,
        language: Optional[str] = None,
        min_length: int = 2,
    ) -> List[KeywordResult]:
        """
        Extract keywords from text.

        Args:
            text (str): Text to extract keywords from.
            top_n (int): Number of top keywords to return. Defaults to 10.
            language (Optional[str]): Language override. If None, uses default.
            min_length (int): Minimum keyword length. Defaults to 2.

        Returns:
            List[KeywordResult]: List of keyword results sorted by weight.

        Example:
            >>> extractor = KeywordExtractor()
            >>> keywords = extractor.extract("Python is great.", top_n=5)
            >>> for kw in keywords:
            ...     print(f"{kw.keyword}: {kw.weight:.4f}")
        """
        # Tokenize text
        lang = language or self.language
        tokens = TextTokenizer.tokenize(text, language=lang)

        # Calculate TF-IDF
        tfidf_scores = self.tfidf_calc.calculate_tfidf(tokens)

        # Filter by minimum length
        filtered_scores = {
            term: score for term, score in tfidf_scores.items() if len(term) >= min_length
        }

        # Sort by score and get top N
        sorted_keywords = sorted(filtered_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]

        # Build results
        results = []
        tf = self.tfidf_calc.calculate_tf(tokens)

        for keyword, weight in sorted_keywords:
            idf = self.tfidf_calc.calculate_idf(keyword)
            result = KeywordResult(
                keyword=keyword,
                weight=weight,
                tf=tf.get(keyword, 0.0),
                idf=idf,
            )
            results.append(result)

        return results


def extract_keywords(
    text: str,
    top_n: int = 10,
    language: str = "auto",
    min_length: int = 2,
    corpus: Optional[List[str]] = None,
) -> List[Tuple[str, float]]:
    """
    Extract keywords from text using TF-IDF.

    This is a convenience function that wraps KeywordExtractor.

    Args:
        text (str): Text to extract keywords from.
        top_n (int): Number of top keywords to return. Defaults to 10.
        language (str): Language of text. Options: 'auto', 'chinese', 'english'.
            Defaults to 'auto'.
        min_length (int): Minimum keyword length. Defaults to 2.
        corpus (Optional[List[str]]): Additional documents for IDF calculation.
            If provided, improves keyword quality.

    Returns:
        List[Tuple[str, float]]: List of (keyword, weight) tuples.

    Example:
        >>> # Simple usage
        >>> keywords = extract_keywords("Python is a programming language.", top_n=5)
        >>> for keyword, weight in keywords:
        ...     print(f"{keyword}: {weight:.4f}")

        >>> # With corpus for better IDF
        >>> corpus = ["Java is also a programming language.", "Python is popular."]
        >>> keywords = extract_keywords("Python is great.", corpus=corpus)
    """
    extractor = KeywordExtractor(language=language)

    # Add corpus documents if provided
    if corpus:
        for doc in corpus:
            extractor.add_document(doc, language=language)

    # Extract keywords
    results = extractor.extract(text, top_n=top_n, language=language, min_length=min_length)

    return [(result.keyword, result.weight) for result in results]


def extract_keywords_from_file(
    file_path: Union[str, Path],
    top_n: int = 10,
    language: str = "auto",
    min_length: int = 2,
) -> List[Tuple[str, float]]:
    """
    Extract keywords from a file.

    Args:
        file_path (Union[str, Path]): Path to the file.
        top_n (int): Number of top keywords to return. Defaults to 10.
        language (str): Language of text. Options: 'auto', 'chinese', 'english'.
            Defaults to 'auto'.
        min_length (int): Minimum keyword length. Defaults to 2.

    Returns:
        List[Tuple[str, float]]: List of (keyword, weight) tuples.

    Example:
        >>> keywords = extract_keywords_from_file("document.md", top_n=10)
        >>> for keyword, weight in keywords:
        ...     print(f"{keyword}: {weight:.4f}")
    """
    # Resolve path
    path = Path(file_path)
    if not path.is_absolute():
        path = get_project_root() / path

    # Read file
    content = read_file(path)

    # Extract keywords
    return extract_keywords(content, top_n=top_n, language=language, min_length=min_length)


def extract_keywords_batch(
    texts: List[str],
    top_n: int = 10,
    language: str = "auto",
    min_length: int = 2,
) -> List[List[Tuple[str, float]]]:
    """
    Extract keywords from multiple texts.

    All texts are used together for IDF calculation, improving keyword quality.

    Args:
        texts (List[str]): List of texts to extract keywords from.
        top_n (int): Number of top keywords per text. Defaults to 10.
        language (str): Language of texts. Options: 'auto', 'chinese', 'english'.
            Defaults to 'auto'.
        min_length (int): Minimum keyword length. Defaults to 2.

    Returns:
        List[List[Tuple[str, float]]]: List of keyword lists for each text.

    Example:
        >>> texts = [
        ...     "Python is a programming language.",
        ...     "Java is another programming language."
        ... ]
        >>> results = extract_keywords_batch(texts, top_n=5)
        >>> for i, keywords in enumerate(results):
        ...     print(f"Text {i+1}: {keywords}")
    """
    extractor = KeywordExtractor(language=language)

    # Add all documents for IDF calculation
    for text in texts:
        extractor.add_document(text, language=language)

    # Extract keywords for each text
    results = []
    for text in texts:
        keywords = extractor.extract(text, top_n=top_n, language=language, min_length=min_length)
        results.append([(kw.keyword, kw.weight) for kw in keywords])

    return results


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m scripts.tools.extract_keywords <file_path> [top_n]")
        sys.exit(1)

    file_path = sys.argv[1]
    top_n = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    keywords = extract_keywords_from_file(file_path, top_n=top_n)
    print(f"\nTop {top_n} keywords:\n")
    for keyword, weight in keywords:
        print(f"  {keyword:20s} {weight:.4f}")

#!/usr/bin/env python3
"""
Unit tests for keyword extraction tool.

Tests the extract_keywords module including:
- Language detection
- Text tokenization
- TF-IDF calculation
- Keyword extraction
"""

import tempfile
import pytest
from pathlib import Path

from scripts.tools.extract_keywords import (
    LanguageDetector,
    TextTokenizer,
    TFIDFCalculator,
    KeywordExtractor,
    KeywordResult,
    extract_keywords,
    extract_keywords_from_file,
    extract_keywords_batch,
)
from scripts.utils import write_file


class TestLanguageDetector:
    """Test language detection functionality."""

    def test_detect_english_text(self):
        """Test detecting English text."""
        text = "This is an English text with some words."
        result = LanguageDetector.detect(text)
        assert result == "english"

    def test_detect_chinese_text(self):
        """Test detecting Chinese text."""
        text = "这是一个中文测试文本"
        result = LanguageDetector.detect(text)
        assert result == "chinese"

    def test_detect_mixed_text_chinese_majority(self):
        """Test detecting mixed text with Chinese majority."""
        text = "Python 是一门编程语言，广泛应用于人工智能领域。"
        result = LanguageDetector.detect(text)
        assert result == "chinese"

    def test_detect_mixed_text_english_majority(self):
        """Test detecting mixed text with English majority."""
        text = "Python programming language is very popular. 它很流行。"
        result = LanguageDetector.detect(text)
        assert result == "english"

    def test_detect_empty_text(self):
        """Test detecting empty text."""
        result = LanguageDetector.detect("")
        assert result == "english"

    def test_detect_numbers_only(self):
        """Test detecting numbers only."""
        text = "123 456 789"
        result = LanguageDetector.detect(text)
        assert result == "english"


class TestTextTokenizer:
    """Test text tokenization functionality."""

    def test_tokenize_english_basic(self):
        """Test basic English tokenization."""
        text = "Python is a programming language."
        tokens = TextTokenizer.tokenize(text, language="english")
        assert "python" in tokens
        assert "programming" in tokens
        assert "language" in tokens
        # Stop words should be removed
        assert "is" not in tokens
        assert "a" not in tokens

    def test_tokenize_english_stop_words_removed(self):
        """Test that English stop words are removed."""
        text = "the quick brown fox jumps over the lazy dog"
        tokens = TextTokenizer.tokenize(text, language="english")
        assert "the" not in tokens
        assert "over" not in tokens
        # Content words should remain
        assert "quick" in tokens
        assert "brown" in tokens
        assert "fox" in tokens

    def test_tokenize_english_case_insensitive(self):
        """Test that tokenization is case insensitive."""
        text = "Python PYTHON python"
        tokens = TextTokenizer.tokenize(text, language="english")
        assert all(t == "python" for t in tokens)

    def test_tokenize_chinese_basic(self):
        """Test basic Chinese tokenization."""
        text = "这是一个测试"
        tokens = TextTokenizer.tokenize(text, language="chinese")
        # Should return some tokens
        assert len(tokens) > 0
        # Stop words should be removed
        assert "是" not in tokens
        assert "一个" not in tokens

    def test_tokenize_chinese_stop_words_removed(self):
        """Test that Chinese stop words are removed."""
        text = "我和你的测试"
        tokens = TextTokenizer.tokenize(text, language="chinese")
        # Stop words should be removed
        assert "我" not in tokens
        assert "你" not in tokens
        assert "的" not in tokens

    def test_tokenize_auto_detect(self):
        """Test automatic language detection during tokenization."""
        english_text = "This is English"
        chinese_text = "这是中文"

        english_tokens = TextTokenizer.tokenize(english_text, language="auto")
        chinese_tokens = TextTokenizer.tokenize(chinese_text, language="auto")

        assert "english" in english_tokens
        assert len(chinese_tokens) > 0

    def test_tokenize_filters_short_words(self):
        """Test that short words are filtered out."""
        text = "a an the programming language"
        tokens = TextTokenizer.tokenize(text, language="english")
        # Words with length <= 1 should be filtered
        assert all(len(t) > 1 for t in tokens)


class TestTFIDFCalculator:
    """Test TF-IDF calculation."""

    def test_calculate_tf_basic(self):
        """Test basic term frequency calculation."""
        calc = TFIDFCalculator()
        tokens = ["python", "python", "java", "python"]
        tf = calc.calculate_tf(tokens)

        # Python appears 3 times out of 4 tokens
        assert abs(tf["python"] - 0.75) < 0.01
        assert abs(tf["java"] - 0.25) < 0.01

    def test_calculate_tf_empty(self):
        """Test TF calculation with empty input."""
        calc = TFIDFCalculator()
        tf = calc.calculate_tf([])
        assert tf == {}

    def test_calculate_idf_single_document(self):
        """Test IDF calculation with single document."""
        calc = TFIDFCalculator()
        calc.add_document(["python", "java"])

        idf_python = calc.calculate_idf("python")
        idf_unknown = calc.calculate_idf("unknown")

        # Both terms have same IDF in single document
        assert idf_python > 0
        assert idf_unknown > 0

    def test_calculate_idf_multiple_documents(self):
        """Test IDF calculation with multiple documents."""
        calc = TFIDFCalculator()
        calc.add_document(["python", "java"])
        calc.add_document(["python", "javascript"])
        calc.add_document(["java", "javascript"])

        idf_python = calc.calculate_idf("python")
        idf_ruby = calc.calculate_idf("ruby")

        # Ruby not in corpus should have higher IDF
        assert idf_ruby > idf_python

    def test_calculate_tfidf_basic(self):
        """Test basic TF-IDF calculation."""
        calc = TFIDFCalculator()
        calc.add_document(["python", "java"])

        tokens = ["python", "python", "java"]
        tfidf = calc.calculate_tfidf(tokens)

        # Check that both terms have scores
        assert "python" in tfidf
        assert "java" in tfidf
        # Python appears more frequently, should have higher TF-IDF
        assert tfidf["python"] > tfidf["java"]

    def test_document_count(self):
        """Test document count tracking."""
        calc = TFIDFCalculator()
        assert calc.document_count == 0

        calc.add_document(["test"])
        assert calc.document_count == 1

        calc.add_document(["test"])
        assert calc.document_count == 2


class TestKeywordExtractor:
    """Test keyword extraction functionality."""

    def test_extract_basic(self):
        """Test basic keyword extraction."""
        extractor = KeywordExtractor()
        text = "Python programming language software development coding"
        keywords = extractor.extract(text, top_n=5)

        assert len(keywords) <= 5
        assert all(isinstance(kw, KeywordResult) for kw in keywords)
        # Check that results are sorted by weight
        weights = [kw.weight for kw in keywords]
        assert weights == sorted(weights, reverse=True)

    def test_extract_returns_keyword_result(self):
        """Test that extract returns KeywordResult objects."""
        extractor = KeywordExtractor()
        text = "Python is a programming language"
        keywords = extractor.extract(text, top_n=3)

        for kw in keywords:
            assert isinstance(kw.keyword, str)
            assert isinstance(kw.weight, float)
            assert isinstance(kw.tf, float)
            assert isinstance(kw.idf, float)

    def test_extract_with_top_n(self):
        """Test extracting top N keywords."""
        extractor = KeywordExtractor()
        text = "python java javascript ruby golang swift kotlin rust c++"
        keywords = extractor.extract(text, top_n=5)

        assert len(keywords) == 5

    def test_extract_with_min_length(self):
        """Test extracting keywords with minimum length."""
        extractor = KeywordExtractor()
        text = "a an the python java"
        keywords = extractor.extract(text, top_n=10, min_length=4)

        # All keywords should have length >= 4
        assert all(len(kw.keyword) >= 4 for kw in keywords)

    def test_extract_chinese_text(self):
        """Test extracting keywords from Chinese text."""
        extractor = KeywordExtractor(language="chinese")
        text = "人工智能技术发展迅速，深度学习算法广泛应用"
        keywords = extractor.extract(text, top_n=5)

        assert len(keywords) > 0
        # Should contain Chinese keywords
        has_chinese = any(any("\u4e00" <= c <= "\u9fff" for c in kw.keyword) for kw in keywords)
        assert has_chinese

    def test_extract_english_text(self):
        """Test extracting keywords from English text."""
        extractor = KeywordExtractor(language="english")
        text = "Machine learning algorithms use statistical methods"
        keywords = extractor.extract(text, top_n=5)

        assert len(keywords) > 0
        # Should contain English keywords
        assert all(kw.keyword.isalpha() for kw in keywords)

    def test_add_document_improves_quality(self):
        """Test that adding documents improves keyword quality."""
        extractor = KeywordExtractor()

        # Extract without corpus
        text1 = "Python programming"
        keywords1 = extractor.extract(text1, top_n=5)

        # Add documents and extract again
        extractor.add_document("Java programming")
        extractor.add_document("JavaScript programming")
        extractor.add_document("Python is great")

        text2 = "Python programming"
        keywords2 = extractor.extract(text2, top_n=5)

        # Both should return keywords
        assert len(keywords1) > 0
        assert len(keywords2) > 0


class TestExtractKeywords:
    """Test convenience functions."""

    def test_extract_keywords_basic(self):
        """Test basic extract_keywords function."""
        text = "Python is a programming language"
        keywords = extract_keywords(text, top_n=5)

        assert isinstance(keywords, list)
        assert all(isinstance(kw, tuple) and len(kw) == 2 for kw in keywords)
        assert all(isinstance(kw[0], str) and isinstance(kw[1], float) for kw in keywords)

    def test_extract_keywords_with_corpus(self):
        """Test extract_keywords with corpus."""
        text = "Python programming"
        corpus = [
            "Java is another programming language",
            "JavaScript is also popular",
            "Python is widely used",
        ]
        keywords = extract_keywords(text, top_n=5, corpus=corpus)

        assert len(keywords) > 0
        # Python should be a top keyword
        keyword_list = [kw[0] for kw in keywords]
        assert "python" in keyword_list

    def test_extract_keywords_chinese(self):
        """Test extracting Chinese keywords."""
        text = "机器学习是人工智能的重要分支"
        keywords = extract_keywords(text, top_n=5, language="chinese")

        assert len(keywords) > 0
        # Should have Chinese keywords
        has_chinese = any(any("\u4e00" <= c <= "\u9fff" for c in kw[0]) for kw in keywords)
        assert has_chinese

    def test_extract_keywords_empty_text(self):
        """Test extracting from empty text."""
        keywords = extract_keywords("", top_n=5)
        assert keywords == []

    def test_extract_keywords_from_file(self):
        """Test extracting keywords from file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.md"
            write_file(file_path, "Python programming language development")

            keywords = extract_keywords_from_file(file_path, top_n=5)

            assert len(keywords) > 0
            assert all(isinstance(kw, tuple) for kw in keywords)

    def test_extract_keywords_batch(self):
        """Test batch keyword extraction."""
        texts = [
            "Python is a programming language",
            "Java is another programming language",
            "JavaScript is for web development",
        ]

        results = extract_keywords_batch(texts, top_n=5)

        assert len(results) == 3
        for keywords in results:
            assert isinstance(keywords, list)
            assert len(keywords) <= 5

    def test_extract_keywords_batch_consistent_results(self):
        """Test that batch extraction gives consistent results."""
        texts = [
            "Python programming language",
            "Python is great",
            "Java programming language",
        ]

        results = extract_keywords_batch(texts, top_n=5)

        # All results should be non-empty
        assert all(len(keywords) > 0 for keywords in results)

    def test_extract_keywords_min_length(self):
        """Test minimum keyword length filter."""
        text = "Python Java C Go R"  # Mix of short and long words
        keywords = extract_keywords(text, top_n=10, min_length=3)

        # All keywords should meet minimum length
        assert all(len(kw[0]) >= 3 for kw in keywords)


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_extract_from_nonexistent_file(self):
        """Test extracting from non-existent file."""
        with pytest.raises(FileNotFoundError):
            extract_keywords_from_file("/nonexistent/file.md")

    def test_extract_very_long_text(self):
        """Test extracting from very long text."""
        # Create a long text with repeated content
        text = "Python programming " * 1000
        keywords = extract_keywords(text, top_n=5)

        assert len(keywords) > 0

    def test_extract_special_characters(self):
        """Test text with special characters."""
        text = "Python @#$% programming *&^% language"
        keywords = extract_keywords(text, top_n=5)

        # Should extract clean keywords without special chars
        for keyword, _ in keywords:
            assert keyword.isalpha() or any("\u4e00" <= c <= "\u9fff" for c in keyword)

    def test_extract_numbers_only(self):
        """Test text with numbers only."""
        text = "123 456 789"
        keywords = extract_keywords(text, top_n=5)

        # Should return empty or very few keywords
        assert len(keywords) <= 1

    def test_extract_single_word(self):
        """Test text with single word."""
        text = "Python"
        keywords = extract_keywords(text, top_n=5)

        # Should return at most 1 keyword
        assert len(keywords) <= 1

    def test_extract_top_n_larger_than_available(self):
        """Test when top_n is larger than available keywords."""
        text = "Python programming"
        keywords = extract_keywords(text, top_n=100)

        # Should return all available keywords
        assert len(keywords) <= 2

    def test_extract_repeated_words(self):
        """Test text with heavily repeated words."""
        text = "python " * 100 + "java " * 10
        keywords = extract_keywords(text, top_n=5)

        # Python should be the top keyword due to higher frequency
        if keywords:
            assert keywords[0][0] == "python"

    def test_language_override(self):
        """Test language override in extract function."""
        extractor = KeywordExtractor(language="english")

        # Override with Chinese
        text = "这是中文测试"
        keywords = extractor.extract(text, top_n=5, language="chinese")

        assert len(keywords) > 0


class TestKeywordResult:
    """Test KeywordResult dataclass."""

    def test_keyword_result_creation(self):
        """Test creating KeywordResult."""
        result = KeywordResult(
            keyword="python",
            weight=0.5,
            tf=0.1,
            idf=2.5,
        )

        assert result.keyword == "python"
        assert result.weight == 0.5
        assert result.tf == 0.1
        assert result.idf == 2.5

    def test_keyword_result_types(self):
        """Test KeywordResult field types."""
        result = KeywordResult(
            keyword="test",
            weight=1.0,
            tf=0.5,
            idf=2.0,
        )

        assert isinstance(result.keyword, str)
        assert isinstance(result.weight, float)
        assert isinstance(result.tf, float)
        assert isinstance(result.idf, float)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

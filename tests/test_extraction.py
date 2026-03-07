#!/usr/bin/env python3
"""
Unit tests for text extraction tools.

This module tests the keyword extraction and summary generation functions.
"""

import pytest
from scripts.tools.extraction import (
    extract_keywords,
    extract_keywords_tfidf,
    extract_keywords_textrank,
    generate_summary,
)


# Test data
CHINESE_TEXT_SHORT = "Python是一种高级编程语言，广泛应用于Web开发、数据科学和人工智能领域。"

CHINESE_TEXT_LONG = """
Python是一种高级编程语言，由Guido van Rossum于1991年首次发布。
Python的设计哲学强调代码的可读性和简洁性，它的语法允许程序员用更少的代码行表达概念。
Python支持多种编程范式，包括面向对象、命令式、函数式和过程式编程。
它拥有一个大型标准库，提供了丰富的功能，如字符串处理、文档操作、网络协议等。
Python广泛应用于Web开发、数据科学、人工智能、科学计算、自动化运维等领域。
Python的流行度在过去几年持续上升，成为最受欢迎的编程语言之一。
"""

ENGLISH_TEXT = """
Python is a high-level programming language. It is widely used in web development,
data science, and artificial intelligence. Python's syntax is clear and concise,
making it easy to learn and use. It has a large standard library that provides
many useful functions. Python is one of the most popular programming languages today.
"""

MIXED_TEXT = """
Python是一种高级编程语言，被广泛应用于Web开发和数据科学。
Python has a clear syntax and is easy to learn.
它的标准库非常丰富，提供了很多实用功能。
Python is also popular in AI and machine learning fields.
"""


class TestExtractKeywordsTFIDF:
    """Test cases for TF-IDF keyword extraction."""
    
    def test_basic_extraction(self):
        """Test basic keyword extraction with TF-IDF."""
        result = extract_keywords_tfidf(CHINESE_TEXT_SHORT, top_n=5)
        
        assert isinstance(result, list)
        assert len(result) <= 5
        assert all('keyword' in item for item in result)
        assert all('score' in item for item in result)
        assert all(isinstance(item['keyword'], str) for item in result)
        assert all(isinstance(item['score'], float) for item in result)
    
    def test_returns_keywords_for_chinese(self):
        """Test that TF-IDF extracts relevant Chinese keywords."""
        result = extract_keywords_tfidf(CHINESE_TEXT_LONG, top_n=10)
        
        # Should extract some keywords
        assert len(result) > 0
        
        # Check that scores are normalized
        assert all(0 <= item['score'] <= 1 for item in result)
        
        # Check that keywords are sorted by score
        scores = [item['score'] for item in result]
        assert scores == sorted(scores, reverse=True)
    
    def test_empty_text(self):
        """Test TF-IDF with empty text."""
        result = extract_keywords_tfidf("", top_n=5)
        assert result == []
        
        result = extract_keywords_tfidf("   ", top_n=5)
        assert result == []
    
    def test_single_word(self):
        """Test TF-IDF with single word."""
        result = extract_keywords_tfidf("Python", top_n=5)
        # Single word should still be extracted (Python has 6 chars)
        assert len(result) == 1
        assert result[0]['keyword'] == 'python'
        assert result[0]['score'] == 1.0
    
    def test_stop_words_filtered(self):
        """Test that stop words are filtered out."""
        text = "这是一个测试的内容"
        result = extract_keywords_tfidf(text, top_n=5)
        
        # Stop words like '的' should be filtered
        keywords = [item['keyword'] for item in result]
        # Common stop words should not appear
        assert '的' not in keywords


class TestExtractKeywordsTextRank:
    """Test cases for TextRank keyword extraction."""
    
    def test_basic_extraction(self):
        """Test basic keyword extraction with TextRank."""
        result = extract_keywords_textrank(CHINESE_TEXT_SHORT, top_n=5)
        
        assert isinstance(result, list)
        assert len(result) <= 5
        assert all('keyword' in item for item in result)
        assert all('score' in item for item in result)
    
    def test_returns_keywords_for_chinese(self):
        """Test that TextRank extracts relevant Chinese keywords."""
        result = extract_keywords_textrank(CHINESE_TEXT_LONG, top_n=10)
        
        # Should extract some keywords
        assert len(result) > 0
        
        # Check that scores are normalized
        assert all(0 <= item['score'] <= 1 for item in result)
    
    def test_empty_text(self):
        """Test TextRank with empty text."""
        result = extract_keywords_textrank("", top_n=5)
        assert result == []
    
    def test_custom_window_size(self):
        """Test TextRank with custom window size."""
        result_default = extract_keywords_textrank(
            CHINESE_TEXT_LONG,
            top_n=5,
            window_size=4
        )
        result_custom = extract_keywords_textrank(
            CHINESE_TEXT_LONG,
            top_n=5,
            window_size=8
        )
        
        # Both should return results
        assert len(result_default) > 0
        assert len(result_custom) > 0
    
    def test_custom_damping(self):
        """Test TextRank with custom damping factor."""
        result = extract_keywords_textrank(
            CHINESE_TEXT_LONG,
            top_n=5,
            damping=0.9
        )
        
        assert isinstance(result, list)
        assert len(result) > 0


class TestExtractKeywords:
    """Test cases for the unified extract_keywords function."""
    
    def test_tfidf_method(self):
        """Test extract_keywords with TF-IDF method."""
        result = extract_keywords(CHINESE_TEXT_SHORT, method="tfidf", top_n=5)
        
        assert isinstance(result, list)
        assert len(result) <= 5
    
    def test_textrank_method(self):
        """Test extract_keywords with TextRank method."""
        result = extract_keywords(CHINESE_TEXT_SHORT, method="textrank", top_n=5)
        
        assert isinstance(result, list)
        assert len(result) <= 5
    
    def test_case_insensitive_method(self):
        """Test that method parameter is case-insensitive."""
        result1 = extract_keywords(CHINESE_TEXT_SHORT, method="TFIDF", top_n=5)
        result2 = extract_keywords(CHINESE_TEXT_SHORT, method="tfidf", top_n=5)
        
        # Should return same results
        assert len(result1) == len(result2)
    
    def test_invalid_method(self):
        """Test that invalid method raises ValueError."""
        with pytest.raises(ValueError, match="Invalid method"):
            extract_keywords(CHINESE_TEXT_SHORT, method="invalid")
    
    def test_empty_text(self):
        """Test with empty text."""
        result = extract_keywords("", method="tfidf")
        assert result == []
    
    def test_passes_kwargs_to_tfidf(self):
        """Test that kwargs are passed to TF-IDF function."""
        result = extract_keywords(
            CHINESE_TEXT_LONG,
            method="tfidf",
            top_n=8,
            min_df=1
        )
        
        assert isinstance(result, list)
        assert len(result) <= 8
    
    def test_passes_kwargs_to_textrank(self):
        """Test that kwargs are passed to TextRank function."""
        result = extract_keywords(
            CHINESE_TEXT_LONG,
            method="textrank",
            top_n=8,
            window_size=6
        )
        
        assert isinstance(result, list)
        assert len(result) <= 8


class TestGenerateSummary:
    """Test cases for summary generation."""
    
    def test_basic_summary(self):
        """Test basic summary generation."""
        result = generate_summary(CHINESE_TEXT_LONG)
        
        assert isinstance(result, dict)
        assert 'summary' in result
        assert 'key_sentences' in result
        assert isinstance(result['summary'], str)
        assert isinstance(result['key_sentences'], list)
    
    def test_max_length_constraint(self):
        """Test summary with max_length constraint."""
        max_len = 100
        result = generate_summary(CHINESE_TEXT_LONG, max_length=max_len)
        
        assert len(result['summary']) <= max_len + 1  # +1 for punctuation
    
    def test_max_sentences_constraint(self):
        """Test summary with max_sentences constraint."""
        max_sent = 2
        result = generate_summary(CHINESE_TEXT_LONG, max_sentences=max_sent)
        
        assert len(result['key_sentences']) <= max_sent
    
    def test_empty_text(self):
        """Test with empty text."""
        result = generate_summary("")
        
        assert result['summary'] == ''
        assert result['key_sentences'] == []
    
    def test_whitespace_only(self):
        """Test with whitespace-only text."""
        result = generate_summary("   \n   \t   ")
        
        assert result['summary'] == ''
        assert result['key_sentences'] == []
    
    def test_single_sentence(self):
        """Test with single sentence."""
        text = "这是一个简单的句子。"
        result = generate_summary(text)
        
        # Summary should contain the sentence content (punctuation may be stripped)
        assert '这是一个简单的句子' in result['summary']
        assert len(result['key_sentences']) == 1
    
    def test_short_text(self):
        """Test with very short text."""
        text = "短文本测试。"
        result = generate_summary(text, max_sentences=3)
        
        assert isinstance(result['summary'], str)
        assert len(result['key_sentences']) > 0
    
    def test_mixed_language(self):
        """Test with mixed Chinese and English text."""
        result = generate_summary(MIXED_TEXT)
        
        assert isinstance(result['summary'], str)
        assert len(result['summary']) > 0
    
    def test_custom_damping(self):
        """Test with custom damping factor."""
        result = generate_summary(CHINESE_TEXT_LONG, damping=0.9)
        
        assert isinstance(result['summary'], str)
        assert len(result['key_sentences']) > 0
    
    def test_key_sentences_order(self):
        """Test that key_sentences maintain some original order."""
        result = generate_summary(CHINESE_TEXT_LONG, max_sentences=3)
        
        # All returned sentences should be in the original text
        for sent in result['key_sentences']:
            assert sent in CHINESE_TEXT_LONG


class TestPerformance:
    """Performance tests."""
    
    def test_tfidf_performance(self):
        """Test TF-IDF performance with 1000 chars."""
        import time
        
        # Create a 1000-character text
        text = CHINESE_TEXT_LONG * 10
        text = text[:1000]
        
        start = time.time()
        result = extract_keywords_tfidf(text, top_n=10)
        elapsed = time.time() - start
        
        # Should complete in less than 1 second
        assert elapsed < 1.0
        assert len(result) > 0
    
    def test_textrank_performance(self):
        """Test TextRank performance with 1000 chars."""
        import time
        
        # Create a 1000-character text
        text = CHINESE_TEXT_LONG * 10
        text = text[:1000]
        
        start = time.time()
        result = extract_keywords_textrank(text, top_n=10)
        elapsed = time.time() - start
        
        # Should complete in less than 1 second
        assert elapsed < 1.0
        assert len(result) > 0
    
    def test_summary_performance(self):
        """Test summary generation performance with 1000 chars."""
        import time
        
        # Create a 1000-character text
        text = CHINESE_TEXT_LONG * 10
        text = text[:1000]
        
        start = time.time()
        result = generate_summary(text)
        elapsed = time.time() - start
        
        # Should complete in less than 5 seconds
        assert elapsed < 5.0
        assert len(result['summary']) > 0


class TestEdgeCases:
    """Edge case tests."""
    
    def test_special_characters(self):
        """Test with special characters."""
        text = "Python！Python？Python。Python，Python；"
        result = extract_keywords(text, method="tfidf")
        
        assert isinstance(result, list)
    
    def test_numbers_in_text(self):
        """Test with numbers in text."""
        text = "2024年Python编程语言排名第1，有超过1000万开发者使用。"
        result = extract_keywords(text, method="tfidf")
        
        assert isinstance(result, list)
    
    def test_very_long_word(self):
        """Test with very long word."""
        text = "这是一个非常长的词语测试"
        result = extract_keywords(text, method="tfidf")
        
        assert isinstance(result, list)
    
    def test_repeated_words(self):
        """Test with repeated words."""
        text = "Python Python Python 编程 编程 语言 语言"
        result = extract_keywords(text, method="tfidf", top_n=5)
        
        assert isinstance(result, list)
        # Should not duplicate keywords
        keywords = [item['keyword'] for item in result]
        assert len(keywords) == len(set(keywords))
    
    def test_only_stopwords(self):
        """Test with only stop words."""
        text = "的 的 的 了 了 了 是 是 是"
        result = extract_keywords(text, method="tfidf")
        
        assert result == []
    
    def test_mixed_punctuation(self):
        """Test summary with mixed punctuation."""
        text = "第一句。第二句！第三句？第四句。"
        result = generate_summary(text, max_sentences=3)
        
        assert isinstance(result['summary'], str)
        assert len(result['key_sentences']) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

#!/usr/bin/env python3
"""
Text Extraction Tools.

This module provides functions for extracting keywords and generating
summaries from Chinese text documents.

Example:
    >>> from scripts.tools.extraction import extract_keywords, generate_summary
    >>>
    >>> # Extract keywords using TF-IDF
    >>> keywords = extract_keywords(
    ...     text="Python是一种高级编程语言...",
    ...     method="tfidf",
    ...     top_n=10
    ... )
    >>>
    >>> # Generate summary
    >>> summary = generate_summary(
    ...     text="Python是一种高级编程语言...",
    ...     max_length=200
    ... )
"""

import re
import string
from collections import Counter
from typing import List, Dict, Tuple, Optional

import jieba
import jieba.analyse
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer


# Chinese and English stop words
STOP_WORDS = set([
    # Chinese stop words
    '的', '了', '和', '是', '就', '都', '而', '及', '与', '着',
    '或', '一个', '没有', '我们', '你们', '他们', '它们', '这个',
    '那个', '之', '也', '在', '有', '上', '中', '下', '为',
    '以', '于', '不', '人', '这', '我', '他', '她', '它',
    '个', '们', '到', '说', '要', '去', '能', '对', '把',
    '从', '被', '比', '但', '因', '所', '让', '给', '很',
    '又', '还', '才', '用', '做', '着', '过', '来', '看',
    # English stop words
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
    'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are',
    'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do',
    'does', 'did', 'will', 'would', 'could', 'should', 'may',
    'might', 'must', 'can', 'this', 'that', 'these', 'those',
])


def _preprocess_text(text: str) -> str:
    """
    Preprocess text by removing extra whitespace and normalizing.
    
    Args:
        text (str): Input text to preprocess.
        
    Returns:
        str: Preprocessed text.
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing whitespace
    text = text.strip()
    return text


def _segment_text(text: str) -> List[str]:
    """
    Segment Chinese text into words using jieba.
    
    Args:
        text (str): Input text to segment.
        
    Returns:
        List[str]: List of words.
    """
    # Use jieba for Chinese word segmentation
    words = jieba.cut(text, cut_all=False)
    # Filter out stop words and single-character words
    filtered_words = [
        word.strip() for word in words
        if word.strip() and len(word.strip()) > 1
        and word.strip() not in STOP_WORDS
        and not word.strip().isdigit()
        and word.strip() not in string.punctuation
    ]
    return filtered_words


def _segment_sentences(text: str) -> List[str]:
    """
    Segment text into sentences.
    
    Args:
        text (str): Input text to segment.
        
    Returns:
        List[str]: List of sentences.
    """
    # Chinese and English sentence delimiters
    sentence_delimiters = r'[。！？!?.;；\n]+'
    # Split text into sentences
    sentences = re.split(sentence_delimiters, text)
    # Filter out empty sentences
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences


def extract_keywords_tfidf(
    text: str,
    top_n: int = 10,
    min_df: int = 1,
) -> List[Dict[str, float]]:
    """
    Extract keywords using TF-IDF algorithm.
    
    Args:
        text (str): Input text to extract keywords from.
        top_n (int): Number of top keywords to return. Defaults to 10.
        min_df (int): Minimum document frequency for TF-IDF. Defaults to 1.
        
    Returns:
        List[Dict[str, float]]: List of keywords with scores.
            Each item is a dict with 'keyword' and 'score' keys.
            
    Example:
        >>> keywords = extract_keywords_tfidf(
        ...     text="Python是一种高级编程语言，广泛应用于Web开发。",
        ...     top_n=5
        ... )
    """
    # Preprocess text
    text = _preprocess_text(text)
    
    # Segment text into words
    words = _segment_text(text)
    
    if not words:
        return []
    
    # For single document, we treat it as one document in a corpus
    # Join words back with spaces for TfidfVectorizer
    doc = ' '.join(words)
    
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        min_df=min_df,
        max_features=top_n * 2,  # Get more features for better selection
        token_pattern=r'(?u)\b\w+\b',  # Match any word
    )
    
    try:
        # Fit and transform the document
        tfidf_matrix = vectorizer.fit_transform([doc])
        
        # Get feature names and scores
        feature_names = vectorizer.get_feature_names_out()
        scores = tfidf_matrix.toarray()[0]
        
        # Create list of (word, score) tuples
        word_scores = list(zip(feature_names, scores))
        
        # Sort by score and get top_n
        word_scores.sort(key=lambda x: x[1], reverse=True)
        top_keywords = word_scores[:top_n]
        
        # Format results
        results = [
            {'keyword': word, 'score': round(float(score), 4)}
            for word, score in top_keywords
            if score > 0
        ]
        
        return results
        
    except Exception:
        # Fallback: return most frequent words
        word_freq = Counter(words)
        top_words = word_freq.most_common(top_n)
        return [
            {'keyword': word, 'score': round(count / len(words), 4)}
            for word, count in top_words
        ]


def extract_keywords_textrank(
    text: str,
    top_n: int = 10,
    window_size: int = 4,
    damping: float = 0.85,
    max_iter: int = 100,
) -> List[Dict[str, float]]:
    """
    Extract keywords using TextRank algorithm.
    
    Args:
        text (str): Input text to extract keywords from.
        top_n (int): Number of top keywords to return. Defaults to 10.
        window_size (int): Co-occurrence window size. Defaults to 4.
        damping (float): Damping factor for PageRank. Defaults to 0.85.
        max_iter (int): Maximum iterations for PageRank. Defaults to 100.
        
    Returns:
        List[Dict[str, float]]: List of keywords with scores.
            Each item is a dict with 'keyword' and 'score' keys.
            
    Example:
        >>> keywords = extract_keywords_textrank(
        ...     text="Python是一种高级编程语言，广泛应用于Web开发。",
        ...     top_n=5
        ... )
    """
    # Preprocess text
    text = _preprocess_text(text)
    
    # Segment text into words
    words = _segment_text(text)
    
    if len(words) < 2:
        return []
    
    # Build word co-occurrence graph
    graph = nx.Graph()
    
    # Add edges based on co-occurrence within window
    for i in range(len(words)):
        for j in range(i + 1, min(i + window_size, len(words))):
            if words[i] != words[j]:
                if graph.has_edge(words[i], words[j]):
                    graph[words[i]][words[j]]['weight'] += 1.0
                else:
                    graph.add_edge(words[i], words[j], weight=1.0)
    
    if len(graph.nodes()) == 0:
        return []
    
    # Calculate PageRank scores
    try:
        scores = nx.pagerank(
            graph,
            alpha=damping,
            max_iter=max_iter,
            weight='weight'
        )
        
        # Sort by score and get top_n
        sorted_words = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_n]
        
        # Format results
        results = [
            {'keyword': word, 'score': round(float(score), 4)}
            for word, score in sorted_words
        ]
        
        return results
        
    except Exception:
        # Fallback: return most frequent words
        word_freq = Counter(words)
        top_words = word_freq.most_common(top_n)
        return [
            {'keyword': word, 'score': round(count / len(words), 4)}
            for word, count in top_words
        ]


def extract_keywords(
    text: str,
    method: str = "tfidf",
    top_n: int = 10,
    **kwargs
) -> List[Dict[str, float]]:
    """
    Extract keywords from text using specified method.
    
    Args:
        text (str): Input text to extract keywords from.
        method (str): Extraction method. Options: 'tfidf', 'textrank'.
            Defaults to 'tfidf'.
        top_n (int): Number of top keywords to return. Defaults to 10.
        **kwargs: Additional parameters passed to the specific method.
            For TF-IDF: min_df
            For TextRank: window_size, damping, max_iter
            
    Returns:
        List[Dict[str, float]]: List of keywords with scores.
            Each item is a dict with 'keyword' and 'score' keys.
            
    Raises:
        ValueError: If an invalid method is specified.
        
    Example:
        >>> # Using TF-IDF
        >>> keywords = extract_keywords(
        ...     text="Python是一种高级编程语言，广泛应用于Web开发。",
        ...     method="tfidf",
        ...     top_n=5
        ... )
        >>> 
        >>> # Using TextRank
        >>> keywords = extract_keywords(
        ...     text="Python是一种高级编程语言...",
        ...     method="textrank",
        ...     top_n=10,
        ...     window_size=5
        ... )
    """
    if not text or not text.strip():
        return []
    
    method = method.lower()
    
    if method == "tfidf":
        return extract_keywords_tfidf(text, top_n=top_n, **kwargs)
    elif method == "textrank":
        return extract_keywords_textrank(text, top_n=top_n, **kwargs)
    else:
        raise ValueError(
            f"Invalid method '{method}'. "
            f"Supported methods: 'tfidf', 'textrank'"
        )


def _sentence_similarity(sent1: str, sent2: str) -> float:
    """
    Calculate similarity between two sentences based on word overlap.
    
    Args:
        sent1 (str): First sentence.
        sent2 (str): Second sentence.
        
    Returns:
        float: Similarity score between 0 and 1.
    """
    words1 = set(_segment_text(sent1))
    words2 = set(_segment_text(sent2))
    
    if not words1 or not words2:
        return 0.0
    
    # Calculate Jaccard similarity
    intersection = words1 & words2
    union = words1 | words2
    
    if not union:
        return 0.0
    
    return len(intersection) / len(union)


def generate_summary(
    text: str,
    max_length: Optional[int] = None,
    max_sentences: Optional[int] = None,
    method: str = "textrank",
    damping: float = 0.85,
    max_iter: int = 100,
) -> Dict[str, any]:
    """
    Generate summary from text using extractive summarization.
    
    Args:
        text (str): Input text to summarize.
        max_length (Optional[int]): Maximum length of summary in characters.
            If None, no length limit is applied.
        max_sentences (Optional[int]): Maximum number of sentences in summary.
            If None, defaults to 3 or calculated based on text length.
        method (str): Summarization method. Currently only 'textrank' is
            supported. Defaults to 'textrank'.
        damping (float): Damping factor for TextRank. Defaults to 0.85.
        max_iter (int): Maximum iterations for TextRank. Defaults to 100.
            
    Returns:
        Dict[str, any]: Dictionary containing:
            - 'summary' (str): Generated summary text
            - 'key_sentences' (List[str]): List of key sentences used
            
    Raises:
        ValueError: If text is empty or invalid method is specified.
        
    Example:
        >>> result = generate_summary(
        ...     text="Python是一种高级编程语言。它广泛应用于Web开发。",
        ...     max_length=50
        ... )
        >>> print(result['summary'])
    """
    if not text or not text.strip():
        return {
            'summary': '',
            'key_sentences': []
        }
    
    # Preprocess text
    text = _preprocess_text(text)
    
    # Segment into sentences
    sentences = _segment_sentences(text)
    
    if not sentences:
        return {
            'summary': '',
            'key_sentences': []
        }
    
    # If only one sentence, return it
    if len(sentences) == 1:
        return {
            'summary': sentences[0],
            'key_sentences': sentences
        }
    
    # Determine max_sentences if not specified
    if max_sentences is None:
        # Default: extract 3 sentences or 30% of total, whichever is larger
        max_sentences = max(3, int(len(sentences) * 0.3))
    
    # Build sentence similarity graph
    graph = nx.Graph()
    
    # Add nodes
    for i in range(len(sentences)):
        graph.add_node(i)
    
    # Add edges based on sentence similarity
    for i in range(len(sentences)):
        for j in range(i + 1, len(sentences)):
            similarity = _sentence_similarity(sentences[i], sentences[j])
            if similarity > 0:
                graph.add_edge(i, j, weight=similarity)
    
    # Calculate TextRank scores for sentences
    if len(graph.edges()) == 0:
        # If no edges, return first few sentences
        selected_indices = list(range(min(max_sentences, len(sentences))))
    else:
        try:
            scores = nx.pagerank(
                graph,
                alpha=damping,
                max_iter=max_iter,
                weight='weight'
            )
            
            # Sort sentences by score
            ranked_sentences = sorted(
                scores.items(),
                key=lambda x: x[1],
                reverse=True
            )
            
            # Select top sentences, maintaining original order
            selected_indices = [idx for idx, _ in ranked_sentences[:max_sentences]]
            selected_indices.sort()
            
        except Exception:
            # Fallback: return first few sentences
            selected_indices = list(range(min(max_sentences, len(sentences))))
    
    # Build summary from selected sentences
    key_sentences = [sentences[i] for i in selected_indices]
    summary = ''.join(key_sentences)
    
    # Apply length constraint if specified
    if max_length and len(summary) > max_length:
        # Truncate summary to max_length
        summary = summary[:max_length]
        
        # Try to end at a complete sentence
        last_period = max(
            summary.rfind('。'),
            summary.rfind('.'),
            summary.rfind('！'),
            summary.rfind('!'),
            summary.rfind('？'),
            summary.rfind('?')
        )
        if last_period > max_length * 0.7:
            summary = summary[:last_period + 1]
    
    return {
        'summary': summary,
        'key_sentences': key_sentences
    }


__all__ = [
    'extract_keywords',
    'extract_keywords_tfidf',
    'extract_keywords_textrank',
    'generate_summary',
]

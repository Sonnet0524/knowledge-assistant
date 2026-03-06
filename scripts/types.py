#!/usr/bin/env python3
"""
Document Metadata Type Definitions.

This module defines the core data structures for document metadata
used throughout the Knowledge Assistant system.

Example:
    >>> from scripts.types import DocumentMetadata
    >>> from datetime import date
    >>>
    >>> metadata = DocumentMetadata(
    ...     title="Research Note",
    ...     date=date(2026, 3, 5),
    ...     tags=["python", "testing"],
    ...     author="Agent B"
    ... )
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import date  # noqa: F401 - Used in type annotations


@dataclass
class DocumentMetadata:
    """
    Document metadata structure.

    Represents the metadata for a document, including required fields
    like title and date, and optional fields like tags, author, type,
    and status.

    Attributes:
        title (str): The document title. Required.
        date (date): The document creation date. Required.
        tags (Optional[List[str]]): List of tags for categorization.
            Optional.
        author (Optional[str]): The document author. Optional.
        type (Optional[str]): The document type (e.g., 'research',
            'meeting'). Optional.
        status (Optional[str]): The document status (e.g., 'draft',
            'published'). Optional.

    Example:
        >>> metadata = DocumentMetadata(
        ...     title="My Document",
        ...     date=date(2026, 3, 5)
        ... )
        >>> metadata.title
        'My Document'

        >>> metadata_with_tags = DocumentMetadata(
        ...     title="Research Note",
        ...     date=date(2026, 3, 5),
        ...     tags=["python", "testing"]
        ... )
        >>> metadata_with_tags.tags
        ['python', 'testing']
    """

    title: str
    date: date
    tags: Optional[List[str]] = None
    author: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None

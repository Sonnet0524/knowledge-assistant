#!/usr/bin/env python3
"""
Metadata Parser Module.

This module provides functionality to parse and validate document metadata
from YAML frontmatter format.

Example:
    >>> from scripts.metadata_parser import MetadataParser
    >>>
    >>> parser = MetadataParser()
    >>> content = '''---
    ... title: Test Document
    ... date: 2026-03-05
    ... ---
    ...
    ... Body content.'''
    >>>
    >>> metadata, body = parser.parse(content)
    >>> is_valid, errors = parser.validate(metadata)
"""

import re
from typing import Dict, Any, Tuple, List, Optional
from datetime import datetime, date

import yaml


class MetadataParser:
    """
    Parse and validate document metadata from YAML frontmatter.

    This class provides methods to extract metadata from documents
    using YAML frontmatter format (delimited by ---) and validate
    the extracted metadata against required fields and types.

    Attributes:
        REQUIRED_FIELDS (List[str]): List of required field names.

    Example:
        >>> parser = MetadataParser()
        >>> content = '''---
        ... title: Test
        ... date: 2026-03-05
        ... ---
        ...
        ... Body'''
        >>> metadata, body = parser.parse(content)
        >>> metadata['title']
        'Test'
        >>> is_valid, errors = parser.validate(metadata)
        >>> is_valid
        True
    """

    REQUIRED_FIELDS = ["title", "date"]

    def __init__(self) -> None:
        """Initialize the MetadataParser."""
        self._frontmatter_pattern = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

    def parse(self, content: str) -> Tuple[Dict[str, Any], str]:
        """
        Parse YAML frontmatter from content.

        Extracts the YAML frontmatter (if present) and separates it
        from the document body.

        Args:
            content (str): The complete document content.

        Returns:
            Tuple[Dict[str, Any], str]: A tuple containing:
                - metadata (Dict[str, Any]): Parsed metadata dictionary.
                - body (str): The document body (content after frontmatter).

        Raises:
            yaml.YAMLError: If the frontmatter contains invalid YAML.

        Example:
            >>> parser = MetadataParser()
            >>> content = '''---
            ... title: Test
            ... date: 2026-03-05
            ... ---
            ...
            ... Body content.'''
            >>> metadata, body = parser.parse(content)
            >>> metadata['title']
            'Test'
            >>> 'Body content.' in body
            True
        """
        if not content or not content.strip():
            return {}, content

        match = self._frontmatter_pattern.match(content)

        if not match:
            return {}, content

        frontmatter_text = match.group(1)
        body = content[match.end() :]

        try:
            metadata = yaml.safe_load(frontmatter_text)
            if metadata is None:
                metadata = {}
            elif not isinstance(metadata, dict):
                metadata = {"_raw": metadata}
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Invalid YAML in frontmatter: {e}")

        return metadata, body

    def validate(self, metadata: Optional[Dict[str, Any]]) -> Tuple[bool, List[str]]:
        """
        Validate metadata against required schema.

        Checks that all required fields are present and have the
        correct types and formats.

        Args:
            metadata (Optional[Dict[str, Any]]): The metadata dictionary
                to validate.

        Returns:
            Tuple[bool, List[str]]: A tuple containing:
                - is_valid (bool): True if validation passes, False otherwise.
                - errors (List[str]): List of validation error messages.

        Example:
            >>> parser = MetadataParser()
            >>> metadata = {'title': 'Test', 'date': '2026-03-05'}
            >>> is_valid, errors = parser.validate(metadata)
            >>> is_valid
            True
            >>> errors
            []
        """
        errors = []

        if metadata is None:
            return False, ["Metadata cannot be None"]

        if not isinstance(metadata, dict):
            return False, ["Metadata must be a dictionary"]

        for field in self.REQUIRED_FIELDS:
            if field not in metadata:
                errors.append(f"Required field '{field}' is missing")

        if "title" in metadata and not isinstance(metadata["title"], str):
            errors.append("Field 'title' must be a string")

        if "date" in metadata:
            date_value = metadata["date"]
            if isinstance(date_value, str):
                try:
                    datetime.strptime(date_value, "%Y-%m-%d")
                except ValueError:
                    errors.append("Field 'date' must be in YYYY-MM-DD format")
            elif not isinstance(date_value, (datetime, date, type(None))):
                errors.append("Field 'date' must be a string, datetime, or date")

        if "tags" in metadata and metadata["tags"] is not None:
            if not isinstance(metadata["tags"], list):
                errors.append("Field 'tags' must be a list")

        is_valid = len(errors) == 0
        return is_valid, errors

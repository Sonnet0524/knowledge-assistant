#!/usr/bin/env python3
"""
Basic Usage Example

This example demonstrates:
- Creating documents from templates
- Parsing document metadata
- Validating metadata
- Working with DocumentMetadata objects

Run: python examples/basic-usage.py
"""

import sys
from pathlib import Path
from datetime import date

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.template_engine import TemplateEngine
from scripts.metadata_parser import MetadataParser
from scripts.types import DocumentMetadata


def main():
    """Run basic usage examples."""
    print("=" * 60)
    print("Knowledge Assistant - Basic Usage Example")
    print("=" * 60)
    print()

    # 1. Create a document from template
    print("1. Creating a document from template")
    print("-" * 60)

    engine = TemplateEngine('./templates')

    # Render a daily note
    content = engine.render(
        'daily-note',
        title='My First Note',
        date=str(date.today()),
        author='Example User'
    )

    print("Generated content:")
    # Use ascii_safe encoding for Windows console compatibility
    print(content.encode('ascii', errors='ignore').decode('ascii'))
    print()

    # 2. Parse metadata from a document
    print("2. Parsing metadata from a document")
    print("-" * 60)

    # Sample document with frontmatter
    document = """---
title: Research Note on Python Testing
date: 2026-03-06
tags: [python, testing, pytest]
author: Example User
type: research
status: draft
---

# Research Note on Python Testing

This is the body of the research note.

## Key Findings

- Finding 1
- Finding 2

## References

- Reference 1
"""

    parser = MetadataParser()
    metadata, body = parser.parse(document)

    print("Parsed metadata:")
    for key, value in metadata.items():
        print(f"  {key}: {value}")
    print()

    print(f"Body preview: {body[:50]}...")
    print()

    # 3. Validate metadata
    print("3. Validating metadata")
    print("-" * 60)

    is_valid, errors = parser.validate(metadata)

    if is_valid:
        print("✓ Metadata is valid")
    else:
        print("✗ Validation errors:")
        for error in errors:
            print(f"  - {error}")
    print()

    # Test invalid metadata
    invalid_metadata = {'title': 'Missing Date'}
    is_valid, errors = parser.validate(invalid_metadata)

    print("Testing invalid metadata:")
    print(f"  Valid: {is_valid}")
    print(f"  Errors: {errors}")
    print()

    # 4. Working with DocumentMetadata objects
    print("4. Working with DocumentMetadata objects")
    print("-" * 60)

    # Create metadata programmatically
    doc_metadata = DocumentMetadata(
        title="Meeting Notes",
        date=date(2026, 3, 6),
        tags=["meeting", "planning"],
        author="Alice",
        type="meeting",
        status="published"
    )

    print("Created DocumentMetadata object:")
    print(f"  Title: {doc_metadata.title}")
    print(f"  Date: {doc_metadata.date}")
    print(f"  Tags: {doc_metadata.tags}")
    print(f"  Author: {doc_metadata.author}")
    print(f"  Type: {doc_metadata.type}")
    print(f"  Status: {doc_metadata.status}")
    print()

    # 5. Complete workflow example
    print("5. Complete workflow example")
    print("-" * 60)

    # Step 1: Create template
    print("Step 1: Creating document from template...")
    meeting_note = engine.render(
        'meeting-minutes',
        title='Sprint Planning',
        date='2026-03-06',
        attendees=['Alice', 'Bob', 'Charlie']
    )
    print("✓ Template created")
    print()

    # Step 2: Parse and validate
    print("Step 2: Parsing and validating...")
    meta, body = parser.parse(meeting_note)
    is_valid, _ = parser.validate(meta)
    print(f"✓ Parsed and validated: {is_valid}")
    print()

    # Step 3: Save (simulated)
    print("Step 3: Saving document...")
    # In real usage: write_file('sprint-planning.md', meeting_note)
    print("✓ Document would be saved to: sprint-planning.md")
    print()

    print("=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == '__main__':
    main()

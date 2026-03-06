#!/usr/bin/env python3
"""
Note Organization Example

This example demonstrates:
- Scanning directories for documents
- Organizing notes by date, tags, or type
- Using the OrganizationResult object
- Creating organizational workflows

Run: python examples/organize-example.py
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path
from datetime import date

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.tools.organize_notes import scan_directory, organize_notes
from scripts.tools.generate_index import generate_index
from scripts.utils import write_file, ensure_directory


def create_sample_notes(directory):
    """Create sample notes for demonstration."""
    print(f"Creating sample notes in {directory}...")
    print()

    notes = [
        {
            'filename': 'research-note.md',
            'content': """---
title: Python Testing Research
date: 2026-03-06
tags: [python, testing, research]
type: research
author: Alice
---

# Python Testing Research

Research on testing frameworks and best practices.
"""
        },
        {
            'filename': 'meeting-notes.md',
            'content': """---
title: Team Meeting
date: 2026-03-05
tags: [meeting, team]
type: meeting
author: Bob
---

# Team Meeting

Discussion about project progress.
"""
        },
        {
            'filename': 'daily-standup.md',
            'content': """---
title: Daily Standup
date: 2026-03-06
tags: [daily, standup]
type: daily
author: Charlie
---

# Daily Standup

Quick update on daily progress.
"""
        },
        {
            'filename': 'task-list.md',
            'content': """---
title: Weekly Tasks
date: 2026-03-04
tags: [tasks, weekly]
type: tasks
author: Alice
---

# Weekly Tasks

Tasks for this week.
"""
        }
    ]

    for note in notes:
        file_path = Path(directory) / note['filename']
        write_file(file_path, note['content'])
        print(f"  Created: {note['filename']}")

    print()


def main():
    """Run note organization examples."""
    print("=" * 60)
    print("Knowledge Assistant - Note Organization Example")
    print("=" * 60)
    print()

    # Create temporary directories for demonstration
    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / 'inbox'
        organized_dir = Path(temp_dir) / 'organized'

        ensure_directory(source_dir)
        ensure_directory(organized_dir)

        # 1. Create sample notes
        print("1. Creating Sample Notes")
        print("-" * 60)
        create_sample_notes(source_dir)

        # 2. Scan directory
        print("2. Scanning Directory")
        print("-" * 60)

        documents = scan_directory(source_dir, recursive=True)

        print(f"Found {len(documents)} documents:")
        for doc in documents:
            print(f"  - {doc.title}")
            print(f"    Date: {doc.date}")
            print(f"    Tags: {doc.tags}")
            print(f"    Type: {doc.type}")
            print(f"    Path: {doc.path.name}")
        print()

        # 3. Organize by date
        print("3. Organizing by Date")
        print("-" * 60)

        result_date = organize_notes(
            source_dir=source_dir,
            target_dir=organized_dir / 'by-date',
            by='date',
            operation='copy'  # Copy instead of move
        )

        print(f"Result:")
        print(f"  Copied: {result_date.copied}")
        print(f"  Skipped: {result_date.skipped}")
        print(f"  Errors: {len(result_date.errors)}")

        if result_date.details:
            print("\n  File mappings:")
            for source, dest in result_date.details.items():
                print(f"    {Path(source).name} -> {Path(dest).relative_to(organized_dir)}")
        print()

        # 4. Organize by tags
        print("4. Organizing by Tags")
        print("-" * 60)

        result_tags = organize_notes(
            source_dir=source_dir,
            target_dir=organized_dir / 'by-tags',
            by='tags',
            operation='copy'
        )

        print(f"Result:")
        print(f"  Copied: {result_tags.copied}")
        print(f"  Skipped: {result_tags.skipped}")
        print(f"  Errors: {len(result_tags.errors)}")

        if result_tags.details:
            print("\n  File mappings:")
            for source, dest in result_tags.details.items():
                print(f"    {Path(source).name} -> {Path(dest).relative_to(organized_dir)}")
        print()

        # 5. Organize by type
        print("5. Organizing by Type")
        print("-" * 60)

        result_type = organize_notes(
            source_dir=source_dir,
            target_dir=organized_dir / 'by-type',
            by='type',
            operation='copy'
        )

        print(f"Result:")
        print(f"  Copied: {result_type.copied}")
        print(f"  Skipped: {result_type.skipped}")
        print(f"  Errors: {len(result_type.errors)}")

        if result_type.details:
            print("\n  File mappings:")
            for source, dest in result_type.details.items():
                print(f"    {Path(source).name} -> {Path(dest).relative_to(organized_dir)}")
        print()

        # 6. Generate index
        print("6. Generating Index")
        print("-" * 60)

        # Generate index for date-organized notes
        index_path = generate_index(
            directory=organized_dir / 'by-date',
            output_file=organized_dir / 'by-date' / 'INDEX.md',
            title='Organized Notes (by Date)',
            group_by='date'
        )

        print(f"Index created: {index_path.relative_to(organized_dir)}")
        print()

        # 7. Show directory structure
        print("7. Directory Structure Created")
        print("-" * 60)

        def show_tree(directory, prefix='', level=0):
            """Show directory tree structure."""
            if level > 3:  # Limit depth
                return

            items = sorted(directory.iterdir(), key=lambda x: (not x.is_dir(), x.name))

            for i, item in enumerate(items):
                is_last = i == len(items) - 1
                current_prefix = '└── ' if is_last else '├── '
                print(f"{prefix}{current_prefix}{item.name}")

                if item.is_dir() and not item.name.startswith('.'):
                    extension = '    ' if is_last else '│   '
                    show_tree(item, prefix + extension, level + 1)

        print("organized/")
        show_tree(organized_dir)
        print()

        # 8. Workflow example
        print("8. Workflow Example: Weekly Organization")
        print("-" * 60)

        print("""
Typical weekly workflow:

1. Create notes throughout the week in 'inbox/'
2. At end of week, run organization:
   - organize_notes('inbox/', 'organized/', by='date')
3. Generate index for reference:
   - generate_index('organized/', 'WEEKLY_INDEX.md')
4. Archive old notes:
   - organize_notes('organized/', 'archive/2026-Q1/', by='date')

This keeps your notes organized and easily searchable.
""")
        print()

    print("=" * 60)
    print("Note organization example completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()

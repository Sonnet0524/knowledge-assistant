#!/usr/bin/env python3
"""
Template System Example

This example demonstrates:
- Loading templates
- Rendering templates with variables
- Listing available templates
- Extracting template variables
- Template caching

Run: python examples/template-example.py
"""

import sys
from pathlib import Path
from datetime import date

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.template_engine import TemplateEngine


def main():
    """Run template system examples."""
    print("=" * 60)
    print("Knowledge Assistant - Template System Example")
    print("=" * 60)
    print()

    # Initialize template engine
    engine = TemplateEngine('./templates')

    # 1. List all available templates
    print("1. Available Templates")
    print("-" * 60)

    templates = engine.list_templates()

    print(f"Found {len(templates)} templates:")
    for template in templates:
        print(f"  - {template}")
    print()

    # 2. Explore each template
    print("2. Exploring Templates")
    print("-" * 60)

    for template_name in templates:
        # Extract variables needed
        variables = engine.extract_variables(template_name)

        print(f"\n{template_name}:")
        print(f"  Variables: {', '.join(variables) if variables else 'None'}")

        # Show template preview
        template_content = engine.load_template(template_name)
        preview_lines = template_content.split('\n')[:5]
        print("  Preview:")
        for line in preview_lines:
            print(f"    {line}")
        if len(template_content.split('\n')) > 5:
            print("    ...")

    print()

    # 3. Render examples for each template
    print("3. Rendering Examples")
    print("-" * 60)

    # Daily note
    print("\nDaily Note:")
    daily = engine.render(
        'daily-note',
        title='Productive Monday',
        date='2026-03-06',
        author='Alice'
    )
    print(daily[:200] + "...")
    print()

    # Research note
    print("Research Note:")
    research = engine.render(
        'research-note',
        title='Python Asyncio Study',
        date='2026-03-06',
        subject='Programming'
    )
    print(research[:200] + "...")
    print()

    # Meeting minutes
    print("Meeting Minutes:")
    meeting = engine.render(
        'meeting-minutes',
        title='Sprint Planning',
        date='2026-03-06',
        attendees=['Alice', 'Bob', 'Charlie']
    )
    print(meeting[:200] + "...")
    print()

    # Task list
    print("Task List:")
    tasks = engine.render(
        'task-list',
        title='Weekly Tasks',
        date='2026-03-06'
    )
    print(tasks[:200] + "...")
    print()

    # Knowledge card
    print("Knowledge Card:")
    card = engine.render(
        'knowledge-card',
        title='Docker Networking',
        date='2026-03-06',
        subject='DevOps'
    )
    print(card[:200] + "...")
    print()

    # 4. Template caching demonstration
    print("4. Template Caching")
    print("-" * 60)

    print("First load (from disk):")
    # This loads from disk
    template1 = engine.load_template('daily-note', use_cache=False)
    print(f"  Template loaded: {len(template1)} characters")

    print("\nSecond load (from cache):")
    # This loads from cache
    template2 = engine.load_template('daily-note', use_cache=True)
    print(f"  Template loaded: {len(template2)} characters")

    print("\nClearing cache...")
    engine.clear_cache()
    print("  Cache cleared")

    print("\nLoad after clear (from disk):")
    template3 = engine.load_template('daily-note', use_cache=True)
    print(f"  Template loaded: {len(template3)} characters")
    print()

    # 5. Custom template example
    print("5. Creating Custom Templates")
    print("-" * 60)

    print("Custom templates can be created by adding .md files to templates/")
    print()
    print("Example custom template structure:")
    print("""
---
title: {{title}}
date: {{date}}
custom_field: {{custom_field}}
---

# {{title}}

Created on: {{date}}

## Overview
{{overview}}

## Details
{{details}}
""")
    print()

    # 6. Batch rendering example
    print("6. Batch Rendering Example")
    print("-" * 60)

    print("Creating multiple daily notes for a week:")
    print()

    from datetime import timedelta

    start_date = date(2026, 3, 2)  # Monday

    for i in range(5):  # Monday to Friday
        current_date = start_date + timedelta(days=i)
        daily_note = engine.render(
            'daily-note',
            title=f'Day {i+1}',
            date=str(current_date)
        )
        print(f"  Created: {current_date.strftime('%Y-%m-%d')} ({current_date.strftime('%A')})")

    print()
    print("✓ Batch rendering completed")
    print()

    print("=" * 60)
    print("Template system example completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()

# User Guide

Complete guide to using Knowledge Assistant for personal knowledge management.

## Table of Contents

1. [Overview](#overview)
2. [Metadata System](#metadata-system)
3. [Template System](#template-system)
4. [Configuration](#configuration)
5. [Automation Tools](#automation-tools)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

---

## Overview

### What is Knowledge Assistant?

Knowledge Assistant is a Python-based personal knowledge management tool that helps you:

- **Organize** your notes with structured metadata
- **Standardize** your documents with templates
- **Automate** note organization and indexing
- **Maintain** a consistent knowledge base

### Architecture

```
knowledge-assistant/
├── scripts/              # Core Python modules
│   ├── types.py         # DocumentMetadata dataclass
│   ├── metadata_parser.py  # YAML frontmatter parser
│   ├── template_engine.py  # Template rendering engine
│   ├── config.py        # Configuration management
│   ├── utils.py         # File and path utilities
│   └── tools/           # Automation tools
│       ├── organize_notes.py
│       └── generate_index.py
├── templates/           # Markdown templates
│   ├── daily-note.md
│   ├── research-note.md
│   ├── meeting-minutes.md
│   ├── task-list.md
│   └── knowledge-card.md
├── tests/               # Test suite
└── config.yaml          # User configuration
```

### Core Concepts

#### 1. Metadata-First Approach

Every document can have structured metadata using YAML frontmatter:

```yaml
---
title: My Note Title
date: 2026-03-06
tags: [python, tutorial]
author: Your Name
type: research
status: draft
---
```

This metadata enables:
- Automatic organization by date
- Tag-based categorization
- Search and filtering
- Index generation

#### 2. Template-Driven Documentation

Templates provide consistent structure for your notes:

```markdown
---
title: {{title}}
date: {{date}}
tags: {{tags}}
---

# {{title}}

Content structure here...
```

#### 3. Automation Tools

Python scripts automate common tasks:
- Organizing notes by date/tags
- Generating indexes
- Extracting keywords (coming soon)

---

## Metadata System

### YAML Frontmatter

Frontmatter is metadata at the beginning of a document, enclosed by `---`:

```markdown
---
title: Meeting Notes
date: 2026-03-06
tags: [work, planning]
attendees: [Alice, Bob, Charlie]
---

# Meeting Notes

Meeting content here...
```

### Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `title` | string | Document title | `"Research Note"` |
| `date` | string or date | Document date | `"2026-03-06"` or `date(2026, 3, 6)` |

### Optional Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `tags` | list | Tags for categorization | `["python", "testing"]` |
| `author` | string | Document author | `"Your Name"` |
| `type` | string | Document type | `"research"`, `"meeting"`, `"daily"` |
| `status` | string | Document status | `"draft"`, `"published"`, `"archived"` |
| `attendees` | list | Meeting participants | `["Alice", "Bob"]` |
| `subject` | string | Research subject | `"Python Testing"` |

### Using the Metadata Parser

#### Basic Parsing

```python
from scripts.metadata_parser import MetadataParser

parser = MetadataParser()

# Parse a document
with open('my_note.md', 'r') as f:
    content = f.read()

metadata, body = parser.parse(content)

# Access metadata
print(metadata['title'])  # "My Note Title"
print(metadata['tags'])   # ["python", "tutorial"]
```

#### Validation

```python
# Validate metadata
is_valid, errors = parser.validate(metadata)

if is_valid:
    print("Metadata is valid")
else:
    print("Validation errors:", errors)
```

#### Working with DocumentMetadata

```python
from scripts.types import DocumentMetadata
from datetime import date

# Create metadata programmatically
metadata = DocumentMetadata(
    title="Research Note",
    date=date(2026, 3, 6),
    tags=["python", "testing"],
    author="Your Name",
    type="research",
    status="draft"
)

# Access fields
print(metadata.title)   # "Research Note"
print(metadata.tags)    # ["python", "testing"]
```

### Best Practices for Metadata

1. **Always include title and date** - These are required for most tools
2. **Use consistent tags** - Establish a tag vocabulary
3. **Keep metadata minimal** - Only add fields you actually use
4. **Use ISO date format** - `YYYY-MM-DD` for consistency

---

## Template System

### Available Templates

#### 1. daily-note.md

For daily journaling and standup notes.

**Variables**:
- `title` (required): Note title
- `date` (required): Note date
- `author` (optional): Your name

**Example**:

```python
from scripts.template_engine import TemplateEngine

engine = TemplateEngine('./templates')
content = engine.render(
    'daily-note',
    title='Daily Standup',
    date='2026-03-06',
    author='Alice'
)
```

#### 2. research-note.md

For research and study notes.

**Variables**:
- `title` (required): Research topic
- `date` (required): Date
- `subject` (optional): Subject area

**Example**:

```python
content = engine.render(
    'research-note',
    title='Python Asyncio Patterns',
    date='2026-03-06',
    subject='Programming'
)
```

#### 3. meeting-minutes.md

For meeting records.

**Variables**:
- `title` (required): Meeting title
- `date` (required): Meeting date
- `attendees` (optional): List of attendees

**Example**:

```python
content = engine.render(
    'meeting-minutes',
    title='Sprint Planning',
    date='2026-03-06',
    attendees=['Alice', 'Bob', 'Charlie']
)
```

#### 4. task-list.md

For task management.

**Variables**:
- `title` (required): Task list title
- `date` (required): Date

**Example**:

```python
content = engine.render(
    'task-list',
    title='Weekly Tasks',
    date='2026-03-06'
)
```

#### 5. knowledge-card.md

For knowledge capture and concept cards.

**Variables**:
- `title` (required): Concept title
- `date` (required): Date
- `subject` (optional): Subject area

**Example**:

```python
content = engine.render(
    'knowledge-card',
    title='Docker Networking',
    date='2026-03-06',
    subject='DevOps'
)
```

### Using the Template Engine

#### Basic Usage

```python
from scripts.template_engine import TemplateEngine

# Initialize with template directory
engine = TemplateEngine('./templates')

# Render a template
content = engine.render('daily-note', title='My Day', date='2026-03-06')
```

#### List Available Templates

```python
templates = engine.list_templates()
print(templates)
# ['daily-note', 'knowledge-card', 'meeting-minutes', 'research-note', 'task-list']
```

#### Extract Template Variables

```python
variables = engine.extract_variables('daily-note')
print(variables)
# ['author', 'date', 'title']
```

#### Template Caching

Templates are cached by default for performance. Clear the cache if you update templates:

```python
engine.clear_cache()
```

### Creating Custom Templates

Create a new template file in `templates/`:

```markdown
<!-- templates/my-template.md -->
---
title: {{title}}
date: {{date}}
tags: [{{tags}}]
---

# {{title}}

Created on: {{date}}

## Overview

Overview section...

## Details

Details section...
```

Use it:

```python
content = engine.render(
    'my-template',
    title='Custom Note',
    date='2026-03-06',
    tags='custom, template'
)
```

---

## Configuration

### Configuration File Structure

`config.yaml`:

```yaml
# Template Configuration
template_dir: ./templates
output_dir: ./output

# Default Values
default_author: Knowledge Assistant
date_format: "%Y-%m-%d"

# Template-Specific Settings
templates:
  daily-note:
    enabled: true
    auto_date: true
    default_tags:
      - daily
      - journal
  
  research-note:
    enabled: true
    default_tags:
      - research
      - notes

# Editor Settings
editor:
  default: vscode
  line_length: 100

# File Naming Convention
naming:
  include_date: true
  date_prefix: true
  format: "{date}_{title}"
```

### Using Configuration

#### Load Configuration

```python
from scripts.config import ConfigManager

# Load from file
config = ConfigManager('config.yaml')
config.load()

# Or use defaults
config = ConfigManager()
config.load()
```

#### Access Values

```python
# Simple values
template_dir = config.get('template_dir')
output_dir = config.get('output_dir', default='./output')

# Nested values (dot notation)
auto_date = config.get('templates.daily-note.auto_date')
default_tags = config.get('templates.daily-note.default_tags')

# Required values (raises error if missing)
template_dir = config.get('template_dir', required=True)
```

#### Modify Configuration

```python
# Set values
config.set('template_dir', './my-templates')
config.set('templates.daily-note.auto_date', False)

# Save changes
config.save('my-config.yaml')
```

#### Validate Configuration

```python
try:
    config.validate()
    print("Configuration is valid")
except ConfigurationError as e:
    print(f"Invalid configuration: {e}")
```

### Configuration Best Practices

1. **Keep config.yaml in .gitignore** - User-specific settings
2. **Provide config.example.yaml** - Template for users
3. **Document configuration options** - Comment your config
4. **Validate on startup** - Catch errors early

---

## Automation Tools

### organize_notes

Organize markdown files by date, tags, or custom criteria.

#### Basic Usage

```python
from scripts.tools.organize_notes import organize_notes

# Organize by date
result = organize_notes(
    source_dir='notes/',
    target_dir='organized/',
    by='date'
)
```

#### Organization Strategies

**By Date** (default):

```python
result = organize_notes(
    source_dir='notes/',
    target_dir='organized/',
    by='date',
    date_format='{year}/{month}'  # Creates 2026/03/ subdirectories
)
```

**By Tags**:

```python
result = organize_notes(
    source_dir='notes/',
    target_dir='organized/',
    by='tags'
)
# Creates: organized/python/note.md, organized/testing/note.md
```

**By Type**:

```python
result = organize_notes(
    source_dir='notes/',
    target_dir='organized/',
    by='type'
)
# Creates: organized/research/note.md, organized/meeting/note.md
```

#### Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `source_dir` | str | required | Source directory |
| `target_dir` | str | required | Target directory |
| `by` | str | `'date'` | Organization strategy: `'date'`, `'tags'`, `'type'` |
| `move` | bool | `True` | Move files (False to copy) |
| `recursive` | bool | `True` | Scan subdirectories |
| `date_format` | str | `'{year}/{month}'` | Date directory format |
| `overwrite` | bool | `False` | Overwrite existing files |

#### Result Object

```python
result = organize_notes(...)

print(f"Moved: {result.moved}")
print(f"Copied: {result.copied}")
print(f"Skipped: {result.skipped}")
print(f"Errors: {result.errors}")

# Details mapping source to destination
for source, dest in result.details.items():
    print(f"{source} -> {dest}")
```

### generate_index

Generate a markdown index file for a directory.

#### Basic Usage

```python
from scripts.tools.generate_index import generate_index

# Generate index
index_path = generate_index(
    directory='notes/',
    output_file='INDEX.md'
)
```

#### Customization

```python
index_path = generate_index(
    directory='notes/',
    output_file='README.md',
    title='My Knowledge Base',
    group_by='date',  # Group by 'date', 'tags', or 'type'
    include_toc=True,  # Include table of contents
    recursive=True     # Include subdirectories
)
```

#### Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `directory` | str | required | Directory to index |
| `output_file` | str | required | Output file path |
| `title` | str | `'Document Index'` | Index title |
| `group_by` | str | `'date'` | Grouping strategy |
| `include_toc` | bool | `True` | Include table of contents |
| `recursive` | bool | `True` | Include subdirectories |

#### Index Format

Generated index format:

```markdown
# My Knowledge Base

## Table of Contents

- [2026-03](#2026-03)
  - [Research Note](notes/research-note.md)
  - [Meeting Minutes](notes/meeting-minutes.md)

## 2026-03

### Research Note
- **File**: `notes/research-note.md`
- **Date**: 2026-03-06
- **Tags**: python, testing

### Meeting Minutes
- **File**: `notes/meeting-minutes.md`
- **Date**: 2026-03-06
- **Tags**: meeting, work
```

### extract_keywords (Coming Soon)

*This tool will be available after M4 completion.*

Extract keywords automatically from documents.

---

## Best Practices

### Directory Organization

```
your-knowledge-base/
├── inbox/              # New, unprocessed notes
├── daily/              # Daily journals
├── research/           # Research notes
├── meetings/           # Meeting minutes
├── tasks/              # Task lists
├── archive/            # Completed/archived items
└── templates/          # Custom templates
```

### Naming Conventions

- **Files**: `YYYY-MM-DD-title.md`
- **Tags**: Use lowercase, hyphens for multi-word: `python-testing`, `devops`
- **Titles**: Clear and descriptive: "Python Testing Best Practices"

### Workflow Example

**Daily Workflow**:

```python
# 1. Create daily note
from scripts.template_engine import TemplateEngine
from datetime import date

engine = TemplateEngine('./templates')
daily = engine.render('daily-note', title='Daily Standup', date=str(date.today()))

# 2. Work on notes...

# 3. End of day: organize new notes
from scripts.tools.organize_notes import organize_notes
organize_notes('inbox/', 'daily/', by='date')

# 4. Generate weekly index
from scripts.tools.generate_index import generate_index
generate_index('daily/', 'INDEX.md', title='Daily Notes')
```

### Metadata Guidelines

1. **Be Consistent**: Use the same tag vocabulary
2. **Be Minimal**: Only add necessary metadata
3. **Be Accurate**: Update metadata when content changes
4. **Be Structured**: Follow templates

### Common Patterns

#### Research Workflow

```python
# Create research note
note = engine.render(
    'research-note',
    title='Python Asyncio Study',
    date=str(date.today()),
    subject='Programming'
)

# Save with consistent naming
filename = f"{date.today()}_python-asyncio-study.md"
# ... save to file
```

#### Meeting Workflow

```python
# Pre-meeting: create template
meeting = engine.render(
    'meeting-minutes',
    title='Sprint Planning',
    date=str(date.today()),
    attendees=['Alice', 'Bob']
)

# Post-meeting: add notes and organize
# ... add content ...
organize_notes('meetings/inbox/', 'meetings/archive/', by='date')
```

---

## Troubleshooting

### Common Errors

#### "Template not found"

**Cause**: Template directory path is incorrect

**Solution**: Use absolute path or verify relative path

```python
# Use absolute path
engine = TemplateEngine('/home/user/knowledge-assistant/templates')

# Or get project root
from scripts.utils import get_project_root
root = get_project_root()
engine = TemplateEngine(root / 'templates')
```

#### "Metadata validation failed"

**Cause**: Missing required fields

**Solution**: Ensure title and date are present

```python
metadata, body = parser.parse(content)
is_valid, errors = parser.validate(metadata)

if not is_valid:
    print("Missing fields:", errors)
    # Add missing fields
    if 'title' not in metadata:
        metadata['title'] = 'Untitled'
```

#### "Configuration not loaded"

**Cause**: Configuration not loaded before use

**Solution**: Always call `config.load()`

```python
config = ConfigManager('config.yaml')
config.load()  # Don't forget this!
value = config.get('template_dir')
```

#### Import Errors

**Cause**: Virtual environment not activated or dependencies not installed

**Solution**:

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Performance Tips

1. **Use template caching**: Enabled by default, improves performance
2. **Batch operations**: Process multiple files together
3. **Recursive scanning**: Disable if you know the structure

### Getting Help

1. **Check the documentation**: [API Reference](api-reference.md)
2. **Review examples**: [Examples](../examples/)
3. **Check tests**: Look at `tests/` for usage patterns

---

## Advanced Topics

### Custom Templates

Create templates with your own structure:

```markdown
<!-- templates/custom-note.md -->
---
title: {{title}}
date: {{date}}
custom_field: {{custom_field}}
---

# {{title}}

## Custom Section

{{content}}
```

### Extending Tools

Build custom workflows:

```python
from scripts.tools.organize_notes import scan_directory

# Get all documents
docs = scan_directory('notes/')

# Custom processing
for doc in docs:
    if 'important' in doc.tags:
        # Special handling
        pass
```

### Integration with Other Tools

Knowledge Assistant can integrate with:

- **Editors**: VS Code, Obsidian
- **Version Control**: Git-based workflows
- **CI/CD**: Automated documentation generation

---

**Next Steps**:
- Explore the [API Reference](api-reference.md)
- Try the [Examples](../examples/)
- Join the community (if applicable)

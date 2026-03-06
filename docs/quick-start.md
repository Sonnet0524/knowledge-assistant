# Quick Start Guide

Get started with Knowledge Assistant in 5 minutes.

## Prerequisites

- **Python 3.8+** installed on your system
- Basic familiarity with command line
- A text editor (VS Code recommended)

## Step 1: Installation (2 minutes)

### Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd knowledge-assistant

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configure

```bash
# Copy the example configuration
cp config.example.yaml config.yaml

# Edit config.yaml to customize settings (optional)
# The defaults work fine for most users
```

## Step 2: Create Your First Note (1 minute)

### Using Python

Create a file `my_first_note.py`:

```python
from scripts.template_engine import TemplateEngine
from datetime import date

# Initialize template engine
engine = TemplateEngine('./templates')

# Create a daily note
content = engine.render(
    'daily-note',
    title='My First Day',
    date=str(date.today()),
    author='Your Name'
)

# Save the note
with open('my_first_note.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("Note created: my_first_note.md")
```

Run it:

```bash
python my_first_note.py
```

### Result

Your `my_first_note.md` will look like:

```markdown
---
title: My First Day
date: 2026-03-06
author: Your Name
tags:
  - daily
  - journal
---

# My First Day

## Highlights

- What went well today?

## Tasks

- [ ] Task 1

## Notes

Daily notes and observations...
```

## Step 3: Parse and Validate Documents (1 minute)

Create `parse_example.py`:

```python
from scripts.metadata_parser import MetadataParser

# Sample document with frontmatter
content = """---
title: Research on Python Testing
date: 2026-03-06
tags: [python, testing, pytest]
author: Your Name
type: research
---

# Research on Python Testing

This is the body of my research note...

## Key Findings

- Finding 1
- Finding 2
"""

# Parse the document
parser = MetadataParser()
metadata, body = parser.parse(content)

# Check metadata
print("Title:", metadata['title'])
print("Tags:", metadata['tags'])

# Validate
is_valid, errors = parser.validate(metadata)
print(f"Valid: {is_valid}")
if not is_valid:
    print("Errors:", errors)
```

Run it:

```bash
python parse_example.py
```

## Step 4: Organize Your Notes (1 minute)

Imagine you have notes scattered in a `notes/` directory. Let's organize them:

```python
from scripts.tools.organize_notes import organize_notes

# Organize notes by date into year/month folders
result = organize_notes(
    source_dir='notes/',
    target_dir='organized/',
    by='date',
    move=True  # Move files (use False to copy)
)

print(f"Moved: {result.moved}")
print(f"Skipped: {result.skipped}")
if result.errors:
    print("Errors:", result.errors)
```

This creates a structure like:

```
organized/
├── 2026/
│   ├── 03/
│   │   ├── note-1.md
│   │   └── note-2.md
│   └── 02/
│       └── note-3.md
```

## Step 5: Generate an Index (30 seconds)

Create an index of all your notes:

```python
from scripts.tools.generate_index import generate_index

# Generate index for your notes directory
index_path = generate_index(
    directory='organized/',
    output_file='INDEX.md',
    title='My Knowledge Base'
)

print(f"Index created: {index_path}")
```

This creates an `INDEX.md` file with links to all your notes, organized by date.

## Next Steps

Congratulations! You've learned the basics. Here's what to explore next:

### 📚 Read the Documentation

- **[User Guide](user-guide.md)** - Complete feature documentation
- **[API Reference](api-reference.md)** - Detailed API documentation
- **[Examples](../examples/)** - More code examples

### 🛠️ Explore Features

1. **Try different templates**
   - `research-note` - For research documentation
   - `meeting-minutes` - For meeting records
   - `task-list` - For task management
   - `knowledge-card` - For knowledge capture

2. **Customize configuration**
   - Edit `config.yaml`
   - Set default values
   - Configure template behavior

3. **Build workflows**
   - Create a daily journaling workflow
   - Automate note organization
   - Generate weekly summaries

### 💡 Common Use Cases

#### Daily Journaling

```python
from scripts.template_engine import TemplateEngine
from datetime import date

engine = TemplateEngine('./templates')
note = engine.render('daily-note', title='Daily Standup', date=str(date.today()))
```

#### Research Notes

```python
engine = TemplateEngine('./templates')
note = engine.render(
    'research-note',
    title='Python Asyncio Study',
    date='2026-03-06',
    subject='Programming'
)
```

#### Meeting Notes

```python
engine = TemplateEngine('./templates')
note = engine.render(
    'meeting-minutes',
    title='Sprint Planning',
    date='2026-03-06',
    attendees=['Alice', 'Bob', 'Charlie']
)
```

## Getting Help

- Check the [User Guide](user-guide.md) for detailed documentation
- Browse [Examples](../examples/) for code samples
- Review the [API Reference](api-reference.md) for technical details

## Troubleshooting

### "Template not found" error

Make sure you're running scripts from the project root directory, or specify the correct template path:

```python
engine = TemplateEngine('/path/to/templates')
```

### "Configuration not loaded" error

Load the configuration before using it:

```python
from scripts.config import ConfigManager

config = ConfigManager('config.yaml')
config.load()
```

### Import errors

Make sure you've:
1. Activated your virtual environment
2. Installed all dependencies: `pip install -r requirements.txt`

---

**Time spent**: ~5 minutes

**What you learned**: Installation, template usage, metadata parsing, note organization, index generation

**Next**: Explore the [User Guide](user-guide.md) for advanced features

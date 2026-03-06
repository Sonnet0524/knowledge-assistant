# Knowledge Assistant

A personal knowledge management assistant with document templates, metadata management, and automation tools.

## Features

- **Metadata System** - Parse and validate YAML frontmatter in your documents
- **Template Engine** - 5 pre-built templates for common note types
- **Organization Tools** - Automatically organize and index your notes
- **Configuration Management** - Flexible YAML-based configuration

## Quick Start

### Requirements

- Python 3.8 or higher
- pip

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd knowledge-assistant

# Install dependencies
pip install -r requirements.txt

# Copy example configuration
cp config.example.yaml config.yaml
```

### First Steps

#### 1. Create a Note from Template

```python
from scripts.template_engine import TemplateEngine

# Initialize template engine
engine = TemplateEngine('./templates')

# Render a daily note
content = engine.render(
    'daily-note',
    title='My Day',
    date='2026-03-06'
)

print(content)
```

#### 2. Parse Document Metadata

```python
from scripts.metadata_parser import MetadataParser

parser = MetadataParser()

# Parse a document
content = """---
title: Research Note
date: 2026-03-06
tags: [python, testing]
---

# Content here"""

metadata, body = parser.parse(content)
print(metadata)  # {'title': 'Research Note', 'date': '2026-03-06', ...}
```

#### 3. Organize Your Notes

```python
from scripts.tools.organize_notes import organize_notes

# Organize notes by date
result = organize_notes(
    source_dir='notes/',
    target_dir='organized/',
    by='date'
)

print(f"Organized {result.moved} notes")
```

## Available Templates

| Template | Description | Required Variables |
|----------|-------------|-------------------|
| `daily-note` | Daily journaling | `title`, `date` |
| `research-note` | Research notes | `title`, `date` |
| `meeting-minutes` | Meeting records | `title`, `date`, `attendees` |
| `task-list` | Task management | `title`, `date` |
| `knowledge-card` | Knowledge cards | `title`, `date`, `subject` |

## Tools

### organize_notes
Organize markdown files by date, tags, or custom criteria.

### generate_index
Generate a markdown index file for a directory of notes.

### extract_keywords (Coming Soon)
Extract keywords from documents automatically.

## Documentation

- **[Quick Start Guide](docs/quick-start.md)** - Step-by-step tutorial
- **[User Guide](docs/user-guide.md)** - Complete usage documentation
- **[API Reference](docs/api-reference.md)** - Detailed API documentation
- **[Examples](examples/)** - Runnable code examples

## Project Status

**Current Version**: v1.0 (in development)

### Milestones

| Milestone | Status | Progress |
|-----------|--------|----------|
| M1 Infrastructure | ✅ Complete | 100% |
| M2 Metadata System | ✅ Complete | 100% |
| M3 Template System | ✅ Complete | 100% |
| M4 Tools | 🔄 In Progress | 66% |
| M5 Test Coverage | ✅ Complete | 96% |
| M6 Release | ⏳ Pending | 0% |

**Overall Progress**: 62% (3.7/6 milestones)

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=scripts --cov-report=html
```

### Code Quality

```bash
# Format code
black scripts/ tests/

# Lint
flake8 scripts/ tests/

# Type check
mypy scripts/
```

## Architecture

```
knowledge-assistant/
├── scripts/              # Core modules
│   ├── types.py         # Document metadata types
│   ├── metadata_parser.py  # YAML frontmatter parser
│   ├── template_engine.py  # Template rendering
│   ├── config.py        # Configuration management
│   ├── utils.py         # Utility functions
│   └── tools/           # Automation tools
│       ├── organize_notes.py
│       └── generate_index.py
├── templates/           # Document templates
├── tests/               # Test suite (96% coverage)
├── docs/                # Documentation
└── examples/            # Code examples
```

## License

See [LICENSE](LICENSE) file for details.

## Contributing

This project is currently in active development. Contributions welcome after v1.0 release.

---

**Built with** ❤️ using Python, YAML, and Markdown

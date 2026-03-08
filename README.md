# Knowledge Assistant

A personal knowledge management assistant with AI-powered semantic search, intelligent text extraction, and seamless integration capabilities.

## Features

### v1.1 Features

- **Semantic Search** - AI-powered search that understands meaning, not just keywords
- **Keyword Extraction** - Automatically extract key terms from documents (TF-IDF, TextRank)
- **Summary Generation** - Generate concise summaries of long documents
- **Email Integration** - Connect and search your email for relevant information
- **opencode Ready** - Designed for integration with opencode master agent

### Core Features (v1.0)

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

### v1.1 Tools

#### build_semantic_index
Build a semantic index for your documents using AI embeddings.

```python
from scripts.tools.indexing import build_semantic_index

result = build_semantic_index(
    documents=[{"path": "notes/python.md", "content": "...", "metadata": {...}}],
    index_path=".ka-index"
)
```

#### semantic_search
Search your knowledge base with natural language queries.

```python
from scripts.tools.search import semantic_search

results = semantic_search(
    query="How to handle async programming?",
    index_path=".ka-index",
    top_k=5
)
```

#### extract_keywords
Extract keywords from documents using TF-IDF or TextRank.

```python
from scripts.tools.extraction import extract_keywords

keywords = extract_keywords(text="...", method="tfidf", top_n=10)
```

#### generate_summary
Generate concise summaries of long documents.

```python
from scripts.tools.extraction import generate_summary

summary = generate_summary(text="...", max_length=200)
```

### Core Tools (v1.0)

#### organize_notes
Organize markdown files by date, tags, or custom criteria.

#### generate_index
Generate a markdown index file for a directory of notes.

## Documentation

- **[Quick Start Guide](docs/quick-start.md)** - Step-by-step tutorial
- **[User Guide](docs/user-guide.md)** - Complete usage documentation
- **[API Reference](docs/api-reference.md)** - Detailed API documentation
- **[Examples](examples/)** - Runnable code examples

## Project Status

**Current Version**: v1.1.0

### Milestones

| Milestone | Status | Progress |
|-----------|--------|----------|
| M1 Infrastructure | ✅ Complete | 100% |
| M2 Metadata System | ✅ Complete | 100% |
| M3 Template System | ✅ Complete | 100% |
| M4 Tools | ✅ Complete | 100% |
| M5 Test Coverage | ✅ Complete | 91.7% |
| M6 Release v1.0 | ✅ Complete | 100% |
| M7 Semantic Index & Search | ✅ Complete | 100% |
| M8 Extraction Tools | ✅ Complete | 100% |
| M9 Integration | ✅ Complete | 100% |
| M10 Release v1.1 | ✅ Complete | 100% |

**Overall Progress**: 100% (v1.1 Released)

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
│   ├── embeddings/      # Vector embeddings (v1.1)
│   ├── index/           # Vector index (v1.1)
│   ├── connectors/      # Data connectors (v1.1)
│   └── tools/           # Automation tools
│       ├── indexing.py  # Semantic index (v1.1)
│       ├── search.py    # Semantic search (v1.1)
│       ├── extraction.py # Text extraction (v1.1)
│       ├── organize_notes.py
│       └── generate_index.py
├── templates/           # Document templates
├── skills/              # opencode skill definitions (v1.1)
├── tests/               # Test suite
├── docs/                # Documentation
└── examples/            # Code examples
```

### opencode Integration (v1.1)

```
opencode (Master Agent)
  ├── File operations (own capability)
  ├── NLU & intent understanding (own capability)
  └── Calls knowledge-assistant tools
      ↓
knowledge-assistant (Tool Library)
  ├── build_semantic_index(documents) → IndexResult
  ├── semantic_search(query) → [SearchResult]
  ├── extract_keywords(content) → [Keyword]
  ├── generate_summary(content) → Summary
  └── EmailConnector → Email data
```

## License

See [LICENSE](LICENSE) file for details.

## Contributing

This project welcomes contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

**Current Version**: v1.1.0 | **Built with** ❤️ using Python, YAML, and Markdown

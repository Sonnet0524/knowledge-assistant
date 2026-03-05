# Test Data Directory

This directory contains test data and fixtures for Knowledge Assistant testing.

## Directory Structure

```
test-data/
├── examples/          # Example documents for testing
│   ├── valid_document.md
│   ├── invalid_yaml.md
│   ├── missing_fields.md
│   └── edge_cases.md
├── fixtures/          # Test fixture data
└── README.md         # This file
```

## Example Documents

### valid_document.md
A valid document with complete frontmatter and content.

### invalid_yaml.md
A document with malformed YAML frontmatter for error handling tests.

### missing_fields.md
A document missing required fields (e.g., date).

### edge_cases.md
Documents with edge cases:
- Empty documents
- Very long content
- Special characters
- Multiple languages

## Usage

Test data is loaded via pytest fixtures defined in `tests/conftest.py`.

## Data Format

All documents use YAML frontmatter format:

```markdown
---
title: Document Title
date: 2026-03-05
type: daily
tags:
  - tag1
  - tag2
---

# Content Title

Document content here.
```

## Maintenance

- Keep examples minimal but representative
- Document the purpose of each file
- Update this README when adding new test data

---
**Created**: 2026-03-05  
**Maintainer**: Test Agent

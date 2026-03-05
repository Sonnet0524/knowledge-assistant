# Document Metadata Specification

> 📋 This document defines the metadata standard for Knowledge Assistant documents.

**Version**: 1.0  
**Last Updated**: 2026-03-05  
**Maintainer**: PM Agent

---

## Overview

All documents in Knowledge Assistant use YAML frontmatter to store metadata. This specification defines the required and optional fields, their types, and formats.

## YAML Frontmatter Format

Documents must begin with YAML frontmatter enclosed by `---` delimiters:

```markdown
---
title: Document Title
date: 2026-03-05
tags:
  - tag1
  - tag2
---

# Document content starts here
```

---

## Required Fields

### title

- **Type**: `string`
- **Required**: ✅ Yes
- **Description**: The document title
- **Constraints**:
  - Cannot be empty
  - Should be descriptive and concise
  - Supports Unicode characters
- **Example**:
  ```yaml
  title: Research Note - Python Testing
  title: 研究笔记 - 知识管理
  ```

### date

- **Type**: `string` (YYYY-MM-DD format) or `date` object
- **Required**: ✅ Yes
- **Description**: Document creation or reference date
- **Format**: `YYYY-MM-DD` (ISO 8601 date format)
- **Constraints**:
  - Must be valid date
  - Format: YYYY-MM-DD
- **Example**:
  ```yaml
  date: 2026-03-05
  date: "2026-03-05"
  ```

---

## Optional Fields

### tags

- **Type**: `list` of `string`
- **Required**: ❌ No
- **Default**: `null`
- **Description**: List of tags for categorization and filtering
- **Constraints**:
  - Each tag should be lowercase
  - Use hyphens for multi-word tags
  - Avoid special characters
- **Example**:
  ```yaml
  tags:
    - python
    - testing
    - knowledge-management
  tags: []  # Empty list
  tags: null  # No tags
  ```

### author

- **Type**: `string`
- **Required**: ❌ No
- **Default**: `null`
- **Description**: Document author name
- **Example**:
  ```yaml
  author: John Doe
  author: 张三
  ```

### type

- **Type**: `string`
- **Required**: ❌ No
- **Default**: `null`
- **Description**: Document type classification
- **Suggested Values**:
  - `daily-note` - Daily journal entries
  - `research-note` - Research notes
  - `meeting-minutes` - Meeting records
  - `task-list` - Task lists
  - `knowledge-card` - Knowledge cards
  - `reference` - Reference materials
- **Example**:
  ```yaml
  type: daily-note
  type: research-note
  ```

### status

- **Type**: `string`
- **Required**: ❌ No
- **Default**: `null`
- **Description**: Document status
- **Suggested Values**:
  - `draft` - Work in progress
  - `in-review` - Under review
  - `published` - Completed and published
  - `archived` - Archived
- **Example**:
  ```yaml
  status: draft
  status: published
  ```

---

## Field Order

Recommended field order in frontmatter:

```yaml
---
title: Document Title
date: 2026-03-05
type: daily-note
status: draft
author: Author Name
tags:
  - tag1
  - tag2
---
```

**Rationale**:
1. `title` and `date` are required, list first
2. `type` and `status` describe document classification
3. `author` is metadata about creator
4. `tags` is often longest, list last

---

## Data Types

### DocumentMetadata Class

The metadata structure is defined in `scripts/types.py`:

```python
from dataclasses import dataclass
from datetime import date
from typing import List, Optional

@dataclass
class DocumentMetadata:
    title: str
    date: date
    tags: Optional[List[str]] = None
    author: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
```

---

## Validation

Metadata is validated by `MetadataParser.validate()` method:

### Validation Rules

1. **Required fields check**
   - `title` must be present
   - `date` must be present

2. **Type validation**
   - `title` must be string
   - `date` must be valid date format (YYYY-MM-DD)
   - `tags` must be list (if present)
   - `author`, `type`, `status` must be strings (if present)

3. **Format validation**
   - `date` string must match YYYY-MM-DD pattern

### Example Validation

```python
from scripts.metadata_parser import MetadataParser

parser = MetadataParser()

# Valid metadata
valid = {
    'title': 'Test Document',
    'date': '2026-03-05',
    'tags': ['python', 'test']
}
is_valid, errors = parser.validate(valid)
# is_valid: True, errors: []

# Invalid metadata
invalid = {
    'title': 'Test Document'
    # Missing 'date'
}
is_valid, errors = parser.validate(invalid)
# is_valid: False, errors: ["Required field 'date' is missing"]
```

---

## Template Variables

When creating templates, use these variable placeholders:

### Standard Variables

- `${{title}}` - Document title
- `${{date}}` - Creation date
- `${{created_at}}` - Timestamp of creation
- `${{tags}}` - Tags placeholder
- `${{author}}` - Author name

### Template-Specific Variables

Different document types may have additional variables:

#### daily-note.md
- `${{tasks}}` - Daily tasks list

#### meeting-minutes.md
- `${{attendees}}` - Meeting attendees
- `${{time}}` - Meeting time
- `${{location}}` - Meeting location
- `${{recorder}}` - Person recording minutes

#### task-list.md
- `${{priority}}` - Task priority level

#### research-note.md
- `${{category}}` - Research category

#### knowledge-card.md
- `${{category}}` - Knowledge category
- `${{source}}` - Information source

---

## Examples

### Minimal Valid Document

```markdown
---
title: My Document
date: 2026-03-05
---

# My Document

Content here.
```

### Complete Document

```markdown
---
title: Research Note - Python Testing Strategies
date: 2026-03-05
type: research-note
status: draft
author: Research Team
tags:
  - python
  - testing
  - quality-assurance
---

# Research Note - Python Testing Strategies

## Overview
This research note explores various testing strategies...

## Key Findings
...
```

### Edge Cases

#### Unicode Title

```markdown
---
title: 研究笔记 - Python测试策略
date: 2026-03-05
tags:
  - python
  - 测试
---

内容...
```

#### Empty Optional Fields

```markdown
---
title: Minimal Document
date: 2026-03-05
tags: []
author: null
type: null
status: null
---

Content...
```

---

## Migration Guide

When migrating existing documents:

1. **Add frontmatter** to documents without metadata
2. **Validate** using MetadataParser
3. **Fix errors** in date formats
4. **Standardize** tag naming (lowercase, hyphens)
5. **Set type** based on document content

---

## Best Practices

### Naming Conventions

- **Tags**: Use lowercase with hyphens
  - ✅ `knowledge-management`
  - ❌ `Knowledge Management`
  - ❌ `knowledgeManagement`

- **Types**: Use lowercase with hyphens
  - ✅ `daily-note`
  - ❌ `Daily Note`

### Date Handling

- Always use ISO 8601 format: `YYYY-MM-DD`
- Let parsers handle date object conversion
- Use string format in templates

### Tag Guidelines

- Keep tags consistent across documents
- Create a tag taxonomy for your project
- Limit to 5-7 tags per document
- Use hierarchical tags when needed: `python/testing`

---

## Implementation Notes

### Parsing

```python
from scripts.metadata_parser import MetadataParser

parser = MetadataParser()
metadata, body = parser.parse(document_content)
is_valid, errors = parser.validate(metadata)
```

### Creating DocumentMetadata

```python
from scripts.types import DocumentMetadata
from datetime import date

metadata = DocumentMetadata(
    title="My Document",
    date=date(2026, 3, 5),
    tags=["python", "example"],
    type="research-note",
    status="draft"
)
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-05 | Initial specification |

---

## References

- [YAML Specification](https://yaml.org/spec/)
- [ISO 8601 Date Format](https://www.iso.org/iso-8601-date-and-time-format.html)
- `scripts/types.py` - DocumentMetadata implementation
- `scripts/metadata_parser.py` - MetadataParser implementation
- `test-data/examples/` - Example documents

---

**Questions?** Contact PM Agent or refer to `project-management/` documentation.

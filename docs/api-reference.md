# API Reference

Complete API documentation for Knowledge Assistant modules.

## Table of Contents

- [scripts.types](#scriptstypes)
- [scripts.utils](#scriptsutils)
- [scripts.metadata_parser](#scriptsmetadata_parser)
- [scripts.template_engine](#scriptstemplate_engine)
- [scripts.config](#scriptsconfig)
- [scripts.tools.organize_notes](#scriptstoolsorganize_notes)
- [scripts.tools.generate_index](#scriptstoolsgenerate_index)

---

## scripts.types

Document metadata type definitions.

### DocumentMetadata

Dataclass representing document metadata.

#### Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `title` | `str` | Yes | Document title |
| `date` | `date` | Yes | Document date |
| `tags` | `Optional[List[str]]` | No | List of tags |
| `author` | `Optional[str]` | No | Document author |
| `type` | `Optional[str]` | No | Document type (e.g., 'research', 'meeting') |
| `status` | `Optional[str]` | No | Document status (e.g., 'draft', 'published') |

#### Example

```python
from scripts.types import DocumentMetadata
from datetime import date

# Create metadata
metadata = DocumentMetadata(
    title="Research Note",
    date=date(2026, 3, 6),
    tags=["python", "testing"],
    author="Your Name",
    type="research",
    status="draft"
)

# Access attributes
print(metadata.title)   # "Research Note"
print(metadata.tags)    # ["python", "testing"]
print(metadata.date)    # datetime.date(2026, 3, 6)
```

---

## scripts.utils

Utility functions for file operations, path handling, and string processing.

### get_project_root()

Get the project root directory.

#### Returns

- `Path`: Project root directory

#### Example

```python
from scripts.utils import get_project_root

root = get_project_root()
print(root)  # PosixPath('/path/to/knowledge-assistant')
```

---

### resolve_path()

Resolve a path relative to the project root.

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `path` | `Union[str, Path]` | required | Path to resolve (relative or absolute) |

#### Returns

- `Path`: Resolved absolute path

#### Example

```python
from scripts.utils import resolve_path

# Relative path
path = resolve_path("scripts/types.py")
print(path.is_absolute())  # True

# Absolute path (returned as-is)
path = resolve_path("/absolute/path")
```

---

### ensure_directory()

Ensure a directory exists, creating it if necessary.

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `directory` | `Union[str, Path]` | required | Directory path |

#### Returns

- `Path`: Directory path

#### Example

```python
from scripts.utils import ensure_directory

# Create directory if it doesn't exist
dir_path = ensure_directory("notes/daily")
print(dir_path.exists())  # True
```

---

### read_file()

Read the contents of a file.

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `file_path` | `Union[str, Path]` | required | File path |
| `encoding` | `str` | `"utf-8"` | File encoding |

#### Returns

- `str`: File contents

#### Raises

- `FileNotFoundError`: File does not exist
- `PermissionError`: Permission denied
- `UnicodeDecodeError`: Encoding error

#### Example

```python
from scripts.utils import read_file

content = read_file("notes/test.md")
print(content)
```

---

### write_file()

Write content to a file.

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `file_path` | `Union[str, Path]` | required | File path |
| `content` | `str` | required | Content to write |
| `encoding` | `str` | `"utf-8"` | File encoding |
| `create_dirs` | `bool` | `True` | Create parent directories |

#### Returns

- `Path`: File path

#### Raises

- `PermissionError`: Permission denied
- `UnicodeEncodeError`: Encoding error

#### Example

```python
from scripts.utils import write_file

write_file("notes/test.md", "# Test\nContent here")
```

---

### sanitize_filename()

Sanitize a filename by removing or replacing invalid characters.

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `filename` | `str` | required | Filename to sanitize |
| `replace_spaces` | `bool` | `False` | Replace spaces with underscores |
| `max_length` | `Optional[int]` | `None` | Maximum filename length |

#### Returns

- `str`: Sanitized filename

#### Example

```python
from scripts.utils import sanitize_filename

# Remove invalid characters
name = sanitize_filename('test<>:"/\\|?*file.txt')
print(name)  # "test________file.txt"

# Replace spaces
name = sanitize_filename("my document.txt", replace_spaces=True)
print(name)  # "my_document.txt"

# Truncate length
name = sanitize_filename("very_long_filename.txt", max_length=10)
print(name)  # "very_l.txt"
```

---

### format_date()

Format a date value to a string.

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `date_value` | `Union[date, datetime, str]` | required | Date value to format |
| `fmt` | `str` | `"%Y-%m-%d"` | Format string (or "iso") |

#### Returns

- `str`: Formatted date string

#### Example

```python
from scripts.utils import format_date
from datetime import date

# Default format
formatted = format_date(date(2026, 3, 6))
print(formatted)  # "2026-03-06"

# Custom format
formatted = format_date(date(2026, 3, 6), fmt="%Y/%m/%d")
print(formatted)  # "2026/03/06"

# String input (returned as-is)
formatted = format_date("2026-03-06")
print(formatted)  # "2026-03-06"
```

---

## scripts.metadata_parser

Parse and validate YAML frontmatter from documents.

### MetadataParser

Parser for YAML frontmatter.

#### Methods

##### \_\_init\_\_()

Initialize the parser.

```python
from scripts.metadata_parser import MetadataParser

parser = MetadataParser()
```

---

##### parse()

Parse YAML frontmatter from content.

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `content` | `str` | Document content with frontmatter |

**Returns**:

- `Tuple[Dict[str, Any], str]`: (metadata dict, body string)

**Raises**:

- `yaml.YAMLError`: Invalid YAML in frontmatter

**Example**:

```python
parser = MetadataParser()

content = """---
title: Test
date: 2026-03-06
tags: [python]
---

Body content."""

metadata, body = parser.parse(content)
print(metadata)  # {'title': 'Test', 'date': '2026-03-06', 'tags': ['python']}
print(body)      # "Body content."
```

---

##### validate()

Validate metadata against required schema.

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `metadata` | `Optional[Dict[str, Any]]` | Metadata to validate |

**Returns**:

- `Tuple[bool, List[str]]`: (is_valid, errors)

**Example**:

```python
metadata = {'title': 'Test', 'date': '2026-03-06'}
is_valid, errors = parser.validate(metadata)

print(is_valid)  # True
print(errors)    # []

# Invalid metadata
metadata = {'title': 'Test'}  # Missing date
is_valid, errors = parser.validate(metadata)

print(is_valid)  # False
print(errors)    # ["Required field 'date' is missing"]
```

---

## scripts.template_engine

Template engine for loading and rendering document templates.

### TemplateEngine

Engine for template rendering with variable substitution.

#### Methods

##### \_\_init\_\_()

Initialize the template engine.

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `template_dir` | `str` | Directory containing templates |

**Raises**:

- `ValueError`: Template directory does not exist

**Example**:

```python
from scripts.template_engine import TemplateEngine

engine = TemplateEngine('./templates')
```

---

##### load_template()

Load a template file by name.

**Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `template_name` | `str` | required | Template name (without .md) |
| `use_cache` | `bool` | `True` | Use cached template |

**Returns**:

- `str`: Template content

**Raises**:

- `FileNotFoundError`: Template not found

**Example**:

```python
template = engine.load_template('daily-note')
print('{{title}}' in template)  # True
```

---

##### render()

Render a template with variable substitution.

**Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `template_name` | `str` | required | Template name |
| `use_cache` | `bool` | `True` | Use cached template |
| `**variables` | `Any` | - | Variables to substitute |

**Returns**:

- `str`: Rendered content

**Raises**:

- `FileNotFoundError`: Template not found

**Example**:

```python
content = engine.render(
    'daily-note',
    title='My Day',
    date='2026-03-06'
)

print('My Day' in content)      # True
print('{{title}}' in content)   # False
```

---

##### list_templates()

List all available templates.

**Returns**:

- `list[str]`: Template names

**Example**:

```python
templates = engine.list_templates()
print(templates)
# ['daily-note', 'knowledge-card', 'meeting-minutes', 'research-note', 'task-list']
```

---

##### extract_variables()

Extract variable names from a template.

**Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `template_name` | `str` | required | Template name |
| `use_cache` | `bool` | `True` | Use cached template |

**Returns**:

- `list[str]`: Variable names

**Example**:

```python
variables = engine.extract_variables('daily-note')
print(variables)
# ['author', 'date', 'title']
```

---

##### clear_cache()

Clear the template cache.

**Example**:

```python
engine.clear_cache()
```

---

## scripts.config

Configuration management for YAML configuration files.

### ConfigurationError

Exception raised for configuration errors.

```python
from scripts.config import ConfigurationError

try:
    # Configuration operation
    pass
except ConfigurationError as e:
    print(f"Configuration error: {e}")
```

---

### ConfigManager

Manager for loading and managing configuration.

#### Methods

##### \_\_init\_\_()

Initialize the configuration manager.

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `config_path` | `Optional[str]` | Path to config file (None for defaults) |

**Example**:

```python
from scripts.config import ConfigManager

# With config file
config = ConfigManager('config.yaml')

# With defaults only
config = ConfigManager()
```

---

##### load()

Load configuration from file.

**Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `use_defaults` | `bool` | `True` | Merge with defaults |

**Raises**:

- `ConfigurationError`: Config file not found or invalid

**Example**:

```python
config = ConfigManager('config.yaml')
config.load()
```

---

##### validate()

Validate the loaded configuration.

**Returns**:

- `bool`: True if valid

**Raises**:

- `ConfigurationError`: Validation failed

**Example**:

```python
config.load()
is_valid = config.validate()  # Raises if invalid
```

---

##### get()

Get a configuration value by key.

**Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `key` | `str` | required | Configuration key (supports dot notation) |
| `default` | `Optional[Any]` | `None` | Default value |
| `required` | `bool` | `False` | Raise error if missing |

**Returns**:

- `Any`: Configuration value

**Raises**:

- `ConfigurationError`: Key required but not found

**Example**:

```python
# Simple key
value = config.get('template_dir')

# Nested key (dot notation)
value = config.get('templates.daily-note.auto_date')

# With default
value = config.get('missing_key', default='default_value')

# Required (raises if missing)
value = config.get('template_dir', required=True)
```

---

##### set()

Set a configuration value.

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `key` | `str` | Configuration key (supports dot notation) |
| `value` | `Any` | Value to set |

**Example**:

```python
config.set('template_dir', './my-templates')
config.set('templates.daily-note.auto_date', False)
```

---

##### save()

Save configuration to a YAML file.

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `path` | `Optional[str]` | Save path (None for original path) |

**Raises**:

- `ConfigurationError`: No path specified

**Example**:

```python
config.set('template_dir', './my-templates')
config.save('new-config.yaml')
```

---

##### reload()

Reload configuration from file.

**Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `use_defaults` | `bool` | `True` | Merge with defaults |

**Example**:

```python
config.load()
# ... file changes ...
config.reload()
```

---

## scripts.tools.organize_notes

Note organization tool for moving/copying files by metadata criteria.

### DocumentInfo

Information about a scanned document.

#### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `path` | `Path` | Document file path |
| `title` | `str` | Document title |
| `date` | `Optional[date]` | Document date |
| `tags` | `List[str]` | Document tags |
| `type` | `Optional[str]` | Document type |
| `author` | `Optional[str]` | Document author |

---

### OrganizationResult

Result of organization operation.

#### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `moved` | `int` | Number of notes moved |
| `copied` | `int` | Number of notes copied |
| `skipped` | `int` | Number of notes skipped |
| `errors` | `List[str]` | Error messages |
| `details` | `Dict[str, str]` | Source to destination mapping |

---

### scan_directory()

Scan a directory for markdown documents.

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `directory` | `Union[str, Path]` | required | Directory to scan |
| `recursive` | `bool` | `True` | Scan subdirectories |
| `extensions` | `Optional[List[str]]` | `[".md", ".markdown"]` | File extensions |

#### Returns

- `List[DocumentInfo]`: List of document information

#### Example

```python
from scripts.tools.organize_notes import scan_directory

docs = scan_directory('notes/')
for doc in docs:
    print(f"{doc.title}: {doc.path}")
```

---

### organize_notes()

Organize notes by date, tags, or type.

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `source_dir` | `Union[str, Path]` | required | Source directory |
| `target_dir` | `Union[str, Path]` | required | Target directory |
| `by` | `str` | `"date"` | Organization strategy |
| `move` | `bool` | `True` | Move files (False to copy) |
| `recursive` | `bool` | `True` | Scan subdirectories |
| `date_format` | `str` | `"{year}/{month}"` | Date directory format |
| `overwrite` | `bool` | `False` | Overwrite existing files |

#### Returns

- `OrganizationResult`: Result object

#### Example

```python
from scripts.tools.organize_notes import organize_notes

# Organize by date
result = organize_notes(
    source_dir='notes/',
    target_dir='organized/',
    by='date'
)

print(f"Moved: {result.moved}")
print(f"Skipped: {result.skipped}")
```

---

## scripts.tools.generate_index

Index generation tool for creating markdown index files.

### DocumentInfo

Information about a scanned document.

#### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `path` | `Path` | Document file path |
| `title` | `str` | Document title |
| `date` | `Optional[date]` | Document date |
| `tags` | `Optional[List[str]]` | Document tags |
| `type` | `Optional[str]` | Document type |
| `author` | `Optional[str]` | Document author |

---

### scan_directory()

Scan a directory for markdown documents.

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `directory` | `Union[str, Path]` | required | Directory to scan |
| `recursive` | `bool` | `True` | Scan subdirectories |
| `extensions` | `Optional[List[str]]` | `[".md", ".markdown"]` | File extensions |

#### Returns

- `List[DocumentInfo]`: List of document information

#### Example

```python
from scripts.tools.generate_index import scan_directory

docs = scan_directory('notes/')
for doc in docs:
    print(f"{doc.title}: {doc.path}")
```

---

### generate_index()

Generate a markdown index for a directory.

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `directory` | `Union[str, Path]` | required | Directory to index |
| `output_file` | `Union[str, Path]` | required | Output file path |
| `title` | `str` | `"Document Index"` | Index title |
| `group_by` | `str` | `"date"` | Grouping strategy |
| `include_toc` | `bool` | `True` | Include table of contents |
| `recursive` | `bool` | `True` | Include subdirectories |

#### Returns

- `Path`: Path to generated index file

#### Example

```python
from scripts.tools.generate_index import generate_index

index_path = generate_index(
    directory='notes/',
    output_file='INDEX.md',
    title='My Knowledge Base'
)

print(f"Index created: {index_path}")
```

---

## Version

- **API Version**: 1.0.0
- **Last Updated**: 2026-03-06
- **Compatibility**: Python 3.8+

## See Also

- [User Guide](user-guide.md) - Complete usage guide
- [Quick Start](quick-start.md) - Getting started tutorial
- [Examples](../examples/) - Code examples

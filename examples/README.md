# Examples

This directory contains runnable examples demonstrating Knowledge Assistant features.

## Examples Overview

| File | Description | Difficulty |
|------|-------------|------------|
| `basic-usage.py` | Basic template and metadata usage | Beginner |
| `template-example.py` | Complete template system demo | Beginner |
| `organize-example.py` | Note organization workflow | Intermediate |
| `config-example.yaml` | Configuration file example | Beginner |

## Running Examples

### Prerequisites

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure you're in the project root:
```bash
cd knowledge-assistant
```

### Run an Example

```bash
python examples/basic-usage.py
```

## Example Descriptions

### 1. Basic Usage (`basic-usage.py`)

**What it demonstrates**:
- Creating documents from templates
- Parsing document metadata
- Validating metadata
- Working with DocumentMetadata objects

**Time to complete**: ~2 minutes

**Run**:
```bash
python examples/basic-usage.py
```

### 2. Template System (`template-example.py`)

**What it demonstrates**:
- Loading templates
- Rendering templates with variables
- Listing available templates
- Extracting template variables
- Template caching

**Time to complete**: ~3 minutes

**Run**:
```bash
python examples/template-example.py
```

### 3. Organize Notes (`organize-example.py`)

**What it demonstrates**:
- Scanning directories for documents
- Organizing notes by date, tags, or type
- Using the OrganizationResult object
- Creating organizational workflows

**Time to complete**: ~5 minutes

**Run**:
```bash
python examples/organize-example.py
```

### 4. Configuration Example (`config-example.yaml`)

**What it demonstrates**:
- Configuration file structure
- Default values
- Template-specific settings
- Editor and naming conventions

**Use**:
```bash
cp examples/config-example.yaml config.yaml
# Edit config.yaml as needed
```

## Common Patterns

### Daily Journaling Workflow

```python
from scripts.template_engine import TemplateEngine
from datetime import date

engine = TemplateEngine('./templates')
daily = engine.render('daily-note', title='Today', date=str(date.today()))
```

### Research Note Creation

```python
engine = TemplateEngine('./templates')
research = engine.render(
    'research-note',
    title='Python Study',
    date='2026-03-06',
    subject='Programming'
)
```

### Note Organization

```python
from scripts.tools.organize_notes import organize_notes

result = organize_notes('inbox/', 'organized/', by='date')
print(f"Organized {result.moved} notes")
```

### Index Generation

```python
from scripts.tools.generate_index import generate_index

generate_index('notes/', 'INDEX.md', title='My Notes')
```

## Troubleshooting

### Import Errors

If you get import errors, make sure:
1. You're in the project root directory
2. Virtual environment is activated
3. Dependencies are installed

```bash
# From project root
cd knowledge-assistant
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Template Not Found

If templates aren't found, check the template directory path:

```python
# Use absolute path if needed
import os
template_dir = os.path.join(os.getcwd(), 'templates')
engine = TemplateEngine(template_dir)
```

### File Permissions

If you get permission errors when writing files:
- Check directory permissions
- Use a different output directory
- Run with appropriate permissions

## Next Steps

After trying these examples:

1. **Read the documentation**:
   - [User Guide](../docs/user-guide.md)
   - [API Reference](../docs/api-reference.md)

2. **Build your own workflows**:
   - Create custom templates
   - Automate note organization
   - Generate reports

3. **Contribute**:
   - Share your workflows
   - Improve examples
   - Add new examples

---

**Questions?** Check the [documentation](../docs/) or review the API reference.

"""Test configuration and shared fixtures for Knowledge Assistant."""

import pytest
from pathlib import Path
from typing import Dict, Any, Callable, Optional, List
from datetime import date


def pytest_configure(config):
    """Configure custom markers for pytest."""
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "slow: mark test as slow running test")


@pytest.fixture
def tmp_project_dir(tmp_path: Path) -> Path:
    """创建临时项目目录结构"""
    project = tmp_path / "test_project"
    project.mkdir()
    (project / "documents").mkdir()
    (project / "templates").mkdir()
    return project


@pytest.fixture
def sample_metadata() -> Dict[str, Any]:
    """示例元数据"""
    return {
        "title": "Test Document",
        "date": "2026-03-05",
        "type": "daily",
        "tags": ["test", "example"],
        "author": "Test Agent",
    }


@pytest.fixture
def sample_document_content() -> str:
    """示例文档内容（包含frontmatter）"""
    return """---
title: Test Document
date: 2026-03-05
type: daily
tags:
  - test
  - example
---

# Test Document

This is a test document for unit testing.

## Section 1

Content goes here.

## Section 2

More content.
"""


@pytest.fixture
def invalid_yaml_content() -> str:
    """无效YAML内容"""
    return """---
title: Test
invalid yaml: [unclosed
---

# Content
"""


@pytest.fixture
def missing_fields_content() -> str:
    """缺失必需字段的文档"""
    return """---
title: Missing Date Document
---

# Content without date field
"""


def create_test_document(directory: Path, filename: str, content: str) -> Path:
    """创建测试文档"""
    filepath = directory / filename
    filepath.write_text(content, encoding="utf-8")
    return filepath


@pytest.fixture
def test_document_factory(tmp_project_dir: Path):
    """测试文档工厂fixture"""

    def _create(filename: str, content: str) -> Path:
        return create_test_document(tmp_project_dir / "documents", filename, content)

    return _create


# ==================== Integration Test Fixtures ====================


@pytest.fixture
def metadata_parser():
    """创建MetadataParser实例"""
    from scripts.metadata_parser import MetadataParser

    return MetadataParser()


@pytest.fixture
def multi_language_document() -> str:
    """多语言文档示例"""
    return """---
title: 多语言测试文档 Multilingual Test Document
date: 2026-03-05
type: research
tags:
  - 测试
  - test
  - テスト
  - 테스트
author: Test Agent
---

# Multilingual Content

## English Section
This is English content for testing Unicode support.

## 中文部分
这是中文内容，用于测试Unicode支持。

## 日本語セクション
これは日本語のコンテンツです。

## 한국어 섹션
이것은 한국어 콘텐츠입니다.

## Mixed Content
Mixed content with 中文, English, 日本語, and 한국어.
"""


@pytest.fixture
def performance_test_document() -> str:
    """性能测试文档（大文件）"""
    large_body = "\n".join([f"## Section {i}\n\nContent for section {i}." for i in range(100)])
    return f"""---
title: Performance Test Document
date: 2026-03-05
type: performance-test
tags:
  - performance
  - large-file
author: Test Agent
---

# Performance Test Document

{large_body}
"""


@pytest.fixture
def edge_case_document() -> str:
    """边界情况测试文档"""
    return """---
title: "Edge Case: Special Characters @#$%^&*()"
date: 2026-03-05
type: edge-case
tags:
  - "tag with spaces"
  - "tag-with-dashes"
  - "tag_with_underscores"
  - "tag.with.dots"
  - "tag@with#special$chars"
author: "Author Name (with parentheses)"
---

# Edge Case Test Document

## Empty Section


## Very Long Line
This is a very long line that tests how the parser handles extremely long lines without any breaks or formatting which could potentially cause issues with line-based parsing algorithms or buffer overflows in older systems but should be handled gracefully by modern parsers.

## Special Characters
Characters: @#$%^&*()_+-=[]{}|;':",./<>?
Unicode: 你好世界 🎉 émojis 🚀

## Code Blocks

```python
def test():
    pass
```

```javascript
function test() {
    return null;
}
```

## Tables
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
"""


@pytest.fixture
def template_directory(tmp_project_dir: Path) -> Path:
    """创建模板目录"""
    templates = tmp_project_dir / "templates"
    templates.mkdir(exist_ok=True)

    # 创建示例模板
    (templates / "daily-note.md").write_text("""---
title: Daily Note Template
date: {date}
type: daily
---

# {title}

## Tasks
- [ ] Task 1
- [ ] Task 2

## Notes
{content}
""")

    (templates / "research-note.md").write_text("""---
title: Research Note Template
date: {date}
type: research
tags:
  - research
---

# {title}

## Abstract
{abstract}

## Content
{content}

## References
{references}
""")

    return templates


@pytest.fixture
def document_factory() -> Callable:
    """文档工厂fixture，用于创建各种类型的测试文档"""

    def _create_document(
        title: str = "Test Document",
        date_str: str = "2026-03-05",
        doc_type: str = "test",
        tags: Optional[List[str]] = None,
        author: str = "Test Agent",
        body: str = "Test content",
    ) -> str:
        """创建自定义测试文档"""
        tags_list = tags if tags is not None else []
        tags_yaml = "\n".join([f"  - {tag}" for tag in tags_list])
        return f"""---
title: {title}
date: {date_str}
type: {doc_type}
{f"tags:{chr(10)}{tags_yaml}" if tags_list else ""}
author: {author}
---

# {title}

{body}
"""

    return _create_document


@pytest.fixture
def integration_test_data(tmp_project_dir: Path) -> Dict[str, Path]:
    """集成测试数据集"""
    data_dir = tmp_project_dir / "test_documents"
    data_dir.mkdir(exist_ok=True)

    # 创建各种测试文档
    documents = {
        "valid": data_dir / "valid_doc.md",
        "invalid_yaml": data_dir / "invalid_yaml.md",
        "missing_fields": data_dir / "missing_fields.md",
        "multi_language": data_dir / "multi_language.md",
        "performance": data_dir / "performance.md",
    }

    # 写入文档内容
    documents["valid"].write_text("""---
title: Valid Document
date: 2026-03-05
type: test
---

Content here.
""")

    documents["invalid_yaml"].write_text("""---
title: Invalid
invalid: [unclosed
---

Content.
""")

    documents["missing_fields"].write_text("""---
title: Missing Fields
---

No date field.
""")

    documents["multi_language"].write_text("""---
title: 多语言测试
date: 2026-03-05
---

中文内容测试。
""")

    documents["performance"].write_text("""---
title: Performance Test
date: 2026-03-05
---

""" + "\n".join([f"Line {i}" for i in range(1000)]))

    return documents

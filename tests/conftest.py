"""Test configuration and shared fixtures for Knowledge Assistant."""

import pytest
from pathlib import Path
from typing import Dict, Any


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
        "author": "Test Agent"
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
    filepath.write_text(content, encoding='utf-8')
    return filepath


@pytest.fixture
def test_document_factory(tmp_project_dir: Path):
    """测试文档工厂fixture"""
    def _create(filename: str, content: str) -> Path:
        return create_test_document(tmp_project_dir / "documents", filename, content)
    return _create

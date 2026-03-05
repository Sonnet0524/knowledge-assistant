#!/usr/bin/env python3
"""
Unit tests for MetadataParser.

Tests the MetadataParser class including:
- YAML frontmatter parsing
- Metadata validation
- Error handling
- Integration with DocumentMetadata type
"""

import pytest
from datetime import date
from scripts.metadata_parser import MetadataParser


class TestMetadataParserBasicParsing:
    """Test basic parsing functionality"""

    def test_parse_basic_frontmatter(self):
        """Test parsing basic YAML frontmatter"""
        content = """---
title: Test Document
date: 2026-03-05
---

This is the body content."""

        parser = MetadataParser()
        metadata, body = parser.parse(content)

        assert metadata["title"] == "Test Document"
        assert str(metadata["date"]) == "2026-03-05"
        assert "This is the body content." in body

    def test_parse_with_all_fields(self):
        """Test parsing frontmatter with all fields"""
        content = """---
title: Complete Document
date: 2026-03-05
tags:
  - python
  - testing
author: Agent B
type: research
status: draft
---

Body content here."""

        parser = MetadataParser()
        metadata, body = parser.parse(content)

        assert metadata["title"] == "Complete Document"
        assert str(metadata["date"]) == "2026-03-05"
        assert metadata["tags"] == ["python", "testing"]
        assert metadata["author"] == "Agent B"
        assert metadata["type"] == "research"
        assert metadata["status"] == "draft"
        assert body.strip() == "Body content here."

    def test_parse_no_frontmatter(self):
        """Test parsing content without frontmatter"""
        content = "Just plain text without frontmatter."

        parser = MetadataParser()
        metadata, body = parser.parse(content)

        assert metadata == {}
        assert body == content

    def test_parse_empty_frontmatter(self):
        """Test parsing empty frontmatter"""
        content = """---
---
Body content."""

        parser = MetadataParser()
        metadata, body = parser.parse(content)

        assert metadata == {}
        assert "Body content." in body

    def test_parse_multiline_body(self):
        """Test parsing with multiline body"""
        content = """---
title: Test
date: 2026-03-05
---

Line 1
Line 2
Line 3

Paragraph 2"""

        parser = MetadataParser()
        metadata, body = parser.parse(content)

        assert metadata["title"] == "Test"
        assert "Line 1" in body
        assert "Line 2" in body
        assert "Line 3" in body
        assert "Paragraph 2" in body

    def test_parse_frontmatter_with_special_characters(self):
        """Test parsing frontmatter with special characters in values"""
        content = """---
title: "Test: A Special Title"
date: 2026-03-05
author: "John Doe <john@example.com>"
---

Body"""

        parser = MetadataParser()
        metadata, body = parser.parse(content)

        assert metadata["title"] == "Test: A Special Title"
        assert metadata["author"] == "John Doe <john@example.com>"


class TestMetadataParserValidation:
    """Test metadata validation functionality"""

    def test_validate_required_fields_present(self):
        """Test validation with all required fields"""
        parser = MetadataParser()
        metadata = {"title": "Test", "date": "2026-03-05"}

        is_valid, errors = parser.validate(metadata)

        assert is_valid is True
        assert len(errors) == 0

    def test_validate_missing_title(self):
        """Test validation when title is missing"""
        parser = MetadataParser()
        metadata = {"date": "2026-03-05"}

        is_valid, errors = parser.validate(metadata)

        assert is_valid is False
        assert len(errors) > 0
        assert any("title" in error.lower() for error in errors)

    def test_validate_missing_date(self):
        """Test validation when date is missing"""
        parser = MetadataParser()
        metadata = {"title": "Test"}

        is_valid, errors = parser.validate(metadata)

        assert is_valid is False
        assert len(errors) > 0
        assert any("date" in error.lower() for error in errors)

    def test_validate_missing_both_required_fields(self):
        """Test validation when both required fields are missing"""
        parser = MetadataParser()
        metadata = {}

        is_valid, errors = parser.validate(metadata)

        assert is_valid is False
        assert len(errors) >= 2

    def test_validate_empty_metadata(self):
        """Test validation with empty metadata dict"""
        parser = MetadataParser()
        metadata = {}

        is_valid, errors = parser.validate(metadata)

        assert is_valid is False

    def test_validate_date_format_valid(self):
        """Test validation with valid date format"""
        parser = MetadataParser()
        from datetime import date as date_type

        metadata = {
            "title": "Test",
            "date": date_type(2026, 3, 5),
        }

        is_valid, errors = parser.validate(metadata)

        assert is_valid is True

    def test_validate_date_format_invalid(self):
        """Test validation with invalid date format"""
        parser = MetadataParser()
        metadata = {"title": "Test", "date": "03/05/2026"}

        is_valid, errors = parser.validate(metadata)

        assert is_valid is False
        assert any("date" in error.lower() for error in errors)

    def test_validate_title_not_string(self):
        """Test validation when title is not a string"""
        parser = MetadataParser()
        metadata = {"title": 123, "date": "2026-03-05"}

        is_valid, errors = parser.validate(metadata)

        assert is_valid is False

    def test_validate_tags_not_list(self):
        """Test validation when tags is not a list"""
        parser = MetadataParser()
        metadata = {
            "title": "Test",
            "date": "2026-03-05",
            "tags": "not-a-list",
        }

        is_valid, errors = parser.validate(metadata)

        assert is_valid is False


class TestMetadataParserErrorHandling:
    """Test error handling"""

    def test_parse_invalid_yaml(self):
        """Test parsing invalid YAML in frontmatter"""
        content = """---
title: Test
date: 2026-03-05
invalid yaml: [unclosed
---

Body"""

        parser = MetadataParser()
        with pytest.raises(Exception):
            parser.parse(content)

    def test_parse_unclosed_frontmatter(self):
        """Test parsing unclosed frontmatter"""
        content = """---
title: Test
date: 2026-03-05

Body without closing"""

        parser = MetadataParser()
        metadata, body = parser.parse(content)

        assert metadata == {}
        assert "---" in body

    def test_validate_with_none_metadata(self):
        """Test validation with None metadata"""
        parser = MetadataParser()

        is_valid, errors = parser.validate(None)

        assert is_valid is False
        assert len(errors) > 0


class TestMetadataParserIntegration:
    """Test integration with DocumentMetadata"""

    def test_parse_to_document_metadata(self):
        """Test parsing and converting to DocumentMetadata"""
        try:
            from scripts.types import DocumentMetadata
        except ImportError:
            pytest.skip("DocumentMetadata not available yet")

        content = """---
title: Integration Test
date: 2026-03-05
tags:
  - integration
author: Agent B
---

Body content."""

        parser = MetadataParser()
        metadata_dict, body = parser.parse(content)

        is_valid, errors = parser.validate(metadata_dict)
        assert is_valid is True

        from datetime import date as date_type

        metadata = DocumentMetadata(
            title=metadata_dict["title"],
            date=(
                metadata_dict["date"]
                if isinstance(metadata_dict["date"], date_type)
                else date_type.fromisoformat(str(metadata_dict["date"]))
            ),
            tags=metadata_dict.get("tags"),
            author=metadata_dict.get("author"),
        )

        assert metadata.title == "Integration Test"
        assert metadata.date == date(2026, 3, 5)
        assert metadata.tags == ["integration"]
        assert metadata.author == "Agent B"


class TestMetadataParserEdgeCases:
    """Test edge cases and special scenarios"""

    def test_parse_frontmatter_with_list_values(self):
        """Test parsing frontmatter with list values"""
        content = """---
title: Test
date: 2026-03-05
tags:
  - tag1
  - tag2
  - tag3
---

Body"""

        parser = MetadataParser()
        metadata, body = parser.parse(content)

        assert metadata["tags"] == ["tag1", "tag2", "tag3"]

    def test_parse_frontmatter_with_nested_structure(self):
        """Test parsing frontmatter with nested structure"""
        content = """---
title: Test
date: 2026-03-05
meta:
  key1: value1
  key2: value2
---

Body"""

        parser = MetadataParser()
        metadata, body = parser.parse(content)

        assert "meta" in metadata
        assert metadata["meta"]["key1"] == "value1"

    def test_parse_frontmatter_with_numbers(self):
        """Test parsing frontmatter with numeric values"""
        content = """---
title: Test
date: 2026-03-05
version: 1.0
count: 42
---

Body"""

        parser = MetadataParser()
        metadata, body = parser.parse(content)

        assert metadata["version"] == 1.0
        assert metadata["count"] == 42

    def test_parse_frontmatter_with_boolean(self):
        """Test parsing frontmatter with boolean values"""
        content = """---
title: Test
date: 2026-03-05
published: true
draft: false
---

Body"""

        parser = MetadataParser()
        metadata, body = parser.parse(content)

        assert metadata["published"] is True
        assert metadata["draft"] is False

    def test_parse_empty_body(self):
        """Test parsing with empty body"""
        content = """---
title: Test
date: 2026-03-05
---
"""

        parser = MetadataParser()
        metadata, body = parser.parse(content)

        assert metadata["title"] == "Test"
        assert body.strip() == ""

    def test_parse_body_with_code_blocks(self):
        """Test parsing body with code blocks"""
        content = """---
title: Test
date: 2026-03-05
---

```python
def hello():
    print("Hello, World!")
```

Some more text."""

        parser = MetadataParser()
        metadata, body = parser.parse(content)

        assert "```python" in body
        assert "def hello():" in body

    def test_parse_multiple_separators_in_body(self):
        """Test parsing body with multiple --- separators"""
        content = """---
title: Test
date: 2026-03-05
---

Some text

---

More text"""

        parser = MetadataParser()
        metadata, body = parser.parse(content)

        assert metadata["title"] == "Test"
        assert "---" in body


class TestMetadataParserWhitespace:
    """Test whitespace handling"""

    def test_parse_with_extra_whitespace_around_separator(self):
        """Test parsing with extra whitespace around separators"""
        content = """---
title: Test
date: 2026-03-05
---

Body content."""

        parser = MetadataParser()
        metadata, body = parser.parse(content)

        assert metadata["title"] == "Test"

    def test_parse_preserves_body_whitespace(self):
        """Test that body whitespace is preserved"""
        content = """---
title: Test
date: 2026-03-05
---

    Indented line

Normal line"""

        parser = MetadataParser()
        metadata, body = parser.parse(content)

        assert "    Indented line" in body


class TestMetadataParserUnicode:
    """Test Unicode handling"""

    def test_parse_unicode_in_title(self):
        """Test parsing Unicode characters in title"""
        content = """---
title: 测试文档 - Test Document
date: 2026-03-05
---

Body"""

        parser = MetadataParser()
        metadata, body = parser.parse(content)

        assert metadata["title"] == "测试文档 - Test Document"

    def test_parse_unicode_in_tags(self):
        """Test parsing Unicode characters in tags"""
        content = """---
title: Test
date: 2026-03-05
tags:
  - 标签1
  - 标签2
---

Body"""

        parser = MetadataParser()
        metadata, body = parser.parse(content)

        assert metadata["tags"] == ["标签1", "标签2"]

    def test_parse_unicode_in_body(self):
        """Test parsing Unicode characters in body"""
        content = """---
title: Test
date: 2026-03-05
---

这是一段中文内容。
This is English content.
日本語のコンテンツも含まれています。"""

        parser = MetadataParser()
        metadata, body = parser.parse(content)

        assert "中文内容" in body
        assert "English content" in body
        assert "日本語" in body


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

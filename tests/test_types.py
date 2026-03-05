#!/usr/bin/env python3
"""
Unit tests for DocumentMetadata type definition.

Tests the DocumentMetadata dataclass including:
- Required fields (title, date)
- Optional fields (tags, author, type, status)
- Type annotations
- Default values
"""

import pytest
from datetime import date
from dataclasses import fields

from scripts.types import DocumentMetadata


class TestDocumentMetadataBasic:
    """Test basic DocumentMetadata functionality"""

    def test_create_with_required_fields_only(self):
        """Test creating DocumentMetadata with only required fields"""
        metadata = DocumentMetadata(title="Test Document", date=date(2026, 3, 5))

        assert metadata.title == "Test Document"
        assert metadata.date == date(2026, 3, 5)
        assert metadata.tags is None
        assert metadata.author is None
        assert metadata.type is None
        assert metadata.status is None

    def test_create_with_all_fields(self):
        """Test creating DocumentMetadata with all fields"""
        metadata = DocumentMetadata(
            title="Complete Document",
            date=date(2026, 3, 5),
            tags=["python", "testing"],
            author="Agent B",
            type="research",
            status="draft",
        )

        assert metadata.title == "Complete Document"
        assert metadata.date == date(2026, 3, 5)
        assert metadata.tags == ["python", "testing"]
        assert metadata.author == "Agent B"
        assert metadata.type == "research"
        assert metadata.status == "draft"

    def test_title_is_required(self):
        """Test that title is a required field"""
        field_names = [f.name for f in fields(DocumentMetadata)]
        assert "title" in field_names

        title_field = [f for f in fields(DocumentMetadata) if f.name == "title"][0]
        assert title_field.default == title_field.default_factory

    def test_date_is_required(self):
        """Test that date is a required field"""
        field_names = [f.name for f in fields(DocumentMetadata)]
        assert "date" in field_names

        date_field = [f for f in fields(DocumentMetadata) if f.name == "date"][0]
        assert date_field.default == date_field.default_factory


class TestDocumentMetadataOptionalFields:
    """Test optional fields in DocumentMetadata"""

    def test_tags_optional_with_default_none(self):
        """Test that tags is optional and defaults to None"""
        metadata = DocumentMetadata(title="Test", date=date(2026, 3, 5))
        assert metadata.tags is None

    def test_tags_can_be_list(self):
        """Test that tags can be a list"""
        metadata = DocumentMetadata(
            title="Test", date=date(2026, 3, 5), tags=["tag1", "tag2", "tag3"]
        )
        assert metadata.tags == ["tag1", "tag2", "tag3"]

    def test_tags_can_be_empty_list(self):
        """Test that tags can be an empty list"""
        metadata = DocumentMetadata(title="Test", date=date(2026, 3, 5), tags=[])
        assert metadata.tags == []

    def test_author_optional_with_default_none(self):
        """Test that author is optional and defaults to None"""
        metadata = DocumentMetadata(title="Test", date=date(2026, 3, 5))
        assert metadata.author is None

    def test_author_can_be_string(self):
        """Test that author can be a string"""
        metadata = DocumentMetadata(title="Test", date=date(2026, 3, 5), author="John Doe")
        assert metadata.author == "John Doe"

    def test_type_optional_with_default_none(self):
        """Test that type is optional and defaults to None"""
        metadata = DocumentMetadata(title="Test", date=date(2026, 3, 5))
        assert metadata.type is None

    def test_type_can_be_string(self):
        """Test that type can be a string"""
        metadata = DocumentMetadata(title="Test", date=date(2026, 3, 5), type="research-note")
        assert metadata.type == "research-note"

    def test_status_optional_with_default_none(self):
        """Test that status is optional and defaults to None"""
        metadata = DocumentMetadata(title="Test", date=date(2026, 3, 5))
        assert metadata.status is None

    def test_status_can_be_string(self):
        """Test that status can be a string"""
        metadata = DocumentMetadata(title="Test", date=date(2026, 3, 5), status="published")
        assert metadata.status == "published"


class TestDocumentMetadataTypeAnnotations:
    """Test type annotations on DocumentMetadata"""

    def test_title_type_annotation(self):
        """Test that title has correct type annotation"""
        title_field = [f for f in fields(DocumentMetadata) if f.name == "title"][0]
        assert title_field.type == str

    def test_date_type_annotation(self):
        """Test that date has correct type annotation"""
        date_field = [f for f in fields(DocumentMetadata) if f.name == "date"][0]
        assert date_field.type == date

    def test_tags_type_annotation(self):
        """Test that tags has correct type annotation"""
        import typing

        tags_field = [f for f in fields(DocumentMetadata) if f.name == "tags"][0]
        assert typing.get_origin(tags_field.type) is not None

    def test_author_type_annotation(self):
        """Test that author has correct type annotation"""
        import typing

        author_field = [f for f in fields(DocumentMetadata) if f.name == "author"][0]
        assert typing.get_origin(author_field.type) is not None


class TestDocumentMetadataEquality:
    """Test equality and comparison of DocumentMetadata"""

    def test_equality_same_values(self):
        """Test that two DocumentMetadata with same values are equal"""
        metadata1 = DocumentMetadata(title="Test", date=date(2026, 3, 5), tags=["a", "b"])
        metadata2 = DocumentMetadata(title="Test", date=date(2026, 3, 5), tags=["a", "b"])
        assert metadata1 == metadata2

    def test_equality_different_title(self):
        """Test that DocumentMetadata with different titles are not equal"""
        metadata1 = DocumentMetadata(title="Test1", date=date(2026, 3, 5))
        metadata2 = DocumentMetadata(title="Test2", date=date(2026, 3, 5))
        assert metadata1 != metadata2

    def test_equality_different_date(self):
        """Test that DocumentMetadata with different dates are not equal"""
        metadata1 = DocumentMetadata(title="Test", date=date(2026, 3, 5))
        metadata2 = DocumentMetadata(title="Test", date=date(2026, 3, 6))
        assert metadata1 != metadata2

    def test_equality_different_tags(self):
        """Test that DocumentMetadata with different tags are not equal"""
        metadata1 = DocumentMetadata(title="Test", date=date(2026, 3, 5), tags=["a"])
        metadata2 = DocumentMetadata(title="Test", date=date(2026, 3, 5), tags=["b"])
        assert metadata1 != metadata2


class TestDocumentMetadataStringRepresentation:
    """Test string representation of DocumentMetadata"""

    def test_repr(self):
        """Test __repr__ method"""
        metadata = DocumentMetadata(title="Test Doc", date=date(2026, 3, 5))
        repr_str = repr(metadata)
        assert "DocumentMetadata" in repr_str
        assert "Test Doc" in repr_str
        assert "2026" in repr_str
        assert "3" in repr_str
        assert "5" in repr_str

    def test_str(self):
        """Test __str__ method"""
        metadata = DocumentMetadata(title="Test Doc", date=date(2026, 3, 5))
        str_result = str(metadata)
        assert "Test Doc" in str_result


class TestDocumentMetadataEdgeCases:
    """Test edge cases and special scenarios"""

    def test_title_with_special_characters(self):
        """Test title with special characters"""
        metadata = DocumentMetadata(title="Test: A Special-Title_123!", date=date(2026, 3, 5))
        assert metadata.title == "Test: A Special-Title_123!"

    def test_title_with_unicode(self):
        """Test title with unicode characters"""
        metadata = DocumentMetadata(title="测试文档 - Test Document", date=date(2026, 3, 5))
        assert metadata.title == "测试文档 - Test Document"

    def test_date_earliest_possible(self):
        """Test with earliest possible date"""
        metadata = DocumentMetadata(title="Test", date=date(1, 1, 1))
        assert metadata.date == date(1, 1, 1)

    def test_date_latest_possible(self):
        """Test with latest possible date"""
        metadata = DocumentMetadata(title="Test", date=date(9999, 12, 31))
        assert metadata.date == date(9999, 12, 31)

    def test_tags_with_special_characters(self):
        """Test tags with special characters"""
        metadata = DocumentMetadata(
            title="Test", date=date(2026, 3, 5), tags=["python-3.10", "test_case", "special!"]
        )
        assert metadata.tags == ["python-3.10", "test_case", "special!"]

    def test_tags_with_unicode(self):
        """Test tags with unicode characters"""
        metadata = DocumentMetadata(title="Test", date=date(2026, 3, 5), tags=["标签1", "标签2"])
        assert metadata.tags == ["标签1", "标签2"]

    def test_many_tags(self):
        """Test with many tags"""
        many_tags = [f"tag{i}" for i in range(100)]
        metadata = DocumentMetadata(title="Test", date=date(2026, 3, 5), tags=many_tags)
        assert metadata.tags == many_tags
        assert len(metadata.tags) == 100


class TestDocumentMetadataImmutable:
    """Test immutability and dataclass features"""

    def test_can_modify_fields(self):
        """Test that fields can be modified (dataclass is mutable by default)"""
        metadata = DocumentMetadata(title="Original", date=date(2026, 3, 5))
        metadata.title = "Modified"
        assert metadata.title == "Modified"

    def test_dataclass_fields_count(self):
        """Test that DocumentMetadata has expected number of fields"""
        all_fields = list(fields(DocumentMetadata))
        assert len(all_fields) == 6

    def test_field_order(self):
        """Test that fields are in expected order"""
        field_names = [f.name for f in fields(DocumentMetadata)]
        assert field_names[0] == "title"
        assert field_names[1] == "date"


class TestDocumentMetadataUsagePatterns:
    """Test common usage patterns"""

    def test_create_from_dict_pattern(self):
        """Test creating DocumentMetadata from dictionary-like data"""
        data = {
            "title": "Research Note",
            "date": date(2026, 3, 5),
            "tags": ["research", "python"],
            "author": "Researcher",
        }
        metadata = DocumentMetadata(**data)
        assert metadata.title == "Research Note"
        assert metadata.tags == ["research", "python"]

    def test_to_dict_pattern(self):
        """Test converting DocumentMetadata to dictionary"""
        metadata = DocumentMetadata(
            title="Test", date=date(2026, 3, 5), tags=["a", "b"], author="Author"
        )

        from dataclasses import asdict

        result = asdict(metadata)

        assert result["title"] == "Test"
        assert result["date"] == date(2026, 3, 5)
        assert result["tags"] == ["a", "b"]
        assert result["author"] == "Author"

    def test_replace_pattern(self):
        """Test using dataclasses.replace to create modified copy"""
        from dataclasses import replace

        original = DocumentMetadata(title="Original", date=date(2026, 3, 5))
        modified = replace(original, title="Modified")

        assert original.title == "Original"
        assert modified.title == "Modified"
        assert original.date == modified.date


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

#!/usr/bin/env python3
"""
Unit tests for note organization tool.

Tests the organize_notes module including:
- Directory scanning
- Organization by date/tag/type
- Move and copy operations
- Dry run functionality
"""

import tempfile
import pytest
from pathlib import Path
from datetime import date

from scripts.tools.organize_notes import (
    DocumentInfo,
    OrganizationResult,
    scan_directory,
    organize_notes,
    list_organization_plan,
    _process_document,
)


class TestDocumentInfo:
    """Test DocumentInfo dataclass"""

    def test_create_basic_document_info(self):
        """Test creating basic document info"""
        doc = DocumentInfo(
            path=Path("/test/doc.md"),
            title="Test Document",
        )
        assert doc.path == Path("/test/doc.md")
        assert doc.title == "Test Document"
        assert doc.date is None
        assert doc.tags == []

    def test_create_full_document_info(self):
        """Test creating document info with all fields"""
        doc = DocumentInfo(
            path=Path("/test/doc.md"),
            title="Test Document",
            date=date(2026, 3, 5),
            tags=["python", "testing"],
            type="research",
            author="Test Author",
        )
        assert doc.date == date(2026, 3, 5)
        assert doc.tags == ["python", "testing"]
        assert doc.type == "research"
        assert doc.author == "Test Author"


class TestOrganizationResult:
    """Test OrganizationResult dataclass"""

    def test_create_default_result(self):
        """Test creating result with defaults"""
        result = OrganizationResult()
        assert result.moved == 0
        assert result.copied == 0
        assert result.skipped == 0
        assert result.errors == []
        assert result.details == {}

    def test_create_result_with_values(self):
        """Test creating result with values"""
        result = OrganizationResult(
            moved=5,
            copied=3,
            skipped=2,
            errors=["error1"],
            details={"src": "dst"},
        )
        assert result.moved == 5
        assert result.copied == 3
        assert result.skipped == 2


class TestScanDirectory:
    """Test directory scanning functionality"""

    def test_scan_empty_directory(self):
        """Test scanning empty directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            docs = scan_directory(tmpdir)
            assert docs == []

    def test_scan_single_markdown_file(self):
        """Test scanning directory with single markdown file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            test_file.write_text("""---
title: Test Document
date: 2026-03-05
tags:
  - python
  - testing
---

Content here.
""")

            docs = scan_directory(tmpdir)

            assert len(docs) == 1
            assert docs[0].title == "Test Document"
            assert docs[0].date == date(2026, 3, 5)
            assert docs[0].tags == ["python", "testing"]

    def test_scan_no_frontmatter(self):
        """Test scanning file without frontmatter"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "no_frontmatter.md"
            test_file.write_text("# Just content\n\nNo frontmatter here.")

            docs = scan_directory(tmpdir)

            assert len(docs) == 1
            assert docs[0].title == "no_frontmatter"

    def test_scan_nonexistent_directory(self):
        """Test scanning nonexistent directory"""
        docs = scan_directory("/nonexistent/path")
        assert docs == []

    def test_scan_recursive(self):
        """Test recursive scanning"""
        with tempfile.TemporaryDirectory() as tmpdir:
            subdir = Path(tmpdir) / "subdir"
            subdir.mkdir()

            (Path(tmpdir) / "root.md").write_text("---\ntitle: Root\n---\nContent")
            (subdir / "nested.md").write_text("---\ntitle: Nested\n---\nContent")

            docs = scan_directory(tmpdir, recursive=True)
            assert len(docs) == 2

    def test_scan_non_recursive(self):
        """Test non-recursive scanning"""
        with tempfile.TemporaryDirectory() as tmpdir:
            subdir = Path(tmpdir) / "subdir"
            subdir.mkdir()

            (Path(tmpdir) / "root.md").write_text("---\ntitle: Root\n---\nContent")
            (subdir / "nested.md").write_text("---\ntitle: Nested\n---\nContent")

            docs = scan_directory(tmpdir, recursive=False)
            assert len(docs) == 1

    def test_scan_with_none_tags(self):
        """Test scanning when tags is explicitly None"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            test_file.write_text("""---
title: Test
tags:
---
Content.
""")

            docs = scan_directory(tmpdir)
            assert len(docs) == 1
            assert docs[0].tags == []


class TestOrganizeNotes:
    """Test note organization functionality"""

    def test_organize_by_date(self):
        """Test organizing by date"""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "source"
            target = Path(tmpdir) / "target"
            source.mkdir()

            # Create test file
            (source / "jan.md").write_text("---\ntitle: January\ndate: 2026-01-15\n---\nContent")
            (source / "mar.md").write_text("---\ntitle: March\ndate: 2026-03-05\n---\nContent")

            result = organize_notes(source, target, by="date", operation="copy")

            assert result.copied == 2
            assert result.skipped == 0
            assert (target / "2026" / "01" / "jan.md").exists()
            assert (target / "2026" / "03" / "mar.md").exists()

    def test_organize_by_tag(self):
        """Test organizing by tag"""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "source"
            target = Path(tmpdir) / "target"
            source.mkdir()

            (source / "python.md").write_text("---\ntitle: Python\ntags: [python]\n---\nContent")
            (source / "no_tags.md").write_text("---\ntitle: No Tags\n---\nContent")

            result = organize_notes(source, target, by="tag", operation="copy")

            assert result.copied == 2
            assert (target / "python" / "python.md").exists()
            assert (target / "untagged" / "no_tags.md").exists()

    def test_organize_by_type(self):
        """Test organizing by type"""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "source"
            target = Path(tmpdir) / "target"
            source.mkdir()

            (source / "research.md").write_text(
                "---\ntitle: Research\ntype: research\n---\nContent"
            )
            (source / "meeting.md").write_text("---\ntitle: Meeting\ntype: meeting\n---\nContent")
            (source / "no_type.md").write_text("---\ntitle: No Type\n---\nContent")

            result = organize_notes(source, target, by="type", operation="copy")

            assert result.copied == 3
            assert (target / "research" / "research.md").exists()
            assert (target / "meeting" / "meeting.md").exists()
            assert (target / "uncategorized" / "no_type.md").exists()

    def test_organize_move_operation(self):
        """Test move operation"""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "source"
            target = Path(tmpdir) / "target"
            source.mkdir()

            (source / "doc.md").write_text("---\ntitle: Doc\ndate: 2026-03-05\n---\nContent")

            result = organize_notes(source, target, by="date", operation="move")

            assert result.moved == 1
            assert not (source / "doc.md").exists()
            assert (target / "2026" / "03" / "doc.md").exists()

    def test_organize_copy_operation(self):
        """Test copy operation"""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "source"
            target = Path(tmpdir) / "target"
            source.mkdir()

            (source / "doc.md").write_text("---\ntitle: Doc\ndate: 2026-03-05\n---\nContent")

            result = organize_notes(source, target, by="date", operation="copy")

            assert result.copied == 1
            assert (source / "doc.md").exists()
            assert (target / "2026" / "03" / "doc.md").exists()

    def test_organize_dry_run(self):
        """Test dry run mode"""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "source"
            target = Path(tmpdir) / "target"
            source.mkdir()

            (source / "doc.md").write_text("---\ntitle: Doc\ndate: 2026-03-05\n---\nContent")

            result = organize_notes(source, target, by="date", operation="move", dry_run=True)

            assert result.moved == 1
            assert (source / "doc.md").exists()
            assert not (target / "2026" / "03" / "doc.md").exists()

    def test_organize_skip_no_date(self):
        """Test skipping documents without date when organizing by date"""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "source"
            target = Path(tmpdir) / "target"
            source.mkdir()

            (source / "with_date.md").write_text(
                "---\ntitle: With Date\ndate: 2026-03-05\n---\nContent"
            )
            (source / "no_date.md").write_text("---\ntitle: No Date\n---\nContent")

            result = organize_notes(source, target, by="date", operation="copy")

            assert result.copied == 1
            assert result.skipped == 1

    def test_organize_duplicate_filenames(self):
        """Test handling duplicate filenames"""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "source"
            target = Path(tmpdir) / "target"
            source.mkdir()

            # Create file in target with same name
            target_date = target / "2026" / "03"
            target_date.mkdir(parents=True)
            (target_date / "doc.md").write_text("Existing content")

            (source / "doc.md").write_text("---\ntitle: Doc\ndate: 2026-03-05\n---\nContent")

            result = organize_notes(source, target, by="date", operation="copy")

            assert result.copied == 1
            assert (target_date / "doc.md").exists()
            assert (target_date / "doc_1.md").exists()

    def test_organize_custom_date_format(self):
        """Test custom date format"""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "source"
            target = Path(tmpdir) / "target"
            source.mkdir()

            (source / "doc.md").write_text("---\ntitle: Doc\ndate: 2026-03-05\n---\nContent")

            result = organize_notes(
                source, target, by="date", operation="copy", date_format="%Y-%m"
            )

            assert result.copied == 1
            assert (target / "2026-03" / "doc.md").exists()

    def test_organize_unknown_criteria(self):
        """Test unknown organization criteria"""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "source"
            target = Path(tmpdir) / "target"
            source.mkdir()

            (source / "doc.md").write_text("---\ntitle: Doc\n---\nContent")

            result = organize_notes(source, target, by="unknown")

            assert len(result.errors) == 1
            assert "unknown" in result.errors[0]

    def test_organize_empty_source(self):
        """Test organizing empty source directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "source"
            target = Path(tmpdir) / "target"
            source.mkdir()

            result = organize_notes(source, target, by="date")

            assert result.moved == 0
            assert result.copied == 0


class TestOrganizeByTagCopy:
    """Test organizing by tag with copy operation"""

    def test_organize_by_tag_copy_to_all_tags(self):
        """Test copying to all tag directories"""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "source"
            target = Path(tmpdir) / "target"
            source.mkdir()

            (source / "doc.md").write_text("---\ntitle: Doc\ntags: [python, testing]\n---\nContent")

            result = organize_notes(source, target, by="tag", operation="copy")

            # Should copy to both tag directories
            assert result.copied == 2
            assert (target / "python" / "doc.md").exists()
            assert (target / "testing" / "doc.md").exists()


class TestListOrganizationPlan:
    """Test list_organization_plan function"""

    def test_list_plan_basic(self):
        """Test listing organization plan"""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "source"
            target = Path(tmpdir) / "target"
            source.mkdir()

            (source / "doc.md").write_text("---\ntitle: Doc\ndate: 2026-03-05\n---\nContent")

            plan = list_organization_plan(source, target, by="date")

            assert len(plan["moves"]) == 1
            assert plan["skipped"] == 0
            assert plan["errors"] == []

    def test_list_plan_with_skip(self):
        """Test listing plan with skipped files"""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "source"
            target = Path(tmpdir) / "target"
            source.mkdir()

            (source / "with_date.md").write_text(
                "---\ntitle: With Date\ndate: 2026-03-05\n---\nContent"
            )
            (source / "no_date.md").write_text("---\ntitle: No Date\n---\nContent")

            plan = list_organization_plan(source, target, by="date")

            assert len(plan["moves"]) == 1
            assert plan["skipped"] == 1


class TestProcessDocument:
    """Test _process_document helper function"""

    def test_process_document_skip_same_path(self):
        """Test skipping when source and destination are the same"""
        with tempfile.TemporaryDirectory() as tmpdir:
            doc = DocumentInfo(
                path=Path(tmpdir) / "doc.md",
                title="Doc",
            )
            result = OrganizationResult()

            _process_document(doc, Path(tmpdir), "move", False, result)

            assert result.skipped == 1
            assert result.moved == 0


class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_scan_file_with_invalid_yaml(self):
        """Test scanning file with invalid YAML"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "invalid.md"
            test_file.write_text("""---
title: [broken yaml
---
Content.
""")

            docs = scan_directory(tmpdir)
            assert len(docs) == 1
            assert docs[0].title == "invalid"

    def test_organize_preserves_content(self):
        """Test that organization preserves file content"""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "source"
            target = Path(tmpdir) / "target"
            source.mkdir()

            original_content = """---
title: Test
date: 2026-03-05
---

# Test Content

Some body text.
"""
            (source / "doc.md").write_text(original_content)

            organize_notes(source, target, by="date", operation="copy")

            target_file = target / "2026" / "03" / "doc.md"
            assert target_file.read_text() == original_content

    def test_organize_tag_move_uses_first_tag(self):
        """Test that move operation uses first tag only"""
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "source"
            target = Path(tmpdir) / "target"
            source.mkdir()

            (source / "doc.md").write_text("---\ntitle: Doc\ntags: [python, testing]\n---\nContent")

            result = organize_notes(source, target, by="tag", operation="move")

            # Should move to first tag only
            assert result.moved == 1
            assert (target / "python" / "doc.md").exists()
            assert not (target / "testing" / "doc.md").exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

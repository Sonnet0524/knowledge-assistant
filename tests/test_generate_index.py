#!/usr/bin/env python3
"""
Unit tests for index generation tool.

Tests the generate_index module including:
- Directory scanning
- Document information extraction
- Index generation with different options
"""

import tempfile
import pytest
from pathlib import Path
from datetime import date

from scripts.tools.generate_index import (
    DocumentInfo,
    scan_directory,
    generate_index,
    _render_document_entry,
    _render_flat_list,
    _render_grouped_by_type,
    _render_grouped_by_date,
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
        assert doc.tags is None

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
            # Create test file
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

    def test_scan_multiple_files(self):
        """Test scanning multiple files"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create multiple test files
            for i in range(3):
                test_file = Path(tmpdir) / f"doc{i}.md"
                test_file.write_text(f"""---
title: Document {i}
date: 2026-03-0{i}
---
Content {i}.
""")

            docs = scan_directory(tmpdir)
            assert len(docs) == 3

    def test_scan_no_frontmatter(self):
        """Test scanning file without frontmatter"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "no_frontmatter.md"
            test_file.write_text("# Just content\n\nNo frontmatter here.")

            docs = scan_directory(tmpdir)

            assert len(docs) == 1
            assert docs[0].title == "no_frontmatter"  # Uses filename

    def test_scan_nonexistent_directory(self):
        """Test scanning nonexistent directory"""
        docs = scan_directory("/nonexistent/path")
        assert docs == []

    def test_scan_recursive(self):
        """Test recursive scanning"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create nested structure
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

    def test_scan_custom_extensions(self):
        """Test scanning with custom extensions"""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "test.md").write_text("---\ntitle: MD\n---\nContent")
            (Path(tmpdir) / "test.txt").write_text("---\ntitle: TXT\n---\nContent")
            (Path(tmpdir) / "test.markdown").write_text("---\ntitle: MARKDOWN\n---\nContent")

            # Default extensions
            docs = scan_directory(tmpdir)
            assert len(docs) == 2  # .md and .markdown

            # Custom extensions
            docs = scan_directory(tmpdir, extensions=[".txt"])
            assert len(docs) == 1

    def test_scan_with_metadata_fields(self):
        """Test scanning extracts all metadata fields"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "full.md"
            test_file.write_text("""---
title: Full Document
date: 2026-03-05
tags:
  - python
type: research
author: Test Author
---
Content.
""")

            docs = scan_directory(tmpdir)
            assert len(docs) == 1
            assert docs[0].type == "research"
            assert docs[0].author == "Test Author"


class TestGenerateIndex:
    """Test index generation functionality"""

    def test_generate_basic_index(self):
        """Test generating basic index"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            for i in range(3):
                test_file = Path(tmpdir) / f"doc{i}.md"
                test_file.write_text(f"""---
title: Document {i}
date: 2026-03-0{i}
---
Content {i}.
""")

            output_path = generate_index(tmpdir, "INDEX.md")

            assert output_path.exists()
            content = output_path.read_text()
            assert "# Document Index" in content
            assert "Total documents: 3" in content

    def test_generate_index_with_custom_title(self):
        """Test generating index with custom title"""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "test.md").write_text("---\ntitle: Test\n---\nContent")

            output_path = generate_index(tmpdir, "INDEX.md", title="My Custom Index")
            content = output_path.read_text()

            assert "# My Custom Index" in content

    def test_generate_index_group_by_type(self):
        """Test grouping by type"""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "research.md").write_text(
                "---\ntitle: Research\ntype: research\n---\nContent"
            )
            (Path(tmpdir) / "meeting.md").write_text(
                "---\ntitle: Meeting\ntype: meeting\n---\nContent"
            )

            output_path = generate_index(tmpdir, "INDEX.md", group_by="type")
            content = output_path.read_text()

            assert "## research" in content.lower()
            assert "## meeting" in content.lower()

    def test_generate_index_group_by_date(self):
        """Test grouping by date"""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "jan.md").write_text(
                "---\ntitle: January\ndate: 2026-01-15\n---\nContent"
            )
            (Path(tmpdir) / "mar.md").write_text(
                "---\ntitle: March\ndate: 2026-03-05\n---\nContent"
            )

            output_path = generate_index(tmpdir, "INDEX.md", group_by="date")
            content = output_path.read_text()

            assert "## 2026-01" in content
            assert "## 2026-03" in content

    def test_generate_index_sort_by_title(self):
        """Test sorting by title"""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "z.md").write_text("---\ntitle: Z Doc\n---\nContent")
            (Path(tmpdir) / "a.md").write_text("---\ntitle: A Doc\n---\nContent")

            output_path = generate_index(tmpdir, "INDEX.md", sort_by="title", sort_desc=False)
            content = output_path.read_text()

            # A should come before Z
            assert content.find("A Doc") < content.find("Z Doc")

    def test_generate_index_sort_by_date(self):
        """Test sorting by date"""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "old.md").write_text("---\ntitle: Old\ndate: 2026-01-01\n---\nContent")
            (Path(tmpdir) / "new.md").write_text("---\ntitle: New\ndate: 2026-12-31\n---\nContent")

            output_path = generate_index(tmpdir, "INDEX.md", sort_by="date", sort_desc=True)
            content = output_path.read_text()

            # New should come before Old (descending)
            assert content.find("New") < content.find("Old")


class TestRenderHelpers:
    """Test render helper functions"""

    def test_render_document_entry_basic(self):
        """Test rendering basic document entry"""
        with tempfile.TemporaryDirectory() as tmpdir:
            notes_dir = Path(tmpdir) / "notes"
            notes_dir.mkdir()
            doc_path = notes_dir / "doc.md"

            doc = DocumentInfo(
                path=doc_path,
                title="Test Document",
            )
            lines: list = []
            _render_document_entry(doc, lines, notes_dir)

            assert len(lines) == 1
            assert "- [Test Document](doc.md)" in lines[0]

    def test_render_document_entry_with_metadata(self):
        """Test rendering document entry with metadata"""
        doc = DocumentInfo(
            path=Path("/test/notes/doc.md"),
            title="Test Document",
            date=date(2026, 3, 5),
            tags=["python", "testing"],
            author="Test Author",
        )
        lines: list = []
        _render_document_entry(doc, lines, Path("/test/notes"))

        assert "2026-03-05" in lines[0]
        assert "python, testing" in lines[0]
        assert "by Test Author" in lines[0]

    def test_render_document_entry_limited_tags(self):
        """Test rendering with many tags (limited to 3)"""
        doc = DocumentInfo(
            path=Path("/test/notes/doc.md"),
            title="Test Document",
            tags=["a", "b", "c", "d", "e"],
        )
        lines: list = []
        _render_document_entry(doc, lines, Path("/test/notes"))

        assert "a, b, c..." in lines[0]
        assert "d" not in lines[0] or "..." in lines[0]

    def test_render_flat_list(self):
        """Test rendering flat list"""
        docs = [
            DocumentInfo(Path("/test/doc1.md"), "Doc 1"),
            DocumentInfo(Path("/test/doc2.md"), "Doc 2"),
        ]
        lines: list = []
        _render_flat_list(docs, lines, Path("/test"))

        assert "## All Documents" in lines

    def test_render_grouped_by_type(self):
        """Test rendering grouped by type"""
        docs = [
            DocumentInfo(Path("/test/r1.md"), "Research 1", type="research"),
            DocumentInfo(Path("/test/r2.md"), "Research 2", type="research"),
            DocumentInfo(Path("/test/m1.md"), "Meeting 1", type="meeting"),
        ]
        lines: list = []
        _render_grouped_by_type(docs, lines, Path("/test"))

        assert "## meeting" in " ".join(lines).lower()
        assert "## research" in " ".join(lines).lower()

    def test_render_grouped_by_date(self):
        """Test rendering grouped by date"""
        docs = [
            DocumentInfo(Path("/test/jan.md"), "Jan", date=date(2026, 1, 15)),
            DocumentInfo(Path("/test/mar.md"), "Mar", date=date(2026, 3, 5)),
        ]
        lines: list = []
        _render_grouped_by_date(docs, lines, Path("/test"))

        assert "## 2026-01" in " ".join(lines)
        assert "## 2026-03" in " ".join(lines)


class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_scan_file_with_invalid_yaml(self):
        """Test scanning file with invalid YAML"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "invalid.md"
            test_file.write_text("""---
title: [broken yaml
date: 2026-03-05
---
Content.
""")

            # Should not raise, creates basic doc info
            docs = scan_directory(tmpdir)
            assert len(docs) == 1
            assert docs[0].title == "invalid"  # Falls back to filename

    def test_scan_file_with_invalid_date(self):
        """Test scanning file with invalid date format"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "bad_date.md"
            test_file.write_text("""---
title: Bad Date
date: not-a-date
---
Content.
""")

            docs = scan_directory(tmpdir)
            assert len(docs) == 1
            assert docs[0].date is None  # Invalid date becomes None

    def test_generate_index_empty_directory(self):
        """Test generating index for empty directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = generate_index(tmpdir, "INDEX.md")
            content = output_path.read_text()

            assert "Total documents: 0" in content

    def test_render_document_entry_nested_path(self):
        """Test rendering with nested path"""
        doc = DocumentInfo(
            path=Path("/test/notes/subdir/nested/doc.md"),
            title="Nested Doc",
        )
        lines: list = []
        _render_document_entry(doc, lines, Path("/test/notes"))

        assert "subdir/nested/doc.md" in lines[0]

    def test_document_without_type(self):
        """Test grouping when document has no type"""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "no_type.md").write_text("---\ntitle: No Type\n---\nContent")

            output_path = generate_index(tmpdir, "INDEX.md", group_by="type")
            content = output_path.read_text()

            assert "Uncategorized" in content

    def test_document_without_date(self):
        """Test grouping when document has no date"""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "no_date.md").write_text("---\ntitle: No Date\n---\nContent")

            output_path = generate_index(tmpdir, "INDEX.md", group_by="date")
            content = output_path.read_text()

            assert "No Date" in content  # Group name or document title


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

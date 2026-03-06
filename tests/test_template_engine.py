#!/usr/bin/env python3
"""
Tests for TemplateEngine module.

This module contains comprehensive tests for the TemplateEngine class.
"""

import pytest
from pathlib import Path
from scripts.template_engine import TemplateEngine


class TestTemplateEngineInit:
    """Tests for TemplateEngine initialization."""

    def test_init_with_valid_directory(self, tmp_path):
        """Test initialization with a valid template directory."""
        # Create a template directory
        template_dir = tmp_path / "templates"
        template_dir.mkdir()

        engine = TemplateEngine(str(template_dir))
        assert engine.template_dir == template_dir
        assert isinstance(engine._cache, dict)
        assert len(engine._cache) == 0

    def test_init_with_nonexistent_directory(self):
        """Test initialization with a non-existent directory raises ValueError."""
        with pytest.raises(ValueError, match="Template directory does not exist"):
            TemplateEngine("/nonexistent/path/templates")

    def test_init_with_file_instead_of_directory(self, tmp_path):
        """Test initialization with a file path raises ValueError."""
        # Create a file instead of directory
        file_path = tmp_path / "not_a_directory.txt"
        file_path.write_text("test")

        with pytest.raises(ValueError, match="Template directory is not a directory"):
            TemplateEngine(str(file_path))


class TestLoadTemplate:
    """Tests for load_template method."""

    @pytest.fixture
    def engine(self, tmp_path):
        """Create a template engine with test templates."""
        template_dir = tmp_path / "templates"
        template_dir.mkdir()

        # Create a test template
        template_content = """---
title: {{title}}
date: {{date}}
---
# {{title}}
Content here.
"""
        (template_dir / "test-template.md").write_text(template_content)

        return TemplateEngine(str(template_dir))

    def test_load_existing_template(self, engine):
        """Test loading an existing template."""
        content = engine.load_template("test-template")
        assert "{{title}}" in content
        assert "{{date}}" in content
        assert "# {{title}}" in content

    def test_load_nonexistent_template(self, engine):
        """Test loading a non-existent template raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError, match="Template not found"):
            engine.load_template("nonexistent-template")

    def test_load_template_with_cache(self, engine):
        """Test that template is cached after first load."""
        # First load
        content1 = engine.load_template("test-template", use_cache=True)
        assert "test-template" in engine._cache

        # Second load should use cache
        content2 = engine.load_template("test-template", use_cache=True)
        assert content1 == content2

    def test_load_template_without_cache(self, engine):
        """Test loading template without caching."""
        # Load without cache
        content1 = engine.load_template("test-template", use_cache=False)
        assert "test-template" not in engine._cache

        # Load again
        content2 = engine.load_template("test-template", use_cache=False)
        assert content1 == content2


class TestRender:
    """Tests for render method."""

    @pytest.fixture
    def engine(self, tmp_path):
        """Create a template engine with test templates."""
        template_dir = tmp_path / "templates"
        template_dir.mkdir()

        # Create a test template
        template_content = """---
title: {{title}}
date: {{date}}
author: {{author}}
---
# {{title}}

Date: {{date}}
Author: {{author}}
"""
        (template_dir / "test-template.md").write_text(template_content)

        return TemplateEngine(str(template_dir))

    def test_render_with_single_variable(self, engine):
        """Test rendering with a single variable."""
        content = engine.render("test-template", title="Test Title")
        assert "Test Title" in content
        assert "{{title}}" not in content
        # Unset variables remain as placeholders
        assert "{{date}}" in content

    def test_render_with_multiple_variables(self, engine):
        """Test rendering with multiple variables."""
        content = engine.render(
            "test-template", title="My Document", date="2026-03-06", author="Test Author"
        )
        assert "My Document" in content
        assert "2026-03-06" in content
        assert "Test Author" in content
        assert "{{" not in content  # No placeholders left

    def test_render_with_numeric_variable(self, engine):
        """Test rendering with numeric values."""
        template_dir = engine.template_dir
        (template_dir / "numeric.md").write_text("Value: {{value}}")

        content = engine.render("numeric", value=42)
        assert "Value: 42" in content

    def test_render_with_none_variable(self, engine):
        """Test rendering with None value."""
        template_dir = engine.template_dir
        (template_dir / "none-test.md").write_text("Value: {{value}}")

        content = engine.render("none-test", value=None)
        assert "Value: None" in content

    def test_render_nonexistent_template(self, engine):
        """Test rendering a non-existent template raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError, match="Template not found"):
            engine.render("nonexistent", title="Test")

    def test_render_with_cache(self, engine):
        """Test rendering uses template cache."""
        # First render
        engine.render("test-template", title="Test 1")
        assert "test-template" in engine._cache

        # Second render should use cache
        content = engine.render("test-template", title="Test 2")
        assert "Test 2" in content


class TestClearCache:
    """Tests for clear_cache method."""

    def test_clear_cache(self, tmp_path):
        """Test clearing the template cache."""
        template_dir = tmp_path / "templates"
        template_dir.mkdir()
        (template_dir / "test.md").write_text("{{title}}")

        engine = TemplateEngine(str(template_dir))

        # Load template to cache it
        engine.load_template("test")
        assert "test" in engine._cache

        # Clear cache
        engine.clear_cache()
        assert len(engine._cache) == 0


class TestListTemplates:
    """Tests for list_templates method."""

    def test_list_templates(self, tmp_path):
        """Test listing all templates in directory."""
        template_dir = tmp_path / "templates"
        template_dir.mkdir()

        # Create multiple templates
        (template_dir / "template1.md").write_text("Template 1")
        (template_dir / "template2.md").write_text("Template 2")
        (template_dir / "template3.md").write_text("Template 3")

        engine = TemplateEngine(str(template_dir))
        templates = engine.list_templates()

        assert len(templates) == 3
        assert "template1" in templates
        assert "template2" in templates
        assert "template3" in templates
        # Should be sorted
        assert templates == sorted(templates)

    def test_list_templates_empty_directory(self, tmp_path):
        """Test listing templates in empty directory."""
        template_dir = tmp_path / "templates"
        template_dir.mkdir()

        engine = TemplateEngine(str(template_dir))
        templates = engine.list_templates()

        assert len(templates) == 0

    def test_list_templates_ignores_non_md_files(self, tmp_path):
        """Test that list_templates only returns .md files."""
        template_dir = tmp_path / "templates"
        template_dir.mkdir()

        # Create .md and non-.md files
        (template_dir / "template.md").write_text("Template")
        (template_dir / "readme.txt").write_text("Readme")
        (template_dir / "data.json").write_text("{}")

        engine = TemplateEngine(str(template_dir))
        templates = engine.list_templates()

        assert len(templates) == 1
        assert "template" in templates


class TestExtractVariables:
    """Tests for extract_variables method."""

    @pytest.fixture
    def engine(self, tmp_path):
        """Create a template engine with test templates."""
        template_dir = tmp_path / "templates"
        template_dir.mkdir()

        # Create a template with multiple variables
        template_content = """---
title: {{title}}
date: {{date}}
tags: {{tags}}
author: {{author}}
---
# {{title}}

Date: {{date}}
Tags: {{tags}}
"""
        (template_dir / "multi-vars.md").write_text(template_content)

        # Create a template with duplicate variables
        template_with_dupes = """# {{title}}
Title again: {{title}}
Date: {{date}}
"""
        (template_dir / "with-dupes.md").write_text(template_with_dupes)

        return TemplateEngine(str(template_dir))

    def test_extract_variables(self, engine):
        """Test extracting variables from template."""
        variables = engine.extract_variables("multi-vars")

        assert len(variables) == 4
        assert "title" in variables
        assert "date" in variables
        assert "tags" in variables
        assert "author" in variables
        # Should be sorted
        assert variables == sorted(variables)

    def test_extract_variables_with_duplicates(self, engine):
        """Test that duplicate variables are removed."""
        variables = engine.extract_variables("with-dupes")

        # Should only have unique variables
        assert len(variables) == 2
        assert variables.count("title") == 1
        assert variables.count("date") == 1

    def test_extract_variables_from_template_without_vars(self, tmp_path):
        """Test extracting variables from template without placeholders."""
        template_dir = tmp_path / "templates"
        template_dir.mkdir()
        (template_dir / "no-vars.md").write_text("No variables here!")

        engine = TemplateEngine(str(template_dir))
        variables = engine.extract_variables("no-vars")

        assert len(variables) == 0


class TestIntegration:
    """Integration tests with actual templates."""

    def test_render_daily_note_template(self):
        """Test rendering the actual daily-note template."""
        # Use the actual templates directory
        templates_dir = Path("./templates")
        if not templates_dir.exists():
            pytest.skip("Templates directory not found")

        engine = TemplateEngine(str(templates_dir))

        # Render daily-note
        content = engine.render(
            "daily-note",
            title="My Daily Note",
            date="2026-03-06",
            tags="work,testing",
            created_at="2026-03-06 10:00",
        )

        assert "My Daily Note" in content
        assert "2026-03-06" in content
        assert "work,testing" in content
        assert "{{title}}" not in content
        assert "{{date}}" not in content

    def test_list_actual_templates(self):
        """Test listing actual templates."""
        templates_dir = Path("./templates")
        if not templates_dir.exists():
            pytest.skip("Templates directory not found")

        engine = TemplateEngine(str(templates_dir))
        templates = engine.list_templates()

        # Should have 5 templates
        assert len(templates) >= 5
        assert "daily-note" in templates
        assert "research-note" in templates
        assert "meeting-minutes" in templates
        assert "task-list" in templates
        assert "knowledge-card" in templates

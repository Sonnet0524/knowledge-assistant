#!/usr/bin/env python3
"""
Template Engine Module.

This module provides a simple template engine for loading and rendering
document templates with variable substitution.

Example:
    >>> from scripts.template_engine import TemplateEngine
    >>> engine = TemplateEngine('./templates')
    >>> content = engine.render('daily-note', title='My Day', date='2026-03-06')
"""

import re
from pathlib import Path
from typing import Dict, Any


class TemplateEngine:
    """
    Template engine for loading and rendering document templates.

    This engine supports loading templates from a directory and rendering
    them with variable substitution using {{variable}} syntax.

    Attributes:
        template_dir (Path): The directory containing template files.
        _cache (Dict[str, str]): Internal cache for loaded templates.

    Example:
        >>> engine = TemplateEngine('./templates')
        >>> template = engine.load_template('daily-note')
        >>> print(template)
        ---
        title: {{title}}
        date: {{date}}
        ...

        >>> content = engine.render('daily-note', title='My Day', date='2026-03-06')
        >>> print(content)
        ---
        title: My Day
        date: 2026-03-06
        ...
    """

    def __init__(self, template_dir: str):
        """
        Initialize the template engine.

        Args:
            template_dir: Path to the directory containing template files.

        Raises:
            ValueError: If template_dir does not exist or is not a directory.

        Example:
            >>> engine = TemplateEngine('./templates')
        """
        self.template_dir = Path(template_dir)
        if not self.template_dir.exists():
            raise ValueError(f"Template directory does not exist: {template_dir}")
        if not self.template_dir.is_dir():
            raise ValueError(f"Template directory is not a directory: {template_dir}")
        self._cache: Dict[str, str] = {}

    def load_template(self, template_name: str, use_cache: bool = True) -> str:
        """
        Load a template file by name.

        Args:
            template_name: The name of the template (without .md extension).
            use_cache: Whether to use cached template if available. Default True.

        Returns:
            The template content as a string.

        Raises:
            FileNotFoundError: If the template file does not exist.

        Example:
            >>> engine = TemplateEngine('./templates')
            >>> content = engine.load_template('daily-note')
            >>> '{{title}}' in content
            True
        """
        # Check cache first
        if use_cache and template_name in self._cache:
            return self._cache[template_name]

        # Load template file
        template_path = self.template_dir / f"{template_name}.md"
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_name}")

        content = template_path.read_text(encoding="utf-8")

        # Cache the template
        if use_cache:
            self._cache[template_name] = content

        return content

    def render(self, template_name: str, use_cache: bool = True, **variables: Any) -> str:
        """
        Render a template with variable substitution.

        Replaces all {{variable}} placeholders with their corresponding values.

        Args:
            template_name: The name of the template (without .md extension).
            use_cache: Whether to use cached template if available. Default True.
            **variables: Variable values to substitute in the template.

        Returns:
            The rendered template content.

        Raises:
            FileNotFoundError: If the template file does not exist.

        Example:
            >>> engine = TemplateEngine('./templates')
            >>> content = engine.render('daily-note', title='My Day', date='2026-03-06')
            >>> 'My Day' in content
            True
            >>> '{{title}}' in content
            False
        """
        # Load template
        content = self.load_template(template_name, use_cache=use_cache)

        # Substitute variables
        for var_name, var_value in variables.items():
            placeholder = "{{" + var_name + "}}"
            content = content.replace(placeholder, str(var_value))

        return content

    def clear_cache(self) -> None:
        """
        Clear the template cache.

        Example:
            >>> engine = TemplateEngine('./templates')
            >>> engine.load_template('daily-note')  # Loads and caches
            >>> engine.clear_cache()  # Clears cache
            >>> 'daily-note' in engine._cache
            False
        """
        self._cache.clear()

    def list_templates(self) -> list[str]:
        """
        List all available template files in the template directory.

        Returns:
            List of template names (without .md extension).

        Example:
            >>> engine = TemplateEngine('./templates')
            >>> templates = engine.list_templates()
            >>> 'daily-note' in templates
            True
        """
        templates = []
        for path in self.template_dir.glob("*.md"):
            if path.is_file():
                templates.append(path.stem)
        return sorted(templates)

    def extract_variables(self, template_name: str, use_cache: bool = True) -> list[str]:
        """
        Extract all variable names from a template.

        Args:
            template_name: The name of the template (without .md extension).
            use_cache: Whether to use cached template if available. Default True.

        Returns:
            List of variable names found in the template.

        Example:
            >>> engine = TemplateEngine('./templates')
            >>> variables = engine.extract_variables('daily-note')
            >>> 'title' in variables
            True
            >>> 'date' in variables
            True
        """
        content = self.load_template(template_name, use_cache=use_cache)
        # Find all {{variable}} patterns
        pattern = r"\{\{(\w+)\}\}"
        variables = re.findall(pattern, content)
        # Return unique variables
        return sorted(list(set(variables)))

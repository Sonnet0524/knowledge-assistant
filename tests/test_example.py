"""Example test to verify test framework setup."""

import pytest
from pathlib import Path


def test_pytest_works():
    """Verify pytest is properly configured."""
    assert True


def test_sample_metadata_fixture(sample_metadata):
    """Test sample_metadata fixture."""
    assert "title" in sample_metadata
    assert sample_metadata["title"] == "Test Document"
    assert "date" in sample_metadata


def test_sample_document_content_fixture(sample_document_content):
    """Test sample_document_content fixture."""
    assert "---" in sample_document_content
    assert "title:" in sample_document_content
    assert "# Test Document" in sample_document_content


def test_tmp_project_dir_fixture(tmp_project_dir):
    """Test tmp_project_dir fixture."""
    assert tmp_project_dir.exists()
    assert (tmp_project_dir / "documents").exists()
    assert (tmp_project_dir / "templates").exists()


def test_test_document_factory(test_document_factory, sample_document_content):
    """Test test_document_factory fixture."""
    doc_path = test_document_factory("test.md", sample_document_content)
    assert doc_path.exists()
    assert doc_path.read_text() == sample_document_content

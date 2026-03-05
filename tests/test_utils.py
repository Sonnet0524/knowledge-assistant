#!/usr/bin/env python3
"""
Unit tests for utility functions.

Tests the utils module including:
- File operations (read_file, write_file, ensure_directory)
- String processing (sanitize_filename, format_date)
- Path utilities (get_project_root, resolve_path)
"""

import os
import tempfile
import pytest
from pathlib import Path
from datetime import date, datetime

from scripts.utils import (
    read_file,
    write_file,
    ensure_directory,
    sanitize_filename,
    format_date,
    get_project_root,
    resolve_path,
)


class TestFileOperations:
    """Test file operation utilities"""

    def test_read_file_success(self):
        """Test reading a file successfully"""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("Test content")
            temp_path = f.name

        try:
            content = read_file(temp_path)
            assert content == "Test content"
        finally:
            os.unlink(temp_path)

    def test_read_file_nonexistent(self):
        """Test reading a non-existent file raises error"""
        with pytest.raises(FileNotFoundError):
            read_file("/nonexistent/path/file.txt")

    def test_read_file_with_encoding(self):
        """Test reading file with specific encoding"""
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".txt", encoding="utf-8"
        ) as f:
            f.write("测试内容")
            temp_path = f.name

        try:
            content = read_file(temp_path, encoding="utf-8")
            assert content == "测试内容"
        finally:
            os.unlink(temp_path)

    def test_write_file_success(self):
        """Test writing to a file successfully"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test.txt")
            write_file(file_path, "Test content")

            assert os.path.exists(file_path)
            with open(file_path, "r") as f:
                assert f.read() == "Test content"

    def test_write_file_creates_directories(self):
        """Test writing creates parent directories if needed"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "subdir", "nested", "test.txt")
            write_file(file_path, "Test content")

            assert os.path.exists(file_path)
            with open(file_path, "r") as f:
                assert f.read() == "Test content"

    def test_write_file_with_encoding(self):
        """Test writing file with specific encoding"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test.txt")
            write_file(file_path, "测试内容", encoding="utf-8")

            with open(file_path, "r", encoding="utf-8") as f:
                assert f.read() == "测试内容"

    def test_ensure_directory_creates_new(self):
        """Test creating a new directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            new_dir = os.path.join(tmpdir, "new_directory")
            ensure_directory(new_dir)

            assert os.path.exists(new_dir)
            assert os.path.isdir(new_dir)

    def test_ensure_directory_nested(self):
        """Test creating nested directories"""
        with tempfile.TemporaryDirectory() as tmpdir:
            nested_dir = os.path.join(tmpdir, "level1", "level2", "level3")
            ensure_directory(nested_dir)

            assert os.path.exists(nested_dir)
            assert os.path.isdir(nested_dir)

    def test_ensure_directory_already_exists(self):
        """Test ensuring directory that already exists"""
        with tempfile.TemporaryDirectory() as tmpdir:
            ensure_directory(tmpdir)

            assert os.path.exists(tmpdir)
            assert os.path.isdir(tmpdir)


class TestStringProcessing:
    """Test string processing utilities"""

    def test_sanitize_filename_basic(self):
        """Test basic filename sanitization"""
        result = sanitize_filename("test_file.txt")
        assert result == "test_file.txt"

    def test_sanitize_filename_removes_special_chars(self):
        """Test removing special characters from filename"""
        result = sanitize_filename('test<>:"/\\|?*file.txt')
        assert all(c not in result for c in '<>:"/\\|?*')

    def test_sanitize_filename_preserves_spaces(self):
        """Test that spaces are preserved by default"""
        result = sanitize_filename("test file name.txt")
        assert result == "test file name.txt"

    def test_sanitize_filename_replaces_spaces(self):
        """Test replacing spaces with underscores"""
        result = sanitize_filename("test file name.txt", replace_spaces=True)
        assert result == "test_file_name.txt"

    def test_sanitize_filename_removes_leading_trailing_spaces(self):
        """Test removing leading and trailing spaces"""
        result = sanitize_filename("  test file.txt  ")
        assert result == "test file.txt"

    def test_sanitize_filename_empty_string(self):
        """Test sanitizing empty string"""
        result = sanitize_filename("")
        assert result == ""

    def test_sanitize_filename_unicode(self):
        """Test sanitizing filename with unicode characters"""
        result = sanitize_filename("测试文件.txt")
        assert result == "测试文件.txt"

    def test_format_date_from_date_object(self):
        """Test formatting date object"""
        test_date = date(2026, 3, 5)
        result = format_date(test_date)
        assert result == "2026-03-05"

    def test_format_date_from_datetime_object(self):
        """Test formatting datetime object"""
        test_datetime = datetime(2026, 3, 5, 14, 30, 0)
        result = format_date(test_datetime)
        assert result == "2026-03-05"

    def test_format_date_custom_format(self):
        """Test formatting with custom format"""
        test_date = date(2026, 3, 5)
        result = format_date(test_date, fmt="%Y/%m/%d")
        assert result == "2026/03/05"

    def test_format_date_iso_format(self):
        """Test formatting in ISO format"""
        test_date = date(2026, 3, 5)
        result = format_date(test_date, fmt="iso")
        assert result == "2026-03-05"

    def test_format_date_string_input(self):
        """Test formatting when input is already a string"""
        result = format_date("2026-03-05")
        assert result == "2026-03-05"


class TestPathUtilities:
    """Test path utility functions"""

    def test_get_project_root_returns_path(self):
        """Test get_project_root returns a Path object"""
        result = get_project_root()
        assert isinstance(result, Path)

    def test_get_project_root_exists(self):
        """Test get_project_root points to existing directory"""
        result = get_project_root()
        assert result.exists()
        assert result.is_dir()

    def test_get_project_root_contains_expected_files(self):
        """Test project root contains expected files"""
        result = get_project_root()
        assert (result / "scripts").exists()
        assert (result / "tests").exists()

    def test_resolve_path_relative(self):
        """Test resolving relative path"""
        root = get_project_root()
        result = resolve_path("scripts/types.py")
        expected = root / "scripts" / "types.py"
        assert result == expected

    def test_resolve_path_absolute(self):
        """Test resolving absolute path"""
        abs_path = "/tmp/test.txt"
        result = resolve_path(abs_path)
        assert result == Path(abs_path)

    def test_resolve_path_with_path_object(self):
        """Test resolving Path object"""
        path_obj = Path("scripts/types.py")
        result = resolve_path(path_obj)
        assert isinstance(result, Path)

    def test_resolve_path_empty_string(self):
        """Test resolving empty string returns project root"""
        result = resolve_path("")
        assert result == get_project_root()


class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_read_file_permission_denied(self):
        """Test reading file with permission denied"""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("content")
            temp_path = f.name

        try:
            os.chmod(temp_path, 0o000)
            with pytest.raises(PermissionError):
                read_file(temp_path)
        finally:
            os.chmod(temp_path, 0o644)
            os.unlink(temp_path)

    def test_write_file_permission_denied(self):
        """Test writing to file with permission denied"""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chmod(tmpdir, 0o444)
            file_path = os.path.join(tmpdir, "test.txt")

            try:
                with pytest.raises(PermissionError):
                    write_file(file_path, "content")
            finally:
                os.chmod(tmpdir, 0o755)

    def test_sanitize_filename_long_name(self):
        """Test sanitizing very long filename"""
        long_name = "a" * 300 + ".txt"
        result = sanitize_filename(long_name, max_length=255)
        assert len(result) <= 255
        assert result.endswith(".txt")

    def test_read_file_large_file(self):
        """Test reading large file"""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            large_content = "x" * 1_000_000
            f.write(large_content)
            temp_path = f.name

        try:
            content = read_file(temp_path)
            assert len(content) == 1_000_000
        finally:
            os.unlink(temp_path)

    def test_write_file_overwrites_existing(self):
        """Test writing overwrites existing file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test.txt")

            write_file(file_path, "Original content")
            write_file(file_path, "New content")

            with open(file_path, "r") as f:
                assert f.read() == "New content"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

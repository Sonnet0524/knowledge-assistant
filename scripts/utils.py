#!/usr/bin/env python3
"""
Utility Functions Module.

This module provides common utility functions for file operations,
string processing, and path handling.

Example:
    >>> from scripts.utils import read_file, write_file, get_project_root
    >>>
    >>> root = get_project_root()
    >>> file_path = root / "notes" / "test.md"
    >>> write_file(file_path, "Test content")
    >>> content = read_file(file_path)
"""

import os
from pathlib import Path
from typing import Union, Optional
from datetime import date, datetime


def get_project_root() -> Path:
    """
    Get the project root directory.

    Returns:
        Path: The project root directory as a Path object.

    Example:
        >>> root = get_project_root()
        >>> root.is_dir()
        True
    """
    current_file = Path(__file__).resolve()
    return current_file.parent.parent


def resolve_path(path: Union[str, Path]) -> Path:
    """
    Resolve a path relative to the project root.

    Args:
        path (Union[str, Path]): The path to resolve. Can be absolute
            or relative to the project root.

    Returns:
        Path: The resolved absolute path.

    Example:
        >>> resolved = resolve_path("scripts/types.py")
        >>> resolved.is_absolute()
        True
    """
    if not path:
        return get_project_root()

    path_obj = Path(path)

    if path_obj.is_absolute():
        return path_obj

    return get_project_root() / path_obj


def ensure_directory(directory: Union[str, Path]) -> Path:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        directory (Union[str, Path]): The directory path to ensure.

    Returns:
        Path: The directory path as a Path object.

    Example:
        >>> ensure_directory("notes/daily")
        >>> # Directory now exists
    """
    dir_path = resolve_path(directory) if not Path(directory).is_absolute() else Path(directory)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def read_file(file_path: Union[str, Path], encoding: str = "utf-8") -> str:
    """
    Read the contents of a file.

    Args:
        file_path (Union[str, Path]): The path to the file to read.
        encoding (str): The file encoding. Defaults to "utf-8".

    Returns:
        str: The file contents as a string.

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If the file cannot be read due to permissions.
        UnicodeDecodeError: If the file cannot be decoded with the
            specified encoding.

    Example:
        >>> content = read_file("notes/test.md")
        >>> print(content)
    """
    path = resolve_path(file_path) if not Path(file_path).is_absolute() else Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with open(path, "r", encoding=encoding) as f:
        return f.read()


def write_file(
    file_path: Union[str, Path],
    content: str,
    encoding: str = "utf-8",
    create_dirs: bool = True,
) -> Path:
    """
    Write content to a file.

    Args:
        file_path (Union[str, Path]): The path to the file to write.
        content (str): The content to write to the file.
        encoding (str): The file encoding. Defaults to "utf-8".
        create_dirs (bool): Whether to create parent directories if
            they don't exist. Defaults to True.

    Returns:
        Path: The file path as a Path object.

    Raises:
        PermissionError: If the file cannot be written due to permissions.
        UnicodeEncodeError: If the content cannot be encoded with the
            specified encoding.

    Example:
        >>> write_file("notes/test.md", "# Test\\nContent here")
    """
    path = resolve_path(file_path) if not Path(file_path).is_absolute() else Path(file_path)

    if create_dirs:
        path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding=encoding) as f:
        f.write(content)

    return path


def sanitize_filename(
    filename: str,
    replace_spaces: bool = False,
    max_length: Optional[int] = None,
) -> str:
    """
    Sanitize a filename by removing or replacing invalid characters.

    Args:
        filename (str): The filename to sanitize.
        replace_spaces (bool): Whether to replace spaces with
            underscores. Defaults to False.
        max_length (Optional[int]): Maximum length for the filename.
            If None, no truncation is applied.

    Returns:
        str: The sanitized filename.

    Example:
        >>> sanitize_filename('test<>:"/\\\\|?*file.txt')
        'test________file.txt'
        >>> sanitize_filename("my document.txt", replace_spaces=True)
        'my_document.txt'
    """
    if not filename:
        return filename

    invalid_chars = '<>:"/\\|?*'
    sanitized = filename

    for char in invalid_chars:
        sanitized = sanitized.replace(char, "_")

    if replace_spaces:
        sanitized = sanitized.replace(" ", "_")

    sanitized = sanitized.strip()

    if max_length and len(sanitized) > max_length:
        name, ext = os.path.splitext(sanitized)
        name_max = max_length - len(ext)
        if name_max > 0:
            sanitized = name[:name_max] + ext
        else:
            sanitized = sanitized[:max_length]

    return sanitized


def format_date(
    date_value: Union[date, datetime, str],
    fmt: str = "%Y-%m-%d",
) -> str:
    """
    Format a date value to a string.

    Args:
        date_value (Union[date, datetime, str]): The date value to format.
            Can be a date object, datetime object, or ISO format string.
        fmt (str): The format string. Use "iso" for ISO format
            (YYYY-MM-DD). Defaults to "%Y-%m-%d".

    Returns:
        str: The formatted date string.

    Example:
        >>> from datetime import date
        >>> format_date(date(2026, 3, 5))
        '2026-03-05'
        >>> format_date(date(2026, 3, 5), fmt="%Y/%m/%d")
        '2026/03/05'
    """
    if isinstance(date_value, str):
        return date_value

    if fmt == "iso":
        fmt = "%Y-%m-%d"

    return date_value.strftime(fmt)

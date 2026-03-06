#!/usr/bin/env python3
"""
Note Organization Tool.

This module provides functionality to organize notes by date, tags,
or other criteria, moving or copying them to target directories.

Example:
    >>> from scripts.tools.organize_notes import organize_notes
    >>>
    >>> # Organize notes by date
    >>> result = organize_notes("notes/", "organized/", by="date")
    >>> print(f"Organized {result.moved} notes")
"""

import shutil
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional, Union

from scripts.metadata_parser import MetadataParser
from scripts.utils import ensure_directory, get_project_root


@dataclass
class DocumentInfo:
    """
    Information about a scanned document.

    Attributes:
        path (Path): The path to the document file.
        title (str): The document title from metadata.
        date (Optional[date]): The document date from metadata.
        tags (List[str]): List of tags from metadata.
        type (Optional[str]): The document type from metadata.
        author (Optional[str]): The document author from metadata.
    """

    path: Path
    title: str
    date: Optional[date] = None
    tags: List[str] = field(default_factory=list)
    type: Optional[str] = None
    author: Optional[str] = None


@dataclass
class OrganizationResult:
    """
    Result of note organization operation.

    Attributes:
        moved (int): Number of notes moved.
        copied (int): Number of notes copied.
        skipped (int): Number of notes skipped.
        errors (List[str]): List of error messages.
        details (Dict[str, str]): Mapping of source to destination paths.
    """

    moved: int = 0
    copied: int = 0
    skipped: int = 0
    errors: List[str] = field(default_factory=list)
    details: Dict[str, str] = field(default_factory=dict)


def scan_directory(
    directory: Union[str, Path],
    recursive: bool = True,
    extensions: Optional[List[str]] = None,
) -> List[DocumentInfo]:
    """
    Scan a directory for markdown documents.

    Args:
        directory (Union[str, Path]): The directory to scan.
        recursive (bool): Whether to scan subdirectories. Defaults to True.
        extensions (Optional[List[str]]): File extensions to include.
            Defaults to [".md", ".markdown"].

    Returns:
        List[DocumentInfo]: List of document information objects.
    """
    if extensions is None:
        extensions = [".md", ".markdown"]

    dir_path = Path(directory)
    if not dir_path.is_absolute():
        dir_path = get_project_root() / dir_path

    if not dir_path.exists():
        return []

    documents: List[DocumentInfo] = []
    parser = MetadataParser()

    # Collect files
    files: List[Path] = []
    if recursive:
        for ext in extensions:
            files.extend(dir_path.rglob(f"*{ext}"))
    else:
        for ext in extensions:
            files.extend(dir_path.glob(f"*{ext}"))

    for file_path in files:
        if not file_path.is_file():
            continue

        try:
            content = file_path.read_text(encoding="utf-8")
            metadata, _ = parser.parse(content)

            # Extract title - use metadata or filename
            title = metadata.get("title", file_path.stem)

            # Extract date
            doc_date = None
            if "date" in metadata:
                date_value = metadata["date"]
                if isinstance(date_value, date):
                    doc_date = date_value
                elif isinstance(date_value, str):
                    try:
                        doc_date = date.fromisoformat(date_value)
                    except ValueError:
                        pass

            # Extract other fields
            tags = metadata.get("tags", [])
            if tags is None:
                tags = []
            doc_type = metadata.get("type")
            author = metadata.get("author")

            doc_info = DocumentInfo(
                path=file_path,
                title=title,
                date=doc_date,
                tags=tags if isinstance(tags, list) else [],
                type=doc_type,
                author=author,
            )
            documents.append(doc_info)

        except Exception:
            # If parsing fails, create a basic document info
            doc_info = DocumentInfo(
                path=file_path,
                title=file_path.stem,
            )
            documents.append(doc_info)

    return documents


def organize_notes(
    source_dir: Union[str, Path],
    target_dir: Union[str, Path],
    by: str = "date",
    operation: str = "move",
    date_format: str = "%Y/%m",
    dry_run: bool = False,
) -> OrganizationResult:
    """
    Organize notes from source directory to target directory.

    Args:
        source_dir (Union[str, Path]): Source directory containing notes.
        target_dir (Union[str, Path]): Target directory for organized notes.
        by (str): Organization criteria. Options: "date", "tag", "type".
            Defaults to "date".
        operation (str): Operation type. Options: "move", "copy".
            Defaults to "move".
        date_format (str): Date format for directory structure.
            Defaults to "%Y/%m" (year/month).
        dry_run (bool): If True, simulate without making changes.
            Defaults to False.

    Returns:
        OrganizationResult: Result of the organization operation.

    Example:
        >>> result = organize_notes(
        ...     "notes/",
        ...     "organized/",
        ...     by="date",
        ...     operation="copy"
        ... )
        >>> print(f"Organized {result.copied} notes")
    """
    # Resolve paths
    source_path = Path(source_dir)
    if not source_path.is_absolute():
        source_path = get_project_root() / source_path

    target_path = Path(target_dir)
    if not target_path.is_absolute():
        target_path = get_project_root() / target_path

    # Initialize result
    result = OrganizationResult()

    # Scan source directory
    documents = scan_directory(source_path)

    if not documents:
        return result

    # Create target directory
    if not dry_run:
        ensure_directory(target_path)

    # Organize based on criteria
    if by == "date":
        _organize_by_date(documents, target_path, operation, date_format, dry_run, result)
    elif by == "tag":
        _organize_by_tag(documents, target_path, operation, dry_run, result)
    elif by == "type":
        _organize_by_type(documents, target_path, operation, dry_run, result)
    else:
        result.errors.append(f"Unknown organization criteria: {by}")

    return result


def _organize_by_date(
    documents: List[DocumentInfo],
    target_path: Path,
    operation: str,
    date_format: str,
    dry_run: bool,
    result: OrganizationResult,
) -> None:
    """Organize documents by date."""
    for doc in documents:
        if doc.date is None:
            result.skipped += 1
            continue

        # Create date-based directory
        date_dir = doc.date.strftime(date_format)
        dest_dir = target_path / date_dir

        # Perform operation
        _process_document(doc, dest_dir, operation, dry_run, result)


def _organize_by_tag(
    documents: List[DocumentInfo],
    target_path: Path,
    operation: str,
    dry_run: bool,
    result: OrganizationResult,
) -> None:
    """Organize documents by tags."""
    for doc in documents:
        if not doc.tags:
            # Move to "untagged" directory
            dest_dir = target_path / "untagged"
            _process_document(doc, dest_dir, operation, dry_run, result)
            continue

        # Create a copy for each tag (for copy operation)
        # Or move to first tag directory (for move operation)
        if operation == "move":
            # Move to first tag directory
            dest_dir = target_path / doc.tags[0]
            _process_document(doc, dest_dir, operation, dry_run, result)
        else:
            # Copy to all tag directories
            for tag in doc.tags:
                dest_dir = target_path / tag
                _process_document(doc, dest_dir, "copy", dry_run, result)


def _organize_by_type(
    documents: List[DocumentInfo],
    target_path: Path,
    operation: str,
    dry_run: bool,
    result: OrganizationResult,
) -> None:
    """Organize documents by type."""
    for doc in documents:
        # Use type or "uncategorized"
        doc_type = doc.type or "uncategorized"
        dest_dir = target_path / doc_type
        _process_document(doc, dest_dir, operation, dry_run, result)


def _process_document(
    doc: DocumentInfo,
    dest_dir: Path,
    operation: str,
    dry_run: bool,
    result: OrganizationResult,
) -> None:
    """Process a single document (move or copy)."""
    try:
        # Create destination directory
        if not dry_run:
            ensure_directory(dest_dir)

        # Determine destination path
        dest_path = dest_dir / doc.path.name

        # Handle duplicate filenames
        if dest_path.exists() and dest_path != doc.path:
            counter = 1
            stem = doc.path.stem
            suffix = doc.path.suffix
            while dest_path.exists():
                dest_path = dest_dir / f"{stem}_{counter}{suffix}"
                counter += 1

        # Skip if source and destination are the same
        if dest_path == doc.path:
            result.skipped += 1
            return

        # Perform operation
        if dry_run:
            # Just record what would happen
            result.details[str(doc.path)] = str(dest_path)
            if operation == "move":
                result.moved += 1
            else:
                result.copied += 1
        else:
            if operation == "move":
                shutil.move(str(doc.path), str(dest_path))
                result.moved += 1
            else:
                shutil.copy2(str(doc.path), str(dest_path))
                result.copied += 1

            result.details[str(doc.path)] = str(dest_path)

    except Exception as e:
        result.errors.append(f"Error processing {doc.path}: {e}")


def list_organization_plan(
    source_dir: Union[str, Path],
    target_dir: Union[str, Path],
    by: str = "date",
    date_format: str = "%Y/%m",
) -> Dict[str, Union[List[tuple], int, List[str]]]:
    """
    List the organization plan without making changes.

    This is a convenience function that runs organize_notes with dry_run=True
    and returns a summary.

    Args:
        source_dir (Union[str, Path]): Source directory containing notes.
        target_dir (Union[str, Path]): Target directory for organized notes.
        by (str): Organization criteria. Options: "date", "tag", "type".
        date_format (str): Date format for directory structure.

    Returns:
        Dict with 'moves', 'skipped', and 'errors' keys.

    Example:
        >>> plan = list_organization_plan("notes/", "organized/", by="date")
        >>> for src, dst in plan['moves']:
        ...     print(f"{src} -> {dst}")
    """
    result = organize_notes(
        source_dir, target_dir, by=by, operation="move", date_format=date_format, dry_run=True
    )

    return {
        "moves": list(result.details.items()),
        "skipped": result.skipped,
        "errors": result.errors,
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python -m scripts.tools.organize_notes <source> <target> [date|tag|type]")
        sys.exit(1)

    source = sys.argv[1]
    target = sys.argv[2]
    by = sys.argv[3] if len(sys.argv) > 3 else "date"

    result = organize_notes(source, target, by=by)
    print(f"Moved: {result.moved}, Copied: {result.copied}, Skipped: {result.skipped}")
    if result.errors:
        print(f"Errors: {len(result.errors)}")
        for error in result.errors:
            print(f"  - {error}")

#!/usr/bin/env python3
"""
Index Generation Tool.

This module provides functionality to scan directories for documents
and generate Markdown index files.

Example:
    >>> from scripts.tools.generate_index import generate_index
    >>>
    >>> # Generate an index for a directory
    >>> index_path = generate_index("notes/", "INDEX.md")
    >>> print(f"Index created at: {index_path}")
"""

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional, Union

from scripts.metadata_parser import MetadataParser
from scripts.utils import get_project_root, write_file


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
    tags: Optional[List[str]] = None
    type: Optional[str] = None
    author: Optional[str] = None


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

    Example:
        >>> docs = scan_directory("notes/")
        >>> for doc in docs:
        ...     print(f"{doc.title}: {doc.path}")
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
    if recursive:
        files = []
        for ext in extensions:
            files.extend(dir_path.rglob(f"*{ext}"))
    else:
        files = []
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
            doc_type = metadata.get("type")
            author = metadata.get("author")

            doc_info = DocumentInfo(
                path=file_path,
                title=title,
                date=doc_date,
                tags=tags if tags else None,
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


def generate_index(
    directory: Union[str, Path],
    output_file: Union[str, Path] = "INDEX.md",
    title: str = "Document Index",
    group_by: str = "none",
    sort_by: str = "date",
    sort_desc: bool = True,
) -> Path:
    """
    Generate a Markdown index file for a directory.

    Args:
        directory (Union[str, Path]): The directory to scan.
        output_file (Union[str, Path]): The output index file path.
            Defaults to "INDEX.md".
        title (str): The title for the index. Defaults to "Document Index".
        group_by (str): How to group documents. Options: "none", "type", "date".
            Defaults to "none".
        sort_by (str): How to sort documents. Options: "date", "title", "path".
            Defaults to "date".
        sort_desc (bool): Sort in descending order. Defaults to True.

    Returns:
        Path: The path to the generated index file.

    Example:
        >>> index_path = generate_index(
        ...     "notes/",
        ...     "INDEX.md",
        ...     title="My Notes",
        ...     group_by="type",
        ...     sort_by="date"
        ... )
    """
    # Scan directory
    documents = scan_directory(directory)

    # Sort documents
    def sort_key(doc: DocumentInfo) -> tuple:
        if sort_by == "date":
            return (doc.date is None, doc.date or date.min)
        elif sort_by == "title":
            return (doc.title.lower(),)
        else:  # path
            return (str(doc.path),)

    documents.sort(key=sort_key, reverse=sort_desc)

    # Generate markdown content
    lines: List[str] = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"*Generated from {directory}*")
    lines.append("")
    lines.append(f"**Total documents: {len(documents)}**")
    lines.append("")

    if group_by == "none":
        _render_flat_list(documents, lines, directory)
    elif group_by == "type":
        _render_grouped_by_type(documents, lines, directory)
    elif group_by == "date":
        _render_grouped_by_date(documents, lines, directory)

    # Write index file
    content = "\n".join(lines)
    dir_path = Path(directory)
    if not dir_path.is_absolute():
        dir_path = get_project_root() / dir_path

    output_path = dir_path / output_file
    write_file(output_path, content)

    return output_path


def _render_flat_list(
    documents: List[DocumentInfo], lines: List[str], base_dir: Union[str, Path]
) -> None:
    """Render documents as a flat list."""
    lines.append("## All Documents")
    lines.append("")

    for doc in documents:
        _render_document_entry(doc, lines, base_dir)


def _render_grouped_by_type(
    documents: List[DocumentInfo], lines: List[str], base_dir: Union[str, Path]
) -> None:
    """Render documents grouped by type."""
    groups: Dict[str, List[DocumentInfo]] = {}

    for doc in documents:
        doc_type = doc.type or "Uncategorized"
        if doc_type not in groups:
            groups[doc_type] = []
        groups[doc_type].append(doc)

    for doc_type, docs in sorted(groups.items()):
        lines.append(f"## {doc_type}")
        lines.append("")
        for doc in docs:
            _render_document_entry(doc, lines, base_dir)
        lines.append("")


def _render_grouped_by_date(
    documents: List[DocumentInfo], lines: List[str], base_dir: Union[str, Path]
) -> None:
    """Render documents grouped by date (year-month)."""
    groups: Dict[str, List[DocumentInfo]] = {}

    for doc in documents:
        if doc.date:
            key = doc.date.strftime("%Y-%m")
        else:
            key = "No Date"
        if key not in groups:
            groups[key] = []
        groups[key].append(doc)

    for date_key, docs in sorted(groups.items(), reverse=True):
        lines.append(f"## {date_key}")
        lines.append("")
        for doc in docs:
            _render_document_entry(doc, lines, base_dir)
        lines.append("")


def _render_document_entry(doc: DocumentInfo, lines: List[str], base_dir: Union[str, Path]) -> None:
    """Render a single document entry."""
    base_path = Path(base_dir)
    if not base_path.is_absolute():
        base_path = get_project_root() / base_path

    # Calculate relative path
    try:
        rel_path = doc.path.relative_to(base_path)
    except ValueError:
        rel_path = doc.path

    # Build entry line
    entry = f"- [{doc.title}]({rel_path.as_posix()})"

    # Add metadata info
    meta_parts = []
    if doc.date:
        meta_parts.append(doc.date.strftime("%Y-%m-%d"))
    if doc.tags:
        tags_str = ", ".join(doc.tags[:3])  # Limit to 3 tags
        if len(doc.tags) > 3:
            tags_str += "..."
        meta_parts.append(f"tags: {tags_str}")
    if doc.author:
        meta_parts.append(f"by {doc.author}")

    if meta_parts:
        entry += f" _({', '.join(meta_parts)})_"

    lines.append(entry)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m scripts.tools.generate_index <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    output_path = generate_index(directory)
    print(f"Index generated: {output_path}")

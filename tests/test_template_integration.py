"""
Integration tests for document processing pipeline.

This module tests the integration between different components:
- Metadata parser
- Template system (when ready)
- Document processing workflow
"""

import pytest
from pathlib import Path
from datetime import date


@pytest.mark.integration
class TestMetadataParserIntegration:
    """Integration tests for MetadataParser with real documents."""

    def test_parse_valid_document_from_file(self, metadata_parser, tmp_project_dir):
        """Test parsing a valid document from file system."""
        doc_path = tmp_project_dir / "test.md"
        doc_path.write_text("""---
title: Integration Test Document
date: 2026-03-05
type: integration
tags:
  - test
  - integration
---

# Integration Test

This is an integration test document.
""")

        content = doc_path.read_text()
        metadata, body = metadata_parser.parse(content)
        is_valid, errors = metadata_parser.validate(metadata)

        assert is_valid
        assert metadata["title"] == "Integration Test Document"
        assert "Integration Test" in body

    @pytest.mark.integration
    def test_parse_multi_language_documents(self, metadata_parser, multi_language_document):
        """Test parsing documents with multiple languages."""
        metadata, body = metadata_parser.parse(multi_language_document)
        is_valid, errors = metadata_parser.validate(metadata)

        assert is_valid
        assert "多语言" in metadata["title"]
        assert "日本語" in body
        assert "한국어" in body

    @pytest.mark.integration
    def test_parse_performance_document(self, metadata_parser, performance_test_document):
        """Test parsing large performance test document."""
        import time

        start_time = time.time()
        metadata, body = metadata_parser.parse(performance_test_document)
        parse_time = time.time() - start_time

        is_valid, errors = metadata_parser.validate(metadata)

        assert is_valid
        assert parse_time < 1.0  # Should parse in less than 1 second
        assert len(body) > 1000  # Body should be substantial

    @pytest.mark.integration
    def test_parse_edge_case_document(self, metadata_parser, edge_case_document):
        """Test parsing document with edge cases."""
        metadata, body = metadata_parser.parse(edge_case_document)
        is_valid, errors = metadata_parser.validate(metadata)

        assert is_valid
        assert "Special Characters" in metadata["title"]
        assert "你好世界" in body
        assert "🎉" in body


@pytest.mark.integration
class TestDocumentProcessingWorkflow:
    """Integration tests for complete document processing workflows."""

    def test_workflow_parse_validate_process(self, metadata_parser, tmp_project_dir):
        """Test complete workflow: parse -> validate -> process."""
        # Create test document
        doc_path = tmp_project_dir / "workflow_test.md"
        doc_path.write_text("""---
title: Workflow Test
date: 2026-03-05
type: workflow
tags:
  - workflow
  - test
author: Test Agent
---

# Workflow Test Document

## Section 1
Content for section 1.

## Section 2
Content for section 2.
""")

        # Step 1: Parse
        content = doc_path.read_text()
        metadata, body = metadata_parser.parse(content)

        # Step 2: Validate
        is_valid, errors = metadata_parser.validate(metadata)
        assert is_valid

        # Step 3: Process - convert to DocumentMetadata
        from scripts.types import DocumentMetadata

        date_value = metadata["date"]
        if isinstance(date_value, str):
            date_obj = date.fromisoformat(date_value)
        else:
            date_obj = date_value

        doc_metadata = DocumentMetadata(
            title=metadata["title"],
            date=date_obj,
            tags=metadata.get("tags"),
            author=metadata.get("author"),
            type=metadata.get("type"),
        )

        # Verify final result
        assert doc_metadata.title == "Workflow Test"
        assert doc_metadata.date == date(2026, 3, 5)
        assert "workflow" in doc_metadata.tags

    @pytest.mark.integration
    def test_workflow_batch_processing(self, metadata_parser, integration_test_data):
        """Test batch processing of multiple documents."""
        results = {"total": 0, "valid": 0, "invalid": 0, "errors": []}

        for doc_name, doc_path in integration_test_data.items():
            results["total"] += 1

            content = doc_path.read_text()
            try:
                metadata, body = metadata_parser.parse(content)
                is_valid, errors = metadata_parser.validate(metadata)

                if is_valid:
                    results["valid"] += 1
                else:
                    results["invalid"] += 1
                    results["errors"].append({"document": doc_name, "errors": errors})
            except Exception as e:
                # Handle YAML parsing errors
                results["invalid"] += 1
                results["errors"].append({"document": doc_name, "errors": [str(e)]})

        # Verify results
        assert results["total"] == 5
        assert results["valid"] == 3  # valid, multi_language, performance
        assert results["invalid"] == 2  # invalid_yaml, missing_fields

    @pytest.mark.integration
    @pytest.mark.slow
    def test_workflow_stress_test(self, metadata_parser, tmp_project_dir, document_factory):
        """Test workflow under stress with many documents."""
        num_documents = 50

        # Create many documents
        for i in range(num_documents):
            doc_content = document_factory(
                title=f"Stress Test Document {i}",
                date_str="2026-03-05",
                doc_type="stress-test",
                tags=[f"tag-{i}", "stress"],
                body=f"Content for stress test document {i}.",
            )
            doc_path = tmp_project_dir / f"stress_{i}.md"
            doc_path.write_text(doc_content)

        # Process all documents
        successful = 0
        failed = 0

        for i in range(num_documents):
            doc_path = tmp_project_dir / f"stress_{i}.md"
            content = doc_path.read_text()
            metadata, body = metadata_parser.parse(content)
            is_valid, errors = metadata_parser.validate(metadata)

            if is_valid:
                successful += 1
            else:
                failed += 1

        assert successful == num_documents
        assert failed == 0


@pytest.mark.integration
class TestCrossLanguageSupport:
    """Integration tests for multi-language document support."""

    @pytest.mark.integration
    def test_chinese_document_processing(self, metadata_parser):
        """Test processing Chinese documents."""
        chinese_doc = """---
title: 中文测试文档
date: 2026-03-05
type: test
tags:
  - 中文
  - 测试
---

# 中文内容

这是一个中文测试文档。

## 章节

更多中文内容。
"""
        metadata, body = metadata_parser.parse(chinese_doc)
        is_valid, errors = metadata_parser.validate(metadata)

        assert is_valid
        assert "中文" in metadata["title"]
        assert "中文内容" in body

    @pytest.mark.integration
    def test_japanese_document_processing(self, metadata_parser):
        """Test processing Japanese documents."""
        japanese_doc = """---
title: 日本語テストドキュメント
date: 2026-03-05
type: test
tags:
  - 日本語
  - テスト
---

# 日本語コンテンツ

これは日本語テストドキュメントです。

## セクション

さらに日本語コンテンツ。
"""
        metadata, body = metadata_parser.parse(japanese_doc)
        is_valid, errors = metadata_parser.validate(metadata)

        assert is_valid
        assert "日本語" in metadata["title"]
        assert "日本語コンテンツ" in body

    @pytest.mark.integration
    def test_korean_document_processing(self, metadata_parser):
        """Test processing Korean documents."""
        korean_doc = """---
title: 한국어 테스트 문서
date: 2026-03-05
type: test
tags:
  - 한국어
  - 테스트
---

# 한국어 콘텐츠

이것은 한국어 테스트 문서입니다.

## 섹션

더 많은 한국어 콘텐츠.
"""
        metadata, body = metadata_parser.parse(korean_doc)
        is_valid, errors = metadata_parser.validate(metadata)

        assert is_valid
        assert "한국어" in metadata["title"]
        assert "한국어 콘텐츠" in body

    @pytest.mark.integration
    def test_mixed_language_document(self, metadata_parser):
        """Test document with mixed languages."""
        mixed_doc = """---
title: Mixed Language Document 多言語ドキュメント 다국어 문서
date: 2026-03-05
type: multilingual
tags:
  - english
  - 中文
  - 日本語
  - 한국어
---

# Mixed Language Content

This document contains multiple languages.

## 中文部分
这是中文内容。

## 日本語セクション
これは日本語のコンテンツです。

## 한국어 섹션
이것은 한국어 콘텐츠입니다.
"""
        metadata, body = metadata_parser.parse(mixed_doc)
        is_valid, errors = metadata_parser.validate(metadata)

        assert is_valid
        assert "Mixed Language" in metadata["title"]
        assert "中文部分" in body
        assert "日本語セクション" in body
        assert "한국어 섹션" in body


@pytest.mark.integration
class TestErrorRecovery:
    """Integration tests for error recovery and resilience."""

    @pytest.mark.integration
    def test_recover_from_invalid_yaml(self, metadata_parser, integration_test_data):
        """Test recovery when encountering invalid YAML."""
        # Try to parse invalid YAML document
        invalid_doc = integration_test_data["invalid_yaml"]
        content = invalid_doc.read_text()

        with pytest.raises(Exception):  # Should raise YAML error
            metadata, body = metadata_parser.parse(content)

    @pytest.mark.integration
    def test_handle_missing_fields_gracefully(self, metadata_parser, integration_test_data):
        """Test graceful handling of missing required fields."""
        missing_fields_doc = integration_test_data["missing_fields"]
        content = missing_fields_doc.read_text()

        metadata, body = metadata_parser.parse(content)
        is_valid, errors = metadata_parser.validate(metadata)

        assert not is_valid
        assert len(errors) > 0
        assert any("date" in error.lower() for error in errors)

    @pytest.mark.integration
    def test_empty_document_handling(self, metadata_parser):
        """Test handling of empty documents."""
        empty_doc = ""
        metadata, body = metadata_parser.parse(empty_doc)

        assert metadata == {}
        assert body == ""

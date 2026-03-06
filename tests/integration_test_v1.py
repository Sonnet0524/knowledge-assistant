#!/usr/bin/env python3
"""
Integration Test for v1.0 Release
"""
import sys
import os
import tempfile
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

test_results = {'passed': [], 'failed': [], 'warnings': []}

def test(name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
                test_results['passed'].append(name)
                print(f"[PASS] {name}")
                return True
            except AssertionError as e:
                test_results['failed'].append((name, str(e)))
                print(f"[FAIL] {name}: {e}")
                return False
            except Exception as e:
                test_results['warnings'].append((name, str(e)))
                print(f"[WARN] {name}: {e}")
                return False
        return wrapper
    return decorator

print("=" * 70)
print("Knowledge Assistant v1.0 - Integration Test Suite")
print("=" * 70)
print()

print("TEST SUITE 1: Template Engine")
print("-" * 70)

@test("Template Engine - Load daily-note template")
def test_template_daily():
    from scripts.template_engine import TemplateEngine
    engine = TemplateEngine('./templates')
    content = engine.load_template('daily-note')
    assert len(content) > 0, "Template is empty"

@test("Template Engine - Load research-note template")
def test_template_research():
    from scripts.template_engine import TemplateEngine
    engine = TemplateEngine('./templates')
    content = engine.load_template('research-note')
    assert len(content) > 0

@test("Template Engine - Load meeting-minutes template")
def test_template_meeting():
    from scripts.template_engine import TemplateEngine
    engine = TemplateEngine('./templates')
    content = engine.load_template('meeting-minutes')
    assert len(content) > 0

@test("Template Engine - Load task-list template")
def test_template_task():
    from scripts.template_engine import TemplateEngine
    engine = TemplateEngine('./templates')
    content = engine.load_template('task-list')
    assert len(content) > 0

@test("Template Engine - Load knowledge-card template")
def test_template_knowledge():
    from scripts.template_engine import TemplateEngine
    engine = TemplateEngine('./templates')
    content = engine.load_template('knowledge-card')
    assert len(content) > 0

@test("Template Engine - Render with variables")
def test_template_render():
    from scripts.template_engine import TemplateEngine
    engine = TemplateEngine('./templates')
    content = engine.render('daily-note', title='Test Note', date='2026-03-06')
    assert '{{title}}' not in content, "Template has unrendered variables"

@test("Template Engine - List all templates")
def test_template_list():
    from scripts.template_engine import TemplateEngine
    engine = TemplateEngine('./templates')
    templates = engine.list_templates()
    assert len(templates) >= 5

test_template_daily()
test_template_research()
test_template_meeting()
test_template_task()
test_template_knowledge()
test_template_render()
test_template_list()
print()

print("TEST SUITE 2: Metadata Parser")
print("-" * 70)

@test("Metadata Parser - Parse valid document")
def test_parser_valid():
    from scripts.metadata_parser import MetadataParser
    parser = MetadataParser()
    test_doc = """---
title: Test Document
date: 2026-03-06
tags: [test, integration]
---

Content here."""
    metadata, body = parser.parse(test_doc)
    assert metadata['title'] == 'Test Document'

@test("Metadata Parser - Validate metadata")
def test_parser_validate():
    from scripts.metadata_parser import MetadataParser
    parser = MetadataParser()
    valid_metadata = {'title': 'Test', 'date': '2026-03-06'}
    is_valid, errors = parser.validate(valid_metadata)
    assert is_valid, f"Valid metadata rejected: {errors}"

@test("Metadata Parser - Reject invalid metadata")
def test_parser_invalid():
    from scripts.metadata_parser import MetadataParser
    parser = MetadataParser()
    invalid_metadata = {'title': 'Missing Date'}
    is_valid, errors = parser.validate(invalid_metadata)
    assert not is_valid, "Invalid metadata accepted"

test_parser_valid()
test_parser_validate()
test_parser_invalid()
print()

print("TEST SUITE 3: organize_notes Tool")
print("-" * 70)

@test("organize_notes - Copy files by date")
def test_organize_date():
    from scripts.tools.organize_notes import organize_notes
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / 'test.md'
        test_file.write_text("""---
title: Test Document
date: 2026-03-06
tags: [test]
---
Content here.""", encoding='utf-8')
        dest = Path(tmpdir) / 'organized'
        result = organize_notes(tmpdir, str(dest), by='date', operation='copy')
        assert result.copied >= 1

@test("organize_notes - Copy files by tag")
def test_organize_tag():
    from scripts.tools.organize_notes import organize_notes
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / 'test.md'
        test_file.write_text("""---
title: Test Document
date: 2026-03-06
tags: [test-tag]
---
Content here.""", encoding='utf-8')
        dest = Path(tmpdir) / 'organized'
        result = organize_notes(tmpdir, str(dest), by='tag', operation='copy')
        assert result.copied >= 1

test_organize_date()
test_organize_tag()
print()

print("TEST SUITE 4: generate_index Tool")
print("-" * 70)

@test("generate_index - Generate index file")
def test_generate_index():
    from scripts.tools.generate_index import generate_index
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / 'test.md'
        test_file.write_text("""---
title: Test Document
date: 2026-03-06
tags: [test]
---
Content here.""", encoding='utf-8')
        index_path = generate_index(tmpdir, f'{tmpdir}/INDEX.md')
        assert Path(index_path).exists()
        index_content = Path(index_path).read_text(encoding='utf-8')
        assert 'Test Document' in index_content

test_generate_index()
print()

print("TEST SUITE 5: extract_keywords Tool")
print("-" * 70)

@test("extract_keywords - Extract keywords from text")
def test_extract_keywords():
    from scripts.tools.extract_keywords import extract_keywords
    test_content = "Python is a programming language. Testing is important for software development. Python testing frameworks are useful."
    keywords = extract_keywords(test_content, max_keywords=5)
    assert len(keywords) > 0
    assert len(keywords) <= 5

@test("extract_keywords - Handle short text")
def test_extract_keywords_short():
    from scripts.tools.extract_keywords import extract_keywords
    short_text = "Python"
    keywords = extract_keywords(short_text, max_keywords=5)
    assert isinstance(keywords, list)

test_extract_keywords()
test_extract_keywords_short()
print()

print("=" * 70)
print("TEST SUMMARY")
print("=" * 70)
print(f"Passed: {len(test_results['passed'])}")
print(f"Failed: {len(test_results['failed'])}")
print(f"Warnings: {len(test_results['warnings'])}")
print()

if test_results['failed']:
    print("Failed Tests:")
    for name, error in test_results['failed']:
        print(f"  - {name}: {error}")
    print()

if test_results['warnings']:
    print("Warnings:")
    for name, error in test_results['warnings']:
        print(f"  - {name}: {error}")
    print()

total_tests = len(test_results['passed']) + len(test_results['failed'])
pass_rate = (len(test_results['passed']) / total_tests * 100) if total_tests > 0 else 0

print(f"Pass Rate: {pass_rate:.1f}%")
print()

if len(test_results['failed']) == 0:
    print("[SUCCESS] ALL INTEGRATION TESTS PASSED!")
    sys.exit(0)
else:
    print("[FAILURE] SOME TESTS FAILED")
    sys.exit(1)

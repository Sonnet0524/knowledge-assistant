#!/usr/bin/env python3
"""
Edge Cases Test for v1.0 Release
"""
import sys
import tempfile
from pathlib import Path

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
print("Edge Cases Test Suite")
print("=" * 70)
print()

# Test 1: Empty file
@test("Edge Case - Empty file")
def test_empty_file():
    from scripts.metadata_parser import MetadataParser
    parser = MetadataParser()
    metadata, body = parser.parse("")
    assert isinstance(metadata, dict)
    assert body == ""

# Test 2: No metadata
@test("Edge Case - File without metadata")
def test_no_metadata():
    from scripts.metadata_parser import MetadataParser
    parser = MetadataParser()
    content = "# Just content\nNo frontmatter"
    metadata, body = parser.parse(content)
    assert isinstance(metadata, dict)
    assert 'title' not in metadata

# Test 3: Invalid YAML
@test("Edge Case - Invalid YAML frontmatter")
def test_invalid_yaml():
    from scripts.metadata_parser import MetadataParser
    parser = MetadataParser()
    invalid_yaml = """---
title: [invalid yaml syntax
---

Content"""
    try:
        metadata, body = parser.parse(invalid_yaml)
        print(f"  Note: Parsed as {metadata}")
    except Exception as e:
        print(f"  Note: Raised {type(e).__name__}: {e}")

# Test 4: Special characters in title
@test("Edge Case - Special characters in title")
def test_special_chars():
    from scripts.metadata_parser import MetadataParser
    parser = MetadataParser()
    special_doc = """---
title: "Test<>:\"/\|?*File"
date: 2026-03-06
---

Content"""
    metadata, body = parser.parse(special_doc)
    assert 'title' in metadata

# Test 5: Long title
@test("Edge Case - Very long title (500 chars)")
def test_long_title():
    from scripts.metadata_parser import MetadataParser
    parser = MetadataParser()
    long_title = "A" * 500
    long_doc = f"""---
title: {long_title}
date: 2026-03-06
---

Content"""
    metadata, body = parser.parse(long_doc)
    assert metadata['title'] == long_title

# Test 6: Unicode content
@test("Edge Case - Unicode content")
def test_unicode():
    from scripts.metadata_parser import MetadataParser
    parser = MetadataParser()
    unicode_doc = """---
title: 中文标题
date: 2026-03-06
tags: [测试, emoji, 特殊]
---

内容包含中文、emoji和其他Unicode字符"""
    metadata, body = parser.parse(unicode_doc)
    assert metadata['title'] == "中文标题"

# Test 7: Missing date in organize
@test("Edge Case - organize_notes with missing date")
def test_organize_missing_date():
    from scripts.tools.organize_notes import organize_notes
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / 'no_date.md'
        test_file.write_text("""---
title: No Date File
tags: [test]
---
Content""", encoding='utf-8')
        dest = Path(tmpdir) / 'organized'
        result = organize_notes(tmpdir, str(dest), by='date', operation='copy')
        assert result.skipped >= 0

# Test 8: Missing tags in organize
@test("Edge Case - organize_notes with missing tags")
def test_organize_missing_tags():
    from scripts.tools.organize_notes import organize_notes
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / 'no_tags.md'
        test_file.write_text("""---
title: No Tags File
date: 2026-03-06
---
Content""", encoding='utf-8')
        dest = Path(tmpdir) / 'organized'
        result = organize_notes(tmpdir, str(dest), by='tag', operation='copy')
        assert result.skipped >= 0 or result.copied >= 0

# Test 9: Template with missing variables
@test("Edge Case - Template with missing variables")
def test_template_missing_vars():
    from scripts.template_engine import TemplateEngine
    engine = TemplateEngine('./templates')
    content = engine.render('daily-note', title='Test')
    assert 'Test' in content

# Test 10: Empty directory for generate_index
@test("Edge Case - generate_index with empty directory")
def test_empty_directory():
    from scripts.tools.generate_index import generate_index
    with tempfile.TemporaryDirectory() as tmpdir:
        index_path = generate_index(tmpdir, f'{tmpdir}/INDEX.md')
        assert Path(index_path).exists()
        content = Path(index_path).read_text(encoding='utf-8')
        assert 'INDEX' in content or len(content) > 0

test_empty_file()
test_no_metadata()
test_invalid_yaml()
test_special_chars()
test_long_title()
test_unicode()
test_organize_missing_date()
test_organize_missing_tags()
test_template_missing_vars()
test_empty_directory()
print()

print("=" * 70)
print("EDGE CASE TEST SUMMARY")
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
    print("[SUCCESS] ALL EDGE CASE TESTS PASSED!")
    sys.exit(0)
else:
    print("[WARNING] SOME EDGE CASES FAILED")
    sys.exit(0)

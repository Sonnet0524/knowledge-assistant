# Knowledge Assistant - Product Requirements Document (PRD)

**Product**: Knowledge Assistant  
**Version**: v1.1  
**Last Updated**: 2026-03-06  
**Owner**: PM Team  

---

## Table of Contents

1. [Product Overview](#product-overview)
2. [Vision & Goals](#vision--goals)
3. [Target Users](#target-users)
4. [Architecture](#architecture)
5. [Core Capabilities](#core-capabilities)
6. [Feature Requirements](#feature-requirements)
7. [Technical Requirements](#technical-requirements)
8. [Development Roadmap](#development-roadmap)
9. [Success Metrics](#success-metrics)
10. [Risks & Mitigation](#risks--mitigation)

---

## Product Overview

### What is Knowledge Assistant?

Knowledge Assistant is a **personal knowledge management tool** that helps users organize, search, and manage their knowledge efficiently through an intelligent agent interface.

### Product Positioning

**"Professional Knowledge Management Tool Library for opencode"**

**Architecture**:
- **opencode**: Master agent with file operations, NLU, and interaction capabilities
- **knowledge-assistant**: Specialized tool library providing algorithms and connectors
- **Relationship**: opencode calls knowledge-assistant tools; knowledge-assistant returns structured data

**Core Value**:
- Semantic search and vector indexing algorithms
- Knowledge extraction algorithms (keywords, summary, entities)
- Multi-source integration connectors (email, database, web)
- **No duplication** of opencode's file operation and NLU capabilities

**Target**: Personal users who use opencode for knowledge management

### Development Phases

```
Phase 1 (v1.x): Tool Library for opencode ← Current Focus
  ├── Knowledge retrieval tools (semantic search)
  ├── Knowledge extraction tools (keywords, summary)
  ├── Multi-source connectors (email, etc.)
  ├── Skills and Agent integration
  └── opencode as master controller

Phase 2 (v2.0): Independent Application (Future)
  ├── Based on einai framework
  ├── Standalone software
  └── Enhanced features
```

---

## Vision & Goals

### Vision Statement

Make personal knowledge management **intelligent, organized, and accessible** through natural language interaction.

### Goals for v1.1

1. **Complete Core Capabilities**
   - Knowledge retrieval (search & query)
   - Knowledge extraction (keywords & summary)
   - Knowledge organization (enhanced tools)

2. **Enable Agent Integration**
   - Design knowledge-assistant agent
   - Map user intents to tool capabilities
   - Provide seamless interaction experience

3. **Improve User Experience**
   - Clear documentation
   - Practical examples
   - Reliable performance

### Non-Goals for v1.1

- ❌ GUI application (v2.0)
- ❌ Knowledge graph visualization
- ❌ Multi-user collaboration
- ❌ Cloud sync

---

## Target Users

### Primary User Persona

**Profile**: Knowledge Worker
- Software developers, researchers, writers
- Manage knowledge through markdown documents
- Use CLI tools and AI assistants (opencode)
- Value efficiency and automation

### User Needs

| Need | Current Solution | Pain Point | Our Solution |
|------|-----------------|------------|--------------|
| Document creation | Manual editing | Inconsistent structure | Templates + auto-metadata |
| Knowledge retrieval | grep/find commands | Limited search | Semantic search |
| Knowledge organization | Manual folder management | Time-consuming | Auto-organization |
| Knowledge extraction | Manual reading | Time-consuming | Auto-keywords & summary |

---

## Architecture

### System Architecture

```
┌──────────────────────────────────────────┐
│  User Interface Layer                    │
│  └── Natural language interaction        │
└──────────────────────────────────────────┘
                ↓
┌──────────────────────────────────────────┐
│  opencode (Master Agent)                 │
│  ├── File operations (scan, read, write) │
│  ├── Natural language understanding     │
│  ├── Intent analysis & planning          │
│  ├── Tool orchestration                  │
│  └── Result display & interaction        │
└──────────────────────────────────────────┘
                ↓ calls tools
┌──────────────────────────────────────────┐
│  knowledge-assistant (Tool Library)      │
│  ├── Indexing Tools                      │
│  │   └── build_semantic_index()         │
│  │   └── update_index()                 │
│  │                                       │
│  ├── Search Tools                        │
│  │   └── semantic_search()              │
│  │   └── hybrid_search()                │
│  │                                       │
│  ├── Extraction Tools                    │
│  │   └── extract_keywords()             │
│  │   └── generate_summary()             │
│  │                                       │
│  └── Connector Tools                     │
│      └── EmailConnector                  │
│      └── DatabaseConnector (future)      │
└──────────────────────────────────────────┘
                ↓ returns data
┌──────────────────────────────────────────┐
│  opencode displays & interacts           │
│  └── Structured results presentation     │
│  └── User interaction handling           │
└──────────────────────────────────────────┘
                ↓
┌──────────────────────────────────────────┐
│  Data Sources                            │
│  ├── Local filesystem (opencode handles) │
│  ├── Email servers (via connectors)      │
│  └── Databases (future)                  │
└──────────────────────────────────────────┘
```

**Key Principles**:
1. **No Duplication**: knowledge-assistant does NOT implement file scanning, reading, or display
2. **Input/Output**: knowledge-assistant receives data from opencode, returns structured results
3. **Tool Focus**: knowledge-assistant focuses on algorithms and data processing

### Capability Maturity Model

```
Level 1: Foundation (v1.0 ✅)
  ├── Document structuring (metadata + template)
  ├── Document organization (organize_notes)
  └── Document indexing (generate_index)

Level 2: Core Capabilities (v1.1 ⭐)
  ├── Knowledge retrieval ⭐
  ├── Knowledge extraction ⭐
  └── Knowledge association

Level 3: Enhancement (v1.2+)
  ├── Intelligent writing assistance
  ├── Knowledge analysis
  └── Advanced automation

Level 4: Advanced (v2.0)
  ├── Knowledge graph
  ├── Multi-dimensional analysis
  └── Independent application
```

---

## Core Capabilities

### 1. Document Management

**Status**: ✅ Completed (v1.0)

**Components**:
- Metadata System (YAML frontmatter)
- Template Engine (5 templates)
- Configuration Management

**Features**:
- Create documents from templates
- Parse and validate metadata
- Configure preferences

### 2. Knowledge Retrieval (NEW in v1.1)

**Status**: 🚧 Planned

**Components**:
- Full-text search
- Metadata search
- Combined queries

**Features**:
- Search by keywords
- Filter by tags, date, type
- Sort by relevance or date

**User Story**:
```
As a user, I want to search "Python asyncio"
So that I can quickly find related documents
```

### 3. Knowledge Extraction (NEW in v1.1)

**Status**: 🚧 Planned

**Components**:
- Keyword extraction
- Summary generation
- Entity recognition

**Features**:
- Extract top-N keywords
- Generate document summary
- Identify key entities

**User Story**:
```
As a user, I want to extract keywords automatically
So that I can understand document topics quickly
```

### 4. Knowledge Organization

**Status**: ✅ Completed (v1.0)

**Components**:
- organize_notes tool
- generate_index tool

**Enhancements** (v1.1):
- Batch operations
- Custom organization rules
- Conflict resolution

### 5. Knowledge Association (NEW in v1.1)

**Status**: 🚧 Planned

**Components**:
- Similar document finder
- Tag-based association
- Reference links

**Features**:
- Find similar documents
- Group by shared tags
- Track document references

---

## Feature Requirements

### Priority Matrix

| Feature | Priority | Effort | Impact | Sprint |
|---------|----------|--------|--------|--------|
| search_notes | **P0** | Medium | High | Sprint 1 |
| extract_keywords | **P0** | Medium | High | Sprint 1 |
| generate_summary | **P1** | Medium | Medium | Sprint 2 |
| find_similar | **P1** | High | Medium | Sprint 2 |
| Agent integration | **P0** | High | High | Sprint 1-3 |
| Performance optimization | P2 | Medium | Medium | Sprint 3 |
| Windows compatibility | P2 | Low | Low | Sprint 3 |

### Detailed Requirements

#### FR-1: Knowledge Search (search_notes)

**Description**: Search documents by content and metadata

**Functional Requirements**:
- FR-1.1: Support full-text search in document content
- FR-1.2: Support metadata search (title, tags, date, author, type)
- FR-1.3: Support combined queries with multiple filters
- FR-1.4: Support relevance ranking
- FR-1.5: Support pagination (limit & offset)

**Non-Functional Requirements**:
- NFR-1.1: Search response time < 1s for 1000 docs
- NFR-1.2: Memory usage < 100MB for 10,000 docs
- NFR-1.3: Support Chinese and English content

**API Design**:
```python
def search_notes(
    query: str,
    directory: str,
    search_in: List[str] = ['title', 'content', 'tags'],
    filters: Optional[Dict] = None,
    sort_by: str = 'relevance',
    limit: int = 50
) -> SearchResult:
    """
    Search documents.
    
    Args:
        query: Search query string
        directory: Directory to search
        search_in: Fields to search in
        filters: Additional filters (tags, date_range, author, type)
        sort_by: Sorting method (relevance, date, title)
        limit: Maximum results
    
    Returns:
        SearchResult with matched documents
    """
```

#### FR-2: Keyword Extraction (extract_keywords)

**Description**: Extract keywords from document content

**Functional Requirements**:
- FR-2.1: Support TF-IDF method
- FR-2.2: Support TextRank method
- FR-2.3: Support configurable top-N keywords
- FR-2.4: Support multi-language (Chinese, English)
- FR-2.5: Support stop words filtering

**Non-Functional Requirements**:
- NFR-2.1: Extraction time < 0.5s per document
- NFR-2.2: Accuracy > 80% (manual evaluation)

**API Design**:
```python
def extract_keywords(
    content: str,
    method: str = 'tfidf',
    top_n: int = 10,
    language: str = 'en'
) -> List[Tuple[str, float]]:
    """
    Extract keywords from content.
    
    Args:
        content: Document content
        method: Extraction method (tfidf, textrank)
        top_n: Number of keywords to return
        language: Content language (en, zh)
    
    Returns:
        List of (keyword, score) tuples
    """
```

#### FR-3: Summary Generation (generate_summary)

**Description**: Generate document summary

**Functional Requirements**:
- FR-3.1: Support extractive summarization
- FR-3.2: Support configurable length
- FR-3.3: Support multi-sentence summary
- FR-3.4: Preserve key information

**API Design**:
```python
def generate_summary(
    content: str,
    max_length: int = 200,
    method: str = 'extractive'
) -> str:
    """
    Generate document summary.
    
    Args:
        content: Document content
        max_length: Maximum summary length
        method: Summarization method
    
    Returns:
        Summary string
    """
```

#### FR-4: Similar Documents (find_similar)

**Description**: Find similar documents based on content

**Functional Requirements**:
- FR-4.1: Support cosine similarity
- FR-4.2: Support Jaccard similarity
- FR-4.3: Support configurable threshold
- FR-4.4: Support TF-IDF vectorization

**API Design**:
```python
def find_similar(
    doc_path: str,
    directory: str,
    threshold: float = 0.5,
    method: str = 'cosine',
    limit: int = 10
) -> List[SimilarDoc]:
    """
    Find similar documents.
    
    Args:
        doc_path: Reference document
        directory: Search directory
        threshold: Similarity threshold
        method: Similarity method
        limit: Maximum results
    
    Returns:
        List of similar documents with scores
    """
```

#### FR-5: Agent Integration

**Description**: Integrate with knowledge-assistant agent

**Functional Requirements**:
- FR-5.1: Define agent capabilities mapping
- FR-5.2: Create intent recognition rules
- FR-5.3: Design conversational flow
- FR-5.4: Provide usage examples

**Agent Configuration**:
```yaml
# Agent definition
name: knowledge-assistant
description: Personal Knowledge Management Assistant

capabilities:
  document_management:
    - create_document
    - read_document
    - update_metadata
  
  knowledge_search:
    - search_by_keyword
    - search_by_tags
    - search_by_date
  
  knowledge_extraction:
    - extract_keywords
    - generate_summary
  
  knowledge_organization:
    - organize_notes
    - generate_index
  
  knowledge_association:
    - find_similar
    - find_by_tags

intent_mapping:
  - patterns:
      - "find documents about {topic}"
      - "search for {query}"
    action: search_documents
    tool: search_notes
  
  - patterns:
      - "what are the keywords of {document}"
      - "extract keywords from {document}"
    action: extract_keywords
    tool: extract_keywords
  
  - patterns:
      - "organize my notes"
      - "sort my documents"
    action: organize_documents
    tool: organize_notes
```

---

## Technical Requirements

### Technology Stack

**Language**: Python 3.8+

**Core Dependencies**:
- `pyyaml` - YAML parsing
- `jinja2` - Template engine
- `jieba` - Chinese text segmentation
- `scikit-learn` - TF-IDF, similarity
- `numpy` - Numerical operations

**New Dependencies** (v1.1):
- `whoosh` or `lunr` - Full-text search
- `sumy` - Extractive summarization
- `networkx` - TextRank algorithm

### Performance Requirements

| Metric | Target | Measurement |
|--------|--------|-------------|
| Search time (1000 docs) | < 1s | P95 latency |
| Keyword extraction | < 0.5s/doc | Average time |
| Memory usage | < 100MB | Peak memory |
| Test coverage | > 85% | Code coverage |

### Quality Requirements

- **Reliability**: No data loss during operations
- **Compatibility**: Windows, macOS, Linux
- **Maintainability**: Modular architecture, clear interfaces
- **Extensibility**: Plugin support for future features

---

## Development Roadmap

### Sprint 1 (Week 1-2): Core Search & Extraction

**Goal**: Implement search and keyword extraction

**Deliverables**:
- [ ] search_notes.py implementation
- [ ] extract_keywords.py implementation
- [ ] Unit tests (>85% coverage)
- [ ] API documentation

**Team**:
- Data Team: Implement tools
- Test Team: Write tests
- PM Team: Documentation

### Sprint 2 (Week 3-4): Enhanced Features

**Goal**: Add summary generation and similarity

**Deliverables**:
- [ ] generate_summary.py implementation
- [ ] find_similar.py implementation
- [ ] Integration tests
- [ ] Usage examples

**Team**:
- Data Team: Implement tools
- Test Team: Integration tests
- PM Team: Examples & guides

### Sprint 3 (Week 5-6): Agent Integration & Polish

**Goal**: Integrate with agent and finalize

**Deliverables**:
- [ ] Agent capability mapping
- [ ] Agent intent recognition
- [ ] Performance optimization
- [ ] Windows compatibility fixes
- [ ] Complete documentation
- [ ] v1.1 release

**Team**:
- All Teams: Integration & testing
- PM Team: Release management

### Milestones

```
M7: Search & Extraction   [Week 2]  ⭐ v1.1 core
M8: Summary & Similarity  [Week 4]  ⭐ v1.1 enhancement
M9: Agent Integration     [Week 5]  ⭐ v1.1 integration
M10: v1.1 Release        [Week 6]  ⭐ v1.1 release
```

---

## Success Metrics

### Feature Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Search accuracy | > 85% | User satisfaction |
| Keyword precision | > 80% | Manual evaluation |
| Summary relevance | > 75% | Manual evaluation |
| Similar document accuracy | > 70% | Manual evaluation |

### Usage Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Agent interaction success | > 90% | Success rate |
| Task completion rate | > 85% | User feedback |
| Documentation clarity | > 4.0/5.0 | User rating |

### Quality Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Test coverage | > 85% | 96% (v1.0) |
| Test pass rate | > 95% | 98.7% (v1.0) |
| Code quality | 100% | 100% (v1.0) |

---

## Risks & Mitigation

### Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Search performance degradation | High | Medium | Implement indexing, pagination |
| Multi-language support complexity | Medium | High | Start with English, add Chinese incrementally |
| Similarity algorithm accuracy | Medium | Medium | Test multiple algorithms, choose best |

### Product Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Agent intent recognition failure | High | Medium | Clear intent mapping, fallback options |
| User adoption difficulty | Medium | Low | Comprehensive documentation, examples |
| Feature scope creep | Medium | Medium | Strict prioritization, phased delivery |

---

## Appendix

### A. User Stories

**US-1**: Knowledge Search
```
As a researcher,
I want to search all my documents by keywords,
So that I can quickly find relevant research notes.
```

**US-2**: Keyword Extraction
```
As a writer,
I want keywords automatically extracted from my articles,
So that I can tag them consistently without manual effort.
```

**US-3**: Document Organization
```
As a knowledge worker,
I want my notes organized by date automatically,
So that my knowledge base stays organized.
```

**US-4**: Agent Interaction
```
As an opencode user,
I want to use natural language to manage my knowledge,
So that I don't need to remember CLI commands.
```

### B. API Endpoints (Future)

```python
# REST API (v2.0)
POST /api/search
POST /api/extract
POST /api/organize
POST /api/similar
```

### C. Configuration Schema

```yaml
# config.yaml additions for v1.1
search:
  index_dir: .index
  enable_cache: true
  cache_size: 1000
  
extraction:
  keyword_method: tfidf
  keyword_count: 10
  summary_length: 200
  
similarity:
  threshold: 0.5
  method: cosine
  max_results: 10
```

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-06 | PM Team | Initial PRD for v1.1 |

---

**Status**: Draft  
**Next Review**: Team discussion  
**Approval**: Pending

---
name: knowledge-assistant
description: Personal knowledge management with semantic search and multi-source integration
version: 1.1.0
triggers:
  - "search knowledge"
  - "find documents"
  - "build knowledge base"
  - "extract keywords"
  - "search emails"
---

# Knowledge Assistant Skill

## Overview

This skill enables opencode to act as a personal knowledge management assistant with semantic search, knowledge extraction, and multi-source integration capabilities.

## Capabilities

### 1. Knowledge Base Management
- Build semantic index from documents
- Update index incrementally
- Query index statistics

### 2. Semantic Search
- Natural language search
- Hybrid search (semantic + keyword)
- Multi-criteria filtering

### 3. Knowledge Extraction
- Keyword extraction
- Summary generation
- Entity recognition

### 4. Multi-Source Integration
- Email integration
- Database integration (future)
- Web sources (future)

## Usage Patterns

### Pattern 1: Build Knowledge Base

**User Intent**: Build a knowledge base from a directory

**Trigger Phrases**:
- "build knowledge base from [directory]"
- "create index for my notes"
- "index all my documents"

**Execution Flow**:
```
1. Scan directory recursively (opencode's file operations)
2. Read all markdown files (opencode's file reading)
3. Extract metadata from frontmatter (opencode's parsing)
4. Call build_semantic_index(documents) → knowledge-assistant
5. Display results to user (opencode's display)
```

**Example Interaction**:
```
User: "Build knowledge base from D:/MyKnowledge"

opencode:
  [Scans D:/MyKnowledge]
  Found 156 markdown files
  
  [Calls knowledge-assistant.build_semantic_index]
  Building semantic index...
  
  ✅ Knowledge base built successfully!
  - Documents: 156
  - Chunks: 489
  - Index size: 23.5 MB
  - Build time: 12.3s
  
  Index saved to: .ka-index/
```

### Pattern 2: Semantic Search

**User Intent**: Search for documents using natural language

**Trigger Phrases**:
- "find documents about [topic]"
- "search for [query] in my notes"
- "where is my [topic] note"
- "show me documents related to [topic]"

**Execution Flow**:
```
1. Understand user query (opencode's NLU)
2. Extract search intent and filters (opencode's analysis)
3. Call semantic_search(query, filters) → knowledge-assistant
4. Read returned document paths (opencode's file reading)
5. Display results with snippets (opencode's display)
```

**Example Interaction**:
```
User: "Find my notes about Python async programming"

opencode:
  [Understands intent: search for Python async programming]
  
  [Calls knowledge-assistant.semantic_search]
  Searching...
  
  Found 3 relevant documents:
  
  📄 Python Asyncio Guide (similarity: 0.89)
     Path: D:/MyKnowledge/python/asyncio-guide.md
     Date: 2026-02-28
     
     Snippet:
     "Python asyncio provides a framework for writing 
     concurrent code using async/await syntax..."
  
  📄 Async Programming Patterns (similarity: 0.85)
     Path: D:/MyKnowledge/notes/async-patterns.md
     Date: 2026-02-15
  
  Would you like to read any of these documents?
```

### Pattern 3: Knowledge Extraction

**User Intent**: Extract knowledge from documents

**Trigger Phrases**:
- "extract keywords from [document]"
- "summarize [document]"
- "what are the main topics in [document]"

**Execution Flow**:
```
1. Read document content (opencode's file reading)
2. Call extract_keywords(content) → knowledge-assistant
3. Call generate_summary(content) → knowledge-assistant (optional)
4. Display results (opencode's display)
```

**Example Interaction**:
```
User: "Extract keywords from python-guide.md"

opencode:
  [Reads D:/MyKnowledge/python-guide.md]
  
  [Calls knowledge-assistant.extract_keywords]
  
  Keywords extracted:
  1. asyncio (score: 0.95)
  2. coroutine (score: 0.89)
  3. async/await (score: 0.85)
  4. event loop (score: 0.82)
  5. concurrency (score: 0.78)
```

### Pattern 4: Multi-Source Search

**User Intent**: Search across multiple data sources

**Trigger Phrases**:
- "search my emails for [topic]"
- "find [topic] in documents and emails"
- "check if I have [topic] in my mailbox"

**Execution Flow**:
```
1. Understand multi-source intent (opencode's NLU)
2. Connect to email if needed (knowledge-assistant connector)
3. Search emails (knowledge-assistant.search_emails)
4. Search knowledge base (knowledge-assistant.semantic_search)
5. Merge and rank results (opencode's analysis)
6. Display unified results (opencode's display)
```

**Example Interaction**:
```
User: "Search my emails for project budget"

opencode:
  [Understands intent: search emails for project budget]
  
  [Checks email configuration]
  Email not configured. Would you like to configure?
  
  User: Yes, server is imap.gmail.com, user@gmail.com
  
  opencode:
  [Calls knowledge-assistant.connect_email]
  Testing connection... Connected!
  
  [Calls knowledge-assistant.search_emails]
  Searching emails...
  
  Found 3 relevant emails:
  
  📧 Project Budget Approval (2026-03-01)
     From: manager@company.com
     Subject: Re: Q1 Project Budget
     
  📧 Budget Adjustment Notice (2026-02-20)
     From: finance@company.com
     Subject: Project Budget Adjustment
  
  Would you like to read any email content?
```

## Tool Functions

### build_semantic_index

**Purpose**: Build semantic index from documents

**Input**: 
```python
{
    "documents": [
        {
            "path": "string",
            "content": "string",
            "metadata": {
                "title": "string",
                "date": "string",
                "tags": ["string"],
                ...
            }
        }
    ],
    "index_path": "string (default: .ka-index)",
    "embedding_model": "string (default: sentence-transformers/...)",
    "chunk_size": "int (default: 512)",
    "overlap": "int (default: 50)"
}
```

**Output**:
```python
{
    "success": "bool",
    "total_docs": "int",
    "total_chunks": "int",
    "index_size": "string",
    "embedding_dim": "int",
    "build_time": "string"
}
```

**Calling Convention**:
```python
from scripts.tools.indexing import build_semantic_index

result = build_semantic_index(
    documents=[...],  # opencode provides document data
    index_path=".ka-index"
)

print(f"Indexed {result['total_docs']} documents")
```

### semantic_search

**Purpose**: Semantic search in knowledge base

**Input**:
```python
{
    "query": "string",
    "index_path": "string (default: .ka-index)",
    "top_k": "int (default: 10)",
    "threshold": "float (default: 0.5)",
    "filters": {
        "date_range": {"start": "string", "end": "string"},
        "tags": ["string"],
        "authors": ["string"],
        "types": ["string"]
    }
}
```

**Output**:
```python
[
    {
        "path": "string",
        "chunk_id": "int",
        "similarity": "float",
        "snippet": "string",
        "metadata": {...}
    }
]
```

**Calling Convention**:
```python
from scripts.tools.search import semantic_search

results = semantic_search(
    query="Python async programming",
    index_path=".ka-index",
    top_k=5
)

for result in results:
    print(f"{result['path']}: {result['similarity']}")
```

### extract_keywords

**Purpose**: Extract keywords from text

**Input**:
```python
{
    "content": "string",
    "method": "string (default: tfidf)",
    "top_n": "int (default: 10)",
    "language": "string (default: en)"
}
```

**Output**:
```python
[
    {"keyword": "string", "score": "float"}
]
```

**Calling Convention**:
```python
from scripts.tools.extraction import extract_keywords

keywords = extract_keywords(
    content=document_content,
    top_n=10
)

for kw in keywords:
    print(f"{kw['keyword']}: {kw['score']}")
```

### connect_email

**Purpose**: Connect to email server

**Input**:
```python
{
    "server": "string",
    "username": "string",
    "password": "string",
    "protocol": "string (default: imap)"
}
```

**Output**:
```python
{
    "success": "bool",
    "connection_id": "string",
    "folders": ["string"]
}
```

### search_emails

**Purpose**: Search emails

**Input**:
```python
{
    "connection_id": "string",
    "query": "string",
    "folders": ["string"],
    "limit": "int (default: 50)"
}
```

**Output**:
```python
[
    {
        "id": "string",
        "subject": "string",
        "from": "string",
        "date": "string",
        "snippet": "string",
        "has_attachments": "bool"
    }
]
```

## Best Practices

### 1. Always Use opencode's File Operations

❌ Don't implement file scanning in knowledge-assistant
✅ Let opencode scan and provide document data

### 2. Return Structured Data

❌ Don't display results directly from knowledge-assistant
✅ Return structured data for opencode to format and display

### 3. Handle Errors Gracefully

```python
try:
    results = semantic_search(query)
except IndexError:
    return {"error": "Knowledge base not found. Please build index first."}
except Exception as e:
    return {"error": str(e)}
```

### 4. Provide Progress Feedback

For long-running operations, provide progress updates:

```python
def build_semantic_index(documents, progress_callback=None):
    total = len(documents)
    for i, doc in enumerate(documents):
        # process document
        if progress_callback:
            progress_callback(i+1, total)
```

## Configuration

### config.yaml additions

```yaml
knowledge_assistant:
  index_path: .ka-index
  embedding_model: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
  
  search:
    default_top_k: 10
    similarity_threshold: 0.5
  
  extraction:
    keyword_method: tfidf
    keyword_count: 10
    summary_length: 200
  
  email:
    # User-specific, should be in separate config
    server: imap.gmail.com
    username: user@gmail.com
    password: ${EMAIL_PASSWORD}  # Environment variable
```

## Integration Checklist

- [ ] Install dependencies: sentence-transformers, faiss-cpu
- [ ] Build initial knowledge base
- [ ] Test semantic search
- [ ] Configure email (optional)
- [ ] Test multi-source search

## Troubleshooting

### Issue: "Knowledge base not found"

**Solution**: Build knowledge base first
```
User: "Build knowledge base from [directory]"
```

### Issue: "Email connection failed"

**Solution**: Check email configuration
```
User: "Configure email with server [server], username [email]"
```

### Issue: "Search returns no results"

**Solution**: 
1. Check if knowledge base is built
2. Lower similarity threshold
3. Try different query phrasing

## Examples

### Complete Workflow Example

```
User: opencode

> Build knowledge base from D:/MyKnowledge

opencode: 
  Scanning D:/MyKnowledge...
  Found 156 markdown files
  Building semantic index...
  ✅ Knowledge base built!
  Documents: 156, Chunks: 489

> Find documents about machine learning

opencode:
  Searching...
  Found 5 relevant documents:
  1. ML Basics Guide (0.92)
  2. Neural Networks Intro (0.88)
  ...

> Extract keywords from the first document

opencode:
  Reading D:/MyKnowledge/ml-basics.md
  Keywords: machine learning, neural networks, deep learning...

> Search my emails for machine learning too

opencode:
  Email not configured. Configure now?
  Server: imap.gmail.com
  Username: user@gmail.com
  
  Connected!
  Searching emails...
  Found 2 emails about machine learning
  ...
```

---

**Version**: 1.1.0  
**Maintainer**: Knowledge Assistant Team  
**Last Updated**: 2026-03-06

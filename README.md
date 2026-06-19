# LLM Zoomcamp

My coursework and homework for [DataTalksClub/llm-zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp) — a free 10-week course on building AI systems with LLMs.

## Course Overview

In 10 weeks you learn how to build an AI system that answers questions about your knowledge base, covering:

- Retrieval-Augmented Generation (RAG)
- Search and indexing techniques
- Agentic RAG and tool use with LLMs
- Monitoring and evaluation
- Deployment

## Setup

**Prerequisites:** Python ≥ 3.14, [uv](https://docs.astral.sh/uv/)

```bash
uv sync
```

Create a `.env` file with your OpenAI API key:

```
OPENAI_API_KEY=sk-...
```

## Modules

| Module | Topic |
|--------|-------|
| 01 | Agentic RAG |

## Structure

```
llm_zoomcamp/
├── rag.ipynb              # RAG development notebook
├── agents.ipynb           # Agentic RAG development notebook
├── rag_helper.py          # Core RAG helper class
├── ingest.py              # Data ingestion utilities
└── 01-agentic-rag/
    └── homework/          # Module 1 homework submission
```

## Course Link

[github.com/DataTalksClub/llm-zoomcamp](https://github.com/DataTalksClub/llm-zoomcamp)

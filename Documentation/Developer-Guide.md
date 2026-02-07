# Developer & API Guide
This document serves as the "Internal Manual" for engineers who will maintain or extend the system. It focuses on the ReAct logic and the specific configurations required for the Agentic RAG pipeline.

## System Orchestration (Retrieval.py)
The core "brain" uses a ReAct (Reasoning + Acting) Agent.
* **Prompt Logic:** The system prompt instructs the agent to extract geographic intent (e.g., "Globe") and `pass` it as a city parameter to the `context` tool.
* **Tool Binding:** The `context` tool is bound to the LLM via LangChain's function-calling interface. It uses Pinecone's metadata filtering to restrict searches to specific city namespaces.

## Data Engineering (Ingestion.py)
The ingestion pipeline is designed for high-throughput, asynchronous updates.
* **Asynchronous Upserting:** The `index_documents` function utilizes the `aadd_documents` method in `langchain-pinecone` to batch vectors (default size: 500) without blocking the primary execution thread.
* **Metadata Schema:** Every vector MUST include a `city` metadata key. The search tool in `Retrieval.py` relies on this exact key for filtering.

## Environment Setup
Create a `.env` file with the following variables:
* `GOOGLE_API_KEY`: For Gemini-3-Flash and Embedding-001.
* `PINECONE_API_KEY`: For vector storage.
* `INDEX_NAME`: The specific Pinecone index (e.g., arizona-real-estate).
* `TAVILY_API_KEY`: For real-time web crawling.

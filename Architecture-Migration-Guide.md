# Arizona Real Estate AI: Agentic RAG Intelligence 🌵🤖
This document details the architectural evolution of the Arizona Real Estate Intelligence project, transitioning from a legacy Static ETL Pipeline to a modern Agentic RAG (Retrieval-Augmented Generation) System

## High-Level Paradigm Shift
The project has evolved from a linear data-processing tool into a dynamic AI agent capable of reasoning about regional context.
* **V1 (Legacy):** A "Service-Oriented" ETL pipeline that performed sequential extraction, cleaning, and visualization via subprocesses.
* **V2 (Current):** An Agentic RAG system that utilizes a ReAct (Reasoning + Acting) framework to autonomously decide which market data to retrieve and how to filter it by geography.

## Core Architectural Transitions
### Data Orchestration & Logic
* **Legacy:** Orchestration was handled by Pipeline.py, which used subprocess.run() to execute scripts in a fixed order.
* **Current:** Orchestration is handled by a LangChain Agent in Retrieval.py. The agent identifies city-specific intent (e.g., "Globe" vs "Phoenix") and dynamically applies metadata filters to the retrieval tool.
### Storage & Knowledge Base
* **Legacy:** Data was persisted in local <area>.json files, which were read by analysis scripts.
* **Current:** Data is indexed in a Pinecone Vector Store. Content is transformed into 1536-dimensional embeddings using google-genai, allowing for semantic retrieval rather than basic keyword matching.
### Extraction Strategy
* **Legacy:** Used a Scrapy engine (Spider.py) for deep crawling of specific domains with custom User-Agents.
* **Current:** Uses a Tavily AI Crawler in Ingestion.py to perform targeted, multi-city "shallow-wide" crawls, tagging every document with city metadata for precise filtering.

## Tech Stack Evolution
| Component     | Legacy V1 (Static Pipeline) | Agentic V2 (RAG Agent) |
|--------------|-----------------------------|------------------------|
| Logic / Brain | Regex & Subprocesses        | Google Gemini 3-Flash (ReAct) |
| Data Access   | Scrapy                      | Tavily AI Crawler |
| Analysis      | Pandas & NumPy              | Semantic Embeddings (1536-d) |
| Persistence   | Local JSON Files            | Pinecone Vector Database |
| Interface     | FastAPI (REST API)          | Streamlit (Interactive Chat) |
| Output        | Static JPEG Reports         | Dynamic Text, Sources, & Graphs |

## Security & Operational Maturity
The migration directly addressed critical "Future Work" items identified in the initial version.
* **Solving Synchronous Blocking:** V1 suffered from "Synchronous I/O," where the API thread would block for the entire crawl duration, creating a DoS risk. V2 utilizes asynchronous document indexing in Ingestion.py to handle large datasets without blocking the main thread.
* **Input Sanitization:** V1 relied on un-sanitized user input to construct command arguments, creating injection vectors. V2 uses structured tool parameters in Retrieval.py, where the agent validates and cleans city names before applying metadata filters.
* **Mitigating Bias:** The V2 architecture introduced targeted city crawls to ensure smaller Arizona towns like Globe are represented, preventing the "Phoenix Bias" inherent in the legacy general crawl.

## Summary of Migration Benefits
1. **Semantic Intelligence:** The system now understands why properties are high-end (e.g., mountain views, historic charm) rather than just looking for price keywords.
2. **Multimodal Interactivity:** Users can interact with the data via a chat interface that persists session history, a significant upgrade over static JPEG report generation.
3. **Scalability:** The move to Pinecone allows the system to scale to millions of listings across all 90+ Arizona municipalities.


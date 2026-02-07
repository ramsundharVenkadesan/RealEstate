# Product Requirements Document (PRD): Arizona Real Estate AI (V2)
**Version:** 2.0
**Status:*** Evolution from Legacy ETL to Agentic RAG
**Project Lead:** Ramsundhar Venkadesan

## Executive Summary
The Arizona Real Estate AI is a dynamic, regionally-aware intelligence platform that transforms raw market data into actionable conversational insights. Moving away from a legacy system of static reports and rigid spiders, V2 utilizes a ReAct (Reasoning + Acting) framework to provide users with real-time, filtered analysis of Arizona’s diverse property markets—from major metros like Phoenix to smaller towns like Globe and Sedona.

## Target Audience
* **The Relocating Professional:** Users moving to Arizona needing semantic comparisons of neighborhoods (e.g., "historic charm" vs. "mountain views").
* **Real Estate Investors:** Individuals seeking data-driven insights on price-per-square-foot and market trends across specific municipalities.
* **Local Researchers:** Users interested in niche markets that are often overshadowed by major metropolitan data.

## Goals & Objectives
* **Eliminate "Phoenix Bias":** Ensure regional representation through targeted multi-city crawls.
* **Enable Semantic Retrieval:** Move beyond keyword matching to "understand" property features using 1536-dimensional embeddings.
* **Minimize Hallucinations:** Use a "Groundedness" strategy where the agent must cite its sources from the vector store.
* **Improve Operational Maturity:** Replace blocking synchronous I/O with asynchronous batch processing for data ingestion.

## Functional Requirements
### Data Ingestion & Knowledge Base (Ingestion.py)
* **Targeted Crawling:** System must perform "shallow-wide" crawls of specific priority towns (Phoenix, Globe, Scottsdale, Tucson, Sedona, Prescott) using Tavily AI.
* **Vectorization:** Raw content must be converted into 1536-dimensional embeddings using gemini-embedding-001.
* **Asynchronous Upserting:** Documents must be indexed into Pinecone in batches to maintain high-speed performance.
### Agentic Reasoning (Retrieval.py)
* **Intent Extraction:** The gemini-3-flash brain must identify city names within user queries.
* **Metadata Filtering:** The system must apply geographic filters (e.g., city: globe) to the Pinecone search to ensure localized accuracy.
* **ReAct Logic:** The agent must autonomously decide when to call the context tool to retrieve relevant market documentation.
### User Interface (FrontEnd.py)
* **Conversational Interface:** A Streamlit-based chat experience that maintains session history.
* **Source Attribution:** Every response must provide expandable citations linking back to the original source URLs.
* **Output Sanitization:** The UI must clean LLM artifacts and render Markdown to ensure professional visual delivery.

## Non-Functional Requirements
* **Security:** Transition from un-sanitized command-line inputs (V1) to structured tool parameters (V2) to prevent injection vectors.
* **Scalability:** The architecture must support scaling to millions of listings across 90+ Arizona municipalities via the Pinecone vector database.
* **Performance:** Data retrieval and agent reasoning should be optimized for real-time interactivity within the Streamlit interface.

## Technical Stack
| Layer               | Technology                              |
| ------------------- | --------------------------------------- |
| **LLM / Brain**     | Google Gemini 3-Flash (ReAct Framework) |
| **Orchestration**   | LangChain (Agents & Tools)              |
| **Vector Database** | Pinecone                                |
| **Embeddings**      | Google Gemini-Embedding-001 (1536-d)    |
| **Web Crawling**    | Tavily AI Crawler                       |
| **Frontend**        | Streamlit                               |

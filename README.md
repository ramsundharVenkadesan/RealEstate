# Arizona Real Estate AI: The Evolution of Market Intelligence 🌵🤖
Welcome to the next generation of real estate analysis. This project has undergone a significant architectural shift, evolving from a static ETL (Extract, Transform, Load) pipeline into a dynamic Agentic RAG (Retrieval-Augmented Generation) system.
While the previous version relied on rigid Scrapy spiders and static JPEG report generation via FastAPI , the new system leverages Large Language Models (LLMs) and Vector Databases to provide conversational, regionally-aware insights in real-time.

## 🚀 The Evolution: Static to Agentic
| Feature              | Legacy System (V1 – Static)              | New Evolution (V2 – Agentic)              | Professional Impact                                                      |
|----------------------|------------------------------------------|-------------------------------------------|--------------------------------------------------------------------------|
| Logic Engine         | Rule-based Regex & Subprocesses           | Google Gemini (ReAct Framework)            | Shift from rigid scripts to autonomous reasoning                          |
| Data Flow            | Synchronous & Blocking Pipeline           | Asynchronous Knowledge Ingestion           | Resolved DoS risks and improved scalability                               |
| Storage              | Flat JSON Files (Static Reads)            | Pinecone Vector DB (Semantic)              | Enabled context-aware search over keyword matching                        |
| Security             | Un-sanitized CLI Command Inputs           | Structured Tool Parameter Validation       | Hardened system against injection vulnerabilities                         |
| Interface & Delivery | FastAPI (REST API) & Static JPEGs         | Streamlit (Conversational UI)              | Transformed a backend tool into an immersive, stateful platform           |
| Validation           | Manual Spot Checks                        | DeepEval (Faithfulness, Relevance)  | Automated KPI tracking for production-ready reliability                   |


### A Detailed Comparison

| Feature        | Legacy Architecture (V1)            | Agentic Evolution (V2)                          | Engineering Impact |
|---------------|-------------------------------------|--------------------------------------------------|--------------------|
| Logic Engine  | Rule-based Regex & Subprocesses     | Google Gemini 3-Flash (ReAct)                   | Shift from rigid scripts to autonomous reasoning |
| Data Retrieval| Sequential Local JSON Reads         | Pinecone Vector Search (1536-d)                 | Enables semantic **understanding** over keyword matching |
| Ingestion     | Synchronous Scrapy Crawls           | Asynchronous Tavily API Batching                | Eliminates I/O blocking and DoS risks |
| Validation    | Manual Spot Checks                  | RAGAS Framework (Faithfulness, Relevance)       | Quantifiable accuracy via automated KPI tracking |
| Security      | Un-sanitized Command-Line Inputs    | Structured Tool Parameters & Input Cleaning     | Hardens system against injection vectors |


## 🏗️ Core System Components
### The Knowledge Harvester (Ingestion.py)
The system no longer just "scrapes"—it targetedly crawls.
* **Priority Regionalism:** Specifically targets key towns like Globe, Sedona, and Phoenix to avoid "major-metro bias".
* **Vectorization:** Transforms raw real estate data into 1536-dimensional embeddings using Google's gemini-embedding-001.
* **High-Speed Upserting:** Uses asynchronous batching to index documents into Pinecone for instant retrieval.
### The Reasoning Brain (Retrieval.py)
This is where the ReAct framework lives.
* **Intent Extraction:** The agent identifies the specific city a user is asking about and applies a metadata filter to the vector store.
* **Groundedness:** The agent is strictly instructed to use its "context" tool and admit when it doesn't know an answer, mitigating hallucinations.
### The Interactive Interface (FrontEnd.py)
A modern, multimodal chat experience built with Streamlit.
* **Clean Formatting:** Features custom sanitization to remove LLM artifacts and render beautiful Markdown.
* **Multimodal Results:** Displays dynamic text answers, source attribution via expandable citations, and property listing images

## 🛠️ Tech Stack
* **LLM:** Google Gemini 3-Flash 
* **Orchestration:** LangChain (Agents & Tools) 
* **Vector Database:** Pinecone 
* **Web Intelligence:** Tavily AI Crawl 
* **Data Handling:** Pandas & Python Dotenv

## 🚦 Getting Started

1. **Environment Configuration**
```bash
GOOGLE_API_KEY=your_key
PINECONE_API_KEY=your_key
INDEX_NAME=arizona-real-estate
TAVILY_API_KEY=your_key
```
2. **Installation**
* Command: ```bash pip install streamlit langchain-google-genai langchain-pinecone langchain-tavily pandas python-dotenv```

3. **Execution**
* First, populate your vector store:
```bash python Ingestion.py```
* Then, launch the AI assistant:
```bash streamlit run FrontEnd.py```

## 📚 Project Documentation Hub
This project follows a rigorous **Product Lifecycle Management (PLM)** framework:

* **[Conception]** [Product Requirements Document (PRD)](./Documentation/Product-Requirements-Document.md) 
* **[Design]** [Architecture Migration Guide](./Documentation/Architecture-Migration-Guide.md)
* **[Development]** [Developer & API Guide](./Documentation/Developer-Guide.md)
* **[Quality]** [QA & Evaluation Plan](./Documentation/Quality-Assurance.md)
* **[Service]** [User Manual](./Documentation/User-Manual.md)
* **[Retirement]** [Archival Plan](./Documentation/Retirement-Archival.md)
* **[Roadmap]** [Project Roadmap](./Documentation/Roadmap.md)
* **[Limitations]** [System Limitations & Constraints](./Documentation/Limitation.md)

## ⚖️ License
Distributed under the MIT License. See `LICENSE` for more information.





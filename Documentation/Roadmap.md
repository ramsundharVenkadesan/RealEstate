# Project Roadmap: Arizona Real Estate AI (V3)
This roadmap defines the evolution of the system from a standard RAG agent to a self-correcting, cloud-native intelligence platform.

## Phase 1: Precision & Standardization (Q2 2026)
* **Model Context Protocol (MCP) Integration:** Adopt the Model Context Protocol to standardize how the agent interfaces with the `context` tool and future APIs (e.g., Zillow/Redfin), ensuring a modular "plug-and-play" architecture for data sources.
* **Hybrid Retrieval:** Implement BM25 (keyword) search alongside vector search to capture specific property IDs or street names that semantic search might miss.
* **Geographic Expansion:** Automate the `priority_towns` list by integrating with an Arizona municipal API to crawl all 90+ cities.

## Phase 2: Agentic Reflection & Reasoning (Q3 2026)
* **Reflective Agent Workflow (LangGraph):** Migrate from a simple ReAct loop to a **LangGraph state machine**. Implement a "Reflection" node that critiques the retrieved documents *before* generating an answer.
    * *Workflow:* Retrieve $\rightarrow$ Grade Documents (Is it relevant?) $\rightarrow$ If No: Rewrite Query & Retry $\rightarrow$ If Yes: Generate Answer.
* **Agent Memory:** Transition from session-only memory to persistent Vectorized Memory, allowing the agent to remember a user's specific preferences (e.g., "I only like mid-century modern") across different weeks.

## Phase 3: DevOps & Cloud-Native Deployment (Q4 2026)
* **Containerization (Docker):** Dockerize the application (Streamlit frontend + LangChain backend) to ensure environment consistency across development and production.
* **Infrastructure as Code (Terraform):** Define the entire Google Cloud infrastructure (Cloud Run services, Pinecone connectors, Secret Manager) in Terraform modules for reproducible deployments.
* **CI/CD Pipeline:** Implement a GitHub Actions workflow that runs the `Test_DeepEval.py` suite and, upon passing, automatically builds and pushes the Docker image to the container registry.

## Phase 4: Multimodal & Human-Centric Intelligence (Q1 2027)
* **Visual Sentiment Analysis:** Use Gemini’s vision capabilities to analyze listing photos and verify descriptions (e.g., confirming "granite countertops" or "mountain views").
* **Evaluator-Optimizer Loop:** Implement an offline "Optimizer" agent that reviews low-scoring user sessions (from the DeepEval logs) and automatically generates better synthetic examples to fine-tune the prompt or few-shot examples.

## Operational Excellence (Ongoing)
* **Cost Monitoring:** Implement a real-time token dashboard to track spending per query.
* **Latency Optimization:** Cache frequent queries (e.g., "Market trends in Phoenix") to reduce LLM calls and speed up response times.

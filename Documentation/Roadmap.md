# Project Roadmap
The roadmap defines the evolution of the Arizona Real Estate AI from its current state to a production-ready enterprise platform.

## Phase 1: Precision & Scale (Q1 2026)
* **Hybrid Retrieval:** Implement BM25 (keyword) search alongside vector search to capture specific property IDs or street names that semantic search might miss.
* **Geographic Expansion:** Automate the `priority_towns` list by integrating with an Arizona municipal API to crawl all 90+ cities.

## Phase 2: Advanced Reasoning (Q2 2026)
* **Agent Memory:** Transition from session-only memory to persistent Vectorized Memory, allowing the agent to remember a user's specific preferences across different weeks.
* **Multi-Step Planning:** Upgrade to LangGraph to allow the agent to perform complex workflows, such as "Find properties in Mesa AND calculate the estimated 30-year mortgage for each".

## Phase 3: Multimodal Intelligence (Q3 2026)
* **Visual Sentiment Analysis:** Use Gemini’s vision capabilities to analyze listing photos and verify descriptions (e.g., confirming "granite countertops" or "mountain views").
* **Predictive Valuation:** Integrate historical transaction data to provide a "Market Heat Index" forecasting price changes over the next 3 months.

## Operational Excellence (Q4 2026)
* **Infrastructure:** Deploy via Docker on AWS ECS or Google Cloud Run with auto-scaling triggered by latency spikes.
* **Cost Monitoring:** Implement a real-time token dashboard to track spending per query and optimize cost-to-accuracy ratios.

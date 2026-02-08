# System Limitations & Constraints

This document outlines the known limitations of the Arizona Real Estate AI pipeline. It serves as a reference for developers and stakeholders regarding boundaries in data ingestion, retrieval accuracy, and system scalability.

## 1. Data Ingestion (`Ingestion.py`)

The current ingestion subsystem is the most critical dependency. It relies on specific external sources and hardcoded configurations.

### **A. Single Source Dependency**
* **Constraint:** The crawler is currently hardcoded to target a single domain: `https://www.arizonarealestate.com`.
* **Risk:** If this website changes its DOM structure, implements strict `robots.txt` policies, adds CAPTCHA challenges, or goes offline, the entire data pipeline will fail to acquire new information.
* **Mitigation:** Future updates should implement a multi-source strategy (e.g., Zillow, Redfin, local MLS feeds) to reduce Single Point of Failure (SPoF) risks.

### **B. Hardcoded Geographic Scope**
* **Constraint:** The crawler loops through a static list of `priority_towns`:
    * *Phoenix, Globe, Scottsdale, Tucson, Sedona, Prescott, Tempe, Gilbert.*
* **Impact:** Any real estate data outside these specific municipalities is ignored. Adding a new region (e.g., Mesa or Chandler) requires a code change and a re-deployment of the ingestion script.

### **C. Shallow Crawling Depth**
* **Constraint:** The `TavilyCrawl` tool is configured with `"max_depth": 2`.
* **Impact:** This is a "surface-level" scan. It captures main landing pages and immediate sub-pages but will likely miss specific property listings, historical transaction data, or granular neighborhood stats buried deeper in pagination or filters.

### **D. Synchronous Execution**
* **Constraint:** While the *indexing* to Pinecone is asynchronous (`asyncio`), the *crawling* process is synchronous. The script iterates through towns one by one.
* **Performance:** As the list of towns or the depth of the crawl grows, the execution time will increase linearly, potentially causing timeouts in serverless deployment environments.

---

## 2. Retrieval & RAG Logic (`Retrieval.py`)

### **A. Metadata Filtering Sensitivity**
* **Constraint:** The retrieval tool uses a hard filter: `{"city": {"$eq": city.lower()}}`.
* **Risk:** This relies on the ingestion script perfectly tagging documents with the correct city metadata. If a document discusses "North Scottsdale" but is tagged simply as "scottsdale," the filter works. However, if a user asks about a neighborhood not explicitly mapped to a city tag, the strict filter may return zero results.

### **B. Agent Tool Selection**
* **Constraint:** The system uses a single tool (`context`) tied to a basic agent loop.
* **Impact:** The agent cannot perform multi-step reasoning effectively (e.g., "Find the price of X, then calculate the mortgage payment"). It is limited to "Search -> Summarize" workflows.

---

## 3. Data Processing & Embeddings

### **A. Text Chunking**
* **Constraint:** Documents are split using `RecursiveCharacterTextSplitter` with a `chunk_size` of 4000 characters.
* **Impact:** While efficient for token limits, 4000 characters is a large context block. Specific details (like the price of a single home in a list of 50 homes) may get "diluted" within the embedding vector, making it harder to retrieve specific data points compared to broader market trends.

### **B. Static Data (No Real-Time Updates)**
* **Constraint:** The system is **not** real-time. Data is only as fresh as the last successful run of `Ingestion.py`.
* **Risk:** Real estate is fast-moving. Prices or active statuses retrieved from the vector store may be outdated by days or weeks depending on the cron schedule of the ingestion script.

---

## 4. Testing & Quality Assurance (`Test_DeepEval.py`)

### **A. Low Quality Thresholds**
* **Constraint:** The DeepEval metrics (`Faithfulness`, `AnswerRelevancy`) are currently set to a threshold of `0.1`.
* **Impact:** Passing these tests only proves the system is not completely broken. It does **not** guarantee high-quality, human-acceptable answers. A score of 0.15 is technically a "pass" but would likely be a poor user experience.

### **B. Synthetic/Limited Test Data**
* **Constraint:** The test suite currently runs on only 2 hardcoded examples.
* **Risk:** This sample size is statistically insignificant for production readiness and does not cover edge cases (e.g., adversarial prompts, out-of-scope locations, gibberish inputs).

---

## 5. Infrastructure

### **A. API Rate Limits**
* **Constraint:** The system relies on quotas from multiple providers:
    * **Tavily:** Crawling limits.
    * **Google Gemini:** Embedding and Generation token limits.
    * **Pinecone:** Vector storage and read/write units.
* **Risk:** Heavy usage during ingestion or a spike in user traffic could hit rate limits, causing the application to crash or return "Service Unavailable" errors.

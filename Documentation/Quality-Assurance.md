# Quality Assurance & Evaluation Plan: Arizona Real Estate AI

## Evaluation Objectives
The primary goal is to validate that the transition from a static ETL pipeline to an Agentic RAG system has improved accuracy and reduced regional bias. We will measure three core pillars:
* **Agent Reasoning:** Does the agent correctly identify when to call the context tool and apply the correct city filter?
* **Retrieval Quality:** Does the Pinecone vector store return the most relevant documents for a given query?
* **Response Integrity:** Is the final answer grounded in the retrieved context without introducing "hallucinations"?

## Key Performance Indicators (KPIs)
We will use the RAGAS (RAG Assessment) framework metrics to quantify performance:
| Metric             | Definition                                                                 | Success Threshold |
|--------------------|-----------------------------------------------------------------------------|-------------------|
| Faithfulness       | Are the claims made in the answer derived solely from the retrieved context? | > 90%             |
| Answer Relevance   | How well does the answer address the specific user prompt?                  | > 85%             |
| Context Precision  | Out of the k=5 documents retrieved, how many are actually useful?           | > 80%             |
| Intent Accuracy    | Rate at which the agent correctly extracts the city parameter for the tool. | > 95%             |

## Test Suite:
A set of benchmark queries will be used to test the system after every code change to `Retrieval.py` or `Ingestion.py.`
* **Regional Specificity:** "What are the price trends in Globe?" (Tests city extraction and metadata filtering).
* **Comparative Analysis:** "Compare Scottsdale pricing to Prescott." (Tests the agent's ability to handle multi-step retrieval).
* **Out-of-Distribution:** "What is the market like in New York?" (Tests the system's ability to gracefully admit it only has Arizona data).
* **Semantic Nuance:** "Find me homes with historic charm and mountain views." (Tests the 1536-d embedding search quality).

## Technical QA Procedures
* **Asynchronous Stress Test:** Verify that index_documents in Ingestion.py handles batch sizes of 500 without timing out or dropping records.
* **Sanitization Check:** Ensure the clean_llm_output function in FrontEnd.py successfully removes specific artifacts like \*$ or stray backslashes that break Streamlit rendering.
* **Source Verification:** Manually audit the "View Sources" expander in the UI to ensure the links match the content provided in the answer.

## Continuous Improvement Loop
The evaluation and maintenance of the Arizona Real Estate AI follow an iterative lifecycle designed to refine the agent's regional intelligence and close knowledge gaps.
* **Log:** The system captures all user queries and corresponding assistant responses within the st.session_state during each active Streamlit session.
* **Audit:** Logs are regularly analyzed to identify "Knowledge Gaps"—specifically queries where the agent returned the default fallback: "I couldn't find a specific answer in the current market data".
* **Expand:** When a gap is identified (e.g., a user asks about a town not in the initial crawl), the priority_towns list in Ingestion.py is updated.
* **Re-index:** The Ingestion.py script is re-executed to perform a targeted Tavily crawl and asynchronously index the new regional data into Pinecone, ensuring the agent is grounded in the most recent market trends.

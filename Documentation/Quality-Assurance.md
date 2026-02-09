# Quality Assurance & Evaluation Plan: Arizona Real Estate AI

## Evaluation Objectives
The primary goal is to validate that the transition from a static ETL pipeline to an Agentic RAG system has improved accuracy and reduced regional bias. We will measure three core pillars:
* **Agent Reasoning:** Does the agent correctly identify when to call the context tool and apply the correct city filter?
* **Retrieval Quality:** Does the Pinecone vector store return the most relevant documents for a given query?
* **Response Integrity:** Is the final answer grounded in the retrieved context without introducing "hallucinations"?

## Key Performance Indicators (KPIs)
We utilize the **DeepEval** framework to implement RAGAS-style metrics for automated evaluation. The evaluation is powered by the `gemini-3-flash-preview` model, serving as the "judge" to score the pipeline's outputs.

| Metric | Definition | Success Threshold |
| :--- | :--- | :--- |
| **Faithfulness** | Are the claims made in the answer derived solely from the retrieved context? | > 0.1 (Baseline) |
| **Answer Relevancy** | How well does the answer address the specific user prompt? | > 0.1 (Baseline) |
| **Contextual Precision** | Out of the retrieved documents, how many are relevant to the query? | > 0.1 (Baseline) |

*(Note: Thresholds are set to 0.1 in `Test_DeepEval.py` for initial pass/fail regression testing, with a goal to increase them as the model matures.)*

## Automated Test Suite
A regression test suite (`Test_DeepEval.py`) utilizing **Pytest** is triggered after changes to `Retrieval.py`. It compares the live pipeline's output against expected ground truths.

### Benchmark Queries (Automated)
* **Market Trends:** "What are the price trends in Tempe?"
    * *Goal:* Validation of localized trend synthesis.
* **Comparative Analysis:** "Compare Scottsdale pricing to Prescott."
    * *Goal:* Verification of multi-entity handling and contrast logic.

### Reporting & Logging
The automated suite generates a persistent log for longitudinal tracking:
* **File:** `kpi_report.csv`
* **Data Points:** Timestamp, Input Query, Faithfulness Score, Answer Relevancy Score, Context Precision Score, and Reason (derived from Context Precision failure reasons).

## Sample Output (`kpi_report.csv`)
| Timestamp           | Query                                   | Faithfulness | Answer Relevancy | Context Precision | Reason |
|:--------------------|:----------------------------------------|-------------:|-----------------:|------------------:|:-------|
| 2026-02-08 20:08:21 | What are the price trends in Tempe?     |         0.87 |             0.89 |              1.00 | The score is 1.00 because all relevant nodes are perfectly prioritized at the top of the list! The first node captures essential "Tempe Trends / February 7, 2026" and the "Residential Median List Price: $482,500," while the second and third nodes establish a helpful "mix of residential listings." The fourth node further details "past sales history, dates and prices of homes recently sold nearby," correctly ensuring that the irrelevant fifth node—which is just a "general navigation menu and contact page"—is ranked last. |
| 2026-02-08 20:11:42 | Compare Scottsdale pricing to Prescott. |         1.00 |             0.86 |              0.58 | The score is 0.58 because while the first two nodes correctly provide Scottsdale's "Residential Median List Price:$1,140,000", several irrelevant nodes are ranked higher than remaining relevant data. Specifically, node 3 contains "generic website navigation links" and node 5 provides "general information about closing costs" instead of specific city data. These, along with node 6 which focuses on "Surprise, Goodyear, and Casa Grande", precede relevant content like node 7, which identifies Prescott as "America’s most authentic Western town", and node 9, which contains "sold property prices in Prescott". Furthermore, irrelevant nodes such as node 10's "general navigation page" and node 14's "list of addresses in Prescott" are ranked ahead of relevant nodes 11, 13, 16, and 18. |


## Technical QA Procedures
* **Asynchronous Stress Test:** Verify that `index_documents` in `Ingestion.py` handles batch sizes of 500 without timing out.
* **Sanitization Check:** Ensure the `clean_llm_output` function in `FrontEnd.py` successfully removes artifacts (e.g., `*$`) that break Streamlit rendering.
* **Metric Automation:** Ensure `Test_DeepEval.py` suppresses asyncio/deprecation warnings to produce clean console output during CI/CD runs.

## Continuous Improvement Loop
The evaluation and maintenance of the Arizona Real Estate AI follow an iterative lifecycle designed to refine the agent's regional intelligence and close knowledge gaps.
* **Log:** The system captures all user queries and corresponding assistant responses within `st.session_state`.
* **Audit:** Logs are analyzed to identify "Knowledge Gaps" (e.g., fallback responses).
* **Expand:** The `priority_towns` list in `Ingestion.py` is updated based on missing regions.
* **Re-index:** The ingestion script is re-executed to perform targeted Tavily crawls and update the Pinecone index.

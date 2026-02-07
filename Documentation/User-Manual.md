# User Manual: Arizona Real Estate AI Assistant
Welcome to the Arizona Real Estate AI Assistant, a specialized tool designed to provide you with grounded, regionally-specific insights into Arizona's property markets. This assistant isn't just a chatbot; it is an Agentic RAG (Retrieval-Augmented Generation) system that reasons through your questions to find the most accurate data available.

## Interacting with the Assistant
To get the most out of your session, use natural language to ask about market trends, pricing, or specific geographic areas in Arizona.
* **Regional Filtering:** When you mention a specific town (e.g., "What’s happening in Globe?"), the assistant automatically identifies that city and filters its search to only show you data from that area.
* **Grounded Answers:** The assistant is trained to prioritize the data it finds in its local knowledge base. If it cannot find specific information for a query, it will notify you rather than making up an answer.

## Understanding Your Results
Every response is designed to be transparent and verifiable.
* **Citations:** At the end of a response, you will often see a "View Sources" expander. Clicking this will reveal the exact URLs the assistant used to generate its answer, allowing you to verify the data yourself.
* **Clean Formatting:** The interface automatically sanitizes technical artifacts to provide you with clean, readable Markdown text and tables.

## Tips for "Golden Queries"
To see the full power of the agent's reasoning, try queries like these:
* **Comparative:** "How does the price-per-square-foot in Sedona compare to Prescott?"
* **Semantic:** "Find me areas in Phoenix known for historic charm rather than new builds."
* **Trend-Based:** "What are the latest luxury market trends in Scottsdale?"

## Troubleshooting & Session Management
* **Missing Information:** If the agent says it "couldn't find a specific answer," it may be because that town isn't in the current priority_towns list. These gaps are regularly audited and filled through new data crawls.
* **Clear History:** If you want to start a new topic, use the "Clear Chat History" button in the sidebar to reset the session and ensure the agent isn't confused by previous context.

## Privacy & Security
This system is built with Privacy by Design principles. It focuses on extracting market data and does not store personal user identifiers within the public knowledge base.

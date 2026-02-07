# Retirement & Archival Plan: Arizona Real Estate AI

## Decommissioning Data & Infrastructure
To avoid "orphaned" costs and secure your data, follow these steps to wind down the operational environment:
* **Vector Database Cleanup:** Use the Pinecone SDK to delete the specific index named in your `.env` (e.g., `arizona-real-estate`). You can use the `delete_all=True` parameter to wipe the vectors while keeping the index structure, or `pc.delete_index()` to remove the resource entirely.
* **Web Crawler Deactivation:** Revoke or rotate the Tavily API keys used in `Ingestion.py` to prevent any accidental automated crawls from consuming credits.
* **Interface Shutdown:** If hosted on Streamlit Community Cloud, use the "Delete app" option in the overflow menu to stop the instance. For Cloud Run or AWS deployments, delete the container image and service to stop billing.

## Knowledge & Research Archival
Preserve the intelligence you’ve gathered so your findings can be reused in future projects:
* **Log Preservation:** Download the final interaction logs from your Streamlit dashboard. These provide a "Knowledge Gap" map of what the AI couldn't answer, which is valuable for future iterations.
* **Documentation Export:** Ensure your Architecture Evolution, PRD, QA Plan, and User Manual are committed to your GitHub repository for a complete "Project Portfolio" view.
* **Environment Snapshot:** Save a final `requirements.txt` file to ensure the specific versions of `langchain-google-genai` and `langchain-pinecone` are documented, preventing "dependency rot" if you revisit the project later.

## Service Sunset & Handover
If the tool had active users, the "Retirement" stage ensures a professional exit:
* **Sunset Notification:** Display a "Project Concluded" message in the `FrontEnd.py` sidebar, informing users that the market data is no longer being updated as of a specific date.
* **Source Code "Cold Storage":** Mark the GitHub repository as Archived (Read-Only). This signals to other developers that the project is a finished work and is no longer being actively maintained.

## End-of-Life (EOL) Checklist
| Task            | Category        | Success Criteria                                                |
|-----------------|-----------------|-----------------------------------------------------------------|
| Purge Vectors   | Financial       | Pinecone index billing is confirmed as $0.00.                   |
| Revoke Keys     | Security        | Gemini and Tavily keys are deleted or rotated.                  |
| Archive Logs    | Research        | Interaction logs are saved locally for analysis.                |
| GitHub Tagging  | Documentation   | Repository is tagged with a "Final Release" version.            |

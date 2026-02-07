from typing import List, Dict, Any
import streamlit as st
from Retrieval import run_llm


def format_sources(context_docs: List[Any]) -> List[str]:
    """Extracts unique source URLs from retrieved LangChain Document metadata."""
    unique_sources = set()
    for doc in context_docs:
        # LangChain Documents store metadata in a .metadata dictionary
        source = getattr(doc, "metadata", {}).get("source")
        if source:
            unique_sources.add(str(source))
    return sorted(list(unique_sources))

def clean_llm_output(text: str) -> str:
    # Removes common artifacts that break Streamlit Markdown
    return text.replace("$*", "*").replace("*$", "*").replace("\\", "")


# --- Page Configuration ---
st.set_page_config(page_title="Arizona Real Estate AI", layout="centered", page_icon="🌵")
st.title("🌵 Arizona Real Estate Intelligence")

# --- Sidebar ---
with st.sidebar:
    st.subheader("Session Management")
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I'm your Arizona Real Estate assistant. How can I help you analyze market trends today?",
            "sources": []
        }
    ]

# --- Display Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            with st.expander("View Sources"):
                for source in message["sources"]:
                    st.markdown(f"- [{source}]({source})")

# --- User Input & Agent Logic ---
if prompt := st.chat_input("Ask about market trends, pricing, or specific areas..."):
    # 1. Display and store user message
    st.session_state.messages.append({"role": "user", "content": prompt, "sources": []})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generate and display assistant response
    with st.chat_message("assistant"):
        try:
            with st.spinner("Searching regional data and analyzing..."):
                # Call your RAG pipeline
                result: Dict[str, Any] = run_llm(query=prompt)

                answer = str(result.get("answer", "")).strip() or "I couldn't find a specific answer in the current market data."
                clean_answer = clean_llm_output(answer)
                sources = format_sources(result.get("context", []))

                # Display in UI
                st.markdown(clean_answer)
                if sources:
                    with st.expander("View Sources"):
                        for source in sources:
                            st.markdown(f"- [{source}]({source})")

                # 3. Store assistant message in session state for persistence
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })
        except Exception as e:
            st.error("I encountered an error while processing your request.")
            st.exception(e)
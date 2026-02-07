import os

from typing import Any, Dict
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_classic.agents.react.agent import create_react_agent # Import function to create a react agent
from langchain.chat_models import init_chat_model

from langchain.messages import ToolMessage
from langchain.tools import tool
from langchain_classic.agents import AgentExecutor

from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from langchain_classic import hub


load_dotenv()

embedding_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001",
                                               chunk_size=50, retry_min_seconds=10,
                                               output_dimensionality=1536)
vector_store = PineconeVectorStore(embedding=embedding_model, index_name=os.environ.get("INDEX_NAME"))
model = init_chat_model(model="gemini-3-flash-preview" , model_provider="google_genai")


@tool(response_format="content_and_artifact")
def context(query:str, city:str=None):
    """Retrieve relevant context from the vector store.
       Args:
            query: The search terms.
            city: Optional city name (e.g., 'globe', 'phoenix') to filter results.
    """
    search_kwargs = {"k": 5}
    if city: search_kwargs["filter"] = {"city": {"$eq": city.lower()}}
    retrieved_docs = vector_store.as_retriever(search_kwargs=search_kwargs).invoke(query)
    serialized_string = "\n\n".join(f"Source: {doc.metadata.get('source', 'Unknown')}\n\nContent:{doc.page_content}"
                                    for doc in retrieved_docs)
    return serialized_string, retrieved_docs

def run_llm(query:str) -> Dict[str, Any]:
    """Run the RAG pipeline to answer a query using retrieved documentation
        Args:
            query (str): The query to answer.
        Returns:
            Dictionary Containing:
                -Answer: The generated answer from the LLM.
                -Context: The relevant context retrieved from the vector store.
    """

    system_message = (
        "You are an expert Arizona Real Estate Assistant. "
        "When a user asks about a specific town (e.g., Globe, Mesa), "
        "extract the city name and pass it to the 'context' tool's 'city' parameter. "
        "This ensures you get data for that specific area rather than general Phoenix trends."
    )
    agent = create_agent(model, tools=[context], system_prompt=system_message)
    messages = [{"role": "user", "content": query}]
    response = agent.invoke({"messages": messages})
    last_message = response["messages"][-1]
    if isinstance(last_message.content, list):
        # Extract the 'text' field from the first text block found
        answer = next((block['text'] for block in last_message.content if
                       isinstance(block, dict) and block.get('type') == 'text'), "")
    else:
        answer = last_message.content
    context_docs = []
    for message in response['messages']:
        if (isinstance(message, ToolMessage)) and (
        hasattr(message, 'artifact')):  # Artifact attribute when tool is executed
            context_docs.extend(message.artifact)  # Value assigned to artifact is a list
    return {"answer": answer, "context": context_docs}  # Context is the list of documents in the artifact attribute

if __name__ == "__main__":
    response = run_llm("Which areas in Arizona have the best price-per-square-foot?")
    print(f"Answer: {response['answer']}")

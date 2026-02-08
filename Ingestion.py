import asyncio, os, ssl, certifi
from typing import Any, Dict, List
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_tavily import TavilyCrawl
from langchain_pinecone import PineconeVectorStore


load_dotenv()

ssl_context = ssl.create_default_context(cafile=certifi.where())
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUEST_CA_BUNDLE"] = certifi.where()

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", show_progress_bar=True,
                                          chunk_size=500, retry_min_seconds=10, output_dimensionality=1536)

vector_store = PineconeVectorStore(embedding=embeddings, index_name=os.environ.get("INDEX_NAME"))
tavily_crawl = TavilyCrawl()
all_docs = []
priority_towns = ["Phoenix", "Globe", "Scottsdale", "Tucson", "Sedona", "Prescott", "Tempe", "Gilbert"]
for town in priority_towns:
    print(f"Targeting data for: {town}")
    # Targeted crawl for each town
    result = tavily_crawl.invoke({
        "url": "https://www.arizonarealestate.com",
        "max_depth": 2,  # Lower depth is faster and more focused
        "instructions": f"Find real estate market trends, pricing, and listings specifically for {town}, Arizona."
    })

    for res in result['results']:
        if res.get('raw_content'):
            all_docs.append(Document(
                page_content=res['raw_content'],
                metadata={
                    "source": res['url'],
                    "city": town.lower()  # Tag with city for filtering
                }
            ))

print(f"Successfully processed {len(all_docs)} documents.")
text_spliter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=200)
docs_split = text_spliter.split_documents(all_docs)
if not docs_split:
    print("Warning: No documents to index. Check crawl instructions or URL.")

async def index_documents(documents:List[Document], batch_size:int) -> bool:
    """Process documents into batches asynchronously and index them into Pinecone."""
    batches = [documents[index:index + batch_size] for index in range(0, len(documents), batch_size)]

    async def add_batch(batch:List[Document], batch_number:int) -> bool:
        try:
            await vector_store.aadd_documents(batch)
        except Exception as e:
            print(f"Error indexing batch {batch_number}: {e}")
            return False
        return True

    tasks = [add_batch(batch=batch, batch_number=batch_number + 1) for batch_number, batch in enumerate(batches)]
    results:List[bool] = await asyncio.gather(*tasks, return_exceptions=True)

async def index_docs():
    await index_documents(docs_split, batch_size=500)


if __name__ == "__main__":
    asyncio.run(index_docs())


import os
import pandas as pd
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision

# Import your existing RAG pipeline
from Retrieval import run_llm, embedding_model, model as eval_llm

# 1. Define Benchmark Queries (From your QA Plan)
test_queries = [
    "What are the price trends in Globe?",
    "Compare Scottsdale pricing to Prescott.",
    "Find me homes with historic charm and mountain views.",
    "What is the average square footage in Sedona?"
]

def run_evaluation():
    results = []

    print(f"🚀 Starting Ragas Evaluation for {len(test_queries)} queries...")

    for query in test_queries:
        # Run your actual Agentic RAG pipeline
        response = run_llm(query)
        
        # Extract data for Ragas
        # Ragas expects contexts as a list of strings
        contexts = [doc.page_content for doc in response.get("context", [])]
        answer = response.get("answer", "")

        results.append({
            "question": query,
            "answer": answer,
            "contexts": contexts
        })

    # 2. Prepare Dataset for Ragas
    dataset = Dataset.from_list(results)

    # 3. Execute Evaluation
    # We use your existing Gemini model and Embeddings for the evaluation 'judge'
    score = evaluate(
        dataset=dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision
        ],
        llm=eval_llm,
        embeddings=embedding_model
    )

    # 4. Export & Display Results
    df = score.to_pandas()
    print("\n--- Ragas Evaluation Scores ---")
    print(df[['question', 'faithfulness', 'answer_relevancy', 'context_precision']])
    
    # Save to CSV for your "Knowledge Archival" process
    df.to_csv("ragas_eval_report.csv", index=False)
    print("\nEvaluation complete. Results saved to 'ragas_eval_report.csv'")

if __name__ == "__main__":
    run_evaluation()

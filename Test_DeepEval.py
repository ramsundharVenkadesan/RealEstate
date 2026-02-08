import os
import pytest
import warnings
import csv
from datetime import datetime
from dotenv import load_dotenv

# 1. SUPPRESS DEPRECATION WARNINGS
warnings.filterwarnings("ignore", category=DeprecationWarning)
# Specific filter for the Google/Aiohttp warning
warnings.filterwarnings("ignore", message="Inheritance class AiohttpClientSession")

from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric, ContextualPrecisionMetric
from deepeval.models.base_model import DeepEvalBaseLLM
from google import genai

# Import your REAL pipeline
from Retrieval import run_llm

load_dotenv()


# 2. GOOGLE GEMINI WRAPPER
class GoogleGemini(DeepEvalBaseLLM):
    def __init__(self, model_name="gemini-3-flash-preview"):
        self.model_name = model_name
        self.client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

    def load_model(self):
        return self.client

    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model_name, contents=prompt
        )
        return response.text

    async def a_generate(self, prompt: str) -> str:
        response = await self.client.aio.models.generate_content(
            model=self.model_name, contents=prompt
        )
        return response.text

    def get_model_name(self):
        return self.model_name


google_gemini = GoogleGemini(model_name="gemini-3-flash-preview")

faithfulness = FaithfulnessMetric(threshold=0.1, model=google_gemini, include_reason=True)
answer_relevancy = AnswerRelevancyMetric(threshold=0.1, model=google_gemini, include_reason=True)
context_precision = ContextualPrecisionMetric(threshold=0.1, model=google_gemini, include_reason=True)

test_data = [
    {
        "input": "What are the price trends in Tempe?",
        "expected_output": "The market in Tempe is showing localized trends with a mix of residential listings."
    },
    {
        "input": "Compare Scottsdale pricing to Prescott.",
        "expected_output": "Scottsdale typically commands luxury premiums, while Prescott remains more residential and historic."
    }
]


def log_kpi(input_query, metrics):
    file_exists = os.path.isfile("kpi_report.csv")
    with open("kpi_report.csv", mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Query", "Faithfulness", "Answer Relevancy", "Context Precision", "Reason"])

        # We grab the 'reason' from the metric to understand WHY it failed
        reason = metrics[2].reason if metrics[2].reason else "No reason provided"

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            input_query,
            f"{metrics[0].score:.2f}",  # Faithfulness
            f"{metrics[1].score:.2f}",  # Relevancy
            f"{metrics[2].score:.2f}",  # Context Precision
            reason
        ])


@pytest.mark.parametrize("test_case", test_data)
def test_customer_support(test_case):
    print(f"\n🧠 Querying Pipeline: {test_case['input']}...")

    # Run Real Pipeline
    real_response = run_llm(test_case['input'])
    actual_answer = real_response['answer']
    retrieved_docs = [doc.page_content for doc in real_response['context']]

    deepeval_case = LLMTestCase(
        input=test_case["input"],
        actual_output=actual_answer,
        retrieval_context=retrieved_docs,
        expected_output=test_case["expected_output"]
    )

    # Measure
    faithfulness.measure(deepeval_case)
    answer_relevancy.measure(deepeval_case)
    context_precision.measure(deepeval_case)

    # Log to CSV
    log_kpi(test_case["input"], [faithfulness, answer_relevancy, context_precision])

    # Assert (Now likely to pass because threshold is 0.1)
    assert_test(deepeval_case, [faithfulness, answer_relevancy, context_precision])


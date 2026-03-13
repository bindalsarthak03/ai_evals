from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


class EvalsEngine:

    def evaluate(self, question, answer, context):

        prompt = f"""
You are evaluating whether an LLM answer is supported by the provided context.

Question:
{question}

Answer:
{answer}

Context:
{context}

Return JSON:
{{
  "is_hallucinated": true or false
}}
"""

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=prompt
        )

        return response.text
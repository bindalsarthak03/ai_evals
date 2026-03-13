import json
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


class EvalsEngine:

    def evaluate(self, question, answer, context):

        prompt = f"""
You are evaluating whether an LLM answer is supported by context.

Question:
{question}

Answer:
{answer}

Context:
{context}

Return ONLY JSON:

{{
 "is_hallucinated": true or false
}}
"""

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=prompt
        )

        text = response.text.strip()

        # remove markdown formatting if present
        text = text.replace("```json", "").replace("```", "").strip()

        try:
            return json.loads(text)
        except Exception:
            return {"is_hallucinated": None}
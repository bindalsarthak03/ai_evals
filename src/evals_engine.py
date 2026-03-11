import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash-lite")

class EvalsEngine:
    def evaluate(self,question,answer,context):
        prompt = f"""
You are evaluating whether an LLM answer is supported by context.

Question:
{question}

Answer:
{answer}

Context:
{context}

Return JSON:
{{
 "is_hallucinated": boolean
}}
"""

        response = model.generate_content(prompt)

        return response.text
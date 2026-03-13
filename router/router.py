import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


class Router:

    def route(self, question):

        prompt = f"""
You are a routing assistant.

Your job is to choose the correct agent for a question.

Agents available:

1. sql_agent
   Use this if the question requires generating or executing SQL queries
   or retrieving information from a database.

2. rag_agent
   Use this if the question requires retrieving information from documents.

Return ONLY JSON.

Format:
{{
 "agent": "sql_agent" or "rag_agent"
}}

Question:
{question}
"""

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=prompt
        )

        text = response.text.strip()

        try:
            decision = json.loads(text)
            return decision["agent"]
        except Exception:
            # fallback if model returns malformed output
            if "sql_agent" in text.lower():
                return "sql_agent"
            return "rag_agent"
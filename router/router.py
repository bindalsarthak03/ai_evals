import os
import json
import sqlite3
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


class Router:

    def __init__(self, db_path="data/sample_db.sqlite"):
        self.db_path = db_path

    def get_schema(self):

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table'
        """)

        tables = cursor.fetchall()

        schema = ""

        for table in tables:

            table_name = table[0]

            cursor.execute(f"PRAGMA table_info({table_name})")

            columns = [col[1] for col in cursor.fetchall()]

            schema += f"{table_name}({', '.join(columns)})\n"

        conn.close()

        return schema


    def route(self, question):

        schema = self.get_schema()

        prompt = f"""
You are a routing assistant.

Your job is to decide which agent should answer a question.

Agents available:

1. sql_agent
   Use this when the question can be answered using the database.

2. rag_agent
   Use this when the question requires general knowledge or documents.

Database schema:
{schema}

Question:
{question}

Return ONLY JSON:

{{
 "agent": "sql_agent" or "rag_agent"
}}
"""

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=prompt
        )

        text = response.text.strip()

        text = text.replace("```json", "").replace("```", "").strip()

        try:
            decision = json.loads(text)
            return decision["agent"]
        except:
            if "sql_agent" in text.lower():
                return "sql_agent"

            return "rag_agent"
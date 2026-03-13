import sqlite3
import os
from dotenv import load_dotenv
from google import genai
import re

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


class SQLAgent:

    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)

    def run(self, question):

        schema = """
Tables:

users(id, name, city, signup_date)

products(id, name, price)

orders(id, user_id, product_id, quantity, order_date)
"""

        prompt = f"""
Convert the following question into a SQL query.

Database schema:
{schema}

Question:
{question}

Rules:
- Only return a SQL SELECT query
- Do not include explanations
"""

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=prompt
        )

        sql = response.text.strip()
        
        # remove markdown formatting
        sql = re.sub(r"```sql|```", "", sql).strip()
        
        # Basic safety check
        if not sql.lower().startswith("select"):
            return sql, "Unsafe query blocked"

        cursor = self.conn.cursor()

        try:
            cursor.execute(sql)
            result = cursor.fetchall()
        except Exception as e:
            result = str(e)

        return sql, result
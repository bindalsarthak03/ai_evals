import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


class LLMGenerator:

    def generate_answer(self, question):

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=question
        )

        return response.text
import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash-lite")

class LLMGenerator:
    
    def generate_answer(self,question):
        response = model.generate_content(question)

        return response.text
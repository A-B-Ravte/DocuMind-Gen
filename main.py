import os
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field

load_dotenv()

client = genai.Client(api_key=os.getenv('Gemini-Flash'))

prompt = "hello whats the data and time today."

response = client.models.generate_content(
    model = 'gemini-2.5-flash',
    contents = [prompt]

)

print(response.text)
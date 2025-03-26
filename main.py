from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY=os.getenv("API_KEY")

client = genai.Client(api_key=API_KEY)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Cual es la capital de Colombia?",
)

print(response.text)
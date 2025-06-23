import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

user_prompt = sys.argv[1]

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=messages
)

try:
    if sys.argv[2] == "--verbose":
        print(f'''
        {response.text}
        User prompt: {user_prompt}
        Prompt tokens: {response.usage_metadata.prompt_token_count}
        Response tokens: {response.usage_metadata.candidates_token_count}
        ''')
except:
    print(response.text)

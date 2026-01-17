import requests
import json
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(env_path)

api_key = os.getenv('DEEPSEEK_API_KEY', '').strip()

print(f"Testing OpenRouter with key: {api_key[:40]}...")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
    "HTTP-Referer": "http://localhost:8000",
    "X-Title": "myRamadan"
}

data = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [
        {"role": "user", "content": "Hello"}
    ]
}

print("\nMaking request to OpenRouter...")
response = requests.post("https://openrouter.io/api/v1/chat/completions", headers=headers, json=data, timeout=30)

print(f"Status: {response.status_code}")
print(f"Headers: {dict(response.headers)}")
print(f"Response: {response.text}")

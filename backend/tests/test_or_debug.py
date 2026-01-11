import requests
import json
import os
from pathlib import Path
from dotenv import load_dotenv

# Enable request logging
import logging
logging.basicConfig(level=logging.DEBUG)

env_path = Path('.') / '.env'
load_dotenv(env_path)

api_key = os.getenv('DEEPSEEK_API_KEY', '').strip()

print(f"Testing OpenRouter API")
print(f"Key: {api_key}\n")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

data = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Hello"}]
}

print("Sending request to https://openrouter.io/api/v1/chat/completions")
print(f"Headers: {headers}")
print(f"Data: {json.dumps(data, indent=2)}\n")

try:
    response = requests.post(
        "https://openrouter.io/api/v1/chat/completions",
        headers=headers,
        json=data,
        timeout=15
    )
    print(f"Response Status: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Exception: {type(e).__name__}: {str(e)}")

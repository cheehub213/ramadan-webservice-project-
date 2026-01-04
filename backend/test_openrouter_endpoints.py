import requests
import json
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(env_path)

api_key = os.getenv('DEEPSEEK_API_KEY', '').strip()

print(f"Testing OpenRouter with key: {api_key[:40]}...")
print(f"Key length: {len(api_key)}\n")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

data = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [
        {"role": "user", "content": "Say hello in JSON format"}
    ]
}

print("Testing different endpoints...")

# Try standard OpenRouter endpoint
endpoints = [
    "https://openrouter.io/api/v1/chat/completions",
    "https://api.openrouter.io/v1/chat/completions",
]

for endpoint in endpoints:
    print(f"\n Testing: {endpoint}")
    try:
        response = requests.post(endpoint, headers=headers, json=data, timeout=10)
        print(f"  Status: {response.status_code}")
        if response.text:
            print(f"  Response: {response.text[:200]}")
        else:
            print(f"  Response: (empty)")
    except Exception as e:
        print(f"  Error: {str(e)}")

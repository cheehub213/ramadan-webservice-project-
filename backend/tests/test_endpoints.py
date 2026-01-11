import requests
import json
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(env_path)

api_key = os.getenv('DEEPSEEK_API_KEY', '').strip()

print(f"Testing alternative OpenRouter endpoints\n")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

data = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Hello"}]
}

# Try different endpoints
endpoints = [
    ("Standard", "https://openrouter.io/api/v1/chat/completions"),
    ("Alternative 1", "https://api.openrouter.io/v1/chat/completions"),
    ("Alternative 2", "https://openrouter.io/v1/chat/completions"),
    ("Direct model", "https://openrouter.io/gpt-3.5-turbo"),
]

for name, url in endpoints:
    print(f"Testing {name}: {url}")
    try:
        response = requests.post(url, headers=headers, json=data, timeout=5)
        print(f"  ✓ Status: {response.status_code}")
        if response.status_code == 200:
            print(f"  SUCCESS! Response: {response.text[:100]}")
            break
        elif response.text:
            print(f"  Response: {response.text[:100]}")
    except requests.exceptions.Timeout:
        print(f"  ✗ Timeout")
    except Exception as e:
        print(f"  ✗ Error: {type(e).__name__}")
    print()

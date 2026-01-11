import requests
import json
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(env_path)

api_key = os.getenv('GROQ_API_KEY', '').strip()

print(f"Testing Groq with key: {api_key[:40]}...")
print(f"Key length: {len(api_key)}")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

data = {
    "model": "llama-3.3-70b-versatile",
    "messages": [
        {"role": "system", "content": "You are an Islamic scholar creating personalized duas."},
        {"role": "user", "content": "Create a dua for someone who fears going to hell. Return ONLY valid JSON with keys: dua_text_en, dua_text_ar, how_to_use_en, how_to_use_ar"}
    ],
    "temperature": 0.7,
    "max_tokens": 500
}

print("\nMaking request to Groq...")
response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data, timeout=30)

print(f"Status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print("SUCCESS! Response:")
    print(result["choices"][0]["message"]["content"][:500])
else:
    print(f"Error: {response.text[:500]}")

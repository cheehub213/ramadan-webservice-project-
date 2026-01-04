import requests
import json

api_key = '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'

print(f"API Key: {api_key}")
print(f"Key length: {len(api_key)}")
print(f"Key starts with: {api_key[:20]}")
print(f"Key format valid: {api_key.startswith('sk-or-v1-')}\n")

# Try POST with minimal headers
print("Testing POST with minimal headers...")
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [
        {"role": "user", "content": "test"}
    ]
}

import urllib.parse
print(f"Headers: {headers}")
print(f"Payload: {json.dumps(payload)}\n")

response = requests.post(
    "https://openrouter.io/api/v1/chat/completions",
    headers=headers,
    json=payload,
    timeout=10,
    allow_redirects=False  # Don't follow redirects
)

print(f"Status: {response.status_code}")
print(f"Headers: {dict(response.headers)}")
print(f"Body: {response.text[:200] if response.text else '(empty)'}")

if response.status_code == 405:
    print("\n405 Method Not Allowed - This API endpoint may not exist or POST is not supported")

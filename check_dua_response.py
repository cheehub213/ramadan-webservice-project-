#!/usr/bin/env python3
import requests
import json

payload = {
    'problem_description': 'I am struggling with anxiety and worry about my future.',
    'problem_category': 'Spiritual',
    'user_email': 'test@example.com',
    'user_name': 'Test User',
    'language': 'English'
}

response = requests.post('http://127.0.0.1:8001/api/v1/dua/generate', json=payload, timeout=30)
if response.status_code == 200:
    result = response.json()
    print("Full Response:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
else:
    print(f"Error: {response.status_code}")
    print(response.text)

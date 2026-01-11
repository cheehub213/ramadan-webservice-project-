import requests
import json
import time

url = "http://localhost:8000/api/dua/generate"

test_case = {
    "email": "test@example.com",
    "category": "Fear & Anxiety",
    "context": "I fear going to hell and worry about my sins"
}

print("=" * 70)
print("TESTING DEEPSEEK AI DUA GENERATION")
print("=" * 70)
print(f"\nInput: {test_case['context']}")
print(f"Category: {test_case['category']}")
print("\nSending request to backend... (may take 10-30 seconds)")

start = time.time()
try:
    response = requests.post(url, json=test_case, timeout=60)
    elapsed = time.time() - start
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nTime: {elapsed:.1f}s")
        print(f"AI Generated: {result.get('ai_generated', False)}")
        print("\n" + "=" * 70)
        print("ENGLISH DUA:")
        print("=" * 70)
        print(result.get('dua_text_en', 'N/A'))
        print("\n" + "=" * 70)
        print("ARABIC DUA:")
        print("=" * 70)
        print(result.get('dua_text_ar', 'N/A'))
    else:
        print(f"Error {response.status_code}: {response.text}")
except requests.exceptions.Timeout:
    print("Request timed out after 60 seconds")
except Exception as e:
    print(f"Error: {str(e)}")

print("\n" + "=" * 70)

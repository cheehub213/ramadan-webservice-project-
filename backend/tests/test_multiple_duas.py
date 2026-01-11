import requests
import json

url = "http://localhost:8000/api/dua/generate"

# Test multiple specific contexts
test_cases = [
    {"context": "I have an important exam tomorrow", "category": "Fear & Anxiety"},
    {"context": "I'm looking for a job and have an interview next week", "category": "Career Guidance"},
    {"context": "My mother is very sick in the hospital", "category": "Health Issues"},
]

for test in test_cases:
    print("=" * 70)
    print(f"INPUT: {test['context']}")
    print(f"CATEGORY: {test['category']}")
    print("=" * 70)
    
    response = requests.post(url, json={
        "email": "test@example.com",
        "category": test["category"],
        "context": test["context"]
    })
    
    if response.status_code == 200:
        result = response.json()
        print("\nENGLISH DUA:")
        print("-" * 70)
        print(result['dua_text_en'][:500])
        print("\n")
    else:
        print(f"Error: {response.status_code}")
    
    print("\n")

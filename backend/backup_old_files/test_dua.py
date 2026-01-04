import requests
import json

# Test the dua generation endpoint
url = "http://localhost:8000/api/dua/generate"

# Test case: "I fear going to hell" - should generate a dua specifically about hellfire, not general fear
test_data = {
    "email": "test@example.com",
    "category": "Fear & Anxiety",
    "context": "I fear going to hell"
}

print("=" * 60)
print("Testing Personalized Dua Generation")
print("=" * 60)
print(f"\nInput: {test_data['context']}")
print(f"Category: {test_data['category']}")
print("\nGenerating dua...")

try:
    response = requests.post(url, json=test_data)
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ Dua Generated Successfully!\n")
        print("-" * 60)
        print("ENGLISH DUA:")
        print("-" * 60)
        print(result.get('dua_text_en', 'No English dua'))
        print("\n" + "-" * 60)
        print("ARABIC DUA:")
        print("-" * 60)
        print(result.get('dua_text_ar', 'No Arabic dua'))
        print("\n" + "-" * 60)
        print("HOW TO USE:")
        print("-" * 60)
        print(result.get('how_to_use_en', 'No instructions'))
        print("\n" + "=" * 60)
        print(f"AI Generated: {result.get('ai_generated', False)}")
        print("=" * 60)
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"\n❌ Connection error: {e}")

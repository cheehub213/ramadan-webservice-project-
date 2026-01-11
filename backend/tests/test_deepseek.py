import requests
import json

# Test the AI-powered dua generation with DeepSeek
url = "http://localhost:8000/api/dua/generate"

test_cases = [
    {
        "email": "test@example.com",
        "category": "Fear & Anxiety",
        "context": "I fear going to hell and worry about my sins"
    },
    {
        "email": "test@example.com",
        "category": "Health Issues",
        "context": "My daughter has a fever and the doctors can't figure out what's wrong"
    },
    {
        "email": "test@example.com",
        "category": "Career Guidance",
        "context": "I'm about to graduate and very anxious about finding a good job"
    }
]

print("=" * 70)
print("TESTING DEEPSEEK AI-POWERED DUA GENERATION")
print("=" * 70)

for i, test_data in enumerate(test_cases, 1):
    print(f"\n{'=' * 70}")
    print(f"TEST CASE {i}: {test_data['context'][:50]}...")
    print(f"{'=' * 70}")
    
    try:
        response = requests.post(url, json=test_data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n✨ AI Generated: {result.get('ai_generated', False)}")
            print(f"\n📖 ENGLISH DUA:")
            print("-" * 70)
            print(result.get('dua_text_en', 'N/A')[:500])
            
            print(f"\n🕌 ARABIC DUA:")
            print("-" * 70)
            print(result.get('dua_text_ar', 'N/A')[:400])
            
            print(f"\n💡 HOW TO USE:")
            print("-" * 70)
            print(result.get('how_to_use_en', 'N/A')[:300])
        else:
            print(f"\n❌ Error {response.status_code}: {response.text}")
            
    except requests.exceptions.Timeout:
        print(f"\n⏱️ Request timed out (DeepSeek may be slow on first call)")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

print(f"\n{'=' * 70}")
print("✅ Testing complete!")
print("=" * 70)

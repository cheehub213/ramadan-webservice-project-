#!/usr/bin/env python3
"""Test the HTTP endpoint"""
import requests
import json

url = "http://localhost:8000/api/analyzer/analyze"
payload = {
    "question": "I am angry with my family",
    "email": "test@example.com"
}

print(f"Testing endpoint: {url}")
print(f"Payload: {json.dumps(payload)}")
print("=" * 70)

try:
    response = requests.post(url, json=payload, timeout=30)
    print(f"Status: {response.status_code}")
    
    result = response.json()
    print(f"\nResponse keys: {list(result.keys())}")
    print(f"AI Generated: {result.get('ai_generated')} (should be False)")
    print(f"Source: {result.get('source', 'N/A')} (should be 'semantic_search')")
    print(f"Hadith: {result.get('hadith')} (should be None)")
    print(f"AI Explanation: {result.get('ai_explanation')} (should be None)")
    
    if result.get('ayah'):
        print(f"Verse: {result['ayah'].get('reference')}")
        print(f"Translation: {result['ayah'].get('translation')[:60]}...")
    
    # Validation
    checks = [
        result.get('ai_generated') == False,
        result.get('source') == 'semantic_search',
        result.get('hadith') is None,
        result.get('ai_explanation') is None,
        result.get('ayah') is not None
    ]
    
    print("\n" + "=" * 70)
    if all(checks):
        print("✓ ALL CHECKS PASSED!")
        print("✓ Semantic search endpoint is working correctly!")
    else:
        print("✗ SOME CHECKS FAILED:")
        checks_names = [
            "ai_generated == False",
            "source == 'semantic_search'",
            "hadith is None",
            "ai_explanation is None",
            "ayah is not None"
        ]
        for i, (name, check) in enumerate(zip(checks_names, checks)):
            print(f"  {name}: {'✓' if check else '✗'}")
            
except requests.exceptions.ConnectionError as e:
    print(f"✗ Connection Error: {e}")
    print("Server might not be running on http://localhost:8000")
except Exception as e:
    print(f"✗ Error: {e}")

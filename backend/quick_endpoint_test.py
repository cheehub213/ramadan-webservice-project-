#!/usr/bin/env python3
"""Quick test of the endpoint behavior"""
import sys
from pathlib import Path

backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

test_data = {
    "question": "I am angry with my family",
    "email": "test@example.com"
}

print("Testing endpoint...")
response = client.post("/api/analyzer/analyze", json=test_data)

print(f"Status: {response.status_code}")
result = response.json()

print(f"\nResponse structure:")
for key, val in result.items():
    if key == 'ai_explanation':
        if val:
            print(f"  {key}: {val[:50]}... ({len(val)} chars)")
        else:
            print(f"  {key}: {val}")
    elif key == 'ayah':
        if val:
            print(f"  {key}: {val.get('reference')} - {str(val)[:60]}...")
        else:
            print(f"  {key}: {val}")
    else:
        print(f"  {key}: {val}")

print(f"\n✓ AI Generated: {result.get('ai_generated')} (should be False)")
print(f"✓ Source: {result.get('source', 'N/A')} (should be 'semantic_search')")
print(f"✓ Hadith: {result.get('hadith')} (should be None)")
print(f"✓ AI Explanation: {result.get('ai_explanation')} (should be None)")

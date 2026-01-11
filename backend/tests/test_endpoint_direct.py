#!/usr/bin/env python3
"""
Direct test of the analyze endpoint to confirm it calls semantic search.
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

# Test the semantic search method directly
async def test_semantic_search():
    print("=" * 70)
    print("TEST 1: Direct semantic search function call")
    print("=" * 70)
    from services_quran_semantic import QuranSemanticSearch
    
    test_prompts = [
        "I am angry with my family",
        "How do I handle marriage problems?",
        "I feel very sad"
    ]
    
    for prompt in test_prompts:
        result = QuranSemanticSearch.find_best_verse(prompt)
        print(f"\nPrompt: {prompt}")
        print(f"Result: {result}")

# Test the AIAnalyzerService method directly  
async def test_analyzer_service():
    print("\n" + "=" * 70)
    print("TEST 2: AIAnalyzerService.analyze_with_semantic_search()")
    print("=" * 70)
    from services_ai_analyzer import AIAnalyzerService
    
    test_prompts = [
        "I am angry with my family",
        "How do I handle marriage problems?"
    ]
    
    for prompt in test_prompts:
        result = await AIAnalyzerService.analyze_with_semantic_search(prompt)
        print(f"\nPrompt: {prompt}")
        print(f"Response keys: {list(result.keys())}")
        print(f"AI Generated: {result.get('ai_generated')}")
        print(f"Source: {result.get('source', 'N/A')}")
        print(f"Hadith: {result.get('hadith')}")
        print(f"AI Explanation: {result.get('ai_explanation')}")
        if result.get('ayah'):
            print(f"Verse: {result['ayah'].get('reference')}")

# Test the endpoint
async def test_endpoint():
    print("\n" + "=" * 70)
    print("TEST 3: Test via FastAPI TestClient (endpoint simulation)")
    print("=" * 70)
    
    # Import FastAPI TestClient and the app
    from fastapi.testclient import TestClient
    from main import app
    
    client = TestClient(app)
    
    test_data = {
        "question": "I am angry with my family",
        "email": "test@example.com"
    }
    
    print(f"Sending POST /api/analyzer/analyze with: {test_data}")
    response = client.post("/api/analyzer/analyze", json=test_data)
    
    print(f"Status: {response.status_code}")
    result = response.json()
    
    print(f"Response keys: {list(result.keys())}")
    print(f"AI Generated: {result.get('ai_generated')}")
    print(f"Source: {result.get('source', 'N/A')}")
    print(f"Hadith: {result.get('hadith')}")
    print(f"AI Explanation present: {'ai_explanation' in result}")
    if result.get('ai_explanation'):
        print(f"  Length: {len(result['ai_explanation'])} chars (SHOULD BE NONE!)")
    if result.get('ayah'):
        print(f"Verse: {result['ayah'].get('reference')}")

if __name__ == "__main__":
    asyncio.run(test_semantic_search())
    asyncio.run(test_analyzer_service())
    asyncio.run(test_endpoint())

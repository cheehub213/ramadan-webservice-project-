#!/usr/bin/env python3
"""Direct test of the analyze function"""
import sys
from pathlib import Path
import asyncio

backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

async def test():
    from services_ai_analyzer import AIAnalyzerService
    
    test_prompt = "I am angry with my family"
    print(f"Testing: {test_prompt}")
    print("=" * 70)
    
    result = await AIAnalyzerService.analyze_with_semantic_search(test_prompt)
    
    print(f"Response keys: {list(result.keys())}")
    print(f"AI Generated: {result.get('ai_generated')} (should be False)")
    print(f"Source: {result.get('source', 'N/A')} (should be 'semantic_search')")
    print(f"Hadith: {result.get('hadith')} (should be None)")
    print(f"AI Explanation: {result.get('ai_explanation')} (should be None)")
    
    if result.get('ayah'):
        print(f"Verse: {result['ayah'].get('reference')}")
        print(f"Similarity: {result['ayah'].get('similarity_score')}")
    
    # Check if response matches expected semantic search format
    checks = [
        result.get('ai_generated') == False,
        result.get('source') == 'semantic_search',
        result.get('hadith') is None,
        result.get('ai_explanation') is None,
        result.get('ayah') is not None
    ]
    
    print("\n" + "=" * 70)
    if all(checks):
        print("✓ ALL CHECKS PASSED - Semantic search is working!")
    else:
        print("✗ SOME CHECKS FAILED")
        for i, check in enumerate(checks):
            print(f"  Check {i+1}: {'✓' if check else '✗'}")

if __name__ == "__main__":
    asyncio.run(test())

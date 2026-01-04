"""Test semantic search functionality"""
import asyncio
from services_ai_analyzer import AIAnalyzerService

async def test():
    test_questions = [
        "I am very angry at my family members",
        "How can I improve my marriage and be a better husband",
        "I have no money and I'm struggling financially",
        "I feel very sad and depressed lately",
        "My mother is old and I want to respect her more",
        "I made mistakes and need forgiveness",
        "I'm worried and anxious about the future"
    ]
    
    print("=" * 70)
    print("TESTING SEMANTIC SEARCH FOR QURAN VERSES")
    print("=" * 70)
    
    for question in test_questions:
        print(f"\n📍 Question: {question}")
        result = await AIAnalyzerService.analyze_with_semantic_search(question)
        
        if result.get("ayah"):
            ayah = result["ayah"]
            print(f"   ✓ Reference: Quran {ayah['reference']}")
            print(f"   ✓ Similarity: {ayah['similarity_score']:.2%}")
            print(f"   ✓ Verse: {ayah['translation'][:100]}...")
        else:
            print(f"   ✗ {result.get('message', 'No match found')}")

if __name__ == "__main__":
    asyncio.run(test())

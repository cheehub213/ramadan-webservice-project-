"""Test Quran Semantic Search"""
import sys
sys.path.insert(0, 'backend')
import asyncio
from services_quran_search import search_quran_by_topic, get_quran_search

async def test():
    print("Initializing Quran Semantic Search...")
    search = get_quran_search()
    
    # Test 1: Money question
    print("\n" + "="*60)
    print("Test 1: 'I have a lack of money'")
    print("="*60)
    result = await search_quran_by_topic('I have a lack of money')
    print(f"📖 Reference: {result.get('reference', 'N/A')}")
    print(f"📜 Arabic: {result.get('arabic', 'N/A')}")
    print(f"📝 Translation: {result.get('translation', 'N/A')}")
    print(f"📊 Score: {result.get('score', 0):.3f}")
    
    # Test 2: Anxiety
    print("\n" + "="*60)
    print("Test 2: 'I am feeling anxious and stressed'")
    print("="*60)
    result2 = await search_quran_by_topic('I am feeling anxious and stressed')
    print(f"📖 Reference: {result2.get('reference', 'N/A')}")
    print(f"📜 Arabic: {result2.get('arabic', 'N/A')}")
    print(f"📝 Translation: {result2.get('translation', 'N/A')}")
    print(f"📊 Score: {result2.get('score', 0):.3f}")
    
    # Test 3: Marriage
    print("\n" + "="*60)
    print("Test 3: 'How should I treat my wife?'")
    print("="*60)
    result3 = await search_quran_by_topic('How should I treat my wife?')
    print(f"📖 Reference: {result3.get('reference', 'N/A')}")
    print(f"📝 Translation: {result3.get('translation', 'N/A')}")
    print(f"📊 Score: {result3.get('score', 0):.3f}")
    
    # Test 4: Debt/Bills
    print("\n" + "="*60)
    print("Test 4: 'I am worried about paying my bills and debt'")
    print("="*60)
    result4 = await search_quran_by_topic('I am worried about paying my bills and debt')
    print(f"📖 Reference: {result4.get('reference', 'N/A')}")
    print(f"📝 Translation: {result4.get('translation', 'N/A')}")
    print(f"📊 Score: {result4.get('score', 0):.3f}")
    
    # Test 5: Hardship
    print("\n" + "="*60)
    print("Test 5: 'I am going through difficult times'")
    print("="*60)
    result5 = await search_quran_by_topic('I am going through difficult times')
    print(f"📖 Reference: {result5.get('reference', 'N/A')}")
    print(f"📝 Translation: {result5.get('translation', 'N/A')}")
    print(f"📊 Score: {result5.get('score', 0):.3f}")

if __name__ == "__main__":
    asyncio.run(test())

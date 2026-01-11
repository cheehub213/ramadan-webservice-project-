"""Test Ask AI with money-related question"""
import asyncio
import sys
sys.path.insert(0, 'backend')

from services_ai_analyzer import AIAnalyzerService

async def test_money_question():
    service = AIAnalyzerService()
    
    print("=" * 60)
    print("Testing Ask AI: 'I have a lack of money'")
    print("=" * 60)
    
    result = await service.analyze("I have a lack of money")
    
    print(f"\n📖 Quran Reference: {result.get('ayah', {}).get('reference', 'N/A')}")
    print(f"Translation: {result.get('ayah', {}).get('translation', 'N/A')}")
    print(f"Explanation: {result.get('ayah', {}).get('explanation', 'N/A')}")
    
    print(f"\n📚 Hadith Source: {result.get('hadith', {}).get('narrator', 'N/A')}")
    print(f"Text: {result.get('hadith', {}).get('text', 'N/A')}")
    print(f"Explanation: {result.get('hadith', {}).get('explanation', 'N/A')}")
    
    print(f"\n🤖 AI Explanation: {result.get('ai_explanation', 'N/A')[:300]}...")
    print(f"\nAI Generated: {result.get('ai_generated', False)}")
    
    print("\n" + "=" * 60)
    print("Testing Ask AI: 'I'm worried about paying my bills'")
    print("=" * 60)
    
    result2 = await service.analyze("I'm worried about paying my bills")
    
    print(f"\n📖 Quran Reference: {result2.get('ayah', {}).get('reference', 'N/A')}")
    print(f"Translation: {result2.get('ayah', {}).get('translation', 'N/A')}")
    
    print(f"\n📚 Hadith Source: {result2.get('hadith', {}).get('narrator', 'N/A')}")
    print(f"Text: {result2.get('hadith', {}).get('text', 'N/A')}")

if __name__ == "__main__":
    asyncio.run(test_money_question())

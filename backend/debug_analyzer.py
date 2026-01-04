"""Debug the AI analyzer"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import asyncio
from services_ai_analyzer import AIAnalyzerService

async def test():
    questions = [
        'I am angry at my family',
        'I want to improve my marriage',
        'I am poor and have no money',
        'I am very sad and depressed',
        'How can I be a better son to my mother',
        'I committed sins and need forgiveness',
        'I am struggling with patience during hardship'
    ]
    for q in questions:
        print('='*60)
        print(f'Question: {q}')
        result = await AIAnalyzerService.analyze_with_full_quran(q)
        ayah = result.get('ayah', {})
        hadith = result.get('hadith', {})
        topic = result.get('topic_identified', 'N/A')
        ref = ayah.get('reference', 'N/A')
        trans = ayah.get('translation', 'N/A')
        hadith_text = hadith.get('text_en', 'N/A')
        
        print(f'Topic identified: {topic}')
        print(f'Ayah Reference: {ref}')
        print(f'Ayah Translation: {trans[:100]}...')
        print(f'Hadith: {hadith_text[:80]}...')
        print()

if __name__ == "__main__":
    asyncio.run(test())

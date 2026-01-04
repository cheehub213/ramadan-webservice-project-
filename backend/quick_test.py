"""Quick test"""
import asyncio
from services_ai_analyzer import AIAnalyzerService

async def test():
    questions = [
        'I am angry at my family',
        'How can I improve my marriage',
        'I have no money',
        'I feel sad',
        'My mother is old',
        'I need forgiveness',
    ]
    
    for q in questions:
        result = await AIAnalyzerService.analyze_with_semantic_search(q)
        if result.get('ayah'):
            ref = result['ayah']['reference']
            score = result['ayah']['similarity_score']
            print(f'✓ {q:35} → {ref:10} ({score:.1%})')
        else:
            msg = result.get('message', 'No match')
            print(f'✗ {q:35} → {msg}')

asyncio.run(test())

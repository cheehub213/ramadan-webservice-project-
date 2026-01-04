#!/usr/bin/env python3
"""Quick test for dua generation endpoint"""

import requests
import json

payload = {
    'problem_description': 'I am struggling with anxiety and worry about my future. I feel overwhelmed with responsibilities.',
    'problem_category': 'Spiritual',
    'user_email': 'test@example.com',
    'user_name': 'Ahmed Ali',
    'language': 'English'
}

print("📝 Testing Dua Generation Endpoint...")
print(f"Problem: {payload['problem_description'][:60]}...")
print()

try:
    response = requests.post('http://127.0.0.1:8001/api/v1/dua/generate', json=payload, timeout=60)
    print(f'Status Code: {response.status_code}')
    
    if response.status_code == 200:
        result = response.json()
        print('\n✅ DUA GENERATED SUCCESSFULLY!\n')
        print('=' * 70)
        print(f'ID: {result.get("id")}')
        print(f'User: {result.get("user_name")}')
        print(f'Problem Category: {result.get("problem_category")}')
        print(f'Language: {result.get("language")}')
        print('=' * 70)
        print('\n🤲 PERSONALIZED DUA (EN):\n')
        print(result.get('dua_text_en', 'No dua generated'))
        print('\n🤲 PERSONALIZED DUA (AR):\n')
        print(result.get('dua_text_ar', 'No dua generated'))
        print('\n' + '=' * 70)
        print('\n📖 HOW TO USE (EN):\n')
        print(result.get('how_to_use_en', 'No instructions'))
        print('\n📖 HOW TO USE (AR):\n')
        print(result.get('how_to_use_ar', 'No instructions'))
        print('\n' + '=' * 70)
    else:
        print(f'\n❌ Error: {response.status_code}')
        print(f'Response: {response.text}')
        
except requests.exceptions.ConnectionError:
    print('❌ Server not responding. Make sure server is running on http://127.0.0.1:8001')
except Exception as e:
    print(f'❌ Error: {e}')

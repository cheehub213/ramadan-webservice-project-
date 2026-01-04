#!/usr/bin/env python3
"""Test bilingual Dua Generation Endpoint"""

import requests
import json

payload = {
    'problem_description': 'I am struggling with anger and impatience. I lose my temper easily and say hurtful words to my family. I want to be more patient like the Prophet.',
    'problem_category': 'Spiritual',
    'user_email': 'fatima@example.com',
    'user_name': 'Fatima Ahmed',
    'language': 'English'
}

print("\n" + "="*80)
print("🤲 BILINGUAL DUA GENERATOR - TEST")
print("="*80)
print(f"\n📝 Problem: {payload['problem_description']}")
print(f"📂 Category: {payload['problem_category']}")
print(f"👤 User: {payload['user_name']}")

try:
    response = requests.post('http://127.0.0.1:8001/api/v1/dua/generate', json=payload, timeout=60)
    
    if response.status_code == 200:
        result = response.json()
        
        print(f"\n✅ Status: {response.status_code}")
        print(f"ID: {result.get('id')}")
        print(f"Created: {result.get('created_at')}")
        
        print("\n" + "="*80)
        print("🇺🇸 ENGLISH DUA:")
        print("="*80)
        print(result.get('dua_text_en', 'No English dua'))
        
        print("\n" + "="*80)
        print("🇸🇦 ARABIC DUA:")
        print("="*80)
        print(result.get('dua_text_ar', 'No Arabic dua'))
        
        print("\n" + "="*80)
        print("📖 HOW TO USE (ENGLISH):")
        print("="*80)
        print(result.get('how_to_use_en', 'No instructions'))
        
        print("\n" + "="*80)
        print("📖 كيفية الاستخدام (ARABIC):")
        print("="*80)
        print(result.get('how_to_use_ar', 'No instructions'))
        
        print("\n" + "="*80)
        print("✅ BILINGUAL DUA GENERATED SUCCESSFULLY!")
        print("="*80 + "\n")
        
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(response.text)
        
except requests.exceptions.ConnectionError:
    print('\n❌ Server not responding. Make sure server is running on http://127.0.0.1:8001')
except Exception as e:
    print(f'\n❌ Error: {e}')

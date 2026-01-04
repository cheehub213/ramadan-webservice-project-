#!/usr/bin/env python3
"""Comprehensive tests for the corrected Dua Generator endpoint"""

import requests
import json

BASE = "http://127.0.0.1:8001/api/v1"

print("\n" + "=" * 80)
print("🤲 DUA GENERATOR - COMPREHENSIVE TEST SUITE")
print("=" * 80)

# Test 1: Spiritual Problem
print("\n" + "=" * 80)
print("TEST 1: Spiritual Problem - Anger Management")
print("=" * 80)

payload1 = {
    'problem_description': 'I struggle with anger and impatience. I lose my temper easily and say hurtful words to my family. I want to be more patient like the Prophet.',
    'problem_category': 'Spiritual',
    'user_email': 'fatima@example.com',
    'user_name': 'Fatima',
    'language': 'English'
}

try:
    r1 = requests.post(f'{BASE}/dua/generate', json=payload1, timeout=30)
    if r1.status_code == 200:
        d1 = r1.json()
        print(f"✅ Status: {r1.status_code}")
        print(f"   User: {d1['user_name']}")
        print(f"   Category: {d1['problem_category']}")
        print(f"   Language: {d1['language']}")
        print(f"\n   DUA (EN):\n   {d1.get('dua_text_en','')}")
        print(f"\n   DUA (AR):\n   {d1.get('dua_text_ar','')}")
        print(f"\n   HOW TO USE (EN):\n   {d1.get('how_to_use_en','')}")
        print(f"\n   HOW TO USE (AR):\n   {d1.get('how_to_use_ar','')}")
    else:
        print(f"❌ Error: {r1.status_code} - {r1.text}")
except Exception as e:
    print(f"❌ Connection error: {e}")

# Test 2: Family Problem
print("\n" + "=" * 80)
print("TEST 2: Family Problem - Marriage Issues")
print("=" * 80)

payload2 = {
    'problem_description': 'My marriage is struggling. Communication has broken down and we barely talk anymore. I fear this might lead to separation.',
    'problem_category': 'Family',
    'user_email': 'ahmed@example.com',
    'user_name': 'Ahmed',
    'language': 'English'
}

try:
    r2 = requests.post(f'{BASE}/dua/generate', json=payload2, timeout=30)
    if r2.status_code == 200:
        d2 = r2.json()
        print(f"✅ Status: {r2.status_code}")
        print(f"   User: {d2['user_name']}")
        print(f"   Category: {d2['problem_category']}")
        print(f"\n   DUA (EN):\n   {d2.get('dua_text_en','')[:120]}...")
    else:
        print(f"❌ Error: {r2.status_code}")
except Exception as e:
    print(f"❌ Connection error: {e}")

# Test 3: Health Problem
print("\n" + "=" * 80)
print("TEST 3: Health Problem - Anxiety")
print("=" * 80)

payload3 = {
    'problem_description': 'I have been diagnosed with severe anxiety disorder. Medication helps but I am also seeking spiritual strength and comfort from Allah.',
    'problem_category': 'Health',
    'user_email': 'sara@example.com',
    'user_name': 'Sara',
    'language': 'English'
}

try:
    r3 = requests.post(f'{BASE}/dua/generate', json=payload3, timeout=30)
    if r3.status_code == 200:
        d3 = r3.json()
        print(f"✅ Status: {r3.status_code}")
        print(f"   User: {d3['user_name']}")
        print(f"   Category: {d3['problem_category']}")
        print(f"\n   DUA (EN):\n   {d3.get('dua_text_en','')[:120]}...")
    else:
        print(f"❌ Error: {r3.status_code}")
except Exception as e:
    print(f"❌ Connection error: {e}")

# Test 4: Get Categories
print("\n" + "=" * 80)
print("TEST 4: Available Problem Categories")
print("=" * 80)

try:
    r4 = requests.get(f'{BASE}/dua/categories', timeout=10)
    if r4.status_code == 200:
        cats = r4.json()
        print(f"✅ Found {len(cats)} problem categories:")
        for cat in cats:
            print(f"   • {cat['name']}: {cat['description']}")
    else:
        print(f"❌ Error: {r4.status_code}")
except Exception as e:
    print(f"❌ Connection error: {e}")

# Test 5: Get History
print("\n" + "=" * 80)
print("TEST 5: User's Dua History")
print("=" * 80)

try:
    r5 = requests.get(f'{BASE}/dua/history/fatima@example.com', timeout=10)
    if r5.status_code == 200:
        history = r5.json()
        print(f"✅ Found {len(history)} dua requests for fatima@example.com:")
        for h in history[:3]:
            print(f"   • ID {h['id']}: {h['problem_description'][:50]}...")
    else:
        print(f"❌ Error: {r5.status_code}")
except Exception as e:
    print(f"❌ Connection error: {e}")

# Test 6: Submit Feedback
print("\n" + "=" * 80)
print("TEST 6: Submit Feedback on Dua")
print("=" * 80)

payload6 = {
    'dua_request_id': 1,
    'is_helpful': 'yes',
    'feedback': 'This dua helped me feel peaceful. I recite it daily.'
}

try:
    r6 = requests.post(f'{BASE}/dua/feedback', json=payload6, timeout=10)
    if r6.status_code == 200:
        print(f"✅ Feedback submitted successfully")
        feedback = r6.json()
        print(f"   Status: {feedback.get('message', 'Recorded')}")
    else:
        print(f"❌ Error: {r6.status_code}")
except Exception as e:
    print(f"❌ Connection error: {e}")

# Test 7: Get Statistics
print("\n" + "=" * 80)
print("TEST 7: Dua Helpfulness Statistics")
print("=" * 80)

try:
    r7 = requests.get(f'{BASE}/dua/stats/helpful', timeout=10)
    if r7.status_code == 200:
        stats = r7.json()
        print(f"✅ Dua Statistics:")
        print(f"   Total Requests: {stats.get('total_requests', 0)}")
        print(f"   Helpful: {stats.get('helpful_count', 0)}")
        print(f"   Not Helpful: {stats.get('not_helpful_count', 0)}")
        if stats.get('total_requests', 0) > 0:
            print(f"   Helpfulness Rate: {stats.get('helpful_percentage', 0):.1f}%")
    else:
        print(f"❌ Error: {r7.status_code}")
except Exception as e:
    print(f"❌ Connection error: {e}")

print("\n" + "=" * 80)
print("✅ ALL TESTS COMPLETE")
print("=" * 80)
print("\n📚 API Documentation: http://127.0.0.1:8001/docs")
print("🔍 Problems should use Search endpoint for Quranic verses & Hadiths\n")

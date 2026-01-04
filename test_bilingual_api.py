"""
Test script for the bilingual Ramadan API with explanations
Tests Arabic prompts, English prompts, and bilingual responses
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8001"

def print_response(title: str, response: Dict[Any, Any]):
    """Pretty print API response"""
    print("\n" + "="*80)
    print(f"✓ {title}")
    print("="*80)
    print(json.dumps(response, ensure_ascii=False, indent=2))

def test_english_prompt_bilingual():
    """Test 1: English prompt with bilingual response"""
    payload = {
        "prompt": "I'm feeling very tired and weak during fasting in Ramadan. My body is exhausted and I'm struggling to focus on prayer.",
        "response_language": "bilingual",
        "include_hadith": True,
        "include_quran": True
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/search/answer", json=payload)
    return response.json()

def test_arabic_prompt_arabic_response():
    """Test 2: Arabic prompt with Arabic response"""
    payload = {
        "prompt": "أشعر بالضعف والإرهاق أثناء الصيام في رمضان. جسدي متعب جداً وأنا أكافح للتركيز على الصلاة.",
        "response_language": "ar",
        "include_hadith": True,
        "include_quran": True
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/search/answer", json=payload)
    return response.json()

def test_arabic_prompt_english_response():
    """Test 3: Arabic prompt with English response"""
    payload = {
        "prompt": "أنا أعاني من الشكوك في إيماني وأسأل نفسي عن معتقداتي.",
        "response_language": "en",
        "include_hadith": True,
        "include_quran": True
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/search/answer", json=payload)
    return response.json()

def test_family_conflict_bilingual():
    """Test 4: Family conflict scenario with bilingual response"""
    payload = {
        "prompt": "أفراد عائلتي يختلفون حول تفسيرات مختلفة للممارسات الإسلامية في رمضان. هناك توتر في المنزل.",
        "response_language": "bilingual",
        "include_hadith": True,
        "include_quran": True
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/search/answer", json=payload)
    return response.json()

def test_grief_english_response():
    """Test 5: Grief scenario with English response only"""
    payload = {
        "prompt": "I lost a loved one recently and I'm grieving during Ramadan. I'm finding it hard to concentrate on worship.",
        "response_language": "en",
        "include_hadith": True,
        "include_quran": True
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/search/answer", json=payload)
    return response.json()

def test_quran_search_bilingual():
    """Test 6: Direct Quran search with bilingual response"""
    params = {
        "keywords": "patience,strength",
        "response_language": "bilingual",
        "limit": 3
    }
    
    response = requests.get(f"{BASE_URL}/api/v1/search/quran", params=params)
    return response.json()

def test_hadith_search_bilingual():
    """Test 7: Direct Hadith search with bilingual response"""
    params = {
        "keywords": "patience,forbearance",
        "response_language": "bilingual",
        "limit": 3
    }
    
    response = requests.get(f"{BASE_URL}/api/v1/search/hadith", params=params)
    return response.json()

def test_work_financial_concern():
    """Test 8: Work/financial concern with explanations"""
    payload = {
        "prompt": "I lost my job during Ramadan and I'm worried about providing for my family. I'm anxious about the future.",
        "response_language": "bilingual",
        "include_hadith": True,
        "include_quran": True
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/search/answer", json=payload)
    return response.json()

def test_moral_dilemma():
    """Test 9: Moral/ethical dilemma"""
    payload = {
        "prompt": "زميل في العمل يطلب مني المساومة على نزاهتي. أنا غير متأكد ما إذا كان يجب أن أرفض.",
        "response_language": "bilingual",
        "include_hadith": True,
        "include_quran": True
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/search/answer", json=payload)
    return response.json()

def test_social_pressure():
    """Test 10: Social pressure scenario"""
    payload = {
        "prompt": "My friends are pressuring me to skip fasting and join them. I want to be a good friend but maintain my faith.",
        "response_language": "bilingual",
        "include_hadith": True,
        "include_quran": True
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/search/answer", json=payload)
    return response.json()

def main():
    print("\n" + "="*80)
    print("RAMADAN DECISION-MAKING API - COMPREHENSIVE TEST SUITE")
    print("="*80)
    print("\nTesting bilingual support, Arabic language, and explanation generation")
    print(f"Base URL: {BASE_URL}\n")
    
    tests = [
        ("Test 1: English Prompt → Bilingual Response", test_english_prompt_bilingual),
        ("Test 2: Arabic Prompt → Arabic Response", test_arabic_prompt_arabic_response),
        ("Test 3: Arabic Prompt → English Response", test_arabic_prompt_english_response),
        ("Test 4: Family Conflict (Arabic) → Bilingual", test_family_conflict_bilingual),
        ("Test 5: Grief (English) → English Response", test_grief_english_response),
        ("Test 6: Direct Quran Search → Bilingual", test_quran_search_bilingual),
        ("Test 7: Direct Hadith Search → Bilingual", test_hadith_search_bilingual),
        ("Test 8: Work/Financial Concern → Bilingual", test_work_financial_concern),
        ("Test 9: Moral Dilemma (Arabic) → Bilingual", test_moral_dilemma),
        ("Test 10: Social Pressure → Bilingual", test_social_pressure),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            print(f"\nRunning: {test_name}")
            result = test_func()
            print_response(test_name, result)
            results.append((test_name, "PASSED"))
        except Exception as e:
            print(f"\n✗ {test_name}")
            print(f"Error: {str(e)}")
            results.append((test_name, "FAILED"))
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    for test_name, status in results:
        symbol = "✓" if status == "PASSED" else "✗"
        print(f"{symbol} {test_name}: {status}")
    
    passed = sum(1 for _, status in results if status == "PASSED")
    print(f"\nTotal: {passed}/{len(results)} tests passed")

if __name__ == "__main__":
    main()

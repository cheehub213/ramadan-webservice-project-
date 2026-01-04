#!/usr/bin/env python3
"""
Test script to register new imams and test the endpoints
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8001/api/v1/imam"

def test_list_imams():
    """Test GET /api/v1/imam/imams"""
    print("\n" + "="*60)
    print("1. GET - List All Imams")
    print("="*60)
    response = requests.get(f"{BASE_URL}/imams")
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Number of imams: {len(data)}")
    if data:
        print("Imams found:")
        for imam in data:
            print(f"  - {imam['id']}: {imam['name']} ({imam['madhab']})")
    else:
        print("No imams found yet")
    return response.status_code == 200

def test_register_imam(imam_data):
    """Test POST /api/v1/imam/imams"""
    print("\n" + "="*60)
    print(f"2. POST - Register New Imam: {imam_data['name']}")
    print("="*60)
    response = requests.post(f"{BASE_URL}/imams", json=imam_data)
    print(f"Status Code: {response.status_code}")
    if response.status_code in [200, 201]:
        imam = response.json()
        print(f"[SUCCESS] Imam registered successfully!")
        print(f"  ID: {imam['id']}")
        print(f"  Name: {imam['name']}")
        print(f"  Email: {imam['email']}")
        print(f"  Rating: {imam['average_rating']}")
        return imam
    else:
        print(f"[ERROR] {response.text}")
        return None

def test_get_imam(imam_id):
    """Test GET /api/v1/imam/imams/{imam_id}"""
    print("\n" + "="*60)
    print(f"3. GET - Get Imam Details (ID: {imam_id})")
    print("="*60)
    response = requests.get(f"{BASE_URL}/imams/{imam_id}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        imam = response.json()
        print(f"[SUCCESS] Imam retrieved successfully!")
        print(f"  Name: {imam['name']}")
        print(f"  Title: {imam.get('title', 'N/A')}")
        print(f"  Madhab: {imam.get('madhab', 'N/A')}")
        print(f"  Specializations: {imam['specializations']}")
        print(f"  Consultation Fee: ${imam['consultation_fee']}")
        print(f"  Available: {imam['is_available']}")
        return imam
    else:
        print(f"[ERROR] {response.text}")
        return None

def test_filter_imams(filter_param, filter_value):
    """Test GET /api/v1/imam/imams with filters"""
    print("\n" + "="*60)
    print(f"4. GET - Filter Imams by {filter_param}: {filter_value}")
    print("="*60)
    response = requests.get(f"{BASE_URL}/imams", params={filter_param: filter_value})
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        imams = response.json()
        print(f"[SUCCESS] Found {len(imams)} imam(s) matching filter")
        for imam in imams:
            print(f"  - {imam['name']} ({imam.get('madhab', 'N/A')})")
        return True
    else:
        print(f"[ERROR] {response.text}")
        return False

def main():
    print("\n" + "="*70)
    print("[IMAM REGISTRATION SYSTEM TEST]")
    print("="*70)
    
    # Test 1: List imams (should be empty initially)
    test_list_imams()
    
    # Test 2: Register first imam
    imam1 = {
        "name": "Dr. Mohammad Ahmed Hassan",
        "title": "Mufti",
        "specializations": "general,fiqh,madhab",
        "madhab": "Hanafi",
        "bio": "Dr. Mohammad Ahmed Hassan is a respected Islamic scholar with 20 years of experience.",
        "years_experience": 20,
        "qualifications": "Masters in Islamic Studies from Al-Azhar University",
        "email": "dr.ahmad@islamicguidance.com",
        "phone": "+1-555-0100",
        "website": "https://dr-ahmad.example.com",
        "consultation_methods": "phone,email,video",
        "consultation_fee": 50.0,
        "currency": "USD",
        "languages": "English,Arabic,Urdu",
        "timezone": "EST",
        "is_available": True
    }
    registered_imam1 = test_register_imam(imam1)
    
    # Test 3: Register second imam
    imam2 = {
        "name": "Shaikh Abdullah Hassan",
        "specializations": "family,youth",
        "madhab": "Maliki",
        "email": "shaikh.abdullah@example.com",
        "consultation_methods": "phone,video",
        "languages": "English,Arabic",
        "years_experience": 15,
        "consultation_fee": 40.0
    }
    registered_imam2 = test_register_imam(imam2)
    
    # Test 4: Register third imam
    imam3 = {
        "name": "Dr. Karim Al-Rashid",
        "title": "Dr.",
        "specializations": "business,fiqh",
        "madhab": "Shafi'i",
        "email": "dr.karim@business.com",
        "consultation_methods": "email,video",
        "languages": "English,Arabic,Malay",
        "consultation_fee": 75.0
    }
    registered_imam3 = test_register_imam(imam3)
    
    # Test 5: List all imams again
    test_list_imams()
    
    # Test 6: Get specific imam details
    if registered_imam1:
        test_get_imam(registered_imam1['id'])
    
    # Test 7: Filter by specialization
    test_filter_imams("specialization", "family")
    
    # Test 8: Filter by madhab
    test_filter_imams("madhab", "Hanafi")
    
    # Test 9: Try to register duplicate email (should fail)
    print("\n" + "="*60)
    print("5. POST - Test Duplicate Email (Should Fail)")
    print("="*60)
    response = requests.post(f"{BASE_URL}/imams", json=imam1)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 400:
        print("[SUCCESS] Correctly rejected duplicate email")
        print(f"  Error: {response.json()['detail']}")
    else:
        print("[FAIL] Should have rejected duplicate email")
    
    print("\n" + "="*70)
    print("[TESTS COMPLETE]")
    print("="*70)

if __name__ == "__main__":
    main()

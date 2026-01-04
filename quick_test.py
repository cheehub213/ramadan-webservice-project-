import requests
import json

BASE_URL = "http://127.0.0.1:8001/api/v1/imam"

print("Testing Imam Registration Endpoint...")
print("=" * 60)

# Test 1: List imams (should be empty)
print("\nTest 1: GET /imams")
try:
    resp = requests.get(f"{BASE_URL}/imams", timeout=5)
    print(f"Status: {resp.status_code}")
    data = resp.json()
    print(f"Imams in DB: {len(data)}")
except Exception as e:
    print(f"ERROR: {e}")

# Test 2: Register an imam
print("\nTest 2: POST /imams (Register)")
imam_data = {
    "name": "Dr. Mohammad Ahmed Hassan",
    "title": "Mufti",
    "specializations": "general,fiqh,madhab",
    "madhab": "Hanafi",
    "email": "dr.ahmad@test.com",
    "consultation_methods": "phone,email,video",
    "languages": "English,Arabic,Urdu",
    "consultation_fee": 50.0
}

try:
    resp = requests.post(f"{BASE_URL}/imams", json=imam_data, timeout=5)
    print(f"Status: {resp.status_code}")
    if resp.status_code in [200, 201]:
        imam = resp.json()
        print(f"SUCCESS - Imam ID: {imam['id']}, Name: {imam['name']}")
    else:
        print(f"FAILED - {resp.text}")
except Exception as e:
    print(f"ERROR: {e}")

# Test 3: List imams again
print("\nTest 3: GET /imams (Check registration)")
try:
    resp = requests.get(f"{BASE_URL}/imams", timeout=5)
    print(f"Status: {resp.status_code}")
    data = resp.json()
    print(f"Imams in DB: {len(data)}")
    if data:
        for imam in data:
            print(f"  - ID {imam['id']}: {imam['name']} ({imam['madhab']})")
except Exception as e:
    print(f"ERROR: {e}")

print("\nDone!")

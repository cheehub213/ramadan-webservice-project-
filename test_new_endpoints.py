#!/usr/bin/env python3
"""
Test script for Chat and Dua endpoints
Run after starting the server: python test_new_endpoints.py
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8001/api/v1"

def test_dua_categories():
    """Test getting dua categories"""
    print("\n" + "="*60)
    print("TEST 1: Get Dua Categories")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/dua/categories")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {len(data)} categories:")
        for cat in data:
            print(f"  - {cat['name']}: {cat['description']}")
        return True
    else:
        print(f"❌ Error: {response.text}")
        return False

def test_create_chat():
    """Test creating a chat conversation"""
    print("\n" + "="*60)
    print("TEST 2: Create Chat Conversation")
    print("="*60)
    
    payload = {
        "imam_id": 1,
        "user_email": "user@example.com",
        "user_name": "Ahmed Ali",
        "title": "Marriage Advice",
        "description": "I need help with marriage communication"
    }
    
    response = requests.post(f"{BASE_URL}/chat/conversations", json=payload)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Chat Created!")
        print(f"  Chat ID: {data.get('id')}")
        print(f"  Imam ID: {data.get('imam_id')}")
        print(f"  User: {data.get('user_name')}")
        return data.get('id')
    else:
        print(f"❌ Error: {response.text}")
        return None

def test_send_message(chat_id):
    """Test sending a message"""
    print("\n" + "="*60)
    print("TEST 3: Send Message in Chat")
    print("="*60)
    
    payload = {
        "message": "How can I improve communication with my spouse?",
        "sender_type": "user",
        "sender_id": "user@example.com",
        "sender_name": "Ahmed Ali"
    }
    
    response = requests.post(
        f"{BASE_URL}/chat/conversations/{chat_id}/messages",
        json=payload
    )
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Message Sent!")
        print(f"  Message ID: {data.get('id')}")
        print(f"  Content: {data.get('message')[:50]}...")
        return True
    else:
        print(f"❌ Error: {response.text}")
        return False

def test_get_chat(chat_id):
    """Test retrieving chat details"""
    print("\n" + "="*60)
    print("TEST 4: Get Chat Details")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/chat/conversations/{chat_id}")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Chat Retrieved!")
        print(f"  Title: {data.get('title')}")
        print(f"  Messages: {data.get('message_count')}")
        print(f"  Unread: {data.get('unread_count')}")
        return True
    else:
        print(f"❌ Error: {response.text}")
        return False

def test_update_imam_availability():
    """Test updating imam availability"""
    print("\n" + "="*60)
    print("TEST 5: Update Imam Availability")
    print("="*60)
    
    payload = {
        "is_online": True,
        "is_available_for_chat": True
    }
    
    response = requests.put(
        f"{BASE_URL}/chat/imam/1/availability",
        json=payload
    )
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Availability Updated!")
        print(f"  Online: {data.get('is_online')}")
        print(f"  Available: {data.get('is_available_for_chat')}")
        return True
    else:
        print(f"❌ Error: {response.text}")
        return False

def test_user_chats():
    """Test getting user's chats"""
    print("\n" + "="*60)
    print("TEST 6: Get User's Chats")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/chat/conversations/user/user@example.com")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ User Chats Retrieved!")
        print(f"  Total Chats: {len(data)}")
        for chat in data:
            print(f"  - {chat.get('title')} (ID: {chat.get('id')})")
        return True
    else:
        print(f"❌ Error: {response.text}")
        return False

def test_health_check():
    """Test health endpoint"""
    print("\n" + "="*60)
    print("TEST 0: Health Check")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Server Running!")
        print(f"  Status: {data.get('status')}")
        print(f"  Database: {data.get('database')}")
        return True
    else:
        print(f"⚠️  Health check failed: {response.text}")
        return False

if __name__ == "__main__":
    print("\n🚀 Testing Chat & Dua Generator Endpoints\n")
    
    # Wait for server
    print("⏳ Waiting for server to be ready...")
    for i in range(10):
        try:
            requests.get(f"{BASE_URL}/health", timeout=1)
            print("✅ Server is ready!")
            break
        except:
            print(f"  Attempt {i+1}/10...", end="\r")
            time.sleep(0.5)
    
    # Run tests
    test_health_check()
    
    if test_dua_categories():
        chat_id = test_create_chat()
        
        if chat_id:
            test_send_message(chat_id)
            test_get_chat(chat_id)
            test_user_chats()
        
        test_update_imam_availability()
    
    print("\n" + "="*60)
    print("✅ All Tests Complete!")
    print("="*60)
    print("\n📚 Access API Documentation:")
    print("   Swagger UI: http://127.0.0.1:8001/docs")
    print("   ReDoc: http://127.0.0.1:8001/redoc")
    print("\n")

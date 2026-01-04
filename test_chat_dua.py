#!/usr/bin/env python3
"""
Test script for Live Chat and Dua Generator features
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8001/api/v1"

def test_chat_system():
    print("\n" + "="*70)
    print("TESTING LIVE CHAT SYSTEM")
    print("="*70)
    
    # 1. Start a chat
    print("\n[1] Starting a new chat with Imam #1...")
    chat_data = {
        "imam_id": 1,
        "user_email": "ahmad@example.com",
        "user_name": "Ahmad",
        "title": "Marriage Communication",
        "description": "I'm having trouble communicating with my wife about finances"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/chat/conversations", json=chat_data, timeout=5)
        if response.status_code == 200:
            chat = response.json()
            chat_id = chat['id']
            print(f"SUCCESS - Chat created with ID: {chat_id}")
            print(f"  Imam ID: {chat['imam_id']}")
            print(f"  User: {chat['user_name']} ({chat['user_email']})")
            print(f"  Title: {chat['title']}")
        else:
            print(f"FAILED - Status {response.status_code}: {response.text}")
            return
    except Exception as e:
        print(f"ERROR: {e}")
        return
    
    # 2. Send a user message
    print("\n[2] Sending a message from user...")
    message_data = {
        "message": "We argue every time we discuss money. I don't know how to approach it without causing conflict.",
        "sender_type": "user",
        "sender_id": "ahmad@example.com",
        "sender_name": "Ahmad"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat/conversations/{chat_id}/messages",
            json=message_data,
            timeout=5
        )
        if response.status_code == 200:
            msg = response.json()
            print(f"SUCCESS - Message sent")
            print(f"  Message ID: {msg['id']}")
            print(f"  Sent at: {msg['created_at']}")
        else:
            print(f"FAILED - {response.text}")
    except Exception as e:
        print(f"ERROR: {e}")
    
    # 3. Simulate imam response
    print("\n[3] Imam responds to the message...")
    imam_message = {
        "message": "Based on Islamic teachings, financial transparency is important in marriage. I recommend...",
        "sender_type": "imam",
        "sender_id": "1",
        "sender_name": "Dr. Mohammad Ahmed Hassan"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/chat/conversations/{chat_id}/messages",
            json=imam_message,
            timeout=5
        )
        if response.status_code == 200:
            print(f"SUCCESS - Imam response sent")
        else:
            print(f"FAILED - {response.text}")
    except Exception as e:
        print(f"ERROR: {e}")
    
    # 4. Get full chat history
    print("\n[4] Retrieving full chat history...")
    try:
        response = requests.get(f"{BASE_URL}/chat/conversations/{chat_id}", timeout=5)
        if response.status_code == 200:
            chat_detail = response.json()
            print(f"SUCCESS - Chat retrieved")
            print(f"  Messages in chat: {len(chat_detail['messages'])}")
            print(f"  Unread count: {chat_detail['unread_count']}")
            print(f"  Is active: {chat_detail['is_active']}")
            print(f"  Imam available: {chat_detail['imam_is_available']}")
        else:
            print(f"FAILED - {response.text}")
    except Exception as e:
        print(f"ERROR: {e}")
    
    # 5. Update imam availability
    print("\n[5] Setting imam as online and available...")
    availability = {
        "is_online": True,
        "is_available_for_chat": True
    }
    
    try:
        response = requests.put(
            f"{BASE_URL}/chat/imam/1/availability",
            json=availability,
            timeout=5
        )
        if response.status_code == 200:
            avail = response.json()
            print(f"SUCCESS - Imam status updated")
            print(f"  Online: {avail['is_online']}")
            print(f"  Available for chat: {avail['is_available_for_chat']}")
        else:
            print(f"FAILED - {response.text}")
    except Exception as e:
        print(f"ERROR: {e}")
    
    # 6. Get user's chats
    print("\n[6] Getting all chats for user...")
    try:
        response = requests.get(
            f"{BASE_URL}/chat/conversations/user/ahmad@example.com",
            timeout=5
        )
        if response.status_code == 200:
            chats = response.json()
            print(f"SUCCESS - Found {len(chats)} chat(s)")
            for c in chats:
                print(f"  - Chat #{c['id']}: {c['title']} (Imam: {c['imam_id']})")
        else:
            print(f"FAILED - {response.text}")
    except Exception as e:
        print(f"ERROR: {e}")


def test_dua_generator():
    print("\n" + "="*70)
    print("TESTING PERSONALIZED DUA GENERATOR")
    print("="*70)
    
    # 1. Get categories
    print("\n[1] Getting dua problem categories...")
    try:
        response = requests.get(f"{BASE_URL}/dua/categories", timeout=5)
        if response.status_code == 200:
            categories = response.json()
            print(f"SUCCESS - Found {len(categories)} categories:")
            for cat in categories:
                print(f"  - {cat['name']}: {cat['description']}")
        else:
            print(f"FAILED - {response.text}")
    except Exception as e:
        print(f"ERROR: {e}")
    
    # 2. Generate personalized dua
    print("\n[2] Generating personalized dua for a user problem...")
    dua_request = {
        "problem_description": "I'm struggling with anger and impatience. I lose my temper easily and regret my words. I want to improve my character.",
        "problem_category": "Spiritual",
        "user_email": "user@example.com",
        "user_name": "Ahmed",
        "language": "English"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/dua/generate", json=dua_request, timeout=15)
        if response.status_code == 200:
            dua = response.json()
            print(f"SUCCESS - Dua generated!")
            print(f"  ID: {dua['id']}")
            print(f"\n  QURANIC VERSE (AYA):")
            print(f"  {dua['generated_aya'][:200]}...")
            print(f"\n  HADITH:")
            print(f"  {dua['generated_hadith'][:200]}...")
            print(f"\n  PERSONALIZED DUA:")
            print(f"  {dua['generated_dua'][:200]}...")
        else:
            print(f"FAILED - {response.text}")
    except Exception as e:
        print(f"ERROR: {e}")
    
    # 3. Submit feedback
    print("\n[3] Submitting feedback on the dua...")
    feedback = {
        "dua_request_id": 1,
        "is_helpful": "yes",
        "feedback": "This dua really helped me feel calmer. I've been reciting it daily."
    }
    
    try:
        response = requests.post(f"{BASE_URL}/dua/feedback", json=feedback, timeout=5)
        if response.status_code == 200:
            result = response.json()
            print(f"SUCCESS - {result['message']}")
        else:
            print(f"FAILED - {response.text}")
    except Exception as e:
        print(f"ERROR: {e}")
    
    # 4. Get user's dua history
    print("\n[4] Getting user's dua history...")
    try:
        response = requests.get(
            f"{BASE_URL}/dua/history/user@example.com?limit=5",
            timeout=5
        )
        if response.status_code == 200:
            history = response.json()
            print(f"SUCCESS - Found {len(history)} dua request(s)")
            for h in history:
                print(f"  - Problem: {h['problem_description'][:50]}...")
                print(f"    Category: {h['problem_category']}")
                print(f"    Helpful: {h['is_helpful']}")
        else:
            print(f"FAILED - {response.text}")
    except Exception as e:
        print(f"ERROR: {e}")
    
    # 5. Get helpfulness statistics
    print("\n[5] Getting dua helpfulness statistics...")
    try:
        response = requests.get(f"{BASE_URL}/dua/stats/helpful", timeout=5)
        if response.status_code == 200:
            stats = response.json()
            print(f"SUCCESS - Statistics:")
            print(f"  Total requests: {stats['total_requests']}")
            print(f"  Marked helpful: {stats['helpful']}")
            print(f"  Not helpful: {stats['not_helpful']}")
            print(f"  Helpfulness rate: {stats['helpful_percentage']}%")
        else:
            print(f"FAILED - {response.text}")
    except Exception as e:
        print(f"ERROR: {e}")


def main():
    print("\n" + "="*70)
    print("CHAT & DUA GENERATOR TEST SUITE")
    print("="*70)
    print("\nTesting new features:")
    print("1. Live Chat System with Imams")
    print("2. Personalized Dua Generator")
    
    test_chat_system()
    test_dua_generator()
    
    print("\n" + "="*70)
    print("TESTS COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()

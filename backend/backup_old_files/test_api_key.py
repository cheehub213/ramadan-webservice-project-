import os
from dotenv import load_dotenv
import asyncio

# Load env
load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")
print(f"API Key loaded: {bool(api_key)}")
if api_key:
    print(f"Key starts with: {api_key[:20]}...")

# Test the async function directly
from services_dua import DuaService

async def test_ai():
    print("\nTesting AI dua generation...")
    result = await DuaService.generate_dua_with_ai("Fear & Anxiety", "I fear going to hell")
    print(f"AI Generated: {result.get('ai_generated')}")
    print(f"Dua: {result.get('dua_text_en', '')[:200]}")

asyncio.run(test_ai())

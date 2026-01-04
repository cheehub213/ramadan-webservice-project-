from services_dua import DEEPSEEK_API_KEY

if DEEPSEEK_API_KEY:
    print(f"API Key loaded: {DEEPSEEK_API_KEY[:40]}...")
else:
    print("API Key NOT loaded")

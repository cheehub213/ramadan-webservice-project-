import requests

api_key = "YOUR_GROQ_API_KEY_HERE"

headers = {
    "Authorization": f"Bearer {api_key}"
}

print("Fetching available Groq models...")
response = requests.get("https://api.groq.com/openai/v1/models", headers=headers, timeout=10)

print(f"Status: {response.status_code}")
if response.status_code == 200:
    models = response.json()
    print(f"Available models:")
    for model in models.get("data", []):
        print(f"  - {model['id']}")
else:
    print(f"Error: {response.text}")


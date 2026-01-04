import requests

api_key = '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'
headers = {'Authorization': f'Bearer {api_key}'}

response = requests.get('https://openrouter.io/api/v1/chat/completions', headers=headers, timeout=5)
print(f'GET Status: {response.status_code}')
print(f'Content-Type: {response.headers.get("Content-Type")}')
print(f'Response length: {len(response.text)}')
print(f'Response:\n{response.text}')

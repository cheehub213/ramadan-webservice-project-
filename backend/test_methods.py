import requests

api_key = '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'
headers = {'Authorization': f'Bearer {api_key}'}

print("Testing HTTP methods with OpenRouter...\n")

# Try GET
response = requests.get('https://openrouter.io/api/v1/chat/completions', headers=headers, timeout=5)
print(f'GET Status: {response.status_code}')

# Try OPTIONS  
response = requests.options('https://openrouter.io/api/v1/chat/completions', headers=headers, timeout=5)
print(f'OPTIONS Status: {response.status_code}')
if 'Allow' in response.headers:
    print(f'Allow header: {response.headers["Allow"]}')
else:
    print('No Allow header in response')

# Try HEAD
response = requests.head('https://openrouter.io/api/v1/chat/completions', headers=headers, timeout=5)
print(f'HEAD Status: {response.status_code}')

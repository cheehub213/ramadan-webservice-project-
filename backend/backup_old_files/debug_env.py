import os
from pathlib import Path
from dotenv import load_dotenv

# Check the env file
env_file = Path(__file__).parent / ".env"
print(f"Env file exists: {env_file.exists()}")
print(f"Env file path: {env_file}")

# Try manual reading
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            if "DEEPSEEK" in line:
                print(f"Found in file: {line.strip()[:60]}")

# Try load_dotenv
result = load_dotenv(env_file)
print(f"load_dotenv returned: {result}")
key = os.getenv("DEEPSEEK_API_KEY")
print(f"API Key from getenv: {key[:30] if key else 'None'}...")

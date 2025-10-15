import os
import requests
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"

def list_available_models():
    if not GEMINI_API_KEY:
        print("GEMINI_API_KEY not found. Please set it in your .env file.")
        return

    url = f"{BASE_URL}?key={GEMINI_API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error fetching models: {response.status_code}")
        print(response.text)
        return

    data = response.json()
    print("\n Available Gemini Models:\n")
    for model in data.get("models", []):
        print(f"- {model['name']} ({model.get('displayName', 'No display name')})")

if __name__ == "__main__":
    list_available_models()

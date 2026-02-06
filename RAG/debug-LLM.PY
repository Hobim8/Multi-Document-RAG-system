import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configure
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Test 1: List available models
print("=== AVAILABLE MODELS ===")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

print("\n=== TESTING MODEL ===")
# Test 2: Try to use a model
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("Say hello")
print(response.text)
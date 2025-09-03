import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Get the Gemini API key from the environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("Gemini API Key not found. Please set it in your .env file.")

print("Gemini API Key loaded successfully.")
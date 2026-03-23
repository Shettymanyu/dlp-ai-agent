import os
from dotenv import load_dotenv

# 1. Ye command .env file ke saare variables ko system memory mein load karti hai
load_dotenv()

class Config:
    # 2. .env se 'OPENAI_API_KEY' uthao, agar nahi milti toh None rakho
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # 3. PDF file ka path (Jo aapke 'data' folder mein hai)
    PDF_PATH = os.getenv("PDF_PATH", "data/dlp_document.pdf")
    
    # 4. Model name jo aap use karna chahte hain
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

    # Error handling: Check karein ki key load hui ya nahi
    if not OPENAI_API_KEY:
        print("⚠️ Warning: OPENAI_API_KEY nahi mili! Apni .env file check karein.")
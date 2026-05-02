import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Get API key from .env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)


# -------------------------
# TEXT MODEL
# -------------------------
def chat_completion(prompt: str):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


# -------------------------
# OCR / VISION MODEL
# -------------------------
def vision_ocr(image_base64: str):
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Analyze this image. Tell if it is a car image with confidence (0-1), and extract any visible text."
                    },
                    {
                        "type": "image_url",
                        "image_url": image_base64
                    }
                ]
            }
        ]
    )
    return response.choices[0].message.content
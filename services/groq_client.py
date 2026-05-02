from groq import Groq

client = Groq(api_key="YOUR_GROQ_API_KEY")

def chat_completion(prompt):
    return client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    ).choices[0].message.content


def vision_ocr(image_base64):
    # Groq multimodal vision model
    response = client.chat.completions.create(
        model="llama-3.2-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Is this a car image? Give confidence 0-1 and extract text."},
                    {"type": "image_url", "image_url": image_base64}
                ]
            }
        ]
    )
    return response.choices[0].message.content
from services.groq_client import vision_ocr

def analyze_image(image_base64):
    result = vision_ocr(image_base64)

    # simulate parsing
    return {
        "raw": result,
        "car_detected": "car" in result.lower(),
        "confidence": 0.87  # parsed from model output ideally
    }
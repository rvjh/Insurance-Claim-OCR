def decide(text_valid, image_result):
    if not text_valid:
        return False, "Text validation failed"

    if not image_result["car_detected"]:
        return False, "No car detected in image"

    if image_result["confidence"] < 0.75:
        return False, "Low confidence in car detection"

    return True, "Claim Successful. Your claim will be deposited within 15 days."
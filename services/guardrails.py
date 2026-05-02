def validate_text(text: str):
    errors = []

    if len(text.strip()) < 20:
        errors.append("Text too short")

    if "policy" not in text.lower():
        errors.append("Missing policy number")

    if "name" not in text.lower():
        errors.append("Missing name")

    if "date" not in text.lower():
        errors.append("Missing accident date")

    return len(errors) == 0, errors


def is_safe_output(text: str):
    banned = ["sexual", "violence", "abuse"]
    return not any(b in text.lower() for b in banned)   
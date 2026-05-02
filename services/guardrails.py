import re

def validate_text(text: str):
    errors = []

    if len(text) > 100:
        errors.append("Text exceeds 100 characters")

    if "policy" not in text.lower():
        errors.append("Missing policy number")

    if "name" not in text.lower():
        errors.append("Missing user name")

    if "date" not in text.lower():
        errors.append("Missing accident date")

    return len(errors) == 0, errors


def is_safe_output(text: str):
    banned_keywords = ["sexual", "violence", "abuse"]
    return not any(k in text.lower() for k in banned_keywords)
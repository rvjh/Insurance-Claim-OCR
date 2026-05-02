from fastapi import FastAPI, UploadFile, File, Form
import base64
import time

from sqlalchemy import text as sql_text

from db.database import SessionLocal, init_db
from services.groq_client import vision_ocr
from services.guardrails import validate_text, is_safe_output


app = FastAPI()
init_db()


@app.post("/claim")
async def process_claim(
    user_id: int = Form(...),
    claim_text: str = Form(...),   # ✅ MUST MATCH CURL
    image: UploadFile = File(...)
):

    timings = {}

    # -------------------------
    # STEP 1: TEXT VALIDATION
    # -------------------------
    t1 = time.time()
    valid, errors = validate_text(claim_text)
    t2 = time.time()
    timings["text_validation"] = round(t2 - t1, 3)

    if not valid:
        return {
            "status": False,
            "message": "Invalid text input",
            "errors": errors
        }

    # -------------------------
    # STEP 2: IMAGE PROCESSING
    # -------------------------
    t3 = time.time()

    img_bytes = await image.read()
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")

    vision_result = vision_ocr(img_base64)

    t4 = time.time()
    timings["vision"] = round(t4 - t3, 3)

    # -------------------------
    # SIMPLE DECISION ENGINE
    # -------------------------
    car_detected = "car" in vision_result.lower()
    confidence = 0.93 if car_detected else 0.30

    t5 = time.time()

    if car_detected and confidence > 0.75:
        status = True
        message = "Claim Successful. Your claim will be deposited within 15 days."
    else:
        status = False
        message = "Claim Rejected. No valid car evidence found."

    t6 = time.time()
    timings["decision"] = round(t6 - t5, 3)

    # -------------------------
    # SAFETY CHECK
    # -------------------------
    if not is_safe_output(message):
        status = False
        message = "Blocked due to safety policy"

    # -------------------------
    # DATABASE LOGGING
    # -------------------------
    db = SessionLocal()

    db.execute(
        sql_text("""
            INSERT INTO claim_logs
            (user_id, text_input, image_confidence, car_detected, status, response_message, step_timings)
            VALUES
            (:user_id, :text_input, :image_confidence, :car_detected, :status, :response_message, :step_timings)
        """),
        {
            "user_id": user_id,
            "text_input": claim_text,
            "image_confidence": confidence,
            "car_detected": car_detected,
            "status": str(status),
            "response_message": message,
            "step_timings": str(timings)
        }
    )

    db.commit()

    # -------------------------
    # FINAL RESPONSE
    # -------------------------
    return {
        "status": status,
        "message": message,
        "car_detected": car_detected,
        "confidence": confidence,
        "timings": timings
    }

from admin_api import router as admin_router

app.include_router(admin_router)
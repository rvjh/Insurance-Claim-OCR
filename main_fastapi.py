from fastapi import FastAPI, UploadFile, Form
from db.database import init_db, SessionLocal
from agents.text_agent import process_text
from agents.vision_agent import analyze_image
from agents.decision_agent import decide
from services.guardrails import validate_text, is_safe_output
import base64, time

app = FastAPI()
init_db()

@app.post("/claim")
async def process_claim(
    user_id: int,
    text: str = Form(...),
    image: UploadFile = Form(...)
):

    timings = {}

    # Step 1: Text validation
    t1 = time.time()
    valid, errors = validate_text(text)
    text_data = process_text(text)
    t2 = time.time()
    timings["text"] = t2 - t1

    # Step 2: Image processing
    t3 = time.time()
    img_bytes = await image.read()
    img_b64 = base64.b64encode(img_bytes).decode()

    vision_result = analyze_image(img_b64)
    t4 = time.time()
    timings["vision"] = t4 - t3

    # Step 3: Decision
    t5 = time.time()
    status, message = decide(valid, vision_result)
    t6 = time.time()
    timings["decision"] = t6 - t5

    # Safety filter
    if not is_safe_output(message):
        message = "Response blocked due to safety policy"
        status = False

    return {
        "status": status,
        "message": message,
        "timings": timings,
        "confidence": vision_result["confidence"]
    }

@app.get("/admin/stats")
def admin_stats():
    db = SessionLocal()

    total_users = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    active_users = db.execute("SELECT COUNT(*) FROM users WHERE active=1").fetchone()[0]

    logs = db.execute("SELECT * FROM claim_logs").fetchall()

    return {
        "total_users": total_users,
        "active_users": active_users,
        "total_claims": len(logs)
    }
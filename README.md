# Insurance Claim OCR

An insurance claim prototype that validates free-text claims, analyzes uploaded images with Groq vision, applies simple business rules and safety checks, and logs outcomes to SQLite. The API is exposed with **FastAPI**; operators can submit claims or view aggregate metrics via **Streamlit** front ends.

---

## Purpose

Automate the early steps of a motor claim submission:

1. **Text guardrails** — ensure the claimant provided enough structured signals (policy, name, accident date).
2. **Vision analysis** — use a multimodal model to describe the image and infer whether a car is present.
3. **Decision + safety** — approve or reject with a clear message; block disallowed wording in outputs.
4. **Persistence** — store each submission in SQLite for auditing and admin metrics.

This is suitable for demos, coursework, or as a starting point for a production pipeline (auth, stronger extraction, real confidence scores, etc.).

---

## Tech stack

| Layer | Technology |
|--------|------------|
| API | [FastAPI](https://fastapi.tiangolo.com/), Uvicorn |
| UI | [Streamlit](https://streamlit.io/) (claim form + admin dashboard) |
| LLM / vision | [Groq](https://groq.com/) (`llama-3.3-70b-versatile`, `meta-llama/llama-4-scout-17b-16e-instruct`) |
| Database | SQLite via SQLAlchemy |
| Agent helpers (optional) | [Agno](https://github.com/agno-agi/agno) in `agents/` |

---

## Project structure

```
Insurance-Claim-OCR/
├── main_fastapi.py          # FastAPI app: POST /claim, mounts admin routes
├── admin_api.py             # GET /admin/metrics (aggregates from claim_logs)
├── streamlit_app.py         # User-facing claim submission UI
├── admin_dashboard.py       # Streamlit admin metrics UI
├── services/
│   ├── groq_client.py       # Groq chat + vision wrappers
│   └── guardrails.py        # Text validation + output safety
├── db/
│   ├── database.py          # Engine, SessionLocal, init_db (claim_logs table)
│   └── models.py            # SQLAlchemy models (optional / extended schema)
├── agents/
│   ├── text_agent.py        # Text extraction agent (Agno + chat_completion)
│   ├── vision_agent.py      # Vision helper around vision_ocr
│   ├── decision_agent.py
│   └── logger_agent.py
├── images/                  # Screenshots for docs (FastAPI / Streamlit output)
├── requirements.txt
├── .env                     # GROQ_API_KEY (not committed — use .gitignore)
└── claim.db                 # SQLite file (created at runtime)
```

---

## Methods and behavior

### FastAPI — `POST /claim`

Multipart form fields:

| Field | Type | Description |
|--------|------|-------------|
| `user_id` | integer | Submitter id (logged) |
| `claim_text` | string | Free-text claim description |
| `image` | file | Car / accident image (`png`, `jpg`, `jpeg`) |

**Pipeline:**

1. `validate_text(claim_text)` — length ≥ 20; must mention policy, name, and date (keyword checks).
2. Read image → Base64 → `vision_ocr(...)` (Groq vision model).
3. Heuristic: `"car" in vision_result.lower()` → `car_detected`; confidence is derived from that (demo values).
4. `is_safe_output(message)` — blocks messages containing disallowed substrings.
5. Insert row into `claim_logs` (timings per step).
6. JSON response: `status`, `message`, `car_detected`, `confidence`, `timings`.

### FastAPI — `GET /admin/metrics`

Returns JSON: `total_users`, `total_claims`, `approved_claims`, `rejected_claims`, `car_detected_cases` from SQL aggregates on `claim_logs`.

### Services

- **`services/groq_client.py`** — `chat_completion(prompt)` (text), `vision_ocr(image_base64)` (image + instructions).
- **`services/guardrails.py`** — `validate_text`, `is_safe_output`.

### Streamlit

- **`streamlit_app.py`** — form → `POST http://127.0.0.1:8000/claim` with `user_id`, `claim_text`, and file field `image`.
- **`admin_dashboard.py`** — `GET http://127.0.0.1:8000/admin/metrics` and displays metrics.

---

## Setup

1. **Python 3.10+** recommended.

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   pip install python-dotenv
   ```

   (`python-dotenv` is used by `services/groq_client.py` for `.env` loading.)

3. **Environment**

   Create `.env` in the project root:

   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Run the API**

   ```bash
   uvicorn main_fastapi:app --reload --host 127.0.0.1 --port 8000
   ```

   Interactive docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

5. **Run Streamlit (user app)**

   ```bash
   streamlit run streamlit_app.py
   ```

6. **Run Streamlit (admin)**

   ```bash
   streamlit run admin_dashboard.py
   ```

---

## Sample data for testing

Use this claim text together with **any plausible car-accident photo** (the vision step looks for evidence of a car in the model’s response):

```text
policy number: P12345
name: John Doe
date of accident: 2026-05-01 accident occurred
car damaged in collision
```

In Streamlit:

- Enter a numeric **User ID** (e.g. `12345` or `1`).
- Paste the claim text above.
- Upload an image and submit.

**cURL example** (adjust path to your image):

```bash
curl -X POST "http://127.0.0.1:8000/claim" ^
  -F "user_id=1" ^
  -F "claim_text=policy number: P12345
name: John Doe
date of accident: 2026-05-01 accident occurred
car damaged in collision" ^
  -F "image=@C:\path\to\your_car_image.jpg"
```

---

## Screenshots

### Normal flow — FastAPI

![FastAPI claim response](images/FastAPI%201.png)

### Normal flow — Streamlit claim UI / result

The user app mirrors the API response (status, message, car detected, confidence, timings). Place your screenshots under `images/` if filenames differ, and update links here.

### Admin — FastAPI metrics response

![FastAPI admin metrics JSON](images/FastAPI%20Admin%20Response%201.png)

### Admin — Streamlit dashboard

![Streamlit admin metrics](images/Streamlit%20Admin%20Dashboard%20Metrices.png)

> **Note:** Image paths assume files live in [`images/`](images/). Encode spaces in filenames in Markdown URLs as `%20` (as above), or rename files without spaces.

---

## Future improvements

- **Structured extraction** — parse policy number, claimant name, and accident date into columns (wire `agents/text_agent.py` into `/claim`, align with `db/models.py`).
- **Real vision confidence** — parse model-reported scores instead of heuristics (`"car" in text` / fixed floats).
- **Authentication** — protect `/claim` and `/admin/*` (API keys, JWT, or OAuth); add admin roles.
- **Tests** — pytest for guardrails, decision logic, and API contracts with mocked Groq.
- **Deployment** — Docker, env-based config, PostgreSQL instead of SQLite for production.
- **Observability** — request IDs, structured logging, retries and timeouts on Groq calls.
- **Streamlit UX** — session state, error handling, configurable `API_URL` via env/secrets.

---

## License

Add a license file if you open-source the repo (MIT, Apache-2.0, etc.).

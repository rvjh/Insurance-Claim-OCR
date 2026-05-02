from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DB_URL = "sqlite:///claim.db"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


def init_db():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS claim_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                text_input TEXT,
                image_confidence REAL,
                car_detected BOOLEAN,
                status TEXT,
                response_message TEXT,
                step_timings TEXT
            )
        """))
        conn.commit()
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    role = Column(String)  # admin/user
    active = Column(Boolean, default=True)

class ClaimLog(Base):
    __tablename__ = "claim_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    text_input = Column(Text)
    image_confidence = Column(Float)
    car_detected = Column(Boolean)

    policy_number = Column(String)
    user_name = Column(String)
    accident_date = Column(String)

    status = Column(String)
    response_message = Column(Text)

    step_timings = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
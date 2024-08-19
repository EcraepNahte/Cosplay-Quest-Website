from sqlalchemy import Column, Integer, String, Text, DateTime, func
from .database import Base

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class BetaSignup(Base):
    __tablename__ = "beta_signup"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    device_os = Column(String)
    next_con = Column(String, nullable=True)
    next_con_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
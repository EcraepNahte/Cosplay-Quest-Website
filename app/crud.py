import datetime
from sqlalchemy.orm import Session
from . import models

def create_feedback(db: Session, name: str, email: str, message: str, created_at: datetime):
    db_feedback = models.Feedback(name=name, email=email, message=message, created_at=created_at)
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def get_all_feedback(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Feedback).offset(skip).limit(limit).all()

def create_beta_signup(db: Session, name: str, email: str, device_os: str, next_con: str = None, next_con_date: datetime = None):
    db_beta_signup = models.BetaSignup(name=name, email=email, device_os=device_os, next_con=next_con, next_con_date=next_con_date)
    db.add(db_beta_signup)
    db.commit()
    db.refresh(db_beta_signup)
    return db_beta_signup

def get_all_beta_signups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.BetaSignup).offset(skip).limit(limit).all()
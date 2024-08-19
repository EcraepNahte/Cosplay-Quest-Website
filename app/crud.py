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
from sqlalchemy import Column, ForeignKey, Integer, Float, String, Text, DateTime, Boolean, func
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
    will_cosplay = Column(Boolean)
    character = Column(String, nullable=True)
    source_media = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    source_media = Column(String, index=True)
    genre = Column(String, nullable=True)
    reference_picture = Column(String, nullable=True)
    reference_link = Column(String, nullable=True)
    description = Column(String, nullable=True)
    active = Column(Boolean)
    pack_id = Column(String, ForeignKey("packs.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "source_media": self.source_media,
            "genre": self.genre if self.genre else '',
            "reference_picture": self.reference_picture if self.reference_picture else '',
            "reference_link": self.reference_link if self.reference_link else '',
            "description": self.description if self.description else '',
            "active": 'true' if self.active else 'false',
            "pack_id": self.pack_id
        }

class Pack(Base):
    __tablename__ = "packs"

    id = Column(String, primary_key=True, index=True)
    display_name = Column(String)
    cost = Column(Float)

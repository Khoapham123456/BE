from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from infrastructure.models.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(120), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="patient")  # guest/patient/dentist/owner/admin/receptionist
    created_at = Column(DateTime(timezone=True), server_default=func.now())


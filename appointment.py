# src/infrastructure/models/appointment.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.models.base import Base
from datetime import datetime

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("users.id"), nullable=False)   # liên kết tới User (bác sĩ)
    patient_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # liên kết tới User (bệnh nhân)
    date = Column(DateTime, nullable=False, default=datetime.now)
    result = Column(String(255), nullable=True)

    # Quan hệ với Prescription
    prescriptions = relationship("Prescription", back_populates="appointment")

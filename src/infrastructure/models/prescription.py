from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from infrastructure.models.base import Base
from datetime import datetime

class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=False)
    medicines = Column(String(255), nullable=False)
    note = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)

    appointment = relationship("Appointment", back_populates="prescriptions")
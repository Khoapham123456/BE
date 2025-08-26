# src/infrastructure/models/patient.py
from datetime import datetime
from models import Column, Integer, String, Date, DateTime, ForeignKey, UniqueConstraint
from models import relationship

from infrastructure.databases.postgres_adapter import db

class Patient(db.Model):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(32), nullable=False)
    dob = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", backref="patient_profile", lazy="joined")

    __table_args__ = (
        UniqueConstraint('phone', name='uq_patients_phone'),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "full_name": self.full_name,
            "phone": self.phone,
            "dob": self.dob.isoformat() if self.dob else None,
            "created_at": self.created_at.isoformat(),
        }

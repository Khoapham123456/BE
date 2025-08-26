# src/infrastructure/models/receptionist.py
from datetime import datetime
from models import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from infrastructure.databases.postgres_adapter import db

class Receptionist(db.Model):
    __tablename__ = "receptionists"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    clinic_id = Column(Integer, ForeignKey("clinics.id", ondelete="CASCADE"), nullable=False)
    display_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", backref="receptionist_profile", lazy="joined")
    clinic = relationship("Clinic", backref="receptionists", lazy="joined")

    __table_args__ = (
        UniqueConstraint('user_id', 'clinic_id', name='uq_receptionists_user_clinic'),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "clinic_id": self.clinic_id,
            "display_name": self.display_name,
            "created_at": self.created_at.isoformat(),
        }

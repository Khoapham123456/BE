from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from infrastructure.models.appointment import Appointment
from infrastructure.models.prescription import Prescription

class DoctorService:
    def __init__(self, db: Session):
        self.db = db

    def get_schedule(self, doctor_id: int):
        today = datetime.now().date()
        end_date = today + timedelta(days=7)
        return (
            self.db.query(Appointment)
            .filter(
                Appointment.doctor_id == doctor_id,
                Appointment.date >= today,
                Appointment.date <= end_date
            )
            .all()
        )

    def update_appointment_result(self, appointment_id: int, result: str):
        appt = self.db.query(Appointment).filter_by(id=appointment_id).first()
        if not appt:
            return None
        appt.result = result
        self.db.commit()
        self.db.refresh(appt)
        return appt

    def add_prescription(self, appointment_id: int, medicines: str, note: str):
        prescription = Prescription(
            appointment_id=appointment_id,
            medicines=medicines,
            note=note
        )
        self.db.add(prescription)
        self.db.commit()
        self.db.refresh(prescription)
        return prescription
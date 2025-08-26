# src/services/patient_service.py
from datetime import datetime, date
from typing import Dict, Any, List, Optional

from infrastructure.databases.postgres_adapter import db
from infrastructure.models.patient import Patient
from infrastructure.models.user_model import User
from infrastructure.models.appointment_model import Appointment
from infrastructure.models.clinic_model import Clinic

# Optional: dùng constant nếu bạn có enum trong domain.constants
try:
    from domain.constants import AppointmentStatus  # Enum
    STATUS_PENDING = AppointmentStatus.PENDING.value
    STATUS_CONFIRMED = AppointmentStatus.CONFIRMED.value
    STATUS_CANCELLED = AppointmentStatus.CANCELLED.value
    STATUS_COMPLETED = AppointmentStatus.COMPLETED.value
except Exception:
    # Fallback string
    STATUS_PENDING = "PENDING"
    STATUS_CONFIRMED = "CONFIRMED"
    STATUS_CANCELLED = "CANCELLED"
    STATUS_COMPLETED = "COMPLETED"

class PatientService:
    def register_patient(self, user_id: int, full_name: str, phone: str, dob: Optional[date]) -> Dict[str, Any]:
        """
        Tạo hồ sơ Patient cho user đã đăng ký (role: patient).
        """
        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise ValueError("User không tồn tại")

        existing = Patient.query.filter((Patient.user_id == user_id) | (Patient.phone == phone)).first()
        if existing:
            raise ValueError("Đã tồn tại hồ sơ bệnh nhân với user hoặc số điện thoại này")

        patient = Patient(user_id=user_id, full_name=full_name, phone=phone, dob=dob)
        db.session.add(patient)
        db.session.commit()
        return patient.to_dict()

    def create_appointment(
        self, patient_user_id: int, clinic_id: int, scheduled_at: datetime, note: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Bệnh nhân đặt lịch khám (guest -> patient đã có user_id).
        Mặc định status = PENDING (đợi lễ tân/clinic xác nhận).
        """
        # Kiểm tra hồ sơ bệnh nhân
        patient = Patient.query.filter_by(user_id=patient_user_id).first()
        if not patient:
            raise ValueError("Chưa có hồ sơ bệnh nhân, vui lòng đăng ký hồ sơ trước")

        clinic = Clinic.query.filter_by(id=clinic_id).first()
        if not clinic:
            raise ValueError("Phòng khám không tồn tại")

        # (MVP) Không check trùng slot sâu, để receptionist xác nhận
        appt = Appointment(
            patient_id=patient.id,
            clinic_id=clinic.id,
            scheduled_at=scheduled_at,
            status=STATUS_PENDING,
            note=note or ""
        )
        db.session.add(appt)
        db.session.commit()
        return self._to_appt_dict(appt)

    def get_appointment_status(self, patient_user_id: int, appointment_id: int) -> Dict[str, Any]:
        patient = Patient.query.filter_by(user_id=patient_user_id).first()
        if not patient:
            raise ValueError("Chưa có hồ sơ bệnh nhân")

        appt = Appointment.query.filter_by(id=appointment_id, patient_id=patient.id).first()
        if not appt:
            raise ValueError("Không tìm thấy lịch hẹn")

        return {"appointment_id": appt.id, "status": appt.status, "scheduled_at": appt.scheduled_at.isoformat()}

    def list_history(self, patient_user_id: int, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """
        Lịch sử khám: tất cả lịch hẹn đã hoàn tất hoặc đã khám/cancel (sắp xếp gần nhất trước).
        """
        patient = Patient.query.filter_by(user_id=patient_user_id).first()
        if not patient:
            raise ValueError("Chưa có hồ sơ bệnh nhân")

        q = (Appointment.query
             .filter(Appointment.patient_id == patient.id)
             .order_by(Appointment.scheduled_at.desc()))
        total = q.count()
        items = q.offset((page - 1) * page_size).limit(page_size).all()
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": [self._to_appt_dict(a) for a in items]
        }

    def _to_appt_dict(self, a: Appointment) -> Dict[str, Any]:
        return {
            "id": a.id,
            "clinic_id": a.clinic_id,
            "dentist_id": a.dentist_id,
            "patient_id": a.patient_id,
            "scheduled_at": a.scheduled_at.isoformat() if a.scheduled_at else None,
            "status": a.status,
            "note": getattr(a, "note", None),
            "created_at": a.created_at.isoformat() if getattr(a, "created_at", None) else None,
        }

# DI-friendly singleton
patient_service = PatientService()

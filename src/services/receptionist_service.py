# src/services/receptionist_service.py
from datetime import datetime, date, timedelta
from typing import Dict, Any, Optional

from infrastructure.databases.postgres_adapter import db
from infrastructure.models.receptionist import Receptionist
from infrastructure.models.appointment_model import Appointment

try:
    from domain.constants import AppointmentStatus  # Enum
    STATUS_PENDING = AppointmentStatus.PENDING.value
    STATUS_CONFIRMED = AppointmentStatus.CONFIRMED.value
    STATUS_CANCELLED = AppointmentStatus.CANCELLED.value
    STATUS_COMPLETED = AppointmentStatus.COMPLETED.value
    STATUS_NO_SHOW = AppointmentStatus.NO_SHOW.value
except Exception:
    STATUS_PENDING = "PENDING"
    STATUS_CONFIRMED = "CONFIRMED"
    STATUS_CANCELLED = "CANCELLED"
    STATUS_COMPLETED = "COMPLETED"
    STATUS_NO_SHOW = "NO_SHOW"

VALID_STATUS_TRANSITIONS = {
    STATUS_PENDING: {STATUS_CONFIRMED, STATUS_CANCELLED},
    STATUS_CONFIRMED: {STATUS_COMPLETED, STATUS_CANCELLED, STATUS_NO_SHOW},
    STATUS_COMPLETED: set(),
    STATUS_CANCELLED: set(),
    STATUS_NO_SHOW: set(),
}

class ReceptionistService:
    def _get_receptionist(self, user_id: int) -> Receptionist:
        r = Receptionist.query.filter_by(user_id=user_id).first()
        if not r:
            raise ValueError("Tài khoản không phải lễ tân hoặc chưa gán phòng khám")
        return r

    def list_today_appointments(self, receptionist_user_id: int, on_date: Optional[date] = None) -> Dict[str, Any]:
        """
        Danh sách lịch hẹn trong ngày theo phòng khám của lễ tân.
        """
        r = self._get_receptionist(receptionist_user_id)
        on_date = on_date or date.today()
        start = datetime(on_date.year, on_date.month, on_date.day)
        end = start + timedelta(days=1)

        q = (Appointment.query
             .filter(Appointment.clinic_id == r.clinic_id)
             .filter(Appointment.scheduled_at >= start, Appointment.scheduled_at < end)
             .order_by(Appointment.scheduled_at.asc()))
        items = q.all()
        return {
            "date": on_date.isoformat(),
            "clinic_id": r.clinic_id,
            "items": [self._to_appt_dict(a) for a in items]
        }

    def confirm_appointment(self, receptionist_user_id: int, appointment_id: int) -> Dict[str, Any]:
        """
        Xác nhận lịch hẹn ở trạng thái PENDING -> CONFIRMED
        """
        r = self._get_receptionist(receptionist_user_id)
        appt = Appointment.query.filter_by(id=appointment_id, clinic_id=r.clinic_id).first()
        if not appt:
            raise ValueError("Không tìm thấy lịch hẹn thuộc phòng khám của bạn")

        if appt.status != STATUS_PENDING:
            raise ValueError("Chỉ có thể xác nhận lịch ở trạng thái PENDING")

        appt.status = STATUS_CONFIRMED
        db.session.commit()
        return self._to_appt_dict(appt)

    def update_appointment_status(self, receptionist_user_id: int, appointment_id: int, new_status: str) -> Dict[str, Any]:
        """
        Cập nhật trạng thái theo luật chuyển trạng thái hợp lệ.
        """
        r = self._get_receptionist(receptionist_user_id)
        appt = Appointment.query.filter_by(id=appointment_id, clinic_id=r.clinic_id).first()
        if not appt:
            raise ValueError("Không tìm thấy lịch hẹn thuộc phòng khám của bạn")

        current = appt.status
        allowed = VALID_STATUS_TRANSITIONS.get(current, set())
        if new_status not in allowed:
            raise ValueError(f"Không thể chuyển trạng thái từ {current} -> {new_status}")

        appt.status = new_status
        db.session.commit()
        return self._to_appt_dict(appt)

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

receptionist_service = ReceptionistService()

from src.infrastructure.models.user_model import UserModel
from src.infrastructure.models.appointment_model import AppointmentModel
from src.infrastructure.database import db

class AdminService:
    def __init__(self):
        self.db = db

    # ================= CRUD USER ==================
    def get_all_users(self):
        return UserModel.query.all()

    def create_user(self, user_data):
        user = UserModel(**user_data)
        self.db.session.add(user)
        self.db.session.commit()
        return user

    def update_user(self, user_id, update_data):
        user = UserModel.query.get(user_id)
        if not user:
            return None
        for key, value in update_data.items():
            setattr(user, key, value)
        self.db.session.commit()
        return user

    def delete_user(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            return None
        self.db.session.delete(user)
        self.db.session.commit()
        return True

    # ================ CRUD APPOINTMENT ==============
    def get_all_appointments(self):
        return AppointmentModel.query.all()

    def approve_appointment(self, appointment_id):
        appointment = AppointmentModel.query.get(appointment_id)
        if not appointment:
            return None
        appointment.status = "approved"
        self.db.session.commit()
        return appointment

    def cancel_appointment(self, appointment_id):
        appointment = AppointmentModel.query.get(appointment_id)
        if not appointment:
            return None
        appointment.status = "canceled"
        self.db.session.commit()
        return appointment

    # ================ REPORTS =======================
    def get_statistics(self):
        total_users = UserModel.query.count()
        total_appointments = AppointmentModel.query.count()
        approved_appointments = AppointmentModel.query.filter_by(status="approved").count()
        canceled_appointments = AppointmentModel.query.filter_by(status="canceled").count()

        return {
            "total_users": total_users,
            "total_appointments": total_appointments,
            "approved_appointments": approved_appointments,
            "canceled_appointments": canceled_appointments,
        }

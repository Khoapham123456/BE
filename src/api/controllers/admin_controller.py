from flask import Blueprint, request, jsonify
from src.services.admin_service import AdminService

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")
admin_service = AdminService()

# --------- CRUD USER -----------
@admin_bp.route("/users", methods=["GET"])
def get_all_users():
    users = admin_service.get_all_users()
    return jsonify([u.to_dict() for u in users])

@admin_bp.route("/users", methods=["POST"])
def create_user():
    data = request.json
    user = admin_service.create_user(data)
    return jsonify(user.to_dict()), 201

@admin_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    user = admin_service.update_user(user_id, data)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict())

@admin_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    result = admin_service.delete_user(user_id)
    if not result:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted"})

# -------- CRUD APPOINTMENT --------
@admin_bp.route("/appointments", methods=["GET"])
def get_all_appointments():
    appointments = admin_service.get_all_appointments()
    return jsonify([a.to_dict() for a in appointments])

@admin_bp.route("/appointments/<int:appointment_id>/approve", methods=["PUT"])
def approve_appointment(appointment_id):
    appointment = admin_service.approve_appointment(appointment_id)
    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404
    return jsonify(appointment.to_dict())

@admin_bp.route("/appointments/<int:appointment_id>/cancel", methods=["PUT"])
def cancel_appointment(appointment_id):
    appointment = admin_service.cancel_appointment(appointment_id)
    if not appointment:
        return jsonify({"error": "Appointment not found"}), 404
    return jsonify(appointment.to_dict())

# --------- REPORTS ----------
@admin_bp.route("/reports", methods=["GET"])
def get_statistics():
    stats = admin_service.get_statistics()
    return jsonify(stats)

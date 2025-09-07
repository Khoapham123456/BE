# src/api/controllers/patient_controller.py
from datetime import datetime
from flask import Blueprint, request, jsonify, g

from services.patient_service import patient_service

# Giả định middleware đã set g.user_id và g.role
# Nếu bạn có decorator require_roles, có thể bật lên để siết quyền.
# from api.middleware import require_roles

bp_patient = Blueprint("patients", __name__, url_prefix="/api/patients")

@bp_patient.route("/register", methods=["POST"])
# @require_roles("patient")  # Nếu muốn: chỉ user role=patient mới được mở hồ sơ
def register_patient():
    data = request.get_json(force=True) or {}
    full_name = data.get("full_name")
    phone = data.get("phone")
    dob_raw = data.get("dob")  # "YYYY-MM-DD" optional

    if not full_name or not phone:
        return jsonify({"error": "full_name và phone là bắt buộc"}), 400

    dob = None
    if dob_raw:
        try:
            dob = datetime.strptime(dob_raw, "%Y-%m-%d").date()
        except Exception:
            return jsonify({"error": "dob phải theo định dạng YYYY-MM-DD"}), 400

    user_id = getattr(g, "user_id", None)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        patient = patient_service.register_patient(user_id=user_id, full_name=full_name, phone=phone, dob=dob)
        return jsonify({"data": patient}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@bp_patient.route("/appointments", methods=["POST"])
# @require_roles("patient")
def create_appointment():
    data = request.get_json(force=True) or {}
    clinic_id = data.get("clinic_id")
    scheduled_at_raw = data.get("scheduled_at")  # ISO 8601, ví dụ: "2025-08-26T09:00:00"
    note = data.get("note")

    if not clinic_id or not scheduled_at_raw:
        return jsonify({"error": "clinic_id và scheduled_at là bắt buộc"}), 400

    try:
        scheduled_at = datetime.fromisoformat(scheduled_at_raw)
    except Exception:
        return jsonify({"error": "scheduled_at phải là ISO 8601, ví dụ 2025-08-26T09:00:00"}), 400

    user_id = getattr(g, "user_id", None)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        appt = patient_service.create_appointment(
            patient_user_id=user_id, clinic_id=int(clinic_id), scheduled_at=scheduled_at, note=note
        )
        return jsonify({"data": appt}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@bp_patient.route("/appointments/<int:appointment_id>", methods=["GET"])
# @require_roles("patient")
def get_appointment_status(appointment_id: int):
    user_id = getattr(g, "user_id", None)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    try:
        data = patient_service.get_appointment_status(patient_user_id=user_id, appointment_id=appointment_id)
        return jsonify({"data": data}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@bp_patient.route("/appointments/history", methods=["GET"])
# @require_roles("patient")
def list_history():
    user_id = getattr(g, "user_id", None)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        page = int(request.args.get("page", 1))
        page_size = int(request.args.get("page_size", 20))
    except ValueError:
        return jsonify({"error": "page và page_size phải là số nguyên"}), 400

    try:
        data = patient_service.list_history(patient_user_id=user_id, page=page, page_size=page_size)
        return jsonify({"data": data}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

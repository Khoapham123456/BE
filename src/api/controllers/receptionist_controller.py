# src/api/controllers/receptionist_controller.py
from datetime import datetime
from flask import Blueprint, request, jsonify, g

from services.receptionist_service import receptionist_service

# from api.middleware import require_roles

bp_reception = Blueprint("receptionists", __name__, url_prefix="/api/receptionists")

@bp_reception.route("/appointments/today", methods=["GET"])
# @require_roles("receptionist", "owner")  # Owner có thể xem theo clinic cũng hợp lý
def list_today_appointments():
    user_id = getattr(g, "user_id", None)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    on_date = request.args.get("date")  # "YYYY-MM-DD" optional
    parsed_date = None
    if on_date:
        try:
            parsed_date = datetime.strptime(on_date, "%Y-%m-%d").date()
        except Exception:
            return jsonify({"error": "date phải có định dạng YYYY-MM-DD"}), 400
    try:
        data = receptionist_service.list_today_appointments(receptionist_user_id=user_id, on_date=parsed_date)
        return jsonify({"data": data}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@bp_reception.route("/appointments/<int:appointment_id>/confirm", methods=["POST"])
# @require_roles("receptionist")
def confirm_appointment(appointment_id: int):
    user_id = getattr(g, "user_id", None)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    try:
        data = receptionist_service.confirm_appointment(receptionist_user_id=user_id, appointment_id=appointment_id)
        return jsonify({"data": data}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@bp_reception.route("/appointments/<int:appointment_id>/status", methods=["PATCH"])
# @require_roles("receptionist")
def update_appointment_status(appointment_id: int):
    user_id = getattr(g, "user_id", None)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    payload = request.get_json(force=True) or {}
    new_status = payload.get("status")
    if not new_status:
        return jsonify({"error": "Thiếu trường 'status'"}), 400

    try:
        data = receptionist_service.update_appointment_status(
            receptionist_user_id=user_id, appointment_id=appointment_id, new_status=new_status
        )
        return jsonify({"data": data}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

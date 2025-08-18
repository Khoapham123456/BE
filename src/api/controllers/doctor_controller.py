from flask import Blueprint, request, jsonify
from infrastructure.databases.db_init import get_db
from services.doctor_service import DoctorService

doctor_bp = Blueprint("doctor", __name__, url_prefix="/api/doctor")

# Xem lịch hẹn 7 ngày
@doctor_bp.route("/schedule", methods=["GET"])
def get_schedule():
    doctor_id = request.args.get("doctor_id")
    if not doctor_id:
        return jsonify({"error": "doctor_id is required"}), 400

    db = next(get_db())
    service = DoctorService(db)
    schedule = service.get_schedule(int(doctor_id))
    return jsonify([{
        "id": appt.id,
        "patient_id": appt.patient_id,
        "date": str(appt.date),
        "status": appt.status
    } for appt in schedule])

# Cập nhật kết quả khám
@doctor_bp.route("/appointments/result", methods=["POST"])
def update_result():
    data = request.json
    appointment_id = data.get("appointment_id")
    result = data.get("result")

    if not appointment_id or not result:
        return jsonify({"error": "appointment_id and result are required"}), 400

    db = next(get_db())
    service = DoctorService(db)
    appt = service.update_appointment_result(appointment_id, result)
    if not appt:
        return jsonify({"error": "Appointment not found"}), 404
    return jsonify({
        "id": appt.id,
        "result": appt.result
    })

# Thêm đơn thuốc
@doctor_bp.route("/prescriptions", methods=["POST"])
def add_prescription():
    data = request.json
    appointment_id = data.get("appointment_id")
    medicines = data.get("medicines")
    note = data.get("note", "")

    if not appointment_id or not medicines:
        return jsonify({"error": "appointment_id and medicines are required"}), 400

    db = next(get_db())
    service = DoctorService(db)
    prescription = service.add_prescription(appointment_id, medicines, note)
    return jsonify({
        "id": prescription.id,
        "appointment_id": prescription.appointment_id,
        "medicines": prescription.medicines,
        "note": prescription.note,
        "created_at": str(prescription.created_at)
    })

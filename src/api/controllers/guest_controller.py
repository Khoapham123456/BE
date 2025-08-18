from flask import Blueprint, jsonify, request
from services.guest_service import GuestService

guest_bp = Blueprint("guest", __name__)

@guest_bp.route("/doctors", methods=["GET"])
def get_doctors():
    return jsonify(GuestService.get_doctors())

@guest_bp.route("/services", methods=["GET"])
def get_services():
    return jsonify(GuestService.get_services())

@guest_bp.route("/appointment", methods=["POST"])
def book_appointment():
    data = request.json
    return jsonify(GuestService.book_appointment(data)), 201

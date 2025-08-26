class GuestService:
    @staticmethod
    def get_doctors():
        # TODO: query DB
        return [{"id": 1, "name": "Dr. Trí"}, {"id": 2, "name": "Dr. X"}]

    @staticmethod
    def get_services():
        return [
            {"id": 1, "name": "Khám tổng quát"},
            {"id": 2, "name": "Khám tim mạch"},
        ]

    @staticmethod
    def book_appointment(data):
        # TODO: insert DB
        return {"message": "Appointment booked", "data": data}

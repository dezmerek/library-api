from db import db


class Reservation:
    collection = db.reservations

    @staticmethod
    def to_json(reservation):
        return {
            "reservation_id": str(reservation["_id"]),
            "book_id": str(reservation["book_id"]),
            "user_id": str(reservation["user_id"]),
            "reservation_date": reservation["reservation_date"].isoformat(),
            "status": reservation.get("status", "active")
        }

from db import db
from models.book import Book
from models.user import User
from models.reservation import Reservation
from bson import ObjectId
from datetime import datetime


def reserve_book(user_id, book_id, user_role):
    try:
        book = Book.collection.find_one({"_id": ObjectId(book_id)})
        if not book:
            return {"msg": "Książka o podanym ID nie istnieje"}, 404

        user = User.collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return {"msg": "Użytkownik o podanym ID nie istnieje"}, 404

        if user_role not in ["admin", "librarian", "user"]:
            return {
                "msg": "Nie masz wystarczających uprawnień do wykonania tej operacji"
            }, 403

        existing_reservation = Reservation.collection.find_one(
            {
                "book_id": ObjectId(book_id),
                "user_id": ObjectId(user_id),
                "status": "active",
            }
        )
        if existing_reservation:
            return {"msg": "Masz już aktywną rezerwację na tę książkę"}, 400

        reservation_data = {
            "user_id": ObjectId(user_id),
            "book_id": ObjectId(book_id),
            "reservation_date": datetime.now(),
            "status": "active",
        }
        Reservation.collection.insert_one(reservation_data)
        return {"msg": "Książka została zarezerwowana"}
    except Exception as e:
        return {"msg": f"Błąd podczas rezerwacji książki: {str(e)}"}, 500


def cancel_reservation(user_id, book_id, user_role):
    try:
        book = Book.collection.find_one({"_id": ObjectId(book_id)})
        if not book:
            return {"msg": "Książka o podanym ID nie istnieje"}, 404

        user = User.collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return {"msg": "Użytkownik o podanym ID nie istnieje"}, 404

        if user_role not in ["admin", "librarian", "user"]:
            return {
                "msg": "Nie masz wystarczających uprawnień do wykonania tej operacji"
            }, 403

        existing_reservation = Reservation.collection.find_one(
            {
                "book_id": ObjectId(book_id),
                "user_id": ObjectId(user_id),
                "status": "active",
            }
        )
        if not existing_reservation:
            return {"msg": "Nie znaleziono aktywnej rezerwacji do anulowania"}, 404

        result = Reservation.collection.delete_one(
            {"_id": existing_reservation["_id"]})
        if result.deleted_count:
            return {"msg": "Rezerwacja książki została anulowana"}
        else:
            return {"msg": "Błąd podczas anulowania rezerwacji książki"}
    except Exception as e:
        return {"msg": f"Błąd podczas anulowania rezerwacji książki: {str(e)}"}, 500

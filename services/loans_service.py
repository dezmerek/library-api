
from models.loan import Loan
from models.book import Book
from models.user import User
from bson import ObjectId
from datetime import datetime, timedelta

def borrow_book(user_id, book_id):
    try:
        book = Book.collection.find_one({"_id": ObjectId(book_id)})
        if not book:
            return {"msg": "Książka o podanym ID nie istnieje"}, 404

        user = User.collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return {"msg": "Użytkownik o podanym ID nie istnieje"}, 404

        if user['role'] not in ['admin', 'librarian']:
            return {"msg": "Nie masz wystarczających uprawnień do wykonania tej operacji"}, 403

        existing_loan = Loan.collection.find_one({"book_id": ObjectId(book_id), "$or": [{"returned": False}, {"returned": None}]})
        if existing_loan:
            return {"msg": "Książka jest już zarezerwowana lub wypożyczona"}, 400

        loan_data = {
            "user_id": ObjectId(user_id),
            "book_id": ObjectId(book_id),
            "loan_date": datetime.now(),
            "return_date": None,
            "returned": False
        }
        Loan.collection.insert_one(loan_data)
        return {"msg": "Książka została wypożyczona"}
    except Exception as e:
        return {"msg": f"Błąd podczas wypożyczania książki: {str(e)}"}, 500

def reserve_book(user_id, book_id):
    try:
        book = Book.collection.find_one({"_id": ObjectId(book_id)})
        if not book:
            return {"msg": "Książka o podanym ID nie istnieje"}, 404

        user = User.collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return {"msg": "Użytkownik o podanym ID nie istnieje"}, 404

        if user['role'] not in ['admin', 'librarian', 'user']:
            return {"msg": "Nie masz wystarczających uprawnień do wykonania tej operacji"}, 403

        existing_loan = Loan.collection.find_one({"book_id": ObjectId(book_id), "$or": [{"returned": False}, {"returned": None}]})
        if existing_loan:
            return {"msg": "Książka jest już zarezerwowana lub wypożyczona"}, 400


        return {"msg": "Książka została zarezerwowana"}
    except Exception as e:
        return {"msg": f"Błąd podczas rezerwacji książki: {str(e)}"}, 500

def cancel_reservation(user_id, book_id):
    try:
        book = Book.collection.find_one({"_id": ObjectId(book_id)})
        if not book:
            return {"msg": "Książka o podanym ID nie istnieje"}, 404

        user = User.collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return {"msg": "Użytkownik o podanym ID nie istnieje"}, 404

        if user['role'] not in ['admin', 'librarian', 'user']:
            return {"msg": "Nie masz wystarczających uprawnień do wykonania tej operacji"}, 403

        existing_loan = Loan.collection.find_one({"book_id": ObjectId(book_id), "user_id": ObjectId(user_id), "returned": False})
        if not existing_loan:
            return {"msg": "Nie znaleziono aktywnej rezerwacji do anulowania"}, 404

        result = Loan.collection.delete_one({"_id": existing_loan["_id"]})
        if result.deleted_count:
            return {"msg": "Rezerwacja książki została anulowana"}
        else:
            return {"msg": "Błąd podczas anulowania rezerwacji książki"}
    except Exception as e:
        return {"msg": f"Błąd podczas anulowania rezerwacji książki: {str(e)}"}, 500

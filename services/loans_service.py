from db import db
from models.loan import Loan
from models.book import Book
from models.user import User
from bson import ObjectId
from datetime import datetime


def borrow_book(user_id, book_id, user_role):
    try:
        book = Book.collection.find_one({"_id": ObjectId(book_id)})
        if not book:
            return {"msg": "Książka o podanym ID nie istnieje"}, 404

        user = User.collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return {"msg": "Użytkownik o podanym ID nie istnieje"}, 404

        if user_role not in ['admin', 'librarian']:
            return {"msg": "Nie masz wystarczających uprawnień do wykonania tej operacji"}, 403

        existing_loan = Loan.collection.find_one({"book_id": ObjectId(
            book_id), "$or": [{"returned": False}, {"returned": None}]})
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


def return_book(loan_id, user_role):
    try:
        loan = Loan.collection.find_one({"_id": ObjectId(loan_id)})
        if not loan:
            return {"msg": "Wypożyczenie o podanym ID nie istnieje"}, 404

        if user_role not in ['admin', 'librarian']:
            return {"msg": "Nie masz wystarczających uprawnień do wykonania tej operacji"}, 403

        if loan['returned']:
            return {"msg": "Książka została już zwrócona wcześniej"}

        Loan.collection.update_one({"_id": ObjectId(loan_id)}, {
                                   "$set": {"returned": True, "return_date": datetime.now()}})
        return {"msg": "Książka została zwrócona"}
    except Exception as e:
        return {"msg": f"Błąd podczas zwracania książki: {str(e)}"}, 500

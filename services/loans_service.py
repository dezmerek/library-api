from models.loan import Loan
from datetime import datetime
from models.book import Book
from models.user import User
from bson import ObjectId 

def borrow_book(user_id, book_id):
    try:
        book = Book.collection.find_one({"_id": ObjectId(book_id)})
        if not book:
            return {"msg": "Książka o podanym ID nie istnieje"}, 404

        user = User.collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return {"msg": "Użytkownik o podanym ID nie istnieje"}, 404

        active_loan = Loan.collection.find_one({"book_id": ObjectId(book_id), "returned": False})
        if active_loan:
            return {"msg": "Książka jest już wypożyczona"}, 400

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

def return_book(user_id, book_id):
    try:
        query = {
            "user_id": ObjectId(user_id),
            "book_id": ObjectId(book_id),
            "returned": False
        }
        loan = Loan.collection.find_one(query)
        if not loan:
            return {"msg": "Nie znaleziono aktywnego wypożyczenia do zwrócenia"}, 404

        update = {
            "$set": {
                "returned": True,
                "return_date": datetime.now()
            }
        }
        result = Loan.collection.update_one(query, update)
        if result.modified_count:
            return {"msg": "Książka została zwrócona"}
        else:
            return {"msg": "Błąd podczas zwracania książki"}
    except Exception as e:
        return {"msg": f"Błąd podczas zwracania książki: {str(e)}"}, 500
from models.loan import Loan
from datetime import datetime

def borrow_book(user_id, book_id):
    active_loan = Loan.collection.find_one({"book_id": book_id, "returned": False})
    if active_loan:
        return {"msg": "Książka jest już wypożyczona"}, 400

    loan_data = {
        "user_id": user_id,
        "book_id": book_id,
        "loan_date": datetime.now(),
        "return_date": None,
        "returned": False
    }
    Loan.collection.insert_one(loan_data)
    return {"msg": "Książka została wypożyczona"}

def return_book(user_id, book_id):
    query = {
        "user_id": user_id,
        "book_id": book_id,
        "returned": False
    }
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
        return {"msg": "Nie znaleziono aktywnego wypożyczenia do zwrócenia"}

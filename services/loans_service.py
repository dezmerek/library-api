from models.loan import Loan
from datetime import datetime

def borrow_book(user_id, book_title):
    loan_data = {
        "user_id": user_id,
        "book_title": book_title,
        "loan_date": datetime.now(),
        "return_date": None,
        "returned": False
    }
    Loan.collection.insert_one(loan_data)
    return {"msg": "Książka została wypożyczona"}

def return_book(user_id, book_title):
    query = {
        "user_id": user_id,
        "book_title": book_title,
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

from db import db
from datetime import datetime

class Loan:
    collection = db.loans

    @staticmethod
    def to_json(loan):
        return {
            "book_title": loan["book_title"],
            "user_id": loan["user_id"],
            "loan_date": loan["loan_date"].isoformat(),
            "return_date": loan["return_date"].isoformat() if loan["return_date"] else None,
            "returned": loan["returned"]
        }

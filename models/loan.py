from db import db
from datetime import datetime

class Loan:
    collection = db.loans

    @staticmethod
    def to_json(loan):
        return {
            "loan_id": str(loan["_id"]), 
            "book_id": str(loan["book_id"]),  
            "user_id": str(loan["user_id"]),  
            "loan_date": loan["loan_date"].isoformat(),
            "return_date": loan["return_date"].isoformat() if loan["return_date"] else None,
            "returned": loan["returned"]
        }

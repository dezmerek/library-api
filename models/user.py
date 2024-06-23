from db import db

class User:
    collection = db.users

    @staticmethod
    def to_json(user):
        return {
            "username": user["username"],
            "email": user["email"],
            "role": user.get("role", "standard")  
        }

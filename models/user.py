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

    @staticmethod
    def create_user(data):
        required_fields = ["username", "email", "password", "role"]  
        if not all(field in data for field in required_fields):
            return {"msg": "Brakuje wymaganych pól"}, 400

        User.collection.insert_one(data)
        return {"msg": "Użytkownik dodany"}

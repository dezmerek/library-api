from db import db
from roles import ROLES

class User:
    collection = db.users

    @staticmethod
    def to_json(user):
        return {
            "username": user["username"],
            "email": user["email"],
            "role": user["role"],
        }

    @staticmethod
    def is_valid_role(role):
        return role in ROLES
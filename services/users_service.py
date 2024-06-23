from models.user import User
from roles import ROLES

def add_user(data, current_role):
    required_fields = ["username", "email", "password", "role"]
    if not all(field in data for field in required_fields):
        return {"msg": "Brakuje wymaganych pól"}, 400

    if current_role not in ["admin", "user"]:
        return {"msg": "Nie masz wystarczających uprawnień do wykonania tej operacji"}, 403

    if data["role"] not in ROLES:
        return {"msg": "Nieprawidłowa rola użytkownika"}, 400

    existing_user = User.collection.find_one({"username": data["username"]})
    if existing_user:
        return {"msg": "Użytkownik o podanej nazwie już istnieje"}, 400

    User.collection.insert_one(data)
    return {"msg": "Użytkownik dodany"}, 201

def get_users():
    users = list(User.collection.find({}, {'_id': 0}))
    return users

def get_user_by_username(username):
    user = User.collection.find_one({'username': username}, {'_id': 0})
    return user if user else None
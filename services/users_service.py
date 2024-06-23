from models.user import User

def add_user(data):
    required_fields = ["username", "email", "password"] 
    if not all(field in data for field in required_fields):
        return {"msg": "Brakuje wymaganych pól"}, 400

    User.collection.insert_one(data)
    return {"msg": "Użytkownik dodany"}

def get_users():
    users = list(User.collection.find({}, {'_id': 0}))
    return users

def get_user_by_username(username):
    user = User.collection.find_one({'username': username}, {'_id': 0})
    if user:
        return user
    else:
        return None

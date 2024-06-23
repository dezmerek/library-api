from models.user import User

def add_user(data):
    return User.create_user(data)

def get_users():
    users = list(User.collection.find({}, {'_id': 0}))
    return users

def get_user_by_username(username):
    user = User.collection.find_one({'username': username}, {'_id': 0})
    if user:
        return user
    else:
        return None

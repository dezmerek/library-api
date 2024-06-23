from flask import Blueprint, jsonify, request, g, abort
from functools import wraps
from db import db
from models.user import User
from roles import ROLES

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

def role_required(role):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if 'user' not in g or g.user['role'] != role:
                return jsonify({"msg": "Nie masz wystarczających uprawnień do wykonania tej operacji"}), 403
            return func(*args, **kwargs)
        return decorated_function
    return decorator

@users_bp.route('/', methods=['POST'])
@role_required('admin') 
def create_user():
    data = request.get_json()
    response = add_user(data)
    return jsonify(response), response[1] if isinstance(response, tuple) else 201

@users_bp.route('/', methods=['GET'])
@role_required('admin')  
def retrieve_users():
    users = get_users()
    return jsonify(users), 200

@users_bp.route('/<username>', methods=['GET'])
@role_required('admin')  
def retrieve_user(username):
    user = get_user_by_username(username)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"msg": "Użytkownik nie znaleziony"}), 404

def add_user(data):
    required_fields = ["username", "email", "password", "role"]
    if not all(field in data for field in required_fields):
        return {"msg": "Brakuje wymaganych pól"}, 400

    if data["role"] not in ROLES:
        return {"msg": "Nieprawidłowa rola użytkownika"}, 400

    existing_user = User.collection.find_one({"username": data["username"]})
    if existing_user:
        return {"msg": "Użytkownik o podanej nazwie już istnieje"}, 400

    User.collection.insert_one(data)
    return {"msg": "Użytkownik dodany"}

def get_users():
    users = list(User.collection.find({}, {'_id': 0}))
    return users

def get_user_by_username(username):
    user = User.collection.find_one({'username': username}, {'_id': 0})
    return user if user else None
from flask import Blueprint, jsonify, request, g
from functools import wraps
from db import db
from models.user import User
from services.users_service import add_user, get_users, get_user_by_username
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
    current_role = g.user['role'] if 'user' in g else None
    response = add_user(data, current_role)
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

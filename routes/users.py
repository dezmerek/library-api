from flask import Blueprint, request, jsonify, g, abort
from services.users_service import add_user, get_users, get_user_by_username
from functools import wraps

users_bp = Blueprint('users', __name__)

def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if g.user['role'] != 'admin':
            abort(403)  
        return func(*args, **kwargs)
    return decorated_function

@users_bp.route('/users', methods=['POST'])
@admin_required
def create_user():
    data = request.get_json()
    response = add_user(data)
    return jsonify(response), 201

@users_bp.route('/users', methods=['GET'])
@admin_required
def retrieve_users():
    users = get_users()
    return jsonify(users), 200

@users_bp.route('/users/<username>', methods=['GET'])
@admin_required
def retrieve_user(username):
    user = get_user_by_username(username)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"msg": "Użytkownik nie znaleziony"}), 404

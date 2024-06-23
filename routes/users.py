from flask import Blueprint, request, jsonify
from services.users_service import add_user, get_users, get_user_by_username

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    response = add_user(data)
    return jsonify(response), 201

@users_bp.route('/users', methods=['GET'])
def retrieve_users():
    users = get_users()
    return jsonify(users), 200

@users_bp.route('/users/<username>', methods=['GET'])
def retrieve_user(username):
    user = get_user_by_username(username)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"msg": "Użytkownik nie znaleziony"}), 404


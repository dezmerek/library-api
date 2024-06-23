from flask import Blueprint, jsonify, request
from models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = "user"  

    if not username or not email or not password:
        return jsonify({"msg": "Brakuje wymaganych pól"}), 400

    existing_user = User.collection.find_one({"username": username})
    if existing_user:
        return jsonify({"msg": "Użytkownik o podanej nazwie już istnieje"}), 400

    user_data = {
        "username": username,
        "email": email,
        "password": password,
        "role": role
    }
    User.collection.insert_one(user_data)
    return jsonify({"msg": "Użytkownik zarejestrowany"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"msg": "Brakuje danych uwierzytelniających"}), 400

    user = User.collection.find_one({'username': username, 'password': password})
    if user:
        return jsonify({"msg": "Zalogowano pomyślnie"}), 200
    else:
        return jsonify({"msg": "Nieprawidłowe dane uwierzytelniające"}), 401

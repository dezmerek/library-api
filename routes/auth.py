from flask import Blueprint, jsonify, request, g
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

    user = User.collection.find_one(
        {'username': username, 'password': password})

    if user:
        g.user = user

        return jsonify({"msg": "Zalogowano pomyślnie"}), 200
    else:
        return jsonify({"msg": "Nieprawidłowe dane uwierzytelniające"}), 401


@auth_bp.route('/change-email', methods=['PUT'])
def change_email():
    data = request.get_json()
    new_email = data.get("new_email")

    if not new_email:
        return jsonify({"msg": "Brakuje nowego adresu e-mail"}), 400

    current_user = g.user
    if not current_user:
        return jsonify({"msg": "Użytkownik niezalogowany"}), 401

    if current_user["username"] == data.get("username") or current_user["role"] == "admin":
        updated_user = User.collection.find_one_and_update(
            {"username": current_user["username"]},
            {"$set": {"email": new_email}},
            return_document=True
        )

        if updated_user:
            return jsonify({"msg": "Adres e-mail został zmieniony"}), 200
        else:
            return jsonify({"msg": "Nie udało się zmienić adresu e-mail"}), 500
    else:
        return jsonify({"msg": "Nie masz uprawnień do wykonania tej operacji"}), 403


@auth_bp.route('/change-password', methods=['PUT'])
def change_password():
    data = request.get_json()
    username = data.get("username")
    new_password = data.get("new_password")

    if not username or not new_password:
        return jsonify({"msg": "Brakuje wymaganych pól"}), 400

    current_user = g.user
    if not current_user:
        return jsonify({"msg": "Użytkownik niezalogowany"}), 401

    if current_user["username"] == username or current_user["role"] == "admin":
        result = User.collection.update_one(
            {"username": username},
            {"$set": {"password": new_password}}
        )

        if result.modified_count > 0:
            return jsonify({"msg": "Hasło zostało zmienione pomyślnie"}), 200
        else:
            return jsonify({"msg": "Nie udało się zmienić hasła"}), 500
    else:
        return jsonify({"msg": "Nie masz uprawnień do wykonania tej operacji"}), 403

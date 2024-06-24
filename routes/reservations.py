from flask import Blueprint, jsonify, request, g
from functools import wraps
from services.reservations_service import reserve_book, cancel_reservation
from models.user import User
from bson import ObjectId

reservations_bp = Blueprint(
    'reservations', __name__, url_prefix='/api/reservations')


def role_required_for_reservation(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'user' not in g or g.user['role'] not in ['admin', 'librarian', 'user']:
            return jsonify({"msg": "Nie masz wystarczających uprawnień do rezerwacji książki"}), 403
        return func(*args, **kwargs)
    return decorated_function


@reservations_bp.route('/reserve', methods=['POST'])
@role_required_for_reservation
def reserve():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        book_id = data.get("book_id")
        user_role = g.user['role']

        response = reserve_book(user_id, book_id, user_role)
        status_code = 201 if 'msg' in response and response[
            'msg'] == "Książka została zarezerwowana" else 400

        return jsonify(response), status_code
    except Exception as e:
        return jsonify({"msg": f"Błąd podczas rezerwacji książki: {str(e)}"}), 500


@reservations_bp.route('/cancel', methods=['POST'])
@role_required_for_reservation
def cancel():
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        book_id = data.get("book_id")
        user_role = g.user['role']

        response = cancel_reservation(user_id, book_id, user_role)
        status_code = 200 if 'msg' in response and response[
            'msg'] == "Rezerwacja książki została anulowana" else 400

        return jsonify(response), status_code
    except Exception as e:
        return jsonify({"msg": f"Błąd podczas anulowania rezerwacji książki: {str(e)}"}), 500

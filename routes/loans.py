from flask import Blueprint, request, jsonify, g
from functools import wraps
from services.loans_service import borrow_book, reserve_book, cancel_reservation
from roles import ROLES

loans_bp = Blueprint('loans', __name__)

def role_required(role):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if 'user' not in g or g.user['role'] != role:
                return jsonify({"msg": "Nie masz wystarczających uprawnień do wykonania tej operacji"}), 403
            return func(*args, **kwargs)
        return decorated_function
    return decorator

@loans_bp.route('/borrow', methods=['POST'])
@role_required('admin') 
def borrow():
    data = request.get_json()
    user_id = data.get("user_id")
    book_id = data.get("book_id")
    response = borrow_book(user_id, book_id)
    return jsonify(response), 201 if 'msg' in response and response['msg'] == "Książka została wypożyczona" else 400

@loans_bp.route('/reserve', methods=['POST'])
@role_required('user') 
def reserve():
    data = request.get_json()
    user_id = data.get("user_id")
    book_id = data.get("book_id")
    response = reserve_book(user_id, book_id)
    return jsonify(response), 200 if 'msg' in response and response['msg'] == "Książka została zarezerwowana" else 400

@loans_bp.route('/cancel-reservation', methods=['POST'])
@role_required('user')  
def cancel_reservation_endpoint():
    data = request.get_json()
    user_id = data.get("user_id")
    book_id = data.get("book_id")
    response = cancel_reservation(user_id, book_id)
    return jsonify(response), 200 if 'msg' in response and response['msg'] == "Rezerwacja książki została anulowana" else 400

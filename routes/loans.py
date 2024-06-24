from flask import Blueprint, request, jsonify, g
from functools import wraps
from services.loans_service import borrow_book, return_book
from roles import ROLES

loans_bp = Blueprint('loans', __name__, url_prefix='/api/loans')


def role_required_for_borrow(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'user' not in g or g.user['role'] not in ['admin', 'librarian']:
            return jsonify({"msg": "Nie masz wystarczających uprawnień do wypożyczenia książki"}), 403
        return func(*args, **kwargs)
    return decorated_function


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
@role_required_for_borrow
def borrow():
    data = request.get_json()
    user_id = data.get("user_id")
    book_id = data.get("book_id")
    user_role = g.user['role']
    response = borrow_book(user_id, book_id, user_role)
    return jsonify(response), 201 if 'msg' in response and response['msg'] == "Książka została wypożyczona" else 400


@loans_bp.route('/return', methods=['POST'])
@role_required('admin')
def return_book_endpoint():
    data = request.get_json()
    loan_id = data.get("loan_id")
    user_role = g.user['role']
    response = return_book(loan_id, user_role)
    return jsonify(response), 200 if 'msg' in response and response['msg'] == "Książka została zwrócona" else 400

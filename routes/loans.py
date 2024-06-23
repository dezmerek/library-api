from flask import Blueprint, request, jsonify, g
from functools import wraps
from services.loans_service import borrow_book, return_book
from roles import ROLES

loans_bp = Blueprint('loans', __name__)

def role_required(role):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if 'user' not in g or g.user['role'] not in ['admin', 'librarian']:
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
    return jsonify(response), 201

@loans_bp.route('/return', methods=['POST'])
@role_required('admin')
def return_loan():
    data = request.get_json()
    user_id = data.get("user_id")
    book_id = data.get("book_id")
    response = return_book(user_id, book_id)
    return jsonify(response), 200

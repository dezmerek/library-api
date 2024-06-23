from flask import Blueprint, request, jsonify
from services.loans_service import borrow_book, return_book

loans_bp = Blueprint('loans', __name__)

@loans_bp.route('/borrow', methods=['POST'])
def borrow():
    data = request.get_json()
    user_id = data.get("user_id")
    book_title = data.get("book_title")
    response = borrow_book(user_id, book_title)
    return jsonify(response), 201

@loans_bp.route('/return', methods=['POST'])
def return_loan():
    data = request.get_json()
    user_id = data.get("user_id")
    book_title = data.get("book_title")
    response = return_book(user_id, book_title)
    return jsonify(response), 200

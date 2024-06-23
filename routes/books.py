from flask import Blueprint, request, jsonify
from services.books_service import add_book, get_books, get_book_by_title, update_book, delete_book

books_bp = Blueprint('books', __name__)

@books_bp.route('/', methods=['POST'])
def create_book():
    data = request.get_json()
    response = add_book(data)
    return jsonify(response), 201

@books_bp.route('/', methods=['GET'])
def retrieve_books():
    books = get_books()
    return jsonify(books), 200

@books_bp.route('/<title>', methods=['GET'])
def retrieve_book(title):
    book = get_book_by_title(title)
    if book:
        return jsonify(book), 200
    else:
        return jsonify({"msg": "Książka nie znaleziona"}), 404

@books_bp.route('/<title>', methods=['PUT'])
def modify_book(title):
    data = request.get_json()
    response = update_book(title, data)
    return jsonify(response), 200

@books_bp.route('/<title>', methods=['DELETE'])
def remove_book(title):
    response = delete_book(title)
    return jsonify(response), 200
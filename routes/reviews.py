from flask import Blueprint, request, jsonify
from models.review import Review

review_bp = Blueprint('review', __name__)


@review_bp.route('/reviews', methods=['POST'])
def add_review():
    data = request.get_json()
    book_id = data.get('book_id')
    user_id = data.get('user_id')
    rating = data.get('rating')
    comment = data.get('comment', '')

    if not book_id or not user_id or not rating:
        return jsonify({"error": "Missing required fields"}), 400

    review = Review.create(book_id, user_id, rating, comment)
    return jsonify(review), 201


@review_bp.route('/books/<book_id>/reviews', methods=['GET'])
def get_reviews(book_id):
    reviews = Review.get_by_book(book_id)
    return jsonify(reviews), 200

from flask import Blueprint, jsonify, g
from models.book import Book
from models.user import User
from models.loan import Loan
from models.reservation import Reservation
from bson import ObjectId
from db import db
from functools import wraps

statistics_bp = Blueprint('statistics', __name__, url_prefix='/api/statistics')


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user and g.user.get('role') == 'admin':
            return f(*args, **kwargs)
        else:
            return jsonify({"msg": "Tylko administratorzy mogą przeglądać statystyki"}), 403
    return decorated_function


@statistics_bp.route('/active_reservations_count', methods=['GET'])
@admin_required
def get_active_reservations_count():
    try:
        count = Reservation.collection.count_documents({"status": "active"})
        return jsonify({"active_reservations_count": count}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve active reservations count: {str(e)}"}), 500


@statistics_bp.route('/most_reserved_books', methods=['GET'])
@admin_required
def get_most_reserved_books():
    try:
        pipeline = [
            {"$group": {"_id": "$book_id", "count": {"$sum": 1}}},
            {"$lookup": {"from": "books", "localField": "_id",
                         "foreignField": "_id", "as": "book"}},
            {"$sort": {"count": -1}},
            {"$limit": 5}
        ]
        results = list(db.reservations.aggregate(pipeline))
        most_reserved_books = [{"title": book['book'][0]['title'],
                                "reservation_count": item['count']} for item, book in zip(results, results)]
        return jsonify({"most_reserved_books": most_reserved_books}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve most reserved books: {str(e)}"}), 500


@statistics_bp.route('/most_borrowed_books', methods=['GET'])
@admin_required
def get_most_borrowed_books():
    try:
        pipeline = [
            {"$group": {"_id": "$book_id", "count": {"$sum": 1}}},
            {"$lookup": {"from": "books", "localField": "_id",
                         "foreignField": "_id", "as": "book"}},
            {"$sort": {"count": -1}},
            {"$limit": 5}
        ]
        results = list(db.loans.aggregate(pipeline))
        most_borrowed_books = [{"title": book['book'][0]['title'],
                                "borrow_count": item['count']} for item, book in zip(results, results)]
        return jsonify({"most_borrowed_books": most_borrowed_books}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve most borrowed books: {str(e)}"}), 500


@statistics_bp.route('/user_borrowed_books_count/<user_id>', methods=['GET'])
@admin_required
def get_user_borrowed_books_count(user_id):
    try:
        user_id = ObjectId(user_id)
        count = Loan.collection.count_documents(
            {"user_id": user_id, "returned": False})
        return jsonify({"user_borrowed_books_count": count}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve user borrowed books count: {str(e)}"}), 500

import pytest
from flask import Flask, jsonify
from models.book import Book
from models.loan import Loan
from models.reservation import Reservation
from models.review import Review
from models.user import User
from bson import ObjectId
from datetime import datetime


@pytest.fixture
def app(test_db):
    app = Flask(__name__)

    @app.route('/statistics', methods=['GET'])
    def get_statistics():
        total_books = Book.collection.count_documents({})
        total_loans = Loan.collection.count_documents({})
        total_reservations = Reservation.collection.count_documents({})
        total_reviews = Review.collection.count_documents({})
        total_users = User.collection.count_documents({})

        return jsonify({
            "total_books": total_books,
            "total_loans": total_loans,
            "total_reservations": total_reservations,
            "total_reviews": total_reviews,
            "total_users": total_users
        }), 200

    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def setup_and_teardown(test_db):
    Book.collection = test_db.books
    Loan.collection = test_db.loans
    Reservation.collection = test_db.reservations
    Review.collection = test_db.reviews
    User.collection = test_db.users

    yield

    test_db.books.delete_many({})
    test_db.loans.delete_many({})
    test_db.reservations.delete_many({})
    test_db.reviews.delete_many({})
    test_db.users.delete_many({})


def test_get_statistics(client, test_db):
    test_db.books.insert_many([
        {"title": "Book 1", "author": "Author 1", "year": 2020,
            "ISBN": "1234567890", "genre": "Fiction", "publisher": "Publisher 1"},
        {"title": "Book 2", "author": "Author 2", "year": 2021,
            "ISBN": "0987654321", "genre": "Non-Fiction", "publisher": "Publisher 2"}
    ])
    test_db.loans.insert_many([
        {"book_id": ObjectId(), "user_id": ObjectId(), "loan_date": datetime.now(),
         "return_date": None, "returned": False},
        {"book_id": ObjectId(), "user_id": ObjectId(), "loan_date": datetime.now(),
         "return_date": datetime.now(), "returned": True}
    ])
    test_db.reservations.insert_many([
        {"book_id": ObjectId(), "user_id": ObjectId(),
         "reservation_date": datetime.now(), "status": "active"},
        {"book_id": ObjectId(), "user_id": ObjectId(),
         "reservation_date": datetime.now(), "status": "completed"}
    ])
    test_db.reviews.insert_many([
        {"book_id": ObjectId(), "user_id": ObjectId(), "rating": 5,
         "comment": "Great book!", "created_at": datetime.now()},
        {"book_id": ObjectId(), "user_id": ObjectId(), "rating": 4,
         "comment": "Good read.", "created_at": datetime.now()}
    ])
    test_db.users.insert_many([
        {"username": "user1", "email": "user1@example.com", "role": "user"},
        {"username": "user2", "email": "user2@example.com", "role": "admin"}
    ])

    response = client.get('/statistics')
    assert response.status_code == 200
    data = response.json
    assert data["total_books"] == 2
    assert data["total_loans"] == 2
    assert data["total_reservations"] == 2
    assert data["total_reviews"] == 2
    assert data["total_users"] == 2

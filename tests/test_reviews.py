import pytest
from flask import Flask, jsonify, request
from models.review import Review
from models.book import Book
from models.user import User
from bson import ObjectId
from datetime import datetime, timedelta, timezone


@pytest.fixture
def app(test_db):
    app = Flask(__name__)

    @app.route('/reviews/<book_id>', methods=['GET'])
    def get_reviews(book_id):
        reviews = Review.get_by_book(book_id)
        return jsonify(reviews), 200

    @app.route('/reviews', methods=['POST'])
    def create_review():
        data = request.json
        try:
            if not 1 <= data['rating'] <= 5:
                raise ValueError("Invalid rating. Must be between 1 and 5.")
            review = Review.create(
                data['book_id'],
                data['user_id'],
                data['rating'],
                data.get('comment', '')
            )
            return jsonify(review), 201
        except ValueError as e:
            return jsonify({"msg": str(e)}), 400

    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def setup_and_teardown(test_db):
    Review.collection = test_db.reviews
    Book.collection = test_db.books
    User.collection = test_db.users

    yield

    test_db.reviews.delete_many({})
    test_db.books.delete_many({})
    test_db.users.delete_many({})


def test_create_review(client, test_db):
    # Insert test book and user
    book_id = test_db.books.insert_one(
        {"title": "Test Book", "author": "Test Author"}).inserted_id
    user_id = test_db.users.insert_one(
        {"username": "testuser", "email": "test@example.com"}).inserted_id

    response = client.post('/reviews', json={
        "book_id": str(book_id),
        "user_id": str(user_id),
        "rating": 5,
        "comment": "Great book!"
    })

    assert response.status_code == 201
    data = response.json
    assert data["book_id"] == str(book_id)
    assert data["user_id"] == str(user_id)
    assert data["rating"] == 5
    assert data["comment"] == "Great book!"


def test_get_reviews_for_book(client, test_db):
    book_id = test_db.books.insert_one(
        {"title": "Test Book", "author": "Test Author"}).inserted_id
    user_id = test_db.users.insert_one(
        {"username": "testuser", "email": "test@example.com"}).inserted_id

    test_db.reviews.insert_many([
        {
            "book_id": book_id,
            "user_id": user_id,
            "rating": 5,
            "comment": "Great book!",
            "created_at": datetime.now(timezone.utc)
        },
        {
            "book_id": book_id,
            "user_id": user_id,
            "rating": 4,
            "comment": "Good read",
            "created_at": datetime.now(timezone.utc) - timedelta(days=1)
        }
    ])

    response = client.get(f'/reviews/{str(book_id)}')

    assert response.status_code == 200
    data = response.json
    assert len(data) == 2
    assert data[0]["rating"] == 5
    assert data[1]["rating"] == 4


def test_create_review_invalid_data(client, test_db):
    response = client.post('/reviews', json={
        "book_id": str(ObjectId()),
        "user_id": str(ObjectId()),
        "rating": 6,
        "comment": "Invalid review"
    })

    assert response.status_code == 400
    assert "Invalid rating" in response.json["msg"]


def test_get_reviews_nonexistent_book(client):
    nonexistent_book_id = str(ObjectId())
    response = client.get(f'/reviews/{nonexistent_book_id}')

    assert response.status_code == 200
    assert response.json == []

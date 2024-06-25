import pytest
from flask import Flask, jsonify, request, g
from models.loan import Loan
from models.book import Book
from models.user import User
from bson import ObjectId
from datetime import datetime, timezone, timedelta


@pytest.fixture
def app(test_db):
    app = Flask(__name__)

    @app.route('/loans', methods=['POST'])
    def create_loan():
        data = request.json
        loan = Loan.collection.insert_one({
            "book_id": ObjectId(data['book_id']),
            "user_id": ObjectId(data['user_id']),
            "loan_date": datetime.now(timezone.utc),
            "return_date": None,
            "returned": False
        })
        return jsonify(Loan.to_json(Loan.collection.find_one({"_id": loan.inserted_id}))), 201

    @app.route('/loans/<loan_id>', methods=['GET'])
    def get_loan(loan_id):
        loan = Loan.collection.find_one({"_id": ObjectId(loan_id)})
        if loan:
            return jsonify(Loan.to_json(loan)), 200
        return jsonify({"msg": "Loan not found"}), 404

    @app.route('/loans/<loan_id>/return', methods=['PUT'])
    def return_loan(loan_id):
        loan = Loan.collection.find_one_and_update(
            {"_id": ObjectId(loan_id)},
            {"$set": {"return_date": datetime.now(
                timezone.utc), "returned": True}},
            return_document=True
        )
        if loan:
            return jsonify(Loan.to_json(loan)), 200
        return jsonify({"msg": "Loan not found"}), 404

    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def setup_and_teardown(test_db):
    Loan.collection = test_db.loans
    Book.collection = test_db.books
    User.collection = test_db.users

    yield

    test_db.loans.delete_many({})
    test_db.books.delete_many({})
    test_db.users.delete_many({})


def test_create_loan(client, test_db):
    # Insert test book and user
    book_id = test_db.books.insert_one(
        {"title": "Test Book", "author": "Test Author"}).inserted_id
    user_id = test_db.users.insert_one(
        {"username": "testuser", "email": "test@example.com"}).inserted_id

    response = client.post('/loans', json={
        "book_id": str(book_id),
        "user_id": str(user_id)
    })

    assert response.status_code == 201
    data = response.json
    assert data["book_id"] == str(book_id)
    assert data["user_id"] == str(user_id)
    assert data["returned"] == False
    assert data["return_date"] is None


def test_get_loan(client, test_db):
    # Insert test book, user, and loan
    book_id = test_db.books.insert_one(
        {"title": "Test Book", "author": "Test Author"}).inserted_id
    user_id = test_db.users.insert_one(
        {"username": "testuser", "email": "test@example.com"}).inserted_id
    loan_id = test_db.loans.insert_one({
        "book_id": book_id,
        "user_id": user_id,
        "loan_date": datetime.now(timezone.utc),
        "return_date": None,
        "returned": False
    }).inserted_id

    response = client.get(f'/loans/{str(loan_id)}')

    assert response.status_code == 200
    data = response.json
    assert data["book_id"] == str(book_id)
    assert data["user_id"] == str(user_id)
    assert data["returned"] == False
    assert data["return_date"] is None


def test_return_loan(client, test_db):
    book_id = test_db.books.insert_one(
        {"title": "Test Book", "author": "Test Author"}).inserted_id
    user_id = test_db.users.insert_one(
        {"username": "testuser", "email": "test@example.com"}).inserted_id
    loan_id = test_db.loans.insert_one({
        "book_id": book_id,
        "user_id": user_id,
        "loan_date": datetime.now(timezone.utc),
        "return_date": None,
        "returned": False
    }).inserted_id

    response = client.put(f'/loans/{str(loan_id)}/return')

    assert response.status_code == 200
    data = response.json
    assert data["book_id"] == str(book_id)
    assert data["user_id"] == str(user_id)
    assert data["returned"] == True
    assert data["return_date"] is not None


def test_get_nonexistent_loan(client):
    nonexistent_loan_id = str(ObjectId())
    response = client.get(f'/loans/{nonexistent_loan_id}')

    assert response.status_code == 404
    assert response.json == {"msg": "Loan not found"}


def test_return_nonexistent_loan(client):
    nonexistent_loan_id = str(ObjectId())
    response = client.put(f'/loans/{nonexistent_loan_id}/return')

    assert response.status_code == 404
    assert response.json == {"msg": "Loan not found"}

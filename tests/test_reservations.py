import pytest
from flask import Flask, jsonify, request, g
from models.reservation import Reservation
from models.book import Book
from models.user import User
from bson import ObjectId
from datetime import datetime, timezone, timedelta
from services.reservations_service import reserve_book, cancel_reservation


@pytest.fixture
def app(test_db):
    app = Flask(__name__)

    @app.route('/api/reservations/reserve', methods=['POST'])
    def create_reservation():
        data = request.json
        g.user = {'role': 'user'}
        response = reserve_book(
            data['user_id'], data['book_id'], g.user['role'])
        if isinstance(response, tuple):
            return jsonify(response[0]), response[1]
        return jsonify(response), 201

    @app.route('/api/reservations/cancel', methods=['POST'])
    def cancel_reservation_route():
        data = request.json
        g.user = {'role': 'user'}
        response = cancel_reservation(
            data['user_id'], data['book_id'], g.user['role'])
        if isinstance(response, tuple):
            return jsonify(response[0]), response[1]
        return jsonify(response), 200

    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def setup_and_teardown(test_db):
    Reservation.collection = test_db.reservations
    Book.collection = test_db.books
    User.collection = test_db.users

    yield

    test_db.reservations.delete_many({})
    test_db.books.delete_many({})
    test_db.users.delete_many({})


def test_create_reservation(client, test_db):
    # Insert test book and user
    book_id = test_db.books.insert_one(
        {"title": "Test Book", "author": "Test Author"}).inserted_id
    user_id = test_db.users.insert_one(
        {"username": "testuser", "email": "test@example.com"}).inserted_id

    response = client.post('/api/reservations/reserve', json={
        "book_id": str(book_id),
        "user_id": str(user_id)
    })

    assert response.status_code == 201
    assert response.json == {"msg": "Książka została zarezerwowana"}

    # Check if the reservation was created in the database
    reservation = Reservation.collection.find_one(
        {"book_id": book_id, "user_id": user_id})
    assert reservation is not None
    assert reservation["status"] == "active"


def test_create_reservation_invalid_book(client, test_db):
    user_id = test_db.users.insert_one(
        {"username": "testuser", "email": "test@example.com"}).inserted_id

    response = client.post('/api/reservations/reserve', json={
        "book_id": str(ObjectId()),
        "user_id": str(user_id)
    })

    assert response.status_code == 404
    assert response.json == {"msg": "Książka o podanym ID nie istnieje"}


def test_create_reservation_invalid_user(client, test_db):
    book_id = test_db.books.insert_one(
        {"title": "Test Book", "author": "Test Author"}).inserted_id

    response = client.post('/api/reservations/reserve', json={
        "book_id": str(book_id),
        "user_id": str(ObjectId())
    })

    assert response.status_code == 404
    assert response.json == {"msg": "Użytkownik o podanym ID nie istnieje"}


def test_cancel_reservation(client, test_db):
    book_id = test_db.books.insert_one(
        {"title": "Test Book", "author": "Test Author"}).inserted_id
    user_id = test_db.users.insert_one(
        {"username": "testuser", "email": "test@example.com"}).inserted_id

    # Create a reservation
    test_db.reservations.insert_one({
        "book_id": book_id,
        "user_id": user_id,
        "reservation_date": datetime.now(timezone.utc),
        "status": "active"
    })

    response = client.post('/api/reservations/cancel', json={
        "book_id": str(book_id),
        "user_id": str(user_id)
    })

    assert response.status_code == 200
    assert response.json == {"msg": "Rezerwacja książki została anulowana"}

    reservation = Reservation.collection.find_one(
        {"book_id": book_id, "user_id": user_id})
    assert reservation is None


def test_cancel_nonexistent_reservation(client, test_db):
    book_id = test_db.books.insert_one(
        {"title": "Test Book", "author": "Test Author"}).inserted_id
    user_id = test_db.users.insert_one(
        {"username": "testuser", "email": "test@example.com"}).inserted_id

    response = client.post('/api/reservations/cancel', json={
        "book_id": str(book_id),
        "user_id": str(user_id)
    })

    assert response.status_code == 404
    assert response.json == {
        "msg": "Nie znaleziono aktywnej rezerwacji do anulowania"}

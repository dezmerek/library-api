import pytest
from flask import Flask, g
from routes.auth import auth_bp
from models.user import User
from bson import ObjectId


@pytest.fixture
def app(test_db):
    app = Flask(__name__)
    app.register_blueprint(auth_bp)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def setup_and_teardown(test_db):
    User.collection = test_db.users
    yield
    test_db.users.delete_many({})


@pytest.fixture
def mock_g(monkeypatch):
    class MockG:
        user = None
    mock_g = MockG()
    monkeypatch.setattr('flask.g', mock_g)
    return mock_g


def test_register_user_success(client):
    response = client.post('/auth/register', json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    assert response.json == {"msg": "Użytkownik zarejestrowany"}

    user = User.collection.find_one({"username": "testuser"})
    assert user is not None
    assert user["email"] == "testuser@example.com"


def test_register_user_missing_fields(client):
    response = client.post('/auth/register', json={
        "username": "testuser",
        "email": "testuser@example.com"
    })
    assert response.status_code == 400
    assert response.json == {"msg": "Brakuje wymaganych pól"}


def test_register_user_existing_username(client, test_db):
    test_db.users.insert_one({
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123",
        "role": "user"
    })

    response = client.post('/auth/register', json={
        "username": "testuser",
        "email": "newemail@example.com",
        "password": "password123"
    })
    assert response.status_code == 400
    assert response.json == {"msg": "Użytkownik o podanej nazwie już istnieje"}


def test_login_user_success(client, test_db):
    test_db.users.insert_one({
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123",
        "role": "user"
    })

    response = client.post('/auth/login', json={
        "username": "testuser",
        "password": "password123"
    })
    assert response.status_code == 200
    assert response.json == {"msg": "Zalogowano pomyślnie"}


def test_login_user_invalid_credentials(client, test_db):
    test_db.users.insert_one({
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123",
        "role": "user"
    })

    response = client.post('/auth/login', json={
        "username": "testuser",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.json == {"msg": "Nieprawidłowe dane uwierzytelniające"}


def test_change_email_success(client, test_db, mock_g):
    user_id = test_db.users.insert_one({
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123",
        "role": "user"
    }).inserted_id
    mock_g.user = {"_id": user_id, "username": "testuser", "role": "user"}

    with client.application.app_context():
        g.user = mock_g.user
        response = client.put('/auth/change-email', json={
            "new_email": "newemail@example.com",
            "username": "testuser"
        })
    assert response.status_code == 200
    assert response.json == {"msg": "Adres e-mail został zmieniony"}

    user = User.collection.find_one({"username": "testuser"})
    assert user["email"] == "newemail@example.com"


def test_change_email_unauthorized(client, test_db, mock_g):
    user_id = test_db.users.insert_one({
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123",
        "role": "user"
    }).inserted_id
    mock_g.user = {"_id": user_id, "username": "testuser", "role": "user"}

    with client.application.app_context():
        g.user = mock_g.user
        response = client.put('/auth/change-email', json={
            "new_email": "newemail@example.com",
            "username": "otheruser"
        })
    assert response.status_code == 403
    assert response.json == {
        "msg": "Nie masz uprawnień do wykonania tej operacji"}


def test_change_password_success(client, test_db, mock_g):
    user_id = test_db.users.insert_one({
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123",
        "role": "user"
    }).inserted_id
    mock_g.user = {"_id": user_id, "username": "testuser", "role": "user"}

    with client.application.app_context():
        g.user = mock_g.user
        response = client.put('/auth/change-password', json={
            "username": "testuser",
            "new_password": "newpassword123"
        })
    assert response.status_code == 200
    assert response.json == {"msg": "Hasło zostało zmienione pomyślnie"}

    user = User.collection.find_one({"username": "testuser"})
    assert user["password"] == "newpassword123"


def test_change_password_unauthorized(client, test_db, mock_g):
    user_id = test_db.users.insert_one({
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123",
        "role": "user"
    }).inserted_id
    mock_g.user = {"_id": user_id, "username": "testuser", "role": "user"}

    with client.application.app_context():
        g.user = mock_g.user
        response = client.put('/auth/change-password', json={
            "username": "otheruser",
            "new_password": "newpassword123"
        })
    assert response.status_code == 403
    assert response.json == {
        "msg": "Nie masz uprawnień do wykonania tej operacji"}

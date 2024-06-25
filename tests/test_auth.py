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
        pass
    mock_g = MockG()
    monkeypatch.setattr('flask.g', mock_g)
    return mock_g


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

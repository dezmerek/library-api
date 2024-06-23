from flask import Flask, jsonify, g, request
from config import Config
from routes.books import books_bp
from routes.users import users_bp
from routes.loans import loans_bp
from routes.auth import auth_bp
from functools import wraps
from db import db

app = Flask(__name__)
app.config.from_object(Config)

@app.before_request
def authenticate():
    auth = request.authorization
    if auth:
        user = db.users.find_one({'username': auth.username, 'password': auth.password})
        if user:
            g.user = user
        else:
            return jsonify({"msg": "Nieprawidłowe dane uwierzytelniające"}), 401
    else:
        g.user = None 

@app.route('/')
def home():
    return "Welcome to the Library API!"

app.register_blueprint(books_bp, url_prefix='/books')
app.register_blueprint(users_bp, url_prefix='/api/users')
app.register_blueprint(loans_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True)

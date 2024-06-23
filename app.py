from flask import Flask, jsonify, g, request, abort
from config import Config
from routes.users import users_bp
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

def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if g.user['role'] != 'admin':
            abort(403)  
        return func(*args, **kwargs)
    return decorated_function

app.register_blueprint(users_bp, url_prefix='/api/users')

if __name__ == '__main__':
    app.run(debug=True)

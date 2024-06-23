from flask import Flask
from config import Config
from routes.books import books_bp
from routes.users import users_bp
from routes.loans import loans_bp

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(books_bp, url_prefix='/books')
app.register_blueprint(users_bp, url_prefix='/api/users')
app.register_blueprint(loans_bp, url_prefix='/api/loans')

if __name__ == '__main__':
    app.run(debug=True)

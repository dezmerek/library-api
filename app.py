from flask import Flask
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize MongoDB client
client = MongoClient(app.config['MONGO_URI'], server_api=ServerApi('1'))

# Test the connection to MongoDB
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

@app.route('/')
def home():
    return "Hello, Flask with MongoDB!"

if __name__ == '__main__':
    app.run(debug=True)

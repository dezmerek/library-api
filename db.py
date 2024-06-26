from pymongo import MongoClient
from pymongo.server_api import ServerApi
from config import Config
import certifi

client = MongoClient(Config.MONGO_URI, server_api=ServerApi('1'), tlsCAFile=certifi.where())
db = client.library

try:
    client.admin.command('ping')
    print("Połączono z MongoDB!")
except Exception as e:
    print(f"Błąd połączenia z MongoDB: {e}")

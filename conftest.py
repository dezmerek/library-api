import pytest
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()


@pytest.fixture(scope="session")
def mongo_client():
    client = MongoClient(os.getenv("MONGO_URI"))
    yield client
    client.close()


@pytest.fixture(scope="session")
def test_db(mongo_client):
    db = mongo_client.get_database("test_library")
    yield db
    mongo_client.drop_database("test_library")

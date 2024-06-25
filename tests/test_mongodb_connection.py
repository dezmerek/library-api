import pytest
from pymongo.errors import ConnectionFailure


def test_mongodb_connection(mongo_client):
    try:
        mongo_client.admin.command('ismaster')
        assert True
    except ConnectionFailure:
        pytest.fail("Nie udało się połączyć z bazą MongoDB")


def test_test_db_creation(test_db):
    test_db.create_collection("test_collection")
    # Sprawdzenie, czy baza testowa została utworzona
    assert "test_library" in test_db.client.list_database_names()


def test_collection_creation(test_db):
    if "test_collection" in test_db.list_collection_names():
        test_db.drop_collection("test_collection")

    test_db.create_collection("test_collection")
    assert "test_collection" in test_db.list_collection_names()

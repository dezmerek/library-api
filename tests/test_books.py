import pytest
from bson import ObjectId
from models.book import Book
from services.books_service import add_book, get_books, get_book_by_title, update_book, delete_book


@pytest.fixture
def sample_book_data():
    return {
        "title": "Test Book",
        "author": "Test Author",
        "year": 2023,
        "ISBN": "1234567890",
        "genre": "Test Genre",
        "publisher": "Test Publisher"
    }


@pytest.fixture
def setup_test_db(test_db):
    Book.collection = test_db.books
    yield
    test_db.books.delete_many({})


def test_add_book(setup_test_db, sample_book_data):
    result = add_book(sample_book_data)
    assert result == {"msg": "Książka dodana"}

    book = Book.collection.find_one({"title": "Test Book"})
    assert book is not None
    assert book["author"] == "Test Author"


def test_add_book_missing_fields(setup_test_db):
    incomplete_data = {"title": "Incomplete Book", "author": "Test Author"}
    result = add_book(incomplete_data)
    assert result == ({"msg": "Brakuje wymaganych pól"}, 400)


def test_get_books(setup_test_db, sample_book_data):
    Book.collection.insert_one(sample_book_data)
    books = get_books()
    assert len(books) == 1
    assert books[0]["title"] == "Test Book"


def test_get_book_by_title(setup_test_db, sample_book_data):
    Book.collection.insert_one(sample_book_data)
    book = get_book_by_title("Test Book")
    assert book is not None
    assert book["author"] == "Test Author"


def test_get_nonexistent_book(setup_test_db):
    book = get_book_by_title("Nonexistent Book")
    assert book is None


def test_update_book(setup_test_db, sample_book_data):
    Book.collection.insert_one(sample_book_data)
    update_data = {"year": 2024, "genre": "Updated Genre"}
    result = update_book("Test Book", update_data)
    assert result == {"msg": "Książka zaktualizowana"}

    updated_book = Book.collection.find_one({"title": "Test Book"})
    assert updated_book["year"] == 2024
    assert updated_book["genre"] == "Updated Genre"


def test_update_nonexistent_book(setup_test_db):
    update_data = {"year": 2024}
    result = update_book("Nonexistent Book", update_data)
    assert result == {"msg": "Książka nie znaleziona"}


def test_delete_book(setup_test_db, sample_book_data):
    Book.collection.insert_one(sample_book_data)
    result = delete_book("Test Book")
    assert result == {"msg": "Książka usunięta"}

    book = Book.collection.find_one({"title": "Test Book"})
    assert book is None


def test_delete_nonexistent_book(setup_test_db):
    result = delete_book("Nonexistent Book")
    assert result == {"msg": "Książka nie znaleziona"}

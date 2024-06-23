from models.book import Book

def add_book(data):
    required_fields = ["title", "author", "year", "ISBN", "genre", "publisher"]
    if not all(field in data for field in required_fields):
        return {"msg": "Brakuje wymaganych pól"}, 400

    Book.collection.insert_one(data)
    return {"msg": "Książka dodana"}

def get_books():
    books = list(Book.collection.find({}, {'_id': 0}))
    return books

def get_book_by_title(title):
    book = Book.collection.find_one({'title': title}, {'_id': 0})
    if book:
        return book
    else:
        return None

def update_book(title, data):
    result = Book.collection.update_one({'title': title}, {'$set': data})
    if result.modified_count:
        return {"msg": "Książka zaktualizowana"}
    else:
        return {"msg": "Książka nie znaleziona"}

def delete_book(title):
    result = Book.collection.delete_one({'title': title})
    if result.deleted_count:
        return {"msg": "Książka usunięta"}
    else:
        return {"msg": "Książka nie znaleziona"}

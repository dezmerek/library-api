from db import db

class Book:
    collection = db.books

    @staticmethod
    def to_json(book):
        return {
            "book_id": str(book["_id"]), 
            "title": book["title"],
            "author": book["author"],
            "year": book["year"],
            "ISBN": book["ISBN"],
            "genre": book["genre"],
            "publisher": book["publisher"]
        }
